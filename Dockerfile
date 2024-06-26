FROM python:3.9.6-slim-buster

WORKDIR /usr/src/app
ENV PYTHONPATH=/usr/src/app

COPY requirements/prod.txt ./
RUN pip install --no-cache-dir -r prod.txt

COPY transport transport/

CMD [ "python", "./transport/app.py" ]

EXPOSE 5000
