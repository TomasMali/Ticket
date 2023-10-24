FROM python:3.11.3

# WORKDIR /app

COPY . .

# RUN apt-get update -y

# RUN apt-get install wkhtmltopdf -y

# RUN pip install pdfkit


RUN pip install psycopg2

RUN pip install telepot

RUN pip install requests

RUN pip install -U scikit-learn scipy matplotlib

RUN pip install pdfkit


RUN pip install mysql-connector-python==8.0.26
EXPOSE 3306




CMD [ "python", "./telepot/tele.py" ]
