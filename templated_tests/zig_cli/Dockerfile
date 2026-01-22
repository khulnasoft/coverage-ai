FROM ziglang/zig:alpine as builder

WORKDIR /app
COPY . .
RUN zig build-exe src/main.zig --name zig_cli

FROM alpine:latest
RUN apk add --no-cache ca-certificates
COPY --from=builder /app/zig_cli /usr/local/bin/zig_cli

ENTRYPOINT ["zig_cli"]
