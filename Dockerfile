FROM python:3.8-alpine

RUN apk add gcc python3-dev musl-dev openssl-dev libffi-dev
RUN pip install "poetry==1.0.9"

WORKDIR /usr/src/example-chat

COPY poetry.lock pyproject.toml /usr/src/example-chat/
RUN poetry config virtualenvs.create false \
   && poetry install --no-dev --no-interaction --no-ansi

COPY . /usr/src/example-chat/

ENTRYPOINT ["python"]

CMD ["app.py"]
