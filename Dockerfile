FROM golang:1.25 AS builder

WORKDIR /app-builder

COPY ./src /app-builder

RUN go build -v

FROM golang:1.25 AS pfa-manager-api

WORKDIR /app

COPY --from=builder /app-builder/pfa-manager-api /app/pfa-manager-api

VOLUME /app/data

EXPOSE 8000

ENTRYPOINT ["/app/pfa-manager-api"]