import time
import datetime
import hypergolix as hgx


class Telemeter:
    ''' Remote monitoring demo app.
    '''
    
    def __init__(self, interval):
        self.hgxlink = hgx.HGXLink()
        self.interval = interval
        
        # These are the actual Hypergolix business parts
        self.status = None
        
    def app_init(self):
        ''' Set up the application.
        '''
        self.status = self.hgxlink.new_threadsafe(
            cls = hgx.JsonObj,
            state = 'Hello world!'
        )
        
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


if __name__ == "__main__":
    try:
        app = Telemeter(interval=1)
        app.app_init()
        app.app_run()
        
    finally:
        app.hgxlink.stop_threadsafe()
