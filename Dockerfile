FROM python:3.8-slim

LABEL maintainer="James Graham <j.graham@software.ac.uk>"

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app
RUN pip3 install --no-cache-dir -r requirements.txt gunicorn

COPY . /app

EXPOSE 8000

CMD ["gunicorn", "lowfat.wsgi:application", "--bind", "0.0.0.0:8000"]
ENTRYPOINT ["./entrypoint.sh"]
