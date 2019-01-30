FROM python:3.7-alpine

RUN adduser -D simplebbc
WORKDIR /home/simplebbc

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY app.py app.py
COPY start.sh start.sh
COPY templates templates
RUN chmod +x start.sh

ENV FLASK_APP app.py

RUN chown -R simplebbc:simplebbc ./
USER simplebbc

EXPOSE 5000
ENTRYPOINT ["./start.sh"]