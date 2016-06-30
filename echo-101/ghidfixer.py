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
import re
import fileinput
import argparse

from golix import Ghid
from hypergolix.service import HypergolixLink


def update(filelist, ipc_port_1, ipc_port_2)
    hgxlink_desktop = HypergolixLink(ipc_port=ipc_port_1)
    hgxlink_razpi = HypergolixLink(ipc_port=ipc_port_2)
    desktop = repr(hgxlink_desktop.whoami_threadsafe())
    razpi = repr(hgxlink_razpi.whoami_threadsafe())

    for fname in filelist:
        with fileinput.FileInput(fname, inplace=True) as f:
            for line in f:
                if re.match(r'razpi = (Ghid\(.+\)$)', line):
                    print('razpi = ' + razpi)
                elif re.match(r'desktop = (Ghid\(.+\)$)', line):
                    print('desktop = ' + desktop)
                else:
                    print(line, end='')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description = 'Automatically update included demo files to use two ' +\
        'Hypergolix clients on the same machine.'
    )
    parser.add_argument(
        '--ipc_port_1', 
        action = 'store',
        default = 7770, 
        type = int,
        help = 'Specify the first ("desktop") IPC port [default: 7770]'
    )
    parser.add_argument(
        '--ipc_port_2', 
        action = 'store',
        default = 7771, 
        type = int,
        help = 'Specify the second ("razpi") IPC port [default: 7771]'
    )

    args = parser.parse_args()

    filelist = ['demo-1.py', 'demo-2.py', 'demo-3.py', 'demo-4.py']
    
    update(filelist, args.ipc_port_1, args.ipc_port_2)