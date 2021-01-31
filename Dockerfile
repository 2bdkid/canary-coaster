FROM python:3.9.1 AS base

RUN pip install --user git+https://github.com/chrysn/aiocoap LinkHeader

WORKDIR /root

COPY hx711py hx711py

RUN pip install --user ./hx711py cbor2

FROM python:3.9.1-alpine

COPY --from=base /root/.local /root/.local

WORKDIR /root

COPY ./server.py .

EXPOSE 5683/udp

CMD python server.py --ep ${EP:-rpi}\
                     --dout ${DOUT:-23} \
                     --pd_sck ${PD_SCK:-24} \
                     --rd ${RD:-coap://rd} \
                     --title ${TITLE:-rpi} \
                     --ref-unit ${REF_UNIT:-441}
