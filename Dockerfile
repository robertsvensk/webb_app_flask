FROM python:3.6-alpine

RUN adduser -D snowblunt_webb

WORKDIR /home/snowblunt_webb

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn 'PyMySQL>=0.8.1,<0.9'

COPY app app
COPY migrations migrations
COPY snowblunt_webb.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP snowblunt_webb.py

RUN chown -R snowblunt_webb:snowblunt_webb ./
USER snowblunt_webb

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
