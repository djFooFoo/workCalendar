FROM python:3.9-slim-bullseye

RUN useradd -ms /bin/bash user
USER user
WORKDIR /home/user

COPY requirements.txt .
RUN pip install -r requirements.txt && rm requirements.txt

COPY --chown=user:user src .
COPY --chown=user:user credentials.json .
COPY --chown=user:user token.json .

EXPOSE 10001
ENTRYPOINT [ "python", "-m", "uvicorn", "main:app", "--port", "10001", "--host", "0.0.0.0"]