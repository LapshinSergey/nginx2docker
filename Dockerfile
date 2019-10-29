FROM alpine:latest

RUN apk add --no-cache nginx
RUN mkdir /app -p
COPY ./nginx2docker.py /app/

EXPOSE 8080

ENTRYPOINT ['/app/nginx2docker daemon']
