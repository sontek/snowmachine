FROM cgr.dev/chainguard/python:latest-dev
WORKDIR /app
COPY . .
RUN pip install -e .
ENTRYPOINT ["python", "-m", "snowmachine"]
