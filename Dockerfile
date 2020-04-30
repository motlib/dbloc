FROM python:3.7

ENV PYTHONUNBUFFERED 1

COPY patches/sources.list /etc/apt/
RUN apt-get update \
  && apt-get upgrade -y \
  && apt-get install -y nginx-light \
  && apt-get clean
COPY tools/nginx.conf /etc/nginx/sites-enabled/default

# Copy patch for pip to use chinese PiPY mirror
RUN mkdir -p /etc/xdg/pip
COPY patches/pip.conf /etc/xdg/pip

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN python3 -m pip install --no-cache-dir -r requirements.txt

ADD . /usr/src/app/

RUN python3 manage.py collectstatic --no-input

EXPOSE 80
# STOPSIGNAL SIGINT
CMD ["./tools/start-server.sh"]
