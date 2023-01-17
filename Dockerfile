FROM python:3.10

RUN pip install gremlinpython

ADD test.py .

CMD python test.py
