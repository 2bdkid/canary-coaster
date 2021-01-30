FROM python:3.9 AS base

WORKDIR /root

COPY hx711py hx711py

RUN pip install --user ./hx711py

FROM python:3.9

EXPOSE 5683/udp

COPY --from=base /root/.local /root/.local

RUN pip install --user git+https://github.com/chrysn/aiocoap LinkHeader cbor2

WORKDIR /root

COPY ./server.py .

CMD python server.py --ep ${EP:-rpi}\
                       --dout ${DOUT:-23} \
		       --pd_sck ${PD_SCK:-24} \
		       --rd ${RD:-coap://rd}
