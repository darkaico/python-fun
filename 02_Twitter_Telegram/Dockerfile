FROM python:3.10-slim-bullseye

RUN mkdir /app 

COPY twitter_telegram.py /app
COPY .env /app
COPY pyproject.toml /app 

WORKDIR /app

ENV PYTHONPATH=${PYTHONPATH}:${PWD} 
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

CMD ["poetry", "run", "python", "twitter_telegram.py" ]