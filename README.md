# PLACEMENTS Campaign Invoice Web App

## Development

The only dependencies for this project should be docker and docker-compose. Install Docker for you platform on:
- https://www.docker.com/
- https://docs.docker.com/get-docker/

### Quick Start

Start the project with the following command once docker is installed

```bash
docker-compose up -d
```
This will download and create containers for the frontend(reactJS), backend(Python/FastAPI), and database (PostgreSQL).

## Run Database Migrations
Once containers are running you'll need to run the following command to setup database schema:
```bash
docker-compose run --rm backend alembic upgrade head
```

# Populate Line Item Data
Once the schema is setup run the following command to populate teaser data:
```bash
docker-compose run backend python app/scripts/populate_line_items.py
```

# Run Backend tests
The following command will run tests against the API
```bash
docker-compose run backend pytest
```

# View project in browser
Frontend - http://localhost:3001
Backend - http://localhost:3002/api/docs


# Features
## Bucket 1
- The user should be able to edit line-item "adjustments".

- The user should be able to see each line-item's billable amount (sub-
total = actuals + adjustments).

- The user should be able to see the invoice grand-total (sum of each
line-item's billable amount).

- The user should be able flag individual line-items as
"reviewed" (meaning they are disabled from further editing).

## Bucket 2
- An integration into an external service that makes sense (eg. a
currency conversion service, an export to Amazon S3, etc)

## Response
I chose the stated tasks because I feel like they are the sort of tasks that come up often in most systems. Using an ORM, sqlAlchemy, made tasks such as creating the billable amount and the invoice grand total straight forward. I decided to integrate with an external service for a similar reason. Whether it is auth, feature flagging, email, or logging at some point it will probably be the best decision to integrate with an external service.

If I spent more time on the exercise I would use optimistic locking to allow users to update records concurrently without overwriting each other. I would create an audit table where I keep track of a user, entity type, entity id, previous value, and new value. I would wire up some new endpoints and display it in a table on the front end.



