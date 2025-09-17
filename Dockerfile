FROM golang:1.25-alpine AS builder

WORKDIR /app

COPY ./src ./app

RUN go build

FROM golang:1.23-alpine AS pfa-manager-api

WORKDIR /app

COPY --from=builder /app/pfa-manager-api /app/pfa-manager-api

VOLUME /app/data

ENTRYPOINT ["/app/pfa-manager-api"]