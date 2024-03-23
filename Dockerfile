FROM python:3.10

# Working Directory
WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy packages required from local requirements file to Docker image requirements file
RUN git clone https://github.com/roshanrai1304/water-quality-db.git

RUN pip3 install -r requirements.txt

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT [ "uvicorn", "main:app", "--reload", "--server.address=0.0.0.0"]