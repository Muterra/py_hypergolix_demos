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
        self.status_reporter = None
        
    def app_init(self):
        ''' Set up the application.
        '''
        self.status_reporter = self.hgxlink.new_threadsafe(
            cls = hgx.JsonObj,
            state = 'Hello world!'
        )
        
    def app_run(self):
        ''' Do the main application loop.
        '''
        while True:
            timestamp = datetime.datetime.now().strftime('%Y.%M.%d @ %H:%M:%S')
            self.status_reporter.state = timestamp
            self.status_reporter.push_threadsafe()
            print('Logged ' + timestamp)
            time.sleep(self.interval)


if __name__ == "__main__":
    try:
        app = Telemeter(interval=1)
        app.app_init()
        app.app_run()
        
    finally:
        app.hgxlink.stop_threadsafe()
