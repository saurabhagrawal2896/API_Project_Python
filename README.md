# Task Summary

This project is developed to expose an API which is able to pass input parameters and fetch the price details from a database.
API is able to take in atmost 4 inputs and then queries the database with the given parameters and displays the result accordingly.
It displays meaningful comments in case of errors in the parameters passed.

## Prerequisites:

1. Install Python
2. An IDE (PyCharm, Spyder, etc.)
3. Install MYSQL
4. Install python libraries - flask, mysql-connector-python,sqlparse (pip install in cmd)

## Instructions to setup and run:

1. Clone the Github repository on your local machine.
2. Update config.ini file with the database connection details as per your system/user configurations.
3. Run main.py file to test the code.


## Sample Test API's:

1. http://127.0.0.1:5000/rates
2. http://127.0.0.1:5000/rates?date_from=2016-01-01
3. http://127.0.0.1:5000/rates?date_to=2016-01-10
4. http://127.0.0.1:5000/rates?date_from=2016-01-01&date_to=2016-01-10
5. http://127.0.0.1:5000/rates?date_from=2016-01-01&date_to=2016-01-10&origin=CNQIN
6. http://127.0.0.1:5000/rates?origin=CNQIN&destination=NOFRO
7. http://127.0.0.1:5000/rates?date_from=2016-01-01&date_to=2016-01-10&origin=CNQIN&destination=NOFRO
8. http://127.0.0.1:5000/rates?date_from=2016-01-01&date_to=2016-01-10&origin=CNQIN&destination=Wrongdata
9. http://127.0.0.1:5000/rates?date_from=2024-01-01&date_to=2016-01-10&origin=CNQIN&destination=NOFRO
10. http://127.0.0.1:5000/rates?date_from=wrongdateformat&date_to=2016-01-10&origin=CNQIN&destination=NOFRO
