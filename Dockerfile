FROM python:3.10

# Working Directory
WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*


RUN git clone https://github.com/yourusername/yourrepository.git /app

COPY config.py /app/config.py

RUN pip3 install -r requirements.txt

EXPOSE 3000

CMD [ "uvicorn", "main:app", "--host=0.0.0.0", "--port=3000" ]