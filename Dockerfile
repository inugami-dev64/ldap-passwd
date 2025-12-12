FROM python:3.13.7-alpine3.22

WORKDIR /app/passwd
COPY . .

RUN pip install -r requirements.txt

CMD ["/usr/local/bin/uwsgi", "--http", "0.0.0.0:8000", "--master", "-p", "4", "-w", "server:app"]