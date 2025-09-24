#!/usr/bin/env bash

set -euo pipefail

IMAGE="xin8/devops/python:latest"
WORKDIR="/workspace"
PROJECT_DIR="$(pwd)"

echo "=== 使用 Docker 运行 pytest ==="

# 确保 reports 目录存在
mkdir -p "${PROJECT_DIR}/reports"

# 校验容器内依赖是否就绪（pytest 与 pytest-cov）
if ! docker run --rm "${IMAGE}" bash -lc "command -v python3 >/dev/null 2>&1 && pytest --version >/dev/null 2>&1 && python3 - <<'PY'
import sys
missing = []
try:
    import pytest  # noqa: F401
except Exception:
    missing.append('pytest')
try:
    import pytest_cov  # noqa: F401
except Exception:
    missing.append('pytest-cov')
sys.exit(1 if missing else 0)
PY
" ; then
  echo "容器依赖缺失，开始本地重建镜像..."
  # 基于根目录 Dockerfile 重建（build.sh 已默认使用根目录 Dockerfile）
  bash "${PROJECT_DIR}/python/build.sh" --local --registry xin8 --tag latest
fi

# 在容器中执行 pytest
echo "=== 运行 pytest ==="
docker run --rm -t \
  -v "${PROJECT_DIR}:${WORKDIR}" \
  -w "${WORKDIR}" \
  "${IMAGE}" bash -lc "python3 -m pip install -q fastapi httpx && mkdir -p reports && pytest test --cov=src --cov-report=xml:reports/coverage.xml --cov-report=term --junitxml=reports/junit.xml"

echo "=== 测试完成，报告已生成在 ./reports ==="


