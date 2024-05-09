ARG PYVER=python.version
ARG DEBIANVER=os.version
ARG PREBUILT_PKG=package.version

FROM python:${PYVER}-${DEBIANVER}

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /cse-live-stream-agent

COPY packages/${PREBUILT_PKG} /cse-live-stream-agent/${PREBUILT_PKG}
COPY requirements.txt /cse-live-stream-agent/requirements.txt
COPY stream_agent.py /cse-live-stream-agent/stream_agent.py

RUN pip3 install -r requirements.txt && \
    rm -rf /root/.cache

CMD [ "/bin/bash" ]