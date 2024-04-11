# water-quality-db

The project is a backend api used for storing the observation's of water quality. The project is made by using fastpai, docker and the database used here is Postgres. The project is also deployed on EC2 instance and
emulated using localstack. I have also used JWT Authentication, so the api's are protected. The type of data that I have stored is in the following format

{
"location": {"latitude": 40.712776, "longitude": -74.005974},
"date_time": "2024-03-19T15:00:00Z",
"description": "early afternoon water quality observation at Nehru
Park",
"parameters": {
"pH": 7.4,
"conductivity": 250,
“DO”: 67,
"contaminants": ["Lead", "Arsenic"]
}
}

The execution of project is by following steps:
  1. Define the schema for the tables that would be used to store the observation and connect to the database
  2. Create the tables.
  3. Define the pydantic model that will be used.
  4. Making the route's for different action of the api such as CRUD.
  5. Dockerize the whole container.
  6. Emulate it using localstack for ec2 instance

To run the repo use the command in order:
  1. docker login (enter username and password)
  2. docker pull roshanrai1304/water-quality-api:0.0.1.RELEASE
  3. docker run -d -p 3000:3000 roshanrai1304/water-quality-api:0.0.1.RELEASE

After running the command you can see you the api on https://localhost:3000/docs
