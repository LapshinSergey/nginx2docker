FROM nginx:alpine

RUN apk add linux-headers gcc musl-dev
RUN apk add python3 python3-dev
RUN pip3 install --upgrade pip
RUN pip3 install flask psutil termcolor docker


RUN mkdir /app

COPY ./nginx2docker.py /app/

#ENTRYPOINT ['/usr/bin/python3 /app/nginx2docker.py daemon']
CMD /usr/bin/python3 /app/nginx2docker.py daemon
