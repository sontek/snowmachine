FROM python:alpine
WORKDIR /app
COPY . .
RUN pip install -e .
ENTRYPOINT ["python", "-m", "snowmachine"]
