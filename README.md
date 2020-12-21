# bot-sylwester

## How to start development
```shell script
# Install dependencies
poetry install

# Setup pre-commit and pre-push hooks
poetry run pre-commit install
```

# Run locally
Requirements:
* Docker
* Docker compose

In order to run bot-sylwester in docker container run below:
```shell script
docker build -t bot-sylwek .
docker run -it --rm -v <local persistence directory>:/home/appuser/data bot-sylwek
```

In order to stop it run:
```shell script
docker-compose down
```
