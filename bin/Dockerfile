FROM python:alpine

RUN pip install "pinboard>2.0"

RUN adduser -D -u 1000 pinboard

USER pinboard

WORKDIR /code/

ENTRYPOINT ["./pinboard"]

CMD ["-h"]

COPY pinboard /code/pinboard
