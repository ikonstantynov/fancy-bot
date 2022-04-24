FROM python:3.8

ARG APP_DIR=app


ADD bot.py /$APP_DIR/
ADD requirements.txt /$APP_DIR/
WORKDIR /$APP_DIR

RUN pip install -r requirements.txt
CMD python bot.py