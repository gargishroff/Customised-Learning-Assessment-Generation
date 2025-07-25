# Setup/Development Guide

## Instructions for running the project

Make sure you have node/npm and python/pip installed. Node v18/v20 and python v3.10/v3.11 are tested (other versions are untested and there may be problems if you try to use them).

### Installing dependencies

Run the below shell snippet in the project root

```sh
cd src
pip install -r requirements.txt
cd my-app
npm install
cd ../..
```

### Setting up the database

We use MongoDB in this project. The database must be initialized with an empty collection called 'assessments'.

### Configuring the app

The app reads the following environment variables:

- `API_TOKEN` (required): The hugging face API token for interfacing with the LLM.
- `MONGO_URI` (required): The Mongo URI used to connect to the database (must be complete with any required authentication and database name).
- `LLM_TIMEOUT` (optional): The timeout (in seconds) of the LLM connection. If not specified, the app uses a reasonable default.

These parameters can be saved in the file `src/.env`, which the app will read from.

### Launching the app

In the `src` folder, run `flask run` to launch a development server.
A gunicorn conf has also been provided, so a production-ready server can be launched by running `gunicorn`.

## Development guide

### Code formatting

Make sure you have `black` and `npx` installed.

We use `black` for python files, and `prettier` for everything else. We have provided a script `format.sh` that runs both tools on the entire codebase.

### Running python-based tests

Make sure you have the `pytest` python module installed.
In the `src` folder, run `python3 -m pytest`
