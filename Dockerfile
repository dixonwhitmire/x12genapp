FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

ENV MODULE_NAME="x12genapp.main"

COPY ./ /app