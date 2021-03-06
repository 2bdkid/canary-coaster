#! /usr/bin/env python3

import argparse
import asyncio
import cbor2

from aiocoap import Context
from aiocoap import Message
from aiocoap import CONTENT
from aiocoap import CHANGED
from aiocoap.resource import Site
from aiocoap.resource import ObservableResource
from aiocoap.resource import WKCResource
from aiocoap.resourcedirectory.client.register import Registerer
from aiocoap.numbers.constants import COAP_PORT
from hx711 import HX711


class LoadCellSensor(ObservableResource):
    """ Construct LoadCellSensor with HX711 object.
        Polls sensor every poll_period seconds.
    """
    def __init__(self, hx711, poll_period, title):
        super().__init__()
        self._poll_period = poll_period
        self._hx711 = hx711
        self._handle = None
        self.rt = 'load weight'
        self.ct = 60  # application/cbor
        self.title = title

    def get_link_description(self):
        """ Returns dict of options suitable for LinkFormat.
            Includes title of sensor.
        """
        desc = super().get_link_description()
        desc['title'] = self.title
        return desc

    async def render_get(self, request):
        """ Returns Message with sensor weight reading encoded in CBOR."""
        weight = self.weight
        return Message(payload=cbor2.dumps(weight), content_format=60)

    async def render_post(self, request):
        """ Tare sensor and return CHANGED Message."""
        self._hx711.tare()
        return Message(code=CHANGED)

    def update_observation_count(self, count):
        """ starts/stops polling cycle as observations come."""
        if count and self._handle is None:
            self._start_polling()
        if count == 0 and self._handle:
            self._handle.cancel()
            self._handle = None

    @property
    def weight(self):
        """ Returns physical load cell reading."""
        return self._hx711.get_weight()

    async def _poll(self):
        """ Does 1 iteration of the polling cycle and returns Message
            with sensor weight in CBOR encoding.
        """
        while True:
            await asyncio.sleep(self._poll_period)
            weight = self.weight
            message = Message(payload=cbor2.dumps(weight), code=CONTENT, content_format=60)
            self.updated_state(message)

    def _start_polling(self):
        """ Starts the polling cycle."""
        self._handle = asyncio.get_event_loop().create_task(self._poll())


def get_command_line_arguments():
    parser = argparse.ArgumentParser()
    required = parser.add_argument_group('required arguments')
    required.add_argument('--dout', dest='dout', type=int,
                          help='GPIO pin: forwarded to HX711 constructor', required=True)
    required.add_argument('--pd_sck', dest='pd_sck', type=int,
                          help='GPIO pin: forwarded to HX711 constructor', required=True)
    parser.add_argument('--port', dest='port', type=int,
                        help='CoAP port (default: %i)' % COAP_PORT, default=COAP_PORT)
    parser.add_argument('--rd', dest='rd', help='Resource directory base URI (default: coap://localhost)',
                        default='coap://localhost')
    parser.add_argument('--ref-unit', dest='ref_unit', type=float,
                        help='HX711 reference unit (default: 1.0)', default=1.0)
    parser.add_argument('--title', dest='title', help='Resource title given to Resource Directory',
                        default="")
    parser.add_argument('--ep', dest='ep', help='EndPoint name', default=None)
    return parser.parse_args()


async def start_server(args):
    hx711 = HX711(args.dout, args.pd_sck)
    hx711.tare()
    hx711.set_reference_unit(args.ref_unit)

    root = Site()
    root.add_resource(['.well-known', 'core'],
                      WKCResource(root.get_resources_as_linkheader, impl_info=None))
    root.add_resource(['weight'], LoadCellSensor(hx711, 1, args.title))

    protocol = await Context.create_server_context(root, bind=('::', args.port))
    registration_parameters = {}
    if args.ep is not None:
        registration_parameters['ep'] = args.ep
    registration = Registerer(protocol, rd=args.rd, registration_parameters=registration_parameters)


def main():
    args = get_command_line_arguments()
    asyncio.get_event_loop().create_task(start_server(args))
    asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    main()
