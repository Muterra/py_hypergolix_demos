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
import time
import argparse
import logging

from hypergolix.persisters import MemoryPersister
from hypergolix.persisters import PersisterBridgeServer

from hypergolix.utils import Aengel

from hypergolix.comms import Autocomms
from hypergolix.comms import WSBasicServer
    
    
parser = argparse.ArgumentParser(
    description = 'Start a Hypergolix demo persistence server.'
)
parser.add_argument(
    '--host', 
    action = 'store',
    default = 'localhost', 
    type = str,
    help = 'Specify the persistence provider host [default: localhost]'
)
parser.add_argument(
    '--port', 
    action = 'store',
    default = 7770, 
    type = int,
    help = 'Specify the persistence provider port [default: 7770]'
)
parser.add_argument(
    '--logfile', 
    action = 'store',
    default = None, 
    type = str,
    help = 'Log to a specified file, relative to current directory.',
)
parser.add_argument(
    '--verbosity', 
    action = 'store',
    default = None, 
    type = str,
    help = 'Set debug mode and specify the logging level. '
            '"debug" -> most verbose, '
            '"info" -> somewhat verbose, '
            '"error" -> quiet.',
)
parser.add_argument(
    '--traceur', 
    action = 'store_true',
    help = 'Enable thorough analysis, including stack tracing. '
            'Implies verbosity of debug.'
)

args = parser.parse_args()

if args.verbosity is not None:
    debug = True
    log_level = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'error': logging.ERROR,
    }[args.verbosity.lower()]
else:
    debug = False
    log_level = logging.WARNING
    
if args.traceur:
    traceur = True
    debug = True
    log_level = logging.DEBUG
else:
    traceur = False
    
if args.logfile:
    logging.basicConfig(filename=args.logfile, level=log_level)
else:
    logging.basicConfig(level=log_level)
    

backend = MemoryPersister()
aengel = Aengel()
server = Autocomms(
    autoresponder_class = PersisterBridgeServer,
    autoresponder_kwargs = { 'persister': backend, },
    connector_class = WSBasicServer,
    connector_kwargs = {
        'host': args.host,
        'port': args.port,
        # 48 bits = 1% collisions at 2.4 e 10^6 connections
        'birthday_bits': 48,
    },
    debug = debug,
    aengel = aengel,
)

signame_lookup = {
    signal.SIGINT: 'SIGINT',
    signal.SIGTERM: 'SIGTERM',
}
def sighandler(signum, sigframe):
    raise ZeroDivisionError('Caught ' + signame_lookup[signum])

try:
    signal.signal(signal.SIGINT, sighandler)
    signal.signal(signal.SIGTERM, sighandler)
    
    # This is a little gross, but will be broken out of by the signal handlers
    # erroring out.
    while True:
        time.sleep(600)
        
except ZeroDivisionError as exc:
    logging.info(str(exc))