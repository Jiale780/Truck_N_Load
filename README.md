# Truck_N_Load
ICT302 - SeaLanes Project

## Installation
### Requirements
* Python 3
* PostgreSQL

The `requirements.txt` has all Python dependencies for this project

Note: Ensure there is a web server (such as Nginx) being used. 
This application is not designed to be accessed directly in production.

### Environment variables
Copy the `example.env` to `.env` and set the environment variables

### Database
This has been tested on PostgreSQL 10.3

When running ensure the database that has been set in `.env` has already been created 
and the user has `CREATEDB` permissions

The following is an example of how to do a database migration:
```
bash$ flask db migrate -m "users table"
bash$ flask db upgrade
```

In the event a rollback is required, execute the following command:
```
bash$ flask db downgrade
```

### Login Setup
To create a user for development use (use the terminal window in Pycharm as it uses the python venv):

Windows:
```
SET FLASK_APP=Truck-n-Load.py
```
Linux:
```
export FLASK_APP=Truck-n-Load.py
```
All operating systems:
```
flask shell
>>> u = User(username='admin', email='admin@trucknload.com')
>>> u.set_password('password')
>>> db.session.add(u)
>>> db.session.commit()
```
