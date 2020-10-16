#! /usr/bin/env python3

import asyncio

from aiocoap import Context
from aiocoap import Message
from aiocoap import GET


async def main():
    protocol = await Context.create_client_context()
    get_rd_req = Message(code=GET, uri='coap://localhost/resource-lookup/?rt=temperature')
    response = await protocol.request(get_rd_req).response
    print('%s' % response.payload.decode('ascii'))
    

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
