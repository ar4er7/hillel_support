FROM --platform=linux/amd64 python:3.12-slim

ENV PYTHONUNBUFFERED=1

RUN apt-get update -y \
    && pip install --upgrade pip \
    # dependencies for building Python packages
    && pip install --upgrade setuptools \
    && apt-get install -y build-essential \
    # install dependencies manager
    && pip install pipenv watchdog \
    #clean up unused files
    && rm -rf /var/lib/apt/lists/*

# Install project dependencies
COPY ./Pipfile ./Pipfile.lock /
RUN pipenv sync --system

# TODO investiogate why this is needed
RUN pip install psycopg[binary]

WORKDIR /app
COPY ./ ./

EXPOSE 8000

ENTRYPOINT [ "python" ]
# CMD ["src/manage.py", "runserver"] 
# default django port, but not accessible from outside the container (do not put it the coment in one line w/ CMD)

CMD [ "src/manage.py", "runserver", "0.0.0.0:8000" ] 
# to be accessible from outside the container (do not put it the coment in one line w/ CMD)