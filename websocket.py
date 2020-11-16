#! /usr/bin/env python3

import asyncio
import websockets
import argparse
import json
import cbor2 as cbor

from websockets.exceptions import ConnectionClosed
from asyncio.queues import Queue
from aiocoap import Message
from aiocoap import Context
from aiocoap import GET
from aiocoap.util.linkformat import parse as Parse

async def start_websocket_server(uri, port):
    weights = {}
    observation_handles = set()
    
    """ send weights from websocket """
    async def send_weights(websocket, path):
        while True:
            try:
                await websocket.send(cbor.dumps(weights))
                await asyncio.sleep(1)
            except ConnectionClosed:
                break

    """ make notifications available to websocket connections """
    async def start_rd_observation(uri):
        protocol = await Context.create_client_context()
        get_obs_req = Message(code=GET, uri=uri, observe=0)
        request = protocol.request(get_obs_req)
        initResponse = await request.response
        
        link = str(initResponse.payload.decode('ascii'))
        myJson = Parse(link).as_json_string()
        resources = json.loads(myJson)
       
        for resource in resources:
            handle = asyncio.create_task(start_node_observation(resource['href'], resource['title']))
            observation_handles.add(handle)

        async for response in request.observation:
            link = str(response.payload.decode('ascii'))
            myJson = Parse(link).as_json_string()
            newResources = json.loads(myJson)
            for resource in newResources:
                handle = asyncio.create_task(start_node_observation(resource['href'], resource['title']))
                observation_handles.add(handle)

    async def start_node_observation(uri, title):
        protocol = await Context.create_client_context()
        get_obs_req = Message(code=GET, uri=uri, observe=0)
        request = protocol.request(get_obs_req)
        initResponse = await request.response
        
        weights[title] = cbor.loads(initResponse.payload)

        async for response in request.observation:    
            weights[title] = cbor.loads(response.payload)

    await asyncio.gather(
        start_rd_observation(uri),
        websockets.serve(send_weights, port=port)
    )

def main():
    parser = argparse.ArgumentParser()
    # Something like coap://<<IP>>:<<PORT>>/resource-lookup/?rt=weight
    parser.add_argument('rd', help='CoAP resource directory URI to observe')
    parser.add_argument('--port', dest='port', required=True, type=int, help='TCP port for websocket to be attached to')
    args = parser.parse_args()
    asyncio.run(start_websocket_server(uri=args.rd, port=args.port))


if __name__ == '__main__':
    main()
