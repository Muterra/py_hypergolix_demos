import argparse
import time
import datetime
import psutil
import collections
import daemoniker
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
INTERVAL_API = hgx.utils.ApiID(
    b'\n\x10\x04\x00\x13\x11\x0b\x11\x06\x02\x19\x00' +
    b'\x11\x12\x10\x10\n\x14\x19\x15\x11\x18\x0f\x0f' +
    b'\x01\r\x0c\x15\x16\x04\x0f\x18\x19\x13\x14\x11' +
    b'\x10\x01\x19\x19\x15\x0b\t\x0e\x15\r\x16\x15' +
    b'\x0e\n\x19\x0b\x14\r\n\x04\x0c\x06\x03\x13\x01' +
    b'\x01\x12\x05'
)


def humanize_bibytes(n, prefixes=collections.OrderedDict((
                    (0, 'B'),
                    (1024, 'KiB'),
                    (1048576, 'MiB'),
                    (1073741824, 'GiB'),
                    (1099511627776, 'TiB'),
                    (1125899906842624, 'PiB'),
                    (1152921504606846976, 'EiB'),
                    (1180591620717411303424, 'ZiB'),
                    (1208925819614629174706176, 'YiB')))):
    ''' Convert big numbers into easily-human-readable ones.
    '''
    for value, prefix in reversed(prefixes.items()):
        if n >= value:
            return '{:.2f} {}'.format(float(n) / value, prefix)
            
            
def format_cpu(cpu_list):
    cpustr = 'CPU:\n----------\n'
    for cpu in cpu_list:
        cpustr += '  ' + str(cpu) + '%\n'
    return cpustr
    
    
def format_mem(mem_tup):
    memstr = 'MEM:\n----------\n'
    memstr += '  Avail: ' + humanize_bibytes(mem_tup.available) + '\n'
    memstr += '  Total: ' + humanize_bibytes(mem_tup.total) + '\n'
    memstr += '  Used:  ' + str(mem_tup.percent) + '%\n'
    return memstr
    
    
def format_disk(disk_tup):
    diskstr = 'DISK:\n----------\n'
    diskstr += '  Avail: ' + humanize_bibytes(disk_tup.free) + '\n'
    diskstr += '  Total: ' + humanize_bibytes(disk_tup.total) + '\n'
    diskstr += '  Used:  ' + str(disk_tup.percent) + '%\n'
    return diskstr


class Telemeter:
    ''' Remote monitoring demo app sender.
    '''
    
    def __init__(self, interval, minimum_interval=1):
        self.hgxlink = hgx.HGXLink()
        self._interval = interval
        self.minimum_interval = minimum_interval
        
        # These are the actual Hypergolix business parts
        self.status = None
        self.paired_fingerprint = None
        
        self.running = True
        
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
        # And set up a handler to change our interval
        interval_handler = self.hgxlink.wrap_threadsafe(self.interval_handler)
        self.hgxlink.register_share_handler_threadsafe(INTERVAL_API,
                                                       interval_handler)
        
    def app_run(self):
        ''' Do the main application loop.
        '''
        while self.running:
            timestamp = datetime.datetime.now()
            timestr = timestamp.strftime('%Y.%M.%d @ %H:%M:%S\n==========\n')
            cpustr = format_cpu(psutil.cpu_percent(interval=.1, percpu=True))
            memstr = format_mem(psutil.virtual_memory())
            diskstr = format_disk(psutil.disk_usage('/'))
            
            status = (timestr + cpustr + memstr + diskstr + '\n')
            
            self.status.state = status
            self.status.push_threadsafe()
            
            elapsed = (datetime.datetime.now() - timestamp).total_seconds()
            print('Logged in {:.3f} seconds:\n{}'.format(elapsed, status))
            # Make sure we clamp this to non-negative values, in case the
            # update took longer than the current interval.
            time.sleep(max(self.interval - elapsed, 0))
            
    def signal_handler(self, signum):
        self.running = False
        self.hgxlink.stop_threadsafe()
        
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
            
    def interval_handler(self, ghid, origin, api_id):
        ''' Interval handlers change our recording interval.
        '''
        # Ignore requests that don't match our pairing.
        # This will also catch un-paired requests.
        if origin != self.paired_fingerprint:
            return
        
        # If the address matches our pairing, use it to change our interval.
        else:
            # We don't need to create an update callback here, because any
            # upstream modifications will automatically be passed to the
            # object. This is true of all hypergolix objects, but by using a
            # proxy, it mimics the behavior of the int itself.
            interval_proxy = self.hgxlink.get_threadsafe(
                cls = hgx.JsonProxy,
                ghid = ghid
            )
            self._interval = interval_proxy
            
    @property
    def interval(self):
        ''' This provides some consumer-side protection against
        malicious interval proxies.
        '''
        try:
            return float(max(self._interval, self.minimum_interval))
        
        except (ValueError, TypeError):
            return self.minimum_interval


