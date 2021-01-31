FROM python:3.9.1-alpine AS base

RUN apk add --no-cache git

RUN pip install --user git+https://github.com/chrysn/aiocoap LinkHeader

FROM python:3.9.1-alpine

COPY --from=base /root/.local /root/.local

EXPOSE 5683/udp

CMD python3 -m aiocoap.cli.rd
