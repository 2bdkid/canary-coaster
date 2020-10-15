# IoT Project 3

## CoAP Server

The server requires the development version of aiocoap

```
git clone https://github.com/chrysn/aiocoap
cd aiocoap
pip3 install --user .
cd ..
pip3 install --user hx711
pip3 install --user LinkFormat
chmod +x server.py
./server.py --dout X --pd_sck Y  # GPIO pins X, Y
```

## get_well-known_core.py

This script sends a GET to /.well-known/core and displays links sent back