# Hypergolix 101: dynamic echo server

Goal: introduce Hypergolix by writing an echo server. By the end of this demo, you should be able to create, update, and share objects between computers, and to set update callbacks for those objects.

Duration: video is about 10 minutes. Your timing may vary!

[![Watch the demo](/echo-101/echo-101-video.png)](https://www.youtube.com/watch?v=UkLBKKsqq2Y)

#### Included source files:

**Note that these will require adjustment of the ```razpi``` and ```desktop``` variables to run.** The included ghidfixer tool will automatically update demo-0 through demo-4 as appropriate, assuming you have two *local* Hypergolix services running using ipc_ports 7770 and 7771.

+ [demo-server.py](/echo-101/demo-server.py): A persistence server.
+ [demo-0.py](/echo-101/demo-0.py): First steps.
+ [demo-1.py](/echo-101/demo-1.py): Sharing our first object.
+ [demo-2.py](/echo-101/demo-2.py): Testing dynamic updates
+ [demo-3.py](/echo-101/demo-3.py): Experiments in parroting
+ [demo-4.py](/echo-101/demo-4.py): Performance assessment
+ [demo-4-instrumented.py](/echo-101/demo-4-instrumented.py): Demo-4, with logging.
+ [demo-4a-instrumented.py](/echo-101/demo-4a-instrumented.py): Demo-4, with logging, using IPC port 7771.
+ [ghidfixer.py](/echo-101/ghidfixer.py): Tool to automatically replace ```razpi``` and ```desktop``` address ```Ghid```s within demo-0.py, demo-1.py, demo-2.py, demo-3.py, and demo-4.py. Can be configured.

## First steps: linking an application, basic objects, and discovery

First, ensure that both computers' Hypergolix background services are [up and running](/README.md#running-hypergolix), and that they have successfully connected to the same [persistence server](/echo-101/demo-server-readme.md). If you want to follow along directly, you'll also want to pip install ```IPython``` and ```pyperclip```.

Now, import Ghid (the hash addresses used by Golix and Hypergolix) and HypergolixLink. Then, start the link, and drop into an IPython interactive session:

```python
from golix import Ghid
from hypergolix.service import HypergolixLink

# Note: if you want to run on a different IPC port, pass ipc_port=XXXX as kwarg
hgxlink = HypergolixLink()

# Start an interactive IPython interpreter with local namespace, but
# suppress all IPython-related warnings.
with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    IPython.embed()
```

Now we have a basic Hypergolix environment to play with. First, we need to get an app token from the Hypergolix service. This is just a unique identifier for our application that helps Hypergolix decide where to send incoming objects.

```python
hgxlink.new_token_threadsafe()
```

Now let's try creating a new, private object:

```python
obj = hgxlink.new_obj_threadsafe(
    state = b'Hello hypergolix!',
    private = True,
    dynamic = True
)
```

Like all other Hypergolix objects, private objects are end-to-end encrypted; however, unlike standard sharable objects, private objects are only available to our specific application. They cannot be shared with other Hypergolix users, and nor can they be shared with other Hypergolix applications. However, they can be updated at will, and that update will be saved to the Hypergolix persistence server and propagate to any other identical applications for the same Hypergolix user:

```python
obj.update_threadsafe(b'A fine day for a demo!')
obj.update_threadsafe(b'Wubbalubbadubdub!')
```

Because sharing a Hypergolix object is a push operation, the recipient needs some kind of identifier so Hypergolix can figure out where to send the shared object. This identifier is the ```api_id```, and it is required for all sharable objects. It can be thought of as a unique identifier for the binary API schema used by the object. They are 65 bytes long, and by convention the first byte is always ```0x00```.

When registering these ```api_id```s with Hypergolix, we tell it two things: first, that this application can handle objects of that type, and second, when incoming objects of that type are shared with the Hypergolix user, pass them to the specified ```object_handler``` callback:

```python
dummy_api = bytes(64) + b'\x07'
hgxlink.register_api_threadsafe(dummy_api, object_handler=print)

obj = hgxlink.new_obj_threadsafe(
    state = b'Hello hypergolix!',
    api_id = dummy_api,
    dynamic = True
)
```

Now we're ready to share this object with our other computer. To do that, we need to know both of our public key fingerprints. Like all content on a (Hyper)Golix network, these are represented by "Golix Hash Identifiers", or GHIDs:

```python
>>> repr(hgxlink.whoami_threadsafe())
Ghid(algo=1, address=b"$\xf4\xf9%]\xbf\x04R\x9fw\x01\xbcJ\xc8&\x8a!]\xb8\x18\xd9c\xca\t8\x08\xc9j\x97\xbf\xfb\x0f\x87\xb0\x03\xea\x00j\x03\x99k\xe9!%\xb3\x8d\xebe\xab9D)\xf1:'MaN*LU\x1c\xd6\xd0")
>>> import pyperclip
>>> # This copies our Ghid to the clipboard
>>> pyperclip.copy(repr(hgxlink.whoami_threadsafe()))
```

With that, Pyperclip has copied our Ghid address to the clipboard. Now we're ready for something a little more involved. Exit the interactive session by typing ```exit()```, and let's return to editing.

## Sharing our first object

This is a short one. Let's first consolidate what we did in our last IPython session:

```python
# Just for interactive interpreter
import IPython
import warnings

# Actually for application
from golix import Ghid
from hypergolix.service import HypergolixLink

# Link to hypergolix service
hgxlink = HypergolixLink()
hgxlink.new_token_threadsafe()

# Declare API
request_api = bytes(64) + b'\x01'
# Register API
hgxlink.register_api_threadsafe(request_api, print)
```

And now let's paste in both of our public key fingerprints / GHIDs (one from each machine), and go back to interactivity (on both machines):

```python
# Identity addresses
razpi = Ghid(algo=1, address=b"$\xf4\xf9%]\xbf\x04R\x9fw\x01\xbcJ\xc8&\x8a!]\xb8\x18\xd9c\xca\t8\x08\xc9j\x97\xbf\xfb\x0f\x87\xb0\x03\xea\x00j\x03\x99k\xe9!%\xb3\x8d\xebe\xab9D)\xf1:'MaN*LU\x1c\xd6\xd0")
desktop = Ghid(algo=1, address=b'\x93x\xc5\xa9Q\xc9\xdf\x9a.\xa3O\xed&\x8b\x05\xb2\xf7\xa3Z\\-Wz\xe9D\x92\xc5e\x8b~k\xab\x82Q\xfdQ\xc1\xc2\xb0\xc8\xcf=`X)\x8fmq\xd8\x937\x17\xa3+Y\xc9\tR\xe3\x98G\x18\x80\xf7')


