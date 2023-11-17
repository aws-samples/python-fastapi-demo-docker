# Roadmap
### Release 1: Genesis
The Genesis Release introduces a foundational blend of software, containerization, and Kubernetes orchestration, setting the stage for scalable and robust cloud-native applications in the EKS & AWS ecosystem.

| Feature              | Description                                                                        | Developed by                                    |
| -------------------- | ---------------------------------------------------------------------------------- | ----------------------------------------------- |
| Setup environment    | All environment variables are defined in .env for configuration in containers.     | [@tucktuck9](https://github.com/tucktuck9)      |
| Bash scripts         | Bash scripts for initializing/deleting PostgreSQL database, user, and table ready. | [@tucktuck9](https://github.com/tucktuck9)      |
| Database connection  | Python application can connect to PostgreSQL database using psycopg2.              | [@tucktuck9](https://github.com/tucktuck9)      |
| PostgreSQL user      | PostgreSQL user with necessary privileges can create/access the database.          | [@tucktuck9](https://github.com/tucktuck9)      |
| Database and table   | PostgreSQL database and 'books' table are created and accessed by the app.         | [@tucktuck9](https://github.com/tucktuck9)      |
| CRUD operations      | Application can perform CRUD operations on the 'books' table in the database.      | [@tucktuck9](https://github.com/tucktuck9)      |
| Database create      | Database initialization script can successfully create the database, user, table.  | [@tucktuck9](https://github.com/tucktuck9)      |
| Database cleanup     | Database cleanup script can successfully delete the database, user and table.      | [@tucktuck9](https://github.com/tucktuck9)      |
| Logging              | Implement and maintain logs for debugging/audit.                                   | [@tucktuck9](https://github.com/tucktuck9)      |
| Dockerize application| Application is dockerized for easy deployment and distribution.                    | [@tucktuck9](https://github.com/tucktuck9)      |
| Docker               | Multi-service build approach is available in Docker Compose.                       | [@tucktuck9](https://github.com/tucktuck9)      |
| Minikube             | Kubernetes manifests are available to deploy all objects to Minikube.              | [@tucktuck9](https://github.com/tucktuck9)      |
| EKS                  | Kubernetes manifests are available to deploy all objects to EKS.                   | [@JoeNorth](https://github.com/JoeNorth)        |
| Request tracing      | Request tracing enabled via AWS Open Telemetry.                                    | [@smrutiranjantripathy](https://github.com/smrutiranjantripathy)|
| Secrets manager      | Sensitive credentials managed via AWS Secrets Manager.                             | [@JoeNorth](https://github.com/JoeNorth)        |
| Managed database     | Database managed via Amazon Aurora PostgreSQL.                                     | [@JoeNorth](https://github.com/JoeNorth)        |

## Under development
| Feature              | Description                                                                        | Developer                                       |
| -------------------- | ---------------------------------------------------------------------------------- | ----------------------------------------------- |
| CI/CD Setup          | CI/CD pipeline managed via Amazon CodeCatalyst.                                    | [@smrutiranjantripathy](https://github.com/smrutiranjantripathy)  |
| Extract features     | Feature extraction from raw data for classification model.                         | -                                               |
| Model building       | Create, train and test a classification model using the provided features.         | -                                               |
| Prediction API       | API endpoint that allows the prediction of book genres based on provided data.     | -                                               |
| API Documentation    | FastAPI documentation is available for endpoints, methods, request/response.       | -                                               |
| Application Testing  | Unit tests and integration tests are written and passing for the application.      | -                                               |
| Monitoring and logs  | Implement monitoring for the application and maintain logs for debugging.          | -                                               |
| Scale up application | Optimize the application and database to handle increased traffic and data.        | -                                               |
| Security measures    | Implement security measures to protect app data/prevent unauthorized access.       | -                                               |
| User authentication  | Implement user authentication and authorization for access control.                | -                                               |
| Monitoring           | Implement monitoring of application performance, errors, metrics.                  | -                                               |

