# Python HelloWorld FastAPI 项目

一个基于 FastAPI 的 Python 应用，提供 HelloWorld API 服务和国密加密算法支持，演示基础的 API 开发、加密功能实现和容器化部署。

## 功能特性

- ✨ 简单的 HelloWorld API
- 🚀 基于 FastAPI 框架
- 🔐 国密加密算法支持（SM2、SM3、SM4）
- 🐳 Docker 容器化支持
- 📊 健康检查端点
- 🔧 环境变量配置
- 📦 使用 uv 进行依赖管理
- 🧪 完整的测试覆盖

## API 端点

- `GET /` - 返回 HelloWorld 消息
- `GET /health` - 健康检查
- `GET /info` - 应用信息
- `GET /hello/{name}` - 个性化问候
- `GET /docs` - FastAPI 自动生成的 API 文档

## 加密功能

项目集成了完整的国密算法实现，支持以下加密算法：

### SM2 椭圆曲线公钥密码算法
- 支持公钥加密和私钥解密
- 提供多种编码格式：原始字节、十六进制、Base64
- 支持 JSON 对象的加密和解密
- 可配置 ASN.1 编码和加密模式

### SM3 密码杂凑算法
- 提供安全的哈希计算功能
- 支持字符串输入，返回固定长度的哈希值
- 符合国密标准

### SM4 分组密码算法
- 支持对称加密和解密
- 使用 CBC 模式和 PKCS7 填充
- 提供多种编码格式：原始字节、十六进制、Base64
- 支持 JSON 对象的加密和解密

### 使用示例

```python
from src.encryption import SM2, SM3, SM4

# SM2 加密
sm2 = SM2(private_key="your_private_key", public_key="your_public_key")
encrypted = sm2.encrypt_2_base64(b"Hello World")

# SM3 哈希
sm3 = SM3()
hash_value = sm3.hash("Hello World")

# SM4 加密
sm4 = SM4(key=b"your_16_byte_key", iv=b"your_16_byte_iv")
encrypted = sm4.encrypt_2_base64(b"Hello World")
```

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
docker run -p 5555:5555 test-python-helloworld
```

### 使用 Docker Compose

```bash
# 构建并启动服务
docker-compose up --build

# 后台运行
docker-compose up -d --build

# 停止服务
docker-compose down
```

### 环境变量

- `SERVER_HOST`: 服务器主机地址（默认: 0.0.0.0）
- `SERVER_PORT`: 服务器端口（默认: 5000，Docker 中为 5555）
- `SERVER_WORKERS`: Gunicorn worker 数量（默认: 4）
- `PIP_INDEX_URL`: Python 包索引 URL（Docker Compose 中配置为内部仓库）

## 项目结构

```
test-python-helloworld/
├── server.py              # FastAPI 应用主文件
├── pyproject.toml          # 项目配置和依赖
├── uv.lock                # 锁定的依赖版本
├── Dockerfile             # Docker 构建文件
├── docker-compose.yml     # Docker Compose 配置
├── Jenkinsfile            # Jenkins CI/CD 配置
├── ruff.toml              # Ruff 代码检查配置
├── VERSION                # 版本文件
├── run-pytest-in-docker.sh # Docker 测试脚本
├── src/
│   └── encryption/        # 加密模块
│       └── __init__.py    # 国密算法实现（SM2、SM3、SM4）
├── test/                  # 测试目录
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_server.py     # API 测试
│   └── test_encryption_init.py # 加密模块测试
└── README.md              # 项目文档
```

## 开发技术栈

- **Web 框架**: FastAPI
- **ASGI 服务器**: Uvicorn + Gunicorn
- **加密算法**: 国密算法（SM2、SM3、SM4）
- **加密库**: gmssl
- **依赖管理**: uv
- **代码检查**: Ruff
- **测试框架**: pytest + pytest-cov
- **容器化**: Docker + Docker Compose
- **CI/CD**: Jenkins
- **Python 版本**: 3.12+

## 测试

### 运行测试

```bash
# 使用 uv 运行测试
uv run pytest

# 运行测试并生成覆盖率报告
uv run pytest --cov=src --cov-report=html

# 运行特定测试文件
uv run pytest test/test_server.py
uv run pytest test/test_encryption_init.py
```

### 使用 Docker 运行测试

```bash
# 使用提供的脚本在 Docker 中运行测试
./run-pytest-in-docker.sh
```

### 测试覆盖

项目包含以下测试：
- **API 测试**: 测试所有 FastAPI 端点的功能
- **加密模块测试**: 测试 SM2、SM3、SM4 算法的各种功能
- **覆盖率要求**: 最低 85% 的代码覆盖率

## 代码质量

```bash
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