FROM python:3.6-alpine

ENV LANG "en_US.utf8"

RUN mkdir -p /home/app
WORKDIR /home/app
COPY . /home/app
RUN chmod +x start.sh
RUN pip3 install -r requirements.txt
RUN mkdir -p /home/app/logs
RUN python3 manage.py collectstatic

ENTRYPOINT ["./start.sh"]