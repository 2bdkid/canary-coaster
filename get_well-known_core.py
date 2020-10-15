#! /usr/bin/env python3

import asyncio
import json

from aiocoap import Context
from aiocoap import Message
from aiocoap import GET
from aiocoap.util.linkformat import parse


async def main():
    protocol = await Context.create_client_context()
    get_rd_req = Message(code=GET, uri='coap://192.168.1.254/.well-known/core')
    response = await protocol.request(get_rd_req).response
    linkformat = parse(response.payload.decode('ascii'))
    rd_data = json.loads(linkformat.as_json_string())

    print('%s' % linkformat)
    
    for resource in rd_data:
        print('%s%s' % (response.remote.uri_base, resource['href']))
    

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
