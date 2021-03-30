FROM node:latest
WORKDIR /app
COPY ./front/package.json .
RUN yarn install
COPY ./front .
RUN yarn build

FROM python:3.8
WORKDIR /app
RUN apt-get install make g++
COPY cgen cgen
RUN cd cgen && make && cd ..
COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt
COPY --from=0 /app/build static/
RUN mkdir templates && mv static/index.html templates/
COPY *.py ./
CMD python3 backend.py
