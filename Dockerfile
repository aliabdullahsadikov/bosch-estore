FROM python:3.9

WORKDIR /code

COPY requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# copy all dir/files to container's directory '/code/'
COPY . /code/

# run
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8013"]