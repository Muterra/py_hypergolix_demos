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

import logging
logging.basicConfig(filename='demo4.log', level=logging.DEBUG)

# Just for interactive interpreter
import IPython
import warnings

# Actually for application
import collections
import time

from golix import Ghid
from hypergolix.service import HypergolixLink


# Link to hypergolix service
hgxlink = HypergolixLink(debug=True)
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
razpi = Ghid(algo=1, address=b'N,M\x8aq1\xf6LL\xf0\xd9\xa3\x0c\x909\xd2\xf7\xb9\xc6 \xc9\xa4\x82W\x00\xbcQF\x80*X\x01\xd2\xf84\xb7!\xa0\xa7\xe6\xff\xc6y\xcc\x8c\xc0\xa39p\xf3\x8eZC\xe2\x90\xbd\xb0\xed\x01\x1fg\x00\xbf&')
desktop = Ghid(algo=1, address=b'+`\xe2\x8b.\xa5DC\x0e?\xfe\x01\x95n\xa9\xdf\xe9\xc0\xbc;\xd3\x95:\x16\xe77^NqOb@\xbf\x18\xa8\x0ejw\x8d\x81\x8a\x07X>\xc9\xebW\xb1\xdc\xaf&\xfeQ\xcf\x85,\x9c\xf6P\xda\xc4\xa6\xd6+')

    
# Create update a timing object
timer = collections.deque([0,0], maxlen=2)

recipients = {razpi, desktop} - {hgxlink.whoami_threadsafe()}
# Automate creating requests
def make_request(msg):
    obj = hgxlink.new_obj_threadsafe(
        state = msg,
        dynamic = True,
        api_id = request_api
    )
    for recipient in recipients:
        obj.share_threadsafe(recipient)
    return obj
    
# Time update reflection
def timed_update(obj, msg):
    timer.appendleft(time.monotonic())
    obj.update_threadsafe(msg)
    
def timed_update_callback(obj):
    timer.appendleft(time.monotonic())
    elapsed = timer[0] - timer[1]
    logging.info('Update mirrored in ' + str(elapsed) + ' seconds.')
    print('Update mirrored in', elapsed, 'seconds.')

# Callback for incoming requests
def request_handler(obj):
    requests_incoming.appendleft(obj)
    logging.debug('Incoming request!')
    reply = hgxlink.new_obj_threadsafe(
        state = obj.state,
        dynamic = True,
        api_id = response_api
    )
    logging.debug('Reply created.')
    reply.share_threadsafe(recipient=obj.author)
    logging.debug('Reply shared.')
    responses_outgoing.appendleft(reply)
    
    def state_mirror(source_obj):
        logging.info('Received update. Mirroring.')
        reply.update_threadsafe(source_obj.state)
    obj.append_threadsafe_callback(state_mirror)
    
# Callback for incoming responses
def response_handler(obj):
    obj.append_threadsafe_callback(timed_update_callback)
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