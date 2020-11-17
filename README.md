# IoT Project 3

## CoAP Server

The server requires the development version of aiocoap and a port of tatobari/hx711py to Python 3.
Remember that the resource directory must run on the well-known CoAP port so choose a different port for the CoAP server.
The server returns [CBOR](https://cbor.io) data.
It is very important to set the ep name. The resource directory differentiates nodes based on it.

```
git clone https://github.com/chrysn/aiocoap
cd aiocoap
pip3 install --user .
cd ..
cd hx711py
pip3 install --user .
cd ..
pip3 install --user cbor2

chmod +x server.py
./server.py -h  # look at the extra options
./server.py --ep rpi --dout X --pd_sck Y --rd coap://rd-ip --port PORT  # GPIO pins X, Y
```

To test the server

```
pip3 install --user pygments
pip3 install --user termcolor
aiocoap-client --observe --pretty-print --quiet coap://localhost:PORT/weight
```

To tare the load cell

```
aiocoap-client -m POST coap://localhost:PORT/weight
```

## Resource Directory

Going to use aiocoap's implementation.
Details: [CoRE Resource Directory](https://tools.ietf.org/html/draft-ietf-core-resource-directory-25).
Note: This is hardcoded to run on the well-known CoAP port.

```
aiocoap-rd
```

To test the RD (once CoAP server has registered)

```
pip3 install --user LinkHeader
aiocoap-client coap://localhost/resource-lookup/?rt=weight
```

## WebSocket Server

The WebSocket server queries the resource directory using the specified query URI, and observes all found resources.
Readings received from these resources are made available to incoming WebSocket connections.
Incomming connections may tare a scale by sending the title string of the scale, this informs the server to send a CoAP POST to the weight resource.

```
pip3 install --user LinkHeader
./websocket.py --port 5688 coap://<rd-ip>/resource-lookup/?rt=weight
```

```

## Observe data from WebSocket Server

```
python3 -m websockets ws://localhost:port/
```

## UI

When we get to the UI, [cbor-js](https://github.com/paroga/cbor-js) can decode CBOR data sent from the WebSocket server.

## Sequence Diagram

Note: This is a slight simplification. The registration process begins with a GET /.well-known/core to the RD, then the server chooses to POST to /resourcedirectory because its Resource-Type is core.rd

![Sequence Diagram](sequence.png)
