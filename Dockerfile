FROM python:3.8-alpine

RUN pip install "poetry==1.0.9"

WORKDIR /usr/src/example-chat

COPY poetry.lock pyproject.toml /usr/src/example-chat/

RUN poetry config virtualenvs.create false \
   && poetry install --no-dev --no-interaction --no-ansi

COPY . /usr/src/example-chat/

ENTRYPOINT ["python"]

CMD ["app.py"]
