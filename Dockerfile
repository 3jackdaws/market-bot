FROM        python:3.7
RUN         mkdir /app
WORKDIR     /app

ADD         . .
RUN         pip install -r requirements.txt
ENTRYPOINT  bash -c "python -m marketbot"


