# Shifts

Simple REST API application using FastAPI

## Tools used

- [FastAPI](https://fastapi.tiangolo.com/)
    - [pydantic](https://pydantic-docs.helpmanual.io/)
    - [SQLAlchemy](https://www.sqlalchemy.org/)
    - [Alembic](https://alembic.sqlalchemy.org/en/latest/)
- [PostgreSQL](https://www.postgresql.org/)
- [pytest](https://docs.pytest.org/)
- [Docker](https://www.docker.com/)


## Requirement analysis

The requirements for the application are as follows.


### Functional requirements

- The application must store Shifts by multiple Workers.
- A Shift must be 8 hours long (slots: 0-8, 8-16, 16-24).
- A Worker must have zero or more Shifts over multiple days.
- A Worker must have zero or one Shift per day. (i.e. A worker never has two shifts on the same day.)
- The application must provide REST APIs.


### Assumptions

In addition, the following assumptions have been made:

- Only Manager can create and delete Shifts.
- Only Manager can create and delete Workers.
- Only Manager can create and delete Managers.
- Workers can choose Shifts.
- Workers can cancel their Shifts.


### Out of scope functionality

The following functionality is out of scope in the current version.

- Front-end application



## Application design

The overview of the application design is as follows.


### Actors

- Worker
- Manager


### Use stories and use cases

- As a Worker, I want to choose a Shift so that Manager can see when I work.
- As a Worker, I want to cancel my Shift so that another worker can choose the Shift.
- As a Worker, I want to view Shifts so that I can make my work schedule.
- As a Manager, I want to view Shifts so that I can make staffing plans.
- As a Manager, I want to create Shifts so that Workers can choose them.
- As a Manager, I want to delete Shifts so that I can adjust staffing plans.

![User case diagram](images/shifts_use_cases.png)


### Class diagram

There are several points to consider.

1. `Worker` and `Manager` have common attributes, such as `username`. Therefore, it would be convenient
   to consider that they are subclasses of a parent class `User`. 

2. A `Worker` can have multiple `Shift`s, and a `Shift` can have multiple `Worker`s. 
   Therefore, the relationship between `Worker` and `Shift` is considered many-to-many. 
   Implementing this relationship would require an association class `WorkerShift` that connects `Worker` and `Shift`.

3. As a `Worker` never has two shifts on the same day, `WorkerShift` should have the attribute `shift_date`. It makes it 
   easier to create a unique constraint on the attributes (`worker_id`, `shift_date`).

4. As there are only three shift slots a day (slots: 0-8, 8-16, 16-24), the attribute `shift_slot` in `Shift` should be an enumeration
   of three values.
   

To summarise, the class diagram is shown below.

![Class diagram](images/shifts_class_diagram.png)


### Sequence diagram

Although the front end is not included in this application, the following sequence diagrams
show how the objects would interact with each other.

![Sequence diagram](images/shifts_sequence_diagram.png)

### Activity diagram

The following diagrams show some of the primary activities' flow.

![Activity diagram](images/shifts_activity_diagram.png)



## Implementation

The application is built using the [FastAPI](https://fastapi.tiangolo.com/) framework.


### Models

The following Pydantic models ([`src/shifts/app/schemas`](https://github.com/mikio-dev/shifts/blob/main/src/shifts/app/schemas/) directory in the repository) are implemented based on the class diagram shown above.

- `User`
- `Worker`
- `Manager`
- `Shift`
- `WorkerShift`

As discussed earlier, `Worker` and `Manager` inherit from `User`. `WorkerShift` works as an association class that connects `Worker` and `Shift`.

The classes are mapped to the database tables using SQLAlchemy ORM. They are stored in the [`src/shifts/app/models`](https://github.com/mikio-dev/shifts/blob/main/src/shifts/app/models/) directory in the repository.


### Routers

The application has the following REST API endpoints, defined in the [`src/shifts/app/api`](https://github.com/mikio-dev/shifts/blob/main/src/shifts/app/api/) directory.

- `worker`
- `manager`
- `shift`

FastAPI automatically generates the Open API documentation, which lists all the APIs.



## Unit test

All unit test files are stored in the [`src/shifts/tests`](https://github.com/mikio-dev/shifts/blob/main/src/shifts/tests) directory. 

To execute the unit tests, run the `pytest` command in the `src/shifts` directory using `poetry`:

```
$ poetry run pytest tests
```

In addition, a Github action runs the `pytest tests` command every time code change is pushed to the Github repository.


## Integration test

All integration test files are stored in the [`src/shifts/integration`](https://github.com/mikio-dev/shifts/blob/main/src/shifts/integration) directory. 

It uses the [pytest-docker-compose](https://github.com/pytest-docker-compose/pytest-docker-compose) pytest plugin to start the Docker images via docker-compose before each test module starts and shut down the Docker images after the test module finishes. As the PostgreSQL database is not persisted in a Docker volume, the integration tests can use the same test data in each module.

To execute the unit tests, run the `pytest` command in the `src/shifts` directory using `poetry`:

```
$ poetry run pytest integration
```


## Deployment

The application runs in Docker. 


### Local environment

The application can run in a local Docker environment. Run the `docker-compose` command at the root of the directory.

```
$ docker-compose up -d
```

This command will build the necessary Docker images and start the application and the PostgreSQL database server. It will also add a few initial test records to the tables.

The Open API document is accessible at [`http://localhost:8001/docs`](http://localhost:8001/docs), which can be used to access the APIs.


### Cloud environment

The application can be deployed to a Docker environment in the cloud. The Github action ([`.github/workflows/heroku.yml`](https://github.com/mikio-dev/shifts/blob/main/.github/workflows/heroku.yml)) contains the actions to deploy the application to [Heroku](https://www.heroku.com/). 

The following steps are required to run the actions:

1. Create a Heroku app with a Heroku Postgres add-on. 

   The `DATABASE_URL` config var needs to have a value starting with `postgresql://...` instead of `postgres://...`.

2. Create the secrets `HEROKU_APP_NAME` and `HEROKU_API_KEY` in Github.

   `HEROKU_APP_NAME` is the application name created in the previous step. `HEROKU_API_KEY` is the API key, which can be found in the Account Settings on Heroku.
