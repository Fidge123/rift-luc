FROM python:3.5
ADD db_scripts /code
WORKDIR /code
RUN pip install -r requirements.txt
CMD python main.py
