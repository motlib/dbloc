FROM python:3.7

ENV PYTHONUNBUFFERED 1

# Copy patch for pip to use chinese PiPY mirror
RUN mkdir -p /etc/xdg/pip
COPY patches/pip.conf /etc/xdg/pip

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app/

RUN python3 -m pip install -r requirements.txt
ADD . /usr/src/app/

EXPOSE 8000
STOPSIGNAL SIGTERM
CMD ["./start-server.sh"]