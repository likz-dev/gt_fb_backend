FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine

WORKDIR /var/www

RUN apk --update add bash nano git

RUN apk add --no-cache python3 postgresql-libs
RUN apk add --no-cache --virtual .build-deps gcc python3-dev musl-dev postgresql-dev

RUN git clone https://github.com/likz-dev/gt_backend.git /var/www

RUN pip install -r /var/www/requirements.txt

RUN apk --purge del .build-deps