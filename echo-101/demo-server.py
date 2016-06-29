'''
This is being written too rapidly to talk about

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

import signal

from hypergolix.persisters import MemoryPersister
from hypergolix.persisters import PersisterBridgeServer

from hypergolix.utils import Aengel

from hypergolix.comms import Autocomms
from hypergolix.comms import WSBasicServer

backend = MemoryPersister()
aengel = Aengel()
server = Autocomms(
    autoresponder_class = PersisterBridgeServer,
    autoresponder_kwargs = { 'persister': backend, },
    connector_class = WSBasicServer,
    connector_kwargs = {
        'host': 'localhost',
        'port': 7770,
        # 48 bits = 1% collisions at 2.4 e 10^6 connections
        'birthday_bits': 48,
    },
    debug = True,
    aengel = aengel,
)

try:
    signal.signal(signal.SIGINT, aengel.stop)
    signal.signal(signal.SIGTERM, aengel.stop)
    # This is an intentional deadlock until someone else does something
    aengel._thread.join()
finally:
    aengel.stop()