# Start an interactive IPython interpreter with local namespace, but
# suppress all IPython-related warnings.
with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    IPython.embed()
```

Now, let's just create an object and share it. We should see our object handler get called on the receiving machine -- in this case, it's just ```print(obj)```:

```python
obj = hgxlink.new_obj_threadsafe(
    state = b'Hello hypergolix!',
    api_id = request_api,
    dynamic = True
)
obj.share_threadsafe(razpi)
```

Success! Back to the editing board.

## Adding a simple object handler and manipulating objects

This time, let's do just a little more with the incoming objects. Instead of printing and then discarding them, let's store them in a deque for easy use:

```python
# Create an object collection
incoming = collections.deque(maxlen=10)

# Callbacks for incoming objects
def request_handler(obj):
    incoming.appendleft(obj)

# Register API
hgxlink.register_api_threadsafe(request_api, request_handler)
```

Or, for the full source (this time around):

```python
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
razpi = Ghid(algo=1, address=b"$\xf4\xf9%]\xbf\x04R\x9fw\x01\xbcJ\xc8&\x8a!]\xb8\x18\xd9c\xca\t8\x08\xc9j\x97\xbf\xfb\x0f\x87\xb0\x03\xea\x00j\x03\x99k\xe9!%\xb3\x8d\xebe\xab9D)\xf1:'MaN*LU\x1c\xd6\xd0")
desktop = Ghid(algo=1, address=b'\x93x\xc5\xa9Q\xc9\xdf\x9a.\xa3O\xed&\x8b\x05\xb2\xf7\xa3Z\\-Wz\xe9D\x92\xc5e\x8b~k\xab\x82Q\xfdQ\xc1\xc2\xb0\xc8\xcf=`X)\x8fmq\xd8\x937\x17\xa3+Y\xc9\tR\xe3\x98G\x18\x80\xf7')

# Start an interactive IPython interpreter with local namespace, but
# suppress all IPython-related warnings.
with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    IPython.embed()
```

Now run it (again, make sure you start it on both computers), and we should be ready to play. From the interactive terminal on our development machine, first let's create and share an object:

```python
obj = hgxlink.new_obj_threadsafe(
    state = b'Hello hypergolix!',
    api_id = request_api,
    dynamic = True
)
obj.share_threadsafe(razpi)
```

Now let's move over to the other computer (from here on out I'm calling them "desktop" for the development box and "razpi" for the echo server) and check out the object a bit...

```python
>>> obj = incoming.pop()
>>> obj.state
b'Hello hypergolix!'
```

Excellent. Both objects have the same state. Is that still true if we update the object? Let's go back to the desktop to find out:

```python
>>> # Call from the desktop
>>> obj.update_threadsafe(b'Is this thing on?')
>>> # Call from the razpi
>>> obj.state
b'Is this thing on?'
```

It does! Awesome. Okay, now let's add a quick update callback, just so that every time we get an update, we'll print it out. Here, just in the razpi terminal:

```python
def update_callback(obj):
    print(obj.state)
    
