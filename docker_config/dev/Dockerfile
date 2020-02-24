FROM tiangolo/uvicorn-gunicorn:python3.7-alpine3.8

RUN apk upgrade -U \
 && apk add --no-cache curl openssh-client\
            g++ gcc wget bash git libffi-dev\
&& rm -rf /var/cache/*

COPY ./requirements/dev/ /config
RUN pip install --upgrade pip && pip install --no-cache-dir -r /config/requirements.txt

COPY ./app /app

WORKDIR /app

CMD ["/start-reload.sh"]