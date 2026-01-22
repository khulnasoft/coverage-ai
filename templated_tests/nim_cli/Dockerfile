FROM nimlang/nim:alpine as builder

WORKDIR /app
COPY . .
RUN nim c -d:release nim_cli.nim

FROM alpine:latest
RUN apk add --no-cache ca-certificates
COPY --from=builder /app/nim_cli /usr/local/bin/nim_cli

ENTRYPOINT ["nim_cli"]
