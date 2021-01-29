FROM python:3.8-alpine

COPY ./ /x12genapp

WORKDIR /x12genapp

RUN python3 setup.py install

CMD ["python3", "x12genapp/main.py"]