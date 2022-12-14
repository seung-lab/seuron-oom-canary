FROM alpine AS compile-image
RUN apk add build-base

WORKDIR /root
COPY oom_canary.c .
RUN gcc -O0 -o oom_canary oom_canary.c

FROM python:3.10-alpine AS runtime-image

COPY --from=compile-image /root/oom_canary /
COPY requirements.txt oom_monitor.py /
RUN pip install --no-cache-dir -r requirements.txt 
