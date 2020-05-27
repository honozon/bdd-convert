FROM python:3.8
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN mkdir tmp
EXPOSE 8080
CMD python ./server.py