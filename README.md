# water-quality-db

The project is a backend api used for storing the observation's of water quality. The project is made by using fastpai, docker and the database used here is Postgres. The project is also deployed on EC2 instance and
emulated using localstack. I have also used JWT Authentication, so the api's are protected.

The execution of project is by following steps:
  1. Define the schema for the tables that would be used to store the observation and connect to the database
  2. Create the tables.
  3. Define the pydantic model that will be used.
  4. Making the route's for different action of the api such as CRUD.
  5. Dockerize the whole container.
  6. Emulate it using localstack for ec2 instance
