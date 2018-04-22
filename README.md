# miri-pr-web-app

## Setup for development

There are multiple ways to set it up for local development. The essential parts are:

1. Install postgresql, create a new database and a user with full privileges on that database.
2. Copy `src/config.py.dist` to `src/config.py` and fill out the information for the database in step 1.
3. Install python 3.6 or above.
4. In the src directory run the following command to install the dependencies:
```
pip install -U -r requirements.txt
```
5. Set your console (this may be different on windows):
```
export FLASK_APP=main.py
export FLASK_DEBUG=true
```
6. Prepare the database:
```
flask initdb
```
7. Run the flask development server:
```flask run```

The server should be running on `http://localhost:8000`.
After the first time, only the last step is required (apart from making sure the database is running).

*There is an easier way if you are on a unix machine and have docker installed:*

1. Copy `src/config.py.dist` to `src/config.py` and don't change anything.
2. In the root of the repository run:
```
docker-compose up
```
3. In a different terminal in the same repository run:
```
docker-compose run app flask initdb
```

The server should be running on `http://localhost:8000`.
After the first time, only step 2. is required.

## Setup for production

1. Ensure docker is installed on the system.
2. [Ensure docker-compose is installed on the system.](https://docs.docker.com/compose/install/#install-compose) 
2. Copy `src/config.py.dist` to `src/config.py` and change the postgresql password
3. Change the postgresql password in `docker-compose.prod.yaml` to the same value as step 2.
4. In the root of the repository run:
```
docker-compose -f docker-compose.prod.yaml up -d
```
5. In the same repository run:
```
docker-compose run app flask initdb
```

The server should be running on `http://localhost`.
