import IPython
import warnings

from golix import Ghid
from hypergolix.service import HypergolixLink

hgxlink = HypergolixLink(threaded=True)
desktop = Ghid(algo=1, address=b'\xc0TZ\x15+\x9a\x8e\x01\xbbvw\x83\xc8%\xd5RG\x9c8<\xf7\x1f\xa4e\x08\xc4\x9a\xa0o\x15\x83f\xf2>P/\xc1\xfbj3\xd6\xa9M\x03z\x98\x1b\xa7U\xb9b\xf3 \xfd\x81T+\xb3\x14\xaa\xcf$s\xac')


with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    IPython.embed()
    
# Not strictly necessary but suppresses warnings
hgxlink.halt()