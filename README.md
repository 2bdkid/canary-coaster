# IoT Project 3

## CoAP Server

The server requires the development version of aiocoap and a port of tatobari/hx711py to Python 3

```
git clone https://github.com/chrysn/aiocoap
cd aiocoap
pip3 install --user .
cd ..
cd hx711py
pip3 install --user .
cd ..
chmod +x server.py
./server.py -h  # look at the extra options
./server.py --dout X --pd_sck Y  # GPIO pins X, Y
```

To test the server

```
aiocoap-client --observe coap://localhost/weight
```

## Resource Directory

Going to use aiocoap's implementation

Details: [CoRE Resource Directory](https://tools.ietf.org/html/draft-ietf-core-resource-directory-25)

Note: This is hardcoded to run on the well-known CoAP port

```
python3 -m aiocoap.cli.rd
```

To test the RD

```
aiocoap-client coap://localhost/resource-lookup/?rt=weight
```

## Sequence Diagram

Note: This is a slight simplification. The registration process begins with a GET /.well-known/core to the RD, then the server chooses to POST to /resourcedirectory because its Resource-Type is core.rd

![Sequence Diagram](sequence.png)
