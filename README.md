# Casting Agency

The Casting Agency is an API that models a company responsible for managing movies and actors and it use the API to store, update, delete and retrieve movies and actors.

This is the last project of the Full-Stack Developer Nanodegree from Udacity. It covers the following topics:

- Database modeling with PostgreSQL and SQLAlchemy and database Migrations.
- API Development and RESTful APIs.
- Perform CRUD operations (create, read, update, delete) on database with Flask.
- Automated testing using Unittest.
- Authorization and role based authentication.
- Deployment on Heroku.

The API is hosted live at Heroku:
https://noura-cap.herokuapp.com


## Models:
Movies with attributes title and release date
Actors with attributes name, age and gender

## Endpoints:

## Movie:
### GET '/actors': 
return a list of all actors

```bash
{
    "actors": [
        {
            "age": 22,
            "gender": "Male",
            "id": 1,
            "name": "salman"
        },
        {
            "age": 22,
            "gender": "Female",
            "id": 2,
            "name": "sarah"
        }
    ],
    "success": true
}
```


### GET ''/actors/<int:actor_id>'': 
return actor with id 'actor_id'

```bash
{
    "actor": [
        {
            "age": 22,
            "gender": "Male",
            "id": 1,
            "name": "salman"
        }
    ],
    "success": true
}
```


### POST '/actors': 
craete an actor with info specified in request json 

request JSON:
```bash
{
    "name": "ola ",
    "age": "50",
    "gender": "female"
}
```

response:
```bash
{
    "actor": 4,
    "success": true
}
```

### DELETE '/actors/<int:id>':
delete actor with id 'id' 
```bash
{
    "delete": 4,
    "success": true
}
```

### PATCH '/actors/<int:actor_id>': 
update the actor with id 'actor_id' usig request json. 

request JSON:
```bash
{
    "name": "salman"
}
```


response:
```bash
{
    "actors": {
        "age": 22,
        "gender": "Male",
        "id": 1,
        "name": "salman"
    },
    "success": true
}
```

## Actor:
### GET '/movies':
return a list of all movies

```bash
{
    "movies": [
        {
            "id": 1,
            "release": "Fri, 12 Dec 2014 00:00:00 GMT",
            "title": "Catch Me If You Can"
        },
        {
            "id": 3,
            "release": "Fri, 12 Dec 2014 00:00:00 GMT",
            "title": "The Imitation Game"
        }
    ],
    "success": true
}
```


### GET '/movies/<int:movie_id>': 
return movie with id 'movie_id'

```bash
{
    "movie": [
        {
            "id": 1,
            "release": "Fri, 12 Dec 2014 00:00:00 GMT",
            "title": "Catch Me If You Can"
        }
    ],
    "success": true
}
```



### POST '/movies': 
craete a movie with info specified in request json.

request JSON:

```bash
{
    "title": "The Imitation Game",
    "release": "2014-12-12"
} 
```

response:
```bash
{
    "movie": 4,
    "success": true
}
```
### DELETE '/movies/<int:id>': 
delete movie with id 'id' 

```bash
{
    "delete": 3,
    "success": true
}
```

### PATCH '/movies/<int:movie_id>': 
update the movie with id 'movie_id' usig request json. 

request JSON:
```bash
{
    "title":"The terminal"
}
```


response:

```bash
{
    "movie": {
        "id": 1,
        "release": "Fri, 12 Dec 2014 00:00:00 GMT",
        "title": "The terminal"
    },
    "success": true,
    "updated": 1
}
```




## Roles and Users:
There are 3 types of roles and 8 permissions each role have different permissions as below: 

#### Casting Assistant:

permissions:

- "get:actors"
- "get:movies"


#### Casting Director:

permissions:
- "get:actors"
- "get:movies"
- "post:actors"
- "patch:actors"
- "patch:movies"
- "delete:actors"


#### Executive Producer:

permissions:
- "get:actors"
- "get:movies"
- "post:actors"
- "post:movies"
- "patch:actors"
- "patch:movies"
- "delete:actors"
- "delete:movies"



## Getting Started

## Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. run the follwing command  in your project directory for setting up a virual enviornment using macos:


1- Installing virtual environment:
```bash
python3 -m pip install --user virtualenv
```

2- Creating a virtual environment:
```bash 
python3 -m venv env
``` 
3- Activating a virtual environment: 
```bash
source env/bin/activate
```

for more details and other platforms visit:
(https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

## Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to your project directory and running:

```bash
pip3 install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.


## setup.sh file 

Replace the values of this file to reflect your setup.

```bash

# Auth0 
export AUTH0_DOMAIN=
export API_AUDIENCE=
export ALGORITHMS=
export CLIENT_ID=

#tokens
export CASTING_ASSISTANT_TOKEN=
export CASTING_DIRECTOR_TOKEN=
export EXEUTIVE_PRODUCER_TOKEN=

# database
export DATABASE_URL=
export SECRET=

```

To export the credentials as environment variable, after activating your environment run

```bash
source setup.sh
```

## Database Setup
#### 1- Create Local Database:
Run the following command:
```bash
createdb agency
```
export the database URI as an environment variable with the key DATABASE_URL.

#### 2-Run Database Migrations:

Run the following command:
```bash
python3 manage.py db init
python3 manage.py db migrate
python3 manage.py db upgrade
```


## Running the server

Ensure all environment variables are seet in setup.sh file. 
cd to the directory and ensure you are working using your created virtual environment.

Run the following command:

```bash
export FLASK_APP=app.py;
export FLASK_ENV=development
flask run 
```


## Running tests

It is reccomended to run the test on local database befor mograting to heroku.

To run the tests run the following command:
```bash
python3 test_app.py
```

## heroku 

### Create Heroku app

in your project command line run: 
```bash
run heroku create name_of_your_app 
```

The output will include a git url for your Heroku application. Copy this as, we'll use it in the next step.Now check your Heroku Dashboard in the browser, you'll see the application you just created. 

### Add git remote for Heroku to local repository
Using the git url obtained from the last step, in terminal run:
```bash
 git remote add heroku heroku_git_url
 ``` 


### Add postgresql add on for our database
Heroku has an addon for apps for a postgresql database instance. Run this code in order to create your database and connect it to your application: 
```bash
heroku addons:create heroku-postgresql:hobby-dev --app name_of_your_application
``` 

To check your configuration variables in Heroku run:
```bash
heroku config --app name_of_your_application
```

You will see DATABASE_URL and the URL of the database you just created.

### Go and fix your configurations in Heroku
In the browser, go to your Heroku Dashboard and access your application's settings. Reveal your config variables and start adding all the required environment variables for your project.

### Push it!
```bash
git push heroku master
```

some handy commands if your using python-3.8.1:
```bash
heroku stack 
heroku stack:set heroku-18
```

after you push your project to heroku make sure to change the 'DATABASE_URL' varible in setup.sh file to your new heroku databse link.

### Run migrations
Once your app is deployed, run migrations by running:
```bash
 heroku run python manage.py db upgrade --app name_of_your_application
 ```


## Authors

- Noura Albllaa, Udacity Full Stack Web Developer Nanodegree Student.
- Udacity Team.






