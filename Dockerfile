FROM python:3.7
COPY . /photomath
WORKDIR /photomath
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install -r requirements.txt
RUN pip install --upgrade pip --user
EXPOSE 5001
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]