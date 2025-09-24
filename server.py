"""
Simple FastAPI HelloWorld Application
"""

from datetime import datetime
import os
import socket

from fastapi import FastAPI

app = FastAPI(
    title="Python HelloWorld API",
    description="A simple HelloWorld FastAPI application",
    version="1.0.0",
)


@app.get("/")
async def read_root():
    """返回简单的 HelloWorld 消息"""
    return {
        "message": "Hello, World!",
        "timestamp": datetime.now().isoformat(),
        "service": "test-python-helloworld",
        "version": "1.0.0",
    }


@app.get("/health")
async def health_check():
    """健康检查端点"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "hostname": socket.gethostname(),
        "service": "test-python-helloworld",
    }


@app.get("/info")
async def get_info():
    """获取应用信息"""
    return {
        "app_name": "Python HelloWorld",
        "version": "1.0.0",
        "python_version": os.sys.version,
        "hostname": socket.gethostname(),
        "environment": {
            "SERVER_HOST": os.getenv("SERVER_HOST", "0.0.0.0"),
            "SERVER_PORT": os.getenv("SERVER_PORT", "5000"),
            "SERVER_WORKERS": os.getenv("SERVER_WORKERS", "4"),
        },
    }


@app.get("/hello/{name}")
async def say_hello(name: str):
    """个性化问候"""
    return {
        "message": f"Hello, {name}!",
        "timestamp": datetime.now().isoformat(),
        "service": "test-python-helloworld",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host=os.getenv("SERVER_HOST", "0.0.0.0"),
        port=int(os.getenv("SERVER_PORT", "5000")),
    )
