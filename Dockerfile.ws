FROM python:3.9.1-alpine AS base

RUN apk add --no-cache git

RUN pip install --user git+https://github.com/chrysn/aiocoap LinkHeader

RUN pip install --user websockets cbor2

FROM python:3.9.1-alpine

COPY --from=base /root/.local /root/.local

WORKDIR /root

COPY websocket.py .

EXPOSE 5688/tcp

CMD python websocket.py --port ${PORT:-5688} ${RD:-coap://rd/resource-lookup/?rt=weight}
