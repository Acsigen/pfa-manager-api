FROM golang:1.25-alpine AS builder

WORKDIR /app-builder

COPY ./main.go ./main.go
COPY ./database ./database
COPY ./models ./models

RUN go mod tidy && go build

FROM golang:1.23-alpine AS pfa-manager-api

WORKDIR /app

COPY --from=builder /app-builder/pfa-manager-api ./pfa-manager-api
