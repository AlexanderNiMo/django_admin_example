FROM python:3.8-slim-buster
WORKDIR /app
COPY ./app ./

RUN mkdir /db & pip3 install -r ./requirements/dev.txt

# run entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]