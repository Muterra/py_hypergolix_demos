import IPython
import warnings

from golix import Ghid
from hypergolix.service import HypergolixLink

hgxlink = HypergolixLink(threaded=True)

desktop = Ghid(algo=1, address=b"\xeb\x16\xc5\x8a\x066>\xceT\x19\xc2\xbc\x00\xe2j\xc2X\xf9\xb7\x10\x05h\xbbZVk\xca0\x8d\xe9#\x11\x0e\x12\x8c<\x85zb\x96w\x9d\xb6\x0e#\xa2\xd6\xa9\xa6\x99T\xce\x96\x86\x8c\x0bV\x10'b\x98\xeeeb")
razpi = 

with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    IPython.embed()