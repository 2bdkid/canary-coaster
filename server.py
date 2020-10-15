#! /usr/bin/env python3

from aiocoap import Context
from aiocoap import Message
from aiocoap import CONTENT
from aiocoap.resource import Site
from aiocoap.resource import ObservableResource
from aiocoap.resource import WKCResource
from hx711 import HX711

import argparse
import asyncio


class LoadCellSensor(ObservableResource):

    """ takes HX711 object as input
        poll sensor every poll_period seconds
    """
    def __init__(self, hx711, poll_period):
        super().__init__()
        self._poll_period = poll_period
        self._hx711 = hx711
        self._handle = None

    """ handles GET requests """
    async def render_get(self, request):
        weight = self._read_load_cell()
        return Message(payload=str(weight).encode('ascii'))

    """ start/stop polling cycle """
    def update_observation_count(self, count):
        if count and self._handle is None:
            self._start_polling()
        if count == 0 and self._handle:
            self._handle.cancel()
            self._handle = None

    """ read physical load cell """
    def _read_load_cell(self):
        return self._hx711.read_weight()

    """ polling cycle """
    def _poll(self):
        self._handle = asyncio.get_event_loop().call_later(self._poll_period, self._poll)
        weight = self._read_load_cell()
        message = Message(payload=str(weight).encode('ascii'), code=CONTENT)
        self.updated_state(message)

    """ initiate polling cycle """
    def _start_polling(self):
        self._handle = asyncio.get_event_loop().call_later(self._poll_period, self._poll)


def get_command_line_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dout', dest='dout', type=int,
                        help='GPIO pin: forwarded to HX711 constructor', required=True)
    parser.add_argument('--pd_sck', dest='pd_sck', type=int,
                        help='GPIO pin: forwarded to HX711 constructor', required=True)
    return parser.parse_args()


def main():
    args = get_command_line_arguments()
    hx711 = HX711(args.dout, args.pd_sck)  # TODO: set reference unit

    root = Site()
    root.add_resource(['.well-known', 'core'],
                      WKCResource(root.get_resources_as_linkheader, impl_info=None))
    root.add_resource(['weight'], LoadCellSensor(hx711, 1))

    asyncio.get_event_loop().create_task(Context.create_server_context(root))
    asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    main()
