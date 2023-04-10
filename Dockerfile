FROM python:3.9-alpine

#Install the dependencies
RUN pip install -Iv pdm==2.*

#Set the working directory
WORKDIR /project

#copy all the files
COPY pyproject.toml pdm.lock /project/

RUN pdm install --check --no-self

#copy project files
COPY main.py /project/

# Run the app
ENTRYPOINT ["python", "-u", "main.py"]