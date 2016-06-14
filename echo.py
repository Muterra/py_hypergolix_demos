import IPYthon
import warnings

from golix import Ghid
from hypergolix.service import HypergolixLink

hgxlink = HypergolixLink(threaded=True)

with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    IPython.embed()