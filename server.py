#! /usr/bin/env python3

import argparse
import asyncio
import struct

from aiocoap import Context
from aiocoap import Message
from aiocoap import CONTENT
from aiocoap.resource import Site
from aiocoap.resource import ObservableResource
from aiocoap.resource import WKCResource
from aiocoap.resourcedirectory.client.register import Registerer
from aiocoap.numbers.constants import COAP_PORT
from hx711 import HX711


class LoadCellSensor(ObservableResource):

    """ takes HX711 object as input
        poll sensor every poll_period seconds
    """
    def __init__(self, hx711, poll_period):
        super().__init__()
        self._poll_period = poll_period
        self._hx711 = hx711
        self._handle = None
        self.rt = 'load weight'

    """ handles GET requests """
    async def render_get(self, request):
        weight = self._read_load_cell()
        return Message(payload=struct.pack('!f', weight))

    """ start/stop polling cycle """
    def update_observation_count(self, count):
        if count and self._handle is None:
            self._start_polling()
        if count == 0 and self._handle:
            self._handle.cancel()
            self._handle = None

    """ read physical load cell """
    def _read_load_cell(self):
        return self._hx711.get_weight()

    """ polling cycle """
    def _poll(self):
        self._handle = asyncio.get_event_loop().call_later(self._poll_period, self._poll)
        weight = self._read_load_cell()
        message = Message(payload=struct.pack('!f', weight), code=CONTENT)
        self.updated_state(message)

    """ initiate polling cycle """
    def _start_polling(self):
        self._handle = asyncio.get_event_loop().call_later(self._poll_period, self._poll)


def get_command_line_arguments():
    parser = argparse.ArgumentParser()
    required = parser.add_argument_group('required arguments')
    required.add_argument('--dout', dest='dout', type=int,
                        help='GPIO pin: forwarded to HX711 constructor', required=True)
    required.add_argument('--pd_sck', dest='pd_sck', type=int,
                        help='GPIO pin: forwarded to HX711 constructor', required=True)
    parser.add_argument('--port', dest='port', type=int, help='CoAP port (default: %i)' % COAP_PORT, default=COAP_PORT)
    parser.add_argument('--rd', dest='rd', help='Resource directory base URI (default: coap://localhost)', default='coap://localhost')
    parser.add_argument('--ep', dest='ep', help='EndPoint name (default: determined by hostname)', default=None)
    parser.add_argument('--ref-unit', dest='ref_unit', type=float, help='HX711 reference unit (default: 1.0)', default=1.0)
    return parser.parse_args()


async def start_server(args):
    hx711 = HX711(args.dout, args.pd_sck)
    hx711.tare()
    hx711.set_reference_unit(args.ref_unit)

    root = Site()
    root.add_resource(['.well-known', 'core'],
                      WKCResource(root.get_resources_as_linkheader, impl_info=None))
    root.add_resource(['weight'], LoadCellSensor(hx711, 1))

    protocol = await Context.create_server_context(root, bind=('::', args.port))
    registration = Registerer(protocol, rd=args.rd, registration_parameters=dict(ep=args.ep))


def main():
    args = get_command_line_arguments()
    asyncio.get_event_loop().create_task(start_server(args))
    asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    main()