obj.append_threadsafe_callback(update_callback)
```

Now call ```obj.update_threadsafe``` from the desktop again, and watch the updates roll in!

## Static echo

Okay, we're starting to get the hang of it. Let's add a second ```api_id``` for a response object, update our ```request_handler```, and make a new ```response_handler``` function:

```python
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
razpi = Ghid(algo=1, address=b"$\xf4\xf9%]\xbf\x04R\x9fw\x01\xbcJ\xc8&\x8a!]\xb8\x18\xd9c\xca\t8\x08\xc9j\x97\xbf\xfb\x0f\x87\xb0\x03\xea\x00j\x03\x99k\xe9!%\xb3\x8d\xebe\xab9D)\xf1:'MaN*LU\x1c\xd6\xd0")
desktop = Ghid(algo=1, address=b'\x93x\xc5\xa9Q\xc9\xdf\x9a.\xa3O\xed&\x8b\x05\xb2\xf7\xa3Z\\-Wz\xe9D\x92\xc5e\x8b~k\xab\x82Q\xfdQ\xc1\xc2\xb0\xc8\xcf=`X)\x8fmq\xd8\x937\x17\xa3+Y\xc9\tR\xe3\x98G\x18\x80\xf7')


# Start an interactive IPython interpreter with local namespace, but
# suppress all IPython-related warnings.
with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    IPython.embed()
```

Okay. Once more to the interactive interpreter, this time on the desktop:

```python
obj = hgxlink.new_obj_threadsafe(
    state = b'Hello hypergolix!',
    api_id = request_api,
    dynamic = True
)
obj.share_threadsafe(razpi)
response = responses_incoming.pop()
```

Check it out! The Pi automatically handled our request, and ran client-side code to create a response to send back. Play with the response a bit; in particular, compare ```obj.state``` and ```response.state```. If we update the original request on the desktop, will it propagate?

```python
>>> obj.update_threadsafe(b'Do updates mirror back?')
>>> obj.state
b'Do updates mirror back?'
>>> response.state
b'Hello hypergolix!'
```

No, they don't, because the request and the response are completely independent objects. Remember that we're running all client-side code here, and everything is end-to-end encrypted; there's no inherent connection between the request the desktop creates and the response the Pi answered with *unless we code it ourselves!* For that, we just need to add an update callback.

# Dynamic echo, plus performance feedback

To start with, we want to modify the request handler so that new updates will be delivered back to the desktop via the response object. While we're at it, let's create a make_request function so we don't have to keep manually creating objects and sharing them:

```python
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
    
    def state_mirror(source_obj):
        reply.update_threadsafe(source_obj.state)
    obj.append_threadsafe_callback(state_mirror)
```

And now, as long as we don't garbage collect those objects, we should be good to go. While we're at it, though, let's time to see how long it takes Hypergolix to make the entire round trip. I won't go into much detail, and it won't be particularly precise, but here's the final code:

```python
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
razpi = Ghid(algo=1, address=b'\x01\xa0\xdc\xbc\xd45\x17|JF\x01s\xf6f\xdb\xe65O,\x82v\xc7\xea&|\xd1,\xecZ\xd3vp\x82\xca\xd5ko7\x84\xa8-\x1a\xd1\x15j\x04\xb4\xa7\x0e\x92\xe9\xa2\xe2\xc8\x80\xa6J\xb59\x8f\xda:@\xfb')
desktop = Ghid(algo=1, address=b'\x14` \xcb\xbbW\x1f*UL\xe4-\xb2\xcc\x16\xee\x03\xca\x0e\xde\x81hp\xe5@\xf2D\xcf_\xb6\xf7\x87\xa25\xc4\x04L\xf8\xd2O\xaa\x95\xa2\x991\xf3(H\xbf\x9bGu\xbbs\xc9xkW\x98\xa3\x02\xed2\xa1')

    
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
    print('Update mirrored in', elapsed, 'seconds.')

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
    
    def state_mirror(source_obj):
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
```

Pop back into the interpreter and let's see how it does. First, create the request/response. We won't get timing here (though if we did, it'd be a bit slower), but it will get everything set up on the desktop and the Pi:


```python
obj = make_request(b'hello')
obj.state
response = responses_incoming.pop()
response.state
```

And now for the big reveal, using our new helper function ```timed_update``` to roughly time the round-trip latency:

```python
timed_update(obj, b'world')
```

If everything went well, you should see a ```print```ed line with the timing. I generally see round-trip latency in the 0.5-1.0 second range. There's still definitely some room for improvement, but still, not bad. And the kicker:

```python
>>> obj.state
b'world'
>>> response.state
b'world'
```

Neat, right?!