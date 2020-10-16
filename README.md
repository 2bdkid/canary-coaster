# IoT Project 3

## CoAP Server

The server requires the development version of aiocoap

```
git clone https://github.com/chrysn/aiocoap
cd aiocoap
pip3 install --user .
cd ..
pip3 install --user hx711
chmod +x server.py
./server.py --dout X --pd_sck Y  # GPIO pins X, Y
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
aiocoap-client coap://localhost/resource-lookup?temperature
```

