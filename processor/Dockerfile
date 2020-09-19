FROM python:3.8.5-buster

WORKDIR /bettingtool

ADD ./processor/ ./processor/
ADD ./pythontools/ ./pythontools/
ADD ./wait-for-it.sh .
RUN touch __init__.py

WORKDIR /bettingtool/processor

RUN pip install pipenv
RUN pipenv install --system --deploy --dev

WORKDIR /bettingtool

CMD ["python", "-m", "processor.sample.main"]