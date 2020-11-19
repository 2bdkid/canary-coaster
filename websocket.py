#! /usr/bin/env python3

import asyncio
import websockets
import argparse
import json
import cbor2 as cbor

from websockets.exceptions import ConnectionClosed
from aiocoap import Message
from aiocoap import Context
from aiocoap import GET
from aiocoap import POST
from aiocoap.util.linkformat import parse as Parse


""" query resource directory, start observations, listen for connections """
async def start_websocket_server(query, port):
    weights = {}  # title -> weight
    uris = {}  # title -> URI
    observation_handles = set()
    protocol = await Context.create_client_context()

    """ send tare (POST) to to coaster weight resource"""
    async def send_tare_to_coaster(uri):
        tare_command = Message(code=POST, uri=uri)
        await protocol.request(tare_command).response

    """ receive tare command from UI """
    async def receive_tare(websocket):
        try:
            async for title in websocket:
                try:
                    asyncio.create_task(send_tare_to_coaster(uris[title]))
                except KeyError:
                    print('WARNING: received tare unknown coaster', title)
        except ConnectionClosed:
            pass


    """ send weights from websocket """
    async def send_weights(websocket, path):
        receive_tare_task = asyncio.create_task(receive_tare(websocket))

        while True:
            try:
                await websocket.send(cbor.dumps(weights))
                await asyncio.sleep(1)
            except ConnectionClosed:
                break

        receive_tare_task.cancel()

    """ make notifications available to websocket connections """
    async def start_rd_observation(uri):
        """ decode Message cbor payload to object """
        def decode_linkformat_payload(payload):
            link = payload.decode('ascii')
            myJson = Parse(link).as_json_string()
            return json.loads(myJson)

        """ start observation of resource """
        def process_resource(resource):
            uris[resource['title']] = resource['href']
            handle = asyncio.create_task(start_node_observation(resource['href'], resource['title']))
            observation_handles.add(handle)

        get_obs_req = Message(code=GET, uri=uri, observe=0)
        request = protocol.request(get_obs_req)
        initResponse = await request.response
        resources = decode_linkformat_payload(initResponse.payload)

        for resource in resources:
            process_resource(resource)

        async for response in request.observation:
            newResources = decode_linkformat_payload(response.payload)
            for resource in newResources:
                process_resource(resource)

    """ observe coaster weight resource at uri with title """
    async def start_node_observation(uri, title):
        get_obs_req = Message(code=GET, uri=uri, observe=0)
        request = protocol.request(get_obs_req)
        initResponse = await request.response
        weights[title] = cbor.loads(initResponse.payload)

        async for response in request.observation:
            weights[title] = cbor.loads(response.payload)

        del weights[title]
        del uris[title]

    await asyncio.gather(
        start_rd_observation(query),
        websockets.serve(send_weights, port=port)
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('query', help='CoAP resource directory query URI')
    parser.add_argument('--port', dest='port', required=True, type=int, help='TCP port for websocket to be attached to')
    args = parser.parse_args()
    asyncio.run(start_websocket_server(query=args.query, port=args.port))


if __name__ == '__main__':
    main()
