# API-PH-APP-V1

## Introduction

API-PH-APP-V1 is a RESTful API built using Flask for CRUD operations and deep learning model triggering (including PSPNet semantic segmentation and CNN Classification). It provides functionalities for managing data with a Flask-based backend, and integrates deep learning model capabilities. This is the backend application server for PH APP

## Technologies

- [![Python](https://img.shields.io/badge/Python-%2314354C.svg?style=flat&logo=python&logoColor=white)](https://www.python.org/)
- [![Flask](https://img.shields.io/badge/Flask-%23000.svg?style=flat&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
- [![Swagger UI](https://img.shields.io/badge/Swagger_UI-%2385EA2D.svg?style=flat&logo=swagger&logoColor=black)](https://swagger.io/)
- [![Google Cloud](https://img.shields.io/badge/Google_Cloud-%234285F4.svg?style=flat&logo=google-cloud&logoColor=white)](https://cloud.google.com/)
- [![Tensorflow](https://img.shields.io/badge/Tensorflow-%23FF6F00.svg?style=flat&logo=tensorflow&logoColor=white)](https://www.tensorflow.org/)
- [![JWT Authentication](https://img.shields.io/badge/JWT_Authentication-%23000000.svg?style=flat&logo=jwt&logoColor=white)](https://jwt.io/)
- [![Firestore](https://img.shields.io/badge/Firestore-%23404E5C.svg?style=flat&logo=firebase&logoColor=white)](https://cloud.google.com/firestore)

## Dependencies

To install the required dependencies, run:

```bash
$ pip install -r requirements.txt
```

To run the app just simply run the main.py
```bash
$ python main.py
```

## API Documentation 
To see the documentation go to /swagger endpoint
##### example: 
```bash
http://localhost:8080/swagger/
```