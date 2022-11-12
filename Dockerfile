FROM python

WORKDIR /flask

COPY requirements.txt .

RUN pip install -r requirements.txt

EXPOSE 8000

COPY . /flask

ENTRYPOINT ["uvicorn", "run:app", "--host", "0.0.0.0", "--reload"]
