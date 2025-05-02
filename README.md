# Taxi Rental Management Application

## Requirements

postgresSQL, python3

## Set up

### 1. Set up venv

It is recommended to set up python virtual environment so it does not break the global python in your system. Although it is not really needed.
Choose a python version of your choice (or you can use the default python in your laptop). Then to generate virtual environment run:

```
python -m venv .venv
```

You will see a folder named .venv is generated. To activate virtual environment run:

```
.\.venv\Scripts\activate # for window
source .venv/bin/activate # for max/linux
```


### 2. Install dependencies

```
pip install -r requirements.txt
```


### 3. Set up database credential:

There is a `.env.example` that contains template for `.env`. Create a new .env file and copy the content from .env.example to .env.
You need to fill in credential for database in the .env in order for the app to connect to database. The database connection is defined in
`/database/db.py`

### 4. Create tables in database:

Run the sql commands in `/database/db.sql` to create tables that are required in this project. Make sure to run this sql command in
your target database. Optionally you have a script `/database/drop_all.sql` to drop all tables found in the target database.


## Run app

Run the script below:

```
python server.py
```