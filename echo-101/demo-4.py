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
import time

from golix import Ghid
from hypergolix.service import HypergolixLink


# Link to hypergolix service
hgxlink = HypergolixLink()
hgxlink.new_token_threadsafe()

# Declare API
request_api = bytes(64) + b'\x01'
response_api = bytes(64) + b'\x02'

# Create an object collection
requests_outgoing = collections.deque(maxlen=10)
requests_incoming = collections.deque(maxlen=10)
responses_incoming = collections.deque(maxlen=10)
responses_outgoing = collections.deque(maxlen=10)


# Identity addresses
razpi = Ghid(algo=1, address=b'\t\xa5\x92\xfd\xc8V#5W\x82e>c~\x1fx\x0b\xd6\xcd\xd1$\n\xbe\x82\xe0\x08SS\xe1\xb8\xf8\xc9\xe0\xef\x13\x0bc\x8d\x18\xaf\x1a4\x10\x97\xfe\x96\xb8\x7f\x05\xc7Q\xd3\x81\x14H\xa7$sc$m\x0bzE')
desktop = Ghid(algo=1, address=b'T@\xfb\xbe\xc0\xf5\n\xac\x86\xdap\xc4I+\xc3\xc52]\xeb\xbe\xea\xfdAwY\xcb\xecH3\xa49\x19\xdd-Q\xe5\nt\x05\xbdP\xf7\xe5C\xac\r\n\xb7\xe7\xb4*6\x1d\xd9h\xeb\xcb\x0f2\x0e\x01,\xd4\xdd')

    
# Create update a timing object
timer = collections.deque([0,0], maxlen=2)

recipients = {razpi, desktop} - {hgxlink.whoami_threadsafe()}
# Automate creating requests
def make_request(msg):
    obj = hgxlink.new_object(
        state = msg,
        dynamic = True,
        api_id = request_api
    )
    for recipient in recipients:
        obj.share(recipient)
    return obj
    
# Time update reflection
def timed_update(obj, msg):
    timer.appendleft(time.monotonic())
    obj.update(msg)
    
def timed_update_callback(obj):
    timer.appendleft(time.monotonic())
    elapsed = timer[0] - timer[1]
    print('Update mirrored in', elapsed, 'seconds.')

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
    
    def state_mirror(source_obj):
        reply.update(source_obj.state)
    obj.add_callback(state_mirror)
    
# Callback for incoming responses
def response_handler(obj):
    obj.add_callback(timed_update_callback)
    responses_incoming.appendleft(obj)


# Register APIs
hgxlink.register_api_threadsafe(request_api, request_handler)
hgxlink.register_api_threadsafe(response_api, response_handler)


# Start an interactive IPython interpreter with local namespace, but
# suppress all IPython-related warnings.
with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    IPython.embed()
    
    
########################################################################
# This bit happens within ipython on desktop
########################################################################


# obj = make_request(b'hello')
# obj.state
# response = responses_incoming.pop()
# response.state

# timed_update(obj, b'world')
# # Wait for timeit display...
# obj.state
# response.state

# timed_update(obj, b'goodbye')
# timed_update(obj, b'thanks')