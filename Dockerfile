FROM python:3.11-alpine

RUN adduser --system --no-create-home flaskuser

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

USER flaskuser
EXPOSE 5000
CMD ["gunicorn", "--access-logfile", "-", "--error-logfile", "-", "-w", "4", "-k","4", "-b", ":5000", "wsgi:application"]