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

# Just for interactive interpreter
import IPython
import warnings

# Actually for application
import collections

from golix import Ghid
from hypergolix.service import HypergolixLink


# Link to hypergolix service
hgxlink = HypergolixLink()
hgxlink.new_token_threadsafe()
# Declare API
request_api = bytes(64) + b'\x01'
# Create an object collection
incoming = collections.deque(maxlen=10)


# Callbacks for incoming objects
def request_handler(obj):
    incoming.appendleft(obj)


# Register API
hgxlink.register_api_threadsafe(request_api, request_handler)


# Identity addresses
razpi = Ghid(algo=1, address=b'\t\xa5\x92\xfd\xc8V#5W\x82e>c~\x1fx\x0b\xd6\xcd\xd1$\n\xbe\x82\xe0\x08SS\xe1\xb8\xf8\xc9\xe0\xef\x13\x0bc\x8d\x18\xaf\x1a4\x10\x97\xfe\x96\xb8\x7f\x05\xc7Q\xd3\x81\x14H\xa7$sc$m\x0bzE')
desktop = Ghid(algo=1, address=b'T@\xfb\xbe\xc0\xf5\n\xac\x86\xdap\xc4I+\xc3\xc52]\xeb\xbe\xea\xfdAwY\xcb\xecH3\xa49\x19\xdd-Q\xe5\nt\x05\xbdP\xf7\xe5C\xac\r\n\xb7\xe7\xb4*6\x1d\xd9h\xeb\xcb\x0f2\x0e\x01,\xd4\xdd')


# Start an interactive IPython interpreter with local namespace, but
# suppress all IPython-related warnings.
with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    IPython.embed()
    
    
########################################################################
# This bit happens within ipython on desktop
########################################################################


# obj = hgxlink.new_object(
#     state = b'Hello hypergolix!',
#     api_id = request_api,
#     dynamic = True
# )
# obj.share(razpi)

# # Goto razpi 1
# # From razpi 2

# obj.update(b'Is this thing on?')

# # Goto razpi 3
# # From razpi 4

# obj.update(b'Yes it is')
    
    
########################################################################
# This bit happens within ipython on razpi
########################################################################


# # From desktop 1

# obj = incoming.pop()
# obj.state

# # Goto desktop 2
# # From desktop 3

# obj.state

# def update_callback(obj):
#     print(obj.state)
    
# obj.add_callback(update_callback)

# # Goto desktop 4