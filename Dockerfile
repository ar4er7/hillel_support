FROM --platform=linux/amd64 python:3.12-slim

RUN apt-get update -y \
    && pip install --upgrade pip \
    # dependencies for building Python packages
    && pip install --upgrade setuptools \
    && apt-get install -y build-essential \
    # install dependencies manager
    && pip install pipenv \
    #clean up unused files
    && rm -rf /var/lib/apt/lists/*

# Install project dependencies
COPY ./Pipfile ./Pipfile.lock /
RUN pipenv sync --dev --system

WORKDIR /app
COPY ./ ./

EXPOSE 8000

ENTRYPOINT [ "python" ]
CMD [ "src/manage.py", "runserver" ]