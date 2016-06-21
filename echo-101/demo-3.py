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
hgxlink = HypergolixLink(threaded=True)

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
    reply = hgxlink.new_object(
        state = obj.state,
        dynamic = True,
        api_id = response_api
    )
    reply.share(recipient=obj.author)
    responses_outgoing.appendleft(reply)
    
# Callback for incoming responses
def response_handler(obj):
    responses_incoming.appendleft(obj)


# Register APIs
hgxlink.register_api(request_api, request_handler)
hgxlink.register_api(response_api, response_handler)


# Identity addresses
razpi = Ghid(algo=1, address=b"$\xf4\xf9%]\xbf\x04R\x9fw\x01\xbcJ\xc8&\x8a!]\xb8\x18\xd9c\xca\t8\x08\xc9j\x97\xbf\xfb\x0f\x87\xb0\x03\xea\x00j\x03\x99k\xe9!%\xb3\x8d\xebe\xab9D)\xf1:'MaN*LU\x1c\xd6\xd0")
desktop = Ghid(algo=1, address=b'\x93x\xc5\xa9Q\xc9\xdf\x9a.\xa3O\xed&\x8b\x05\xb2\xf7\xa3Z\\-Wz\xe9D\x92\xc5e\x8b~k\xab\x82Q\xfdQ\xc1\xc2\xb0\xc8\xcf=`X)\x8fmq\xd8\x937\x17\xa3+Y\xc9\tR\xe3\x98G\x18\x80\xf7')


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
# response = responses_incoming.pop()
# obj.state
# response.state

# # Goto razpi 1
# # From razpi 2

# obj.update(b'will not propagate')
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

# obj = hgxlink.new_object(
#     state = b'Hello hypergolix!',
#     api_id = request_api,
#     dynamic = True
# )
# obj.share(desktop)
# response = responses_incoming.pop()
# obj.state
# response.state

# # Goto desktop 2
# # From desktop 3

# my_response.update(b'these objects are independent')

# # Goto desktop 4