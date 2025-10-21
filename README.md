# About
this is the backend project for ticketing web platform

The pipenv is used as a main package manager for the project. For more info please follow [documentation](https://pipenv.pypa.io/en/latest/)

# `pipenv` usage

```sh
# Creating new virtual environment
pipenv shell

#Creating a .lock file form Pipenv five
pipenv lock

#Installing dependencies from .lock file
pipenv sync
```

```python


```

# 🐳 Deploy with Docker Compose 

```sh
cp .env.default .env
docker compose build && docker compose up -d
```

### some useful commands

```sh
# getting last 20 lines of a container's log and follow the stdout flow 
docker compose logs --tail 20 -f <container name>

#execute a command inside the container
docker compose exec <container name> <command>
```
