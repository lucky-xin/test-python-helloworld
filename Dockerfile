FROM python:3.12-slim

WORKDIR /app

ENV SERVER_PORT=5555

EXPOSE 5555

# 从第一阶段复制可执行文件（需要构建产物存在）
COPY ./dist/main /app/main

# Set executable permission and run
RUN chmod +x /app/main

ENTRYPOINT ["./main"]