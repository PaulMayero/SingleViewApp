# pull official base image
FROM python:3.9-slim

ENV PYTHONUNBUFFERED 1

#Install required system libs
RUN apt-get update \
    && apt-get -y install libpq-dev gcc

#set work directory
WORKDIR /SingleViewApp
ADD . /SingleViewApp


#install server side requiremsnts
RUN pip install -r requirements.txt

EXPOSE 8000

# Env vars
ENV DB_NAME musical_works
ENV USERNAME bmat
ENV HOSTNAME localhost
ENV PORT 5432
#ENV TOKEN_FOR_MY_APP 3FsMv8pTt62aDwaKkCzsPbBQZ0dSaff4tiP5a2eP

# Run Python's dev web server when the container launches
CMD ["/SingleViewApp/musicalsingleview/manage.py", "runserver", "0.0.0.0:8000"]

