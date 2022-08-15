FROM python:3.9

# WORKDIR /app

COPY . .

# RUN apt-get update -y

# RUN apt-get install wkhtmltopdf -y

# RUN pip install pdfkit

RUN pip install psycopg2

RUN pip install telepot

RUN pip install requests



CMD [ "python", "./telepot/tele.py" ]
