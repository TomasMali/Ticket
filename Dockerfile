FROM python:3.9

COPY . .

RUN pip install psycopg2

RUN pip install telepot

RUN pip install requests

RUN apt-get install pdfkit -Y

RUN pip install pdfkit


CMD [ "python", "./telepot/tele.py" ]
