#FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11
FROM  --platform=$TARGETPLATFORM python:3.11
WORKDIR /code
COPY ./requirment.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN uname -a > /os.txt
COPY ./sql_app /code/app



ENTRYPOINT ["uvicorn", "app.maingog:app", "--host", "0.0.0.0", "--port", "80"]
