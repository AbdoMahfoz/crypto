FROM alpine:latest
RUN apk add make g++
WORKDIR /app
COPY . .
RUN make
CMD sh
