FROM python:3.9

EXPOSE 5683/udp

RUN pip install git+https://github.com/chrysn/aiocoap && pip install LinkHeader

CMD aiocoap-rd