class Telereader:
    ''' Remote monitoring demo app receiver.
    '''
    
    def __init__(self, telemeter_fingerprint):
        self.hgxlink = hgx.HGXLink()
        self.telemeter_fingerprint = telemeter_fingerprint
        
        # These are the actual Hypergolix business parts
        self.status = None
        self.pair = None
        self.interval = None
        
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
        
    def app_run(self):
        ''' For now, just busy-wait.
        '''
        while True:
            time.sleep(1)
        
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
        
    def set_interval(self, interval):
        ''' Set the recording interval remotely.
        '''
        # This is some supply-side protection of the interval.
        interval = float(interval)
        
        if self.interval is None:
            self.interval = self.hgxlink.new_threadsafe(
                cls = hgx.JsonProxy,
                state = interval,
                api_id = INTERVAL_API
            )
            self.interval.hgx_share_threadsafe(self.telemeter_fingerprint)
        else:
            # We can't directly reassign the proxy here, because it would just
            # overwrite the self.interval name with the interval float from
            # above. Instead, we need to assign to the state.
            self.interval.hgx_state = interval
            self.interval.hgx_push_threadsafe()


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
    argparser.add_argument(
        '--interval',
        action = 'store',
        default = None,
        type = float,
        help = 'Set the Telemeter recording interval from the Telereader. ' +
               'Ignored by a Telemeter.'
    )
    argparser.add_argument(
        '--pidfile',
        action = 'store',
        default = 'telemeter.pid',
        type = str,
        help = 'Set the name for the PID file for the Telemeter daemon.'
    )
    argparser.add_argument(
        '--stop',
        action = 'store_true',
        help = 'Stop an existing Telemeter daemon.'
    )
    args = argparser.parse_args()
    
    # This is the READER
    if args.telereader is not None:
        telemeter_fingerprint = hgx.Ghid.from_str(args.telereader)
        app = Telereader(telemeter_fingerprint)
        
        try:
            app.app_init()
            
            if args.interval is not None:
                app.set_interval(args.interval)
            
            app.app_run()
            
        finally:
            app.hgxlink.stop_threadsafe()
    
    # This is the SENDER, but we're stopping it.
    elif args.stop:
        daemoniker.send(args.pidfile, daemoniker.SIGTERM)
        
    # This is the SENDER, and we're starting it.
    else:
        # We need to actually daemonize the app so that it persists without
        # an SSH connection
        with daemoniker.Daemonizer() as (is_setup, daemonizer):
            is_parent, pidfile = daemonizer(
                args.pidfile,
                args.pidfile,
                strip_cmd_args = False
            )
            
            # Parent exits here
        
        # Just the child from here
        app = Telemeter(interval=5)
            
        try:
            sighandler = daemoniker.SignalHandler1(
                pidfile,
                sigint = app.signal_handler,
                sigterm = app.signal_handler,
                sigabrt = app.signal_handler
            )
            sighandler.start()
            
            app.app_init()
            app.app_run()
            
        finally:
            app.hgxlink.stop_threadsafe()
