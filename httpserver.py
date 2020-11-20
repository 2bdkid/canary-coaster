#! /usr/bin/env python3

import cbor2
import argparse

from bottle import route, run, template, response
from hx711 import HX711


def start_server(hx711, bind, port):
    @route('/weight')
    def temp():
        t = hx711.get_weight()
        response.set_header('Content-Type', 'application/cbor')
        return cbor2.dumps(t)

    run(host=bind, port=port)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ref-unit', dest='ref_unit', type=float,
                        help='HX711 reference unit (default: 1.0)', default=1.0)
    parser.add_argument('--bind', dest='bind', default='127.0.0.1', help='Bind address')
    parser.add_argument('--port', dest='port', type=int, default=80,
                        help='Listens on this port')
    required = parser.add_argument_group('required arguments')
    required.add_argument('--dout', dest='dout', type=int,
                          help='GPIO pin: forwarded to HX711 constructor', required=True)
    required.add_argument('--pd_sck', dest='pd_sck', type=int,
                          help='GPIO pin: forwarded to HX711 constructor', required=True)
    args = parser.parse_args()

    hx711 = HX711(args.dout, args.pd_sck)
    hx711.set_reference_unit(args.ref_unit)
    start_server(hx711, args.bind, args.port)


if __name__ == '__main__':
    main()

