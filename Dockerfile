FROM python:3.7

ENV PYTHONUNBUFFERED 1
ENV APP_DIR /usr/src/app

# Copy patches for apt-get and pip to use Chinese mirrors
COPY tools/patches/sources.list /etc/apt/
RUN mkdir -p /etc/xdg/pip
COPY tools/patches/pip.conf /etc/xdg/pip

# Update all packages and install required packages
RUN apt-get update \
        && apt-get upgrade -y \
        && apt-get install -y nginx-light \
        && apt-get clean

COPY tools/nginx.conf /etc/nginx/sites-enabled/default

RUN mkdir -p ${APP_DIR} ${APP_DIR}/media
WORKDIR /${APP_DIR}

RUN mkdir requirements
ADD requirements ${APP_DIR}/requirements
RUN python3 -m pip install --no-cache-dir -r requirements/prod.txt

ADD . ${APP_DIR}

RUN python3 manage.py collectstatic --no-input

EXPOSE 80

CMD ["./tools/start-server.sh"]
