FROM python:3.7

ENV PYTHONUNBUFFERED 1

ENV APP_DIR /usr/src/app

# Copy patches for apt-get and pip to use Chinese mirrors
COPY tools/patches/sources.list /etc/apt/
RUN mkdir -p /etc/xdg/pip
COPY tools/patches/pip.conf /etc/xdg/pip

RUN apt-get update \
  && apt-get upgrade -y \
  && apt-get install -y nginx-light \
  && apt-get clean
COPY tools/nginx.conf /etc/nginx/sites-enabled/default

RUN mkdir -p ${APP_DIR}
WORKDIR /${APP_DIR}

COPY requirements.txt ${APP_DIR}
RUN python3 -m pip install --no-cache-dir -r requirements.txt

ADD . ${APP_DIR}

RUN python3 manage.py collectstatic --no-input

EXPOSE 80
# STOPSIGNAL SIGINT
CMD ["./tools/start-server.sh"]
