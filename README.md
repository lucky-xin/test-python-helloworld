# Python HelloWorld FastAPI 项目

一个简单的 Python FastAPI HelloWorld 应用，演示基础的 API 开发和容器化部署。

## 功能特性

- ✨ 简单的 HelloWorld API
- 🚀 基于 FastAPI 框架
- 🐳 Docker 容器化支持
- 📊 健康检查端点
- 🔧 环境变量配置
- 📦 使用 uv 进行依赖管理

## API 端点

- `GET /` - 返回 HelloWorld 消息
- `GET /health` - 健康检查
- `GET /info` - 应用信息
- `GET /hello/{name}` - 个性化问候
- `GET /docs` - FastAPI 自动生成的 API 文档

## 本地开发

### 使用 uv（推荐）

```bash
# 安装依赖
uv sync

# 运行应用
uv run python server.py
```

### 使用传统方式

```bash
# 创建虚拟环境
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 安装依赖
pip install -e .

# 运行应用
python server.py
```

## Docker 部署

### 构建镜像

```bash
docker build -t test-python-helloworld .
```

### 运行容器

```bash
docker run -p 5000:5000 test-python-helloworld
```

### 环境变量

- `SERVER_HOST`: 服务器主机地址（默认: 0.0.0.0）
- `SERVER_PORT`: 服务器端口（默认: 5000）
- `SERVER_WORKERS`: Gunicorn worker 数量（默认: 4）
- `PIP_INDEX_URL`: Python 包索引 URL

## 项目结构

```
test-python-helloworld/
├── server.py          # FastAPI 应用主文件
├── pyproject.toml      # 项目配置和依赖
├── uv.lock            # 锁定的依赖版本
├── Dockerfile         # Docker 构建文件
├── .dockerignore      # Docker 忽略文件
└── README.md          # 项目文档
```

## 开发技术栈

- **Web 框架**: FastAPI
- **ASGI 服务器**: Uvicorn + Gunicorn
- **依赖管理**: uv
- **容器化**: Docker
- **Python 版本**: 3.12+


```
# 检查代码质量
uv run ruff check .

# 自动修复问题
uv run ruff check . --fix

# 格式化代码
uv run ruff format .

# 检查特定文件
uv run ruff check server.py

# 显示详细输出
uv run ruff check . --output-format=text

# 检查特定文件
uv run ruff check server.py

# 显示详细输出
uv run ruff check . --output-format=text


```

# 过程 debug

```powershell
docker run --rm -it `
  -v ${PWD}:/workspace `
  -e "DOCKER_CONFIG=/kaniko/.docker" `
  gcr.io/kaniko-project/executor:debug `
  --registry-mirror gzv-nex.piston.ink `
  --context=dir:///workspace `
  --dockerfile=Dockerfile.optimized `
  --destination=gzv-nex.xyz.ink/image:dev `
  --build-arg=PIP_INDEX_URL=http://172.29.35.103:8081/repository/python-group/simple `
  --verbosity=debug `
  --no-push

```

```bash
docker run --rm -it \
  -v ${PWD}:/workspace \
  -e "DOCKER_CONFIG=/kaniko/.docker" \
  gcr.io/kaniko-project/executor:debug \
  --registry-mirror gzv-nex.piston.ink \
  --context=dir:///workspace \
  --dockerfile=Dockerfile \
  --destination=gzv-nex.xyz.ink/image:dev \
  --build-arg=PIP_INDEX_URL=http://172.29.35.103:8081/repository/python-group/simple \
  --verbosity=debug \
  --no-push

```