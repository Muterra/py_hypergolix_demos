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
response_api = bytes(64) + b'\x02'

# Create an object collection
requests_incoming = collections.deque(maxlen=10)
responses_incoming = collections.deque(maxlen=10)
responses_outgoing = collections.deque(maxlen=10)


# Callback for incoming requests
def request_handler(obj):
    requests_incoming.appendleft(obj)
    reply = hgxlink.new_obj_threadsafe(
        state = obj.state,
        dynamic = True,
        api_id = response_api
    )
    reply.share_threadsafe(recipient=obj.author)
    responses_outgoing.appendleft(reply)
    
# Callback for incoming responses
def response_handler(obj):
    responses_incoming.appendleft(obj)


# Register APIs
hgxlink.register_api_threadsafe(request_api, request_handler)
hgxlink.register_api_threadsafe(response_api, response_handler)


# Identity addresses
razpi = Ghid(algo=1, address=b'"\x7f\x0bP\x85\x84\x13\xacv\x1f4\x0b\x1e\xad\x01n?\x8f\x9b\r\\\xe3\x1f$\x8b9;\xb6x\xe8\xb4\xd6{1\x01T=\xa7gp\x01u\xda~M\x1a\xa9\x95\x82\xc0\xde\xd8\x85#\xd51\xf2\xcf\xe6\xb2{\xbe\xfe\x13')
desktop = Ghid(algo=1, address=b'V\x9b\x87\xc3\xd8\xe2\xca\r\xd7\x9fa:,A\x0f\xddo\x05*\xc9\xd4 \xe9X\xcb\xff`\xd2\xd5\x16Q\xff^\r`\xa8\xf2\x1d\xbe)Yw\xf1\xb5\xbd\xd9\xb4_`2g\xe5\x0b\x7fr\xc0\xe6#\xfa\xb9\x15K\x1cY')


# Start an interactive IPython interpreter with local namespace, but
# suppress all IPython-related warnings.
with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    IPython.embed()
    
    
########################################################################
# This bit happens within ipython on desktop
########################################################################


# obj = hgxlink.new_obj_threadsafe(
#     state = b'Hello hypergolix!',
#     api_id = request_api,
#     dynamic = True
# )
# obj.share_threadsafe(razpi)
# response = responses_incoming.pop()
# obj.state
# response.state

# # Goto razpi 1
# # From razpi 2

# obj.update_threadsafe(b'will not propagate')
# obj.state
# response.state

# # Goto razpi 3
# # From razpi 4

# obj.state
# response.state
    
    
########################################################################
# This bit happens within ipython on razpi
########################################################################


# # From desktop 1

# my_response = responses_outgoing.pop()
# my_response.state

# obj = hgxlink.new_obj_threadsafe(
#     state = b'Hello hypergolix!',
#     api_id = request_api,
#     dynamic = True
# )
# obj.share_threadsafe(desktop)
# response = responses_incoming.pop()
# obj.state
# response.state

# # Goto desktop 2
# # From desktop 3

# my_response.update_threadsafe(b'these objects are independent')

# # Goto desktop 4