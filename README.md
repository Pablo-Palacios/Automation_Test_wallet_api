# Automation_Test_Api
This project focuses on automated testing and verification of the functionality and stability of a virtual wallet and commerce mobile application. Multiple technologies were utilized to ensure the system's reliability and performance.

### Features
Database Queries:
SQL queries were implemented to validate critical data and ensure proper persistence and retrieval of information within the system.

Redis Extractions:
Redis was used for temporary data storage and caching, ensuring fast and efficient application operations. Automated tests were conducted to verify the integrity of the extractions.

Task Automation:
Automated scripts were developed to handle repetitive tasks and scheduled operations within the application, optimizing efficiency and reducing human error.

Endpoint Assertions:
Extensive validation was performed on various backend endpoints, including load testing and functionality verification to ensure the system's reliability under different conditions.

Negative Scenarios:
Negative testing was conducted to validate how the system handles errors, incorrect responses, and network failures. This included the validation of appropriate error messages and the system's robustness against invalid inputs.

Permissions System:
Implementation and validation of the user roles and permissions system, ensuring that access controls are correctly enforced and users can interact only with authorized resources.

### Technologies Used
Programming Language: Python
Testing Framework: Pytest
Cache and Temporary Data Management: Redis
Database: SQL
Automation Tools: Selenium, Appium, Postman



 python version: 3.10.0 >= 3.11.9

## Configure proyecto mc_automation

- create virtual venv

```shell
python3 -m venv venv
```

- activate venv

```shell
source venv/bin/activate
```

- install dependencies

```shell
pip install pytest
pip install redis
pip install locust
pip install python-dotenv
pip install faker
pip install psycopg2
pip install pickle5
pip install unittest
```

### Commands opcionales:

- deactivate venv

```shell
deactivate
```

- delete venv

```shell
rm -r venv
```

### Commands run test:

- run all tests 

```shell
pytest -v -s
```

- run test_archivo

```shell
pytest -v -s test_archivo.py
```

- run test_especific

```shell
pytest -v -s test_archivo.py::className::test_name
```
