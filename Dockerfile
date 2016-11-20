FROM python:3.5
ADD . /code
WORKDIR /code
RUN pip install -r db_scripts/requirements.txt
CMD python db_scripts/main.py --start
