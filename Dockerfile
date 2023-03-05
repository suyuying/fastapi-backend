FROM python:3.11
WORKDIR /code
COPY ./requirment.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./sql_app /code/app
ENV PORT 8080
EXPOSE 8080

CMD ["uvicorn", "app.maingog:app", "--host", "0.0.0.0", "--port", "8080"]
