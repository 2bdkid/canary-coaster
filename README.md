# IoT Project 3

## CoAP Server

```
git clone https://github.com/tatobari/hx711py.git
cd hx711py
python3 setup.py install --prefix=$HOME/.local/
cd ..
chmod +x server.py
./server.py --dout X --pd_sck Y  # GPIO pins X, Y

```