'''
LICENSING
-------------------------------------------------

hypergolix: A python Golix client.
    Copyright (C) 2016 Muterra, Inc.
    
    Contributors
    ------------
    Nick Badger 
        badg@muterra.io | badg@nickbadger.com | nickbadger.com

    This library is free software; you can redistribute it and/or
    modify it under the terms of the GNU Lesser General Public
    License as published by the Free Software Foundation; either
    version 2.1 of the License, or (at your option) any later version.

    This library is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public
    License along with this library; if not, write to the 
    Free Software Foundation, Inc.,
    51 Franklin Street, 
    Fifth Floor, 
    Boston, MA  02110-1301 USA

------------------------------------------------------

'''

import IPython
import warnings

from golix import Ghid
from hypergolix.service import HypergolixLink


hgxlink = HypergolixLink()


# Start an interactive IPython interpreter with local namespace, but
# suppress all IPython-related warnings.
with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    IPython.embed()
    
    
########################################################################
# This bit happens within ipython.
########################################################################
    
# hgxlink.new_token_threadsafe()

# obj = hgxlink.new_object(
#     state = b'Hello hypergolix!',
#     private = True,
#     dynamic = True
# )

# obj.update(b'A fine day for a ride in the Scottish countryside!')
# obj.update(b'Wubbalubbadubdub')

# dummy_api = bytes(64) + b'\x07'
# hgxlink.register_api_threadsafe(dummy_api, print)

# obj = hgxlink.new_object(
#     state = b'Hello hypergolix!',
#     api_id = dummy_api,
#     dynamic = True
# )
    
# import pyperclip
# pyperclip.copy(repr(hgxlink.whoami_threadsafe()))