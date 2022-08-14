FROM python:3.9

COPY . .

RUN pip install psycopg2

RUN pip install telepot

RUN pip install requests

CMD [ "python", "./telepot/tele.py" ]
