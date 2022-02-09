FROM python:3.10.0-alpine


WORKDIR /src/helper_v2


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN pip install pipenv


COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

RUN pipenv install --system 


COPY . .

CMD ["python", "manage.py", "runserver"]