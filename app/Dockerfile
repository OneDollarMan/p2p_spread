FROM python:3.11

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY entrypoint.sh entrypoint.sh

COPY . .

RUN chmod +x /app/entrypoint.sh
RUN chmod -R 644 /app/static
ENTRYPOINT ["/app/entrypoint.sh"]