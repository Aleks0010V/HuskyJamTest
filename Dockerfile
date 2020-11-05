FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80
EXPOSE 3306
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]