FROM python:3.8-alpine

ENV PYTHONUNBUFFERED 1
ENV APP_DIR /usr/src/app

# Patches for apk and pip to use Chinese mirrors
COPY tools/patches/pip.conf /etc/xdg/pip/pip.conf
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apk/repositories 

# Install nginx
RUN apk update \
        && apk --no-cache add nginx \
        && mkdir /run/nginx
COPY tools/nginx.conf /etc/nginx/conf.d/default.conf

RUN mkdir -p ${APP_DIR} ${APP_DIR}/media
WORKDIR /${APP_DIR}

# Install python packages (needs -dev packages for building, can be removed later)
ADD requirements ${APP_DIR}/requirements
RUN apk --no-cache add jpeg-dev zlib-dev musl-dev build-base \
        && python3 -m pip install --no-cache-dir -r requirements/prod.txt \
        && apk --no-cache del build-base jpeg-dev zlib-dev musl-dev \
        && apk --no-cache add musl zlib jpeg \
        && rm -rf /var/cache/apk/*

# Add the application
ADD . ${APP_DIR}
RUN python3 manage.py collectstatic --no-input

EXPOSE 80

CMD ["./tools/start-server.sh"]
