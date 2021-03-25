FROM node:latest
WORKDIR /app
COPY ./front/package.json .
RUN yarn install
COPY ./front .
RUN yarn build

FROM python:3.8
ENV FLASK_APP=backend.py
COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt
WORKDIR /app
COPY --from=0 /app/build static/
RUN mkdir templates && mv static/index.html templates/
COPY *.py ./
CMD flask run --host=0.0.0.0 --port=$PORT
