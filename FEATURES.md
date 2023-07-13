# Roadmap

## Features
| Feature              | Description                                                                                                                    | Complete |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------ | -------- |
| Setup environment    | All necessary environment variables are defined in .env file for project configuration in containers.                          | X        |
| Bash scripts         | Bash scripts for initializing and deleting PostgreSQL database, user, and table are functioning properly.                      | X        |
| Database connection  | Python application can connect to PostgreSQL database using psycopg2.                                                          | X        |
| PostgreSQL user      | PostgreSQL user with the necessary privileges is created and can access the database.                                          | X        |
| Database and table   | PostgreSQL database and 'books' table are created and accessed by the application.                                             | X        |
| CRUD operations      | Application can perform CRUD operations on the 'books' table in the PostgreSQL database.                                       | X        |
| Database create      | Database initialization script can successfully create the database, user and table.                                           | X        |
| Database cleanup     | Database cleanup script can successfully delete the database, user and table.                                                  | X        |
| Dockerize application| Application is dockerized for easy deployment and distribution.                                                                | X        |
| Docker               | Multi-service build approach is available in Docker Compose.                                                                   | X        |
| Docker               | Container utilizes a multi-architecture compatible image.                                                                      | X        |
| Minikube             | Kubernetes manifests are available to deploy all objects to Minikube.                                                          | X        |
| EKS                  | Kubernetes manifests are available to deploy all objects to EKS.                                                               | X        |


## Under development
| Feature              | Description                                                                                                                    | Complete |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------ | -------- |
| Handle CSV           | Application can successfully load CSV data into the 'books' table in the database.                                             |          |
| Extract features     | Feature extraction from raw data for classification model.                                                                     |          |
| Model building       | Create, train and test a classification model using the provided features.                                                     |          |
| Prediction API       | API endpoint that allows the prediction of book genres based on provided data.                                                 |          |
| API Documentation    | Comprehensive API documentation detailing the endpoints, methods, required payloads, and responses.                            |          |
| Application Testing  | Unit tests and integration tests are written and passing for the application.                                                  |          |
| CI/CD Setup          | Setup continuous integration and continuous deployment (CI/CD) pipeline using tools like GitHub Actions.                       |          |
| Monitoring and logs  | Implement monitoring for the application and maintain logs for debugging and audit.                                            |          |
| Scale up application | Optimize the application and database to handle increased traffic and data.                                                    |          |
| Security measures    | Implement necessary security measures to protect application data and prevent unauthorized access.                             |          |
| User authentication  | Implement user authentication and authorization for access control.                                                            |          |
