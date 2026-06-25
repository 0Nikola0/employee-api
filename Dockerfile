FROM python:3.11

WORKDIR /code

ENV PYTHONPATH=/code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./tests /code/tests
COPY ./src /code/src

CMD ["python", "src"]