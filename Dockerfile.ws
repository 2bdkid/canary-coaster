FROM python:3.9.1

WORKDIR /root

RUN pip install --user git+https://github.com/chrysn/aiocoap LinkHeader websockets cbor2

EXPOSE 5688/tcp

COPY websocket.py .

CMD python websocket.py --port ${PORT:-5688} ${RD:-coap://rd/resource-lookup/?rt=weight}
