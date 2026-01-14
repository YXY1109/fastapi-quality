# FastAPI 代码质量检测项目

一个配置了完整代码质量检测工具的 FastAPI 应用示例。

## 特性

- FastAPI Web 框架
- **Ruff** - 快速的 Python linter 和 formatter
- **Mypy** - 静态类型检查
- **Bandit** - 安全漏洞检测
- **Pre-commit** - Git 提交前自动检测
- **GitHub Actions CI** - 持续集成检测

## 快速开始

### 1. 安装 uv

uv 是一个快速的 Python 包管理器。

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. 安装依赖

```bash
uv sync --extra dev
```

### 3. 启动开发服务器

```bash
uv run uvicorn src.fastapi_quality.main:app --reload
```

访问 http://localhost:8000 查看 API
访问 http://localhost:8000/docs 查看 Swagger 文档

### 4. 运行测试

```bash
uv run pytest tests/ -v
```

### 5. 代码质量检测

```bash
# Ruff 检查
uv run ruff check .

# Ruff 格式化
uv run ruff format .

# Mypy 类型检查
uv run mypy src/

# Bandit 安全检查
uv run bandit -r src/
```

---

## 项目结构

```
fastapi-quality/
├── .github/workflows/
│   └── quality.yml          # GitHub Actions CI 配置
├── .pre-commit-config.yaml  # Pre-commit 钩子配置
├── pyproject.toml           # 项目配置（依赖 + 工具配置）
├── src/
│   └── fastapi_quality/
│       ├── main.py          # FastAPI 应用入口
│       ├── api/
│       │   └── routes.py    # API 路由和业务逻辑
│       └── models/
│           └── schemas.py   # Pydantic 数据模型
└── tests/
    └── test_api.py          # API 测试
```

---

## 代码质量工具说明

### Ruff - 代码检查与格式化

Ruff 是用 Rust 编写的快速 Python linter，替代了 flake8、pylint、isort、black 等工具。

```bash
# 检查代码问题
uv run ruff check .

# 自动修复可修复的问题
uv run ruff check . --fix

# 格式化代码
uv run ruff format .

# 仅检查格式（不修改文件）
uv run ruff format . --check
```

**配置位置：** `pyproject.toml` 中的 `[tool.ruff]` 部分

### Mypy - 静态类型检查

检查 Python 类型注解，在运行前发现类型错误。

```bash
uv run mypy src/
```

**配置位置：** `pyproject.toml` 中的 `[tool.mypy]` 部分

### Bandit - 安全漏洞检测

检测常见安全问题，如硬编码密码、SQL 注入风险等。

```bash
uv run bandit -r src/
```

### Pre-commit - Git 提交钩子

在 `git commit` 前自动运行代码检测。

**安装钩子：**
```bash
uv run pre-commit install
```

**手动运行所有检测：**
```bash
uv run pre-commit run --all-files
```

---

## 常用命令速查

### uv 命令

```bash
# 添加生产依赖
uv add fastapi uvicorn

# 添加开发依赖
uv add --dev pytest

# 运行 Python 脚本
uv run python script.py
```

### 质量检测命令

```bash
uv run ruff check .              # 检查
uv run ruff check . --fix        # 检查并修复
uv run ruff format .             # 格式化
uv run mypy src/                 # 类型检查
uv run bandit -r src/            # 安全检查
uv run pre-commit run --all-files # 手动运行所有检测
uv run pytest tests/ -v          # 运行测试
```

---

## API 接口说明

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/` | 健康检查 |
| GET | `/items/` | 获取项目列表（支持分页） |
| GET | `/items/{id}` | 获取单个项目 |
| POST | `/items/` | 创建新项目 |

### 示例请求

```bash
# 创建项目
curl -X POST "http://localhost:8000/items/" \
  -H "Content-Type: application/json" \
  -d '{"name": "Laptop", "price": 999.99, "tax": 99.99}'

# 获取所有项目
curl "http://localhost:8000/items/"

# 获取单个项目
curl "http://localhost:8000/items/1"

# 分页查询
curl "http://localhost:8000/items/?skip=0&limit=10"
```

---

## CI/CD 集成

项目包含 GitHub Actions 配置 (`.github/workflows/quality.yml`)，在以下情况自动运行检测：
- Push 到 main/develop 分支
- 创建 Pull Request

检测项目包括：
- Ruff lint
- Ruff format
- Mypy
- Bandit
- Pytest

---

## 常见问题

### Q: Ruff 检测失败怎么办？

运行 `uv run ruff check . --fix` 自动修复大部分问题。

### Q: Mypy 报类型错误？

检查函数参数和返回值是否有类型注解。如需忽略某行，添加 `# type: ignore`。

### Q: Pre-commit 太慢？

只在提交关键代码时使用，或使用 `git commit --no-verify` 跳过（不推荐）。
