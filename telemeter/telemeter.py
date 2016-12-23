import argparse
import time
import datetime
import hypergolix as hgx


# These are app-specific (here, totally random) API schema identifiers
STATUS_API = hgx.utils.ApiID(
    b'\x02\x0b\x16\x19\x00\x19\x10\x18\x08\x12\x03' +
    b'\x11\x07\x07\r\x0c\n\x14\x04\x13\x07\x04\x06' +
    b'\x13\x01\x0c\x04\x00\x0b\x03\x01\x12\x05\x0f' +
    b'\x01\x0c\x05\x11\x03\x01\x0e\x13\x16\x13\x11' +
    b'\x10\x13\t\x06\x10\x00\x14\x0c\x15\x0b\x07' +
    b'\x0c\x0c\x04\x07\x0b\x0f\x18\x03'
)
PAIR_API = hgx.utils.ApiID(
    b'\x17\n\x12\x17\x03\x0f\x14\x11\x07\x10\x05\x04' +
    b'\x14\x18\x11\x11\x12\x02\x17\x12\x15\x0e\x04' +
    b'\x0f\x11\x19\x07\x19\n\r\x03\x06\x12\x04\x17' +
    b'\x11\x14\x07\t\x08\x13\x19\x04\n\x0f\x15\x12' +
    b'\x14\x07\x19\x16\x13\x18\x0b\x18\x0e\x12\x15\n' +
    b'\n\x16\x0f\x08\x14'
)


class Telemeter:
    ''' Remote monitoring demo app sender.
    '''
    
    def __init__(self, interval):
        self.hgxlink = hgx.HGXLink()
        self.interval = interval
        
        # These are the actual Hypergolix business parts
        self.status = None
        self.paired_fingerprint = None
        
    def app_init(self):
        ''' Set up the application.
        '''
        print('My fingerprint is: ' + self.hgxlink.whoami.as_str())
        self.status = self.hgxlink.new_threadsafe(
            cls = hgx.JsonObj,
            state = 'Hello world!',
            api_id = STATUS_API
        )
        
        # Share handlers are called from within the HGXLink event loop, so they
        # must be wrapped before use
        pair_handler = self.hgxlink.wrap_threadsafe(self.pair_handler)
        self.hgxlink.register_share_handler_threadsafe(PAIR_API, pair_handler)
        
    def app_run(self):
        ''' Do the main application loop.
        '''
        while True:
            timestamp = datetime.datetime.now()
            timestr = timestamp.strftime('%Y.%M.%d @ %H:%M:%S')
            
            self.status.state = timestr
            self.status.push_threadsafe()
            
            elapsed = (datetime.datetime.now() - timestamp).total_seconds()
            print('Logged {0} in {1:.3f} seconds.'.format(timestr, elapsed))
            time.sleep(self.interval - elapsed)
        
    def pair_handler(self, ghid, origin, api_id):
        ''' Pair handlers ignore the object itself, instead setting up
        the origin as the paired_fingerprint (unless one already exists,
        in which case it is ignored) and sharing the status object with
        them.
        
        This also doubles as a way to re-pair the same fingerprint, in
        the event that they have gone offline for a long time and are no
        longer receiving updates.
        '''
        # The initial pairing (pair/trust on first connect)
        if self.paired_fingerprint is None:
            self.paired_fingerprint = origin
        
        # Subsequent pairing requests from anyone else are ignored
        elif self.paired_fingerprint != origin:
            return
            
        # Now we want to share the status reporter, if we have one, with the
        # origin
        if self.status is not None:
            self.status.share_threadsafe(origin)


class Telereader:
    ''' Remote monitoring demo app receiver.
    '''
    
    def __init__(self, telemeter_fingerprint):
        self.hgxlink = hgx.HGXLink()
        self.telemeter_fingerprint = telemeter_fingerprint
        
        # These are the actual Hypergolix business parts
        self.status = None
        self.pair = None
        
    def app_init(self):
        ''' Set up the application.
        '''
        # Because we're using a native coroutine for this share handler, it
        # needs no wrapping.
        self.hgxlink.register_share_handler_threadsafe(STATUS_API,
                                                       self.status_handler)
        
        # Wait until after registering the share handler to avoid a race
        # condition with the Telemeter
        self.pair = self.hgxlink.new_threadsafe(
            cls = hgx.JsonObj,
            state = 'Hello world!',
            api_id = PAIR_API
        )
        self.pair.share_threadsafe(self.telemeter_fingerprint)
        
    async def status_handler(self, ghid, origin, api_id):
        ''' We sent the pairing, and the Telemeter shared its status obj
        with us in return. Get it, store it locally, and register a
        callback to run every time the object is updated.
        '''
        status = await self.hgxlink.get(
            cls = hgx.JsonObj,
            ghid = ghid
        )
        # This registers the update callback. It will be run in the hgxlink
        # event loop, so if it were blocking/threaded, we would need to wrap
        # it like this: self.hgxlink.wrap_threadsafe(self.update_handler)
        status.callback = self.update_handler
        # We're really only doing this to prevent garbage collection
        self.status = status
        
    async def update_handler(self, obj):
        ''' A very simple, **asynchronous** handler for status updates.
        This will be called every time the Telemeter changes their
        status.
        '''
        print(obj.state)
        
    def app_run(self):
        ''' For now, just busy-wait.
        '''
        while True:
            time.sleep(1)


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(
        description = 'A simple remote telemetry app.'
    )
    argparser.add_argument(
        '--telereader',
        action = 'store',
        default = None,
        help = 'Pass a Telemeter fingerprint to run as a reader.'
    )
    args = argparser.parse_args()
    
    if args.telereader is not None:
        telemeter_fingerprint = hgx.Ghid.from_str(args.telereader)
        app = Telereader(telemeter_fingerprint)
        
    else:
        app = Telemeter(interval=5)
        
    try:
        app.app_init()
        app.app_run()
        
    finally:
        app.hgxlink.stop_threadsafe()
