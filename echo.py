import IPython
import warnings

# These are actually used for the application
import collections

from golix import Ghid
from hypergolix.service import HypergolixLink

hgxlink = HypergolixLink(threaded=True)
desktop = Ghid(algo=1, address=b'\xc0TZ\x15+\x9a\x8e\x01\xbbvw\x83\xc8%\xd5RG\x9c8<\xf7\x1f\xa4e\x08\xc4\x9a\xa0o\x15\x83f\xf2>P/\xc1\xfbj3\xd6\xa9M\x03z\x98\x1b\xa7U\xb9b\xf3 \xfd\x81T+\xb3\x14\xaa\xcf$s\xac')
razpi = Ghid(algo=1, address=b'D\xe90\x1bpr\xd3\xed\xdd\xac-,\xa9{i\xca{[\xa8\x9fy\xe4\xf2C\x0fv\x18\xa4}\xd9\xa9)=+\xe0F\xd8j~6\x07H\xadD\xb9\xa9x/\x9a\xab\x9e\x8e\xe6\x03\xe9\xaf\xd7\xbaH\x08"w\xa1>')

# Declare api
request_api = bytes(64) + b'\x01'

# Store objects
incoming_requests = collections.deque(maxlen=10)
def request_handler(obj):
    incoming_requests.appendleft(obj)

# register api
hgxlink.register_api(request_api, object_handler=request_handler)

with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    IPython.embed()
    
# Not strictly necessary but suppresses warnings
hgxlink.halt()