FROM        python:3.7
RUN         mkdir /app
WORKDIR     /app

ADD . .

ENTRYPOINT bash -c "python -m marketbot"