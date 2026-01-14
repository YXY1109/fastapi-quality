# FastAPI 质量检测项目使用指南

本项目展示了一个完整的 FastAPI 应用配置，包含全面的代码质量检测工具。

## 环境准备

### 1. 安装 uv

uv 是一个快速的 Python 包管理器，替代 pip。

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

验证安装：
```bash
uv --version
```

### 2. 初始化项目环境

```bash
# 克隆项目后，进入项目目录
cd fastapi-quality

# 安装所有依赖（包括开发依赖）
uv sync --extra dev
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

## 代码质量工具

### Ruff - 代码检查与格式化

Ruff 是一个用 Rust 编写的快速 Python linter 和 formatter，替代了以下工具：
- **flake8/pycodestyle** - PEP8 风格检查
- **pylint** - 代码质量检查
- **isort** - import 排序
- **black** - 代码格式化

**使用命令：**
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

**启用的规则：**
- `E/W` - PEP8 风格错误/警告
- `F` - Pyflakes 逻辑错误
- `I` - Import 排序
- `N` - 命名规范
- `UP` - 语法现代化
- `B` - Bug 风险检测
- `S` - 安全问题检测
- `PL` - Pylint 规则
- 更多...（见 pyproject.toml）

---

### Mypy - 静态类型检查

Mypy 检查 Python 类型注解，在运行前发现类型错误。

**使用命令：**
```bash
uv run mypy src/
```

**配置位置：** `pyproject.toml` 中的 `[tool.mypy]` 部分

**配置说明：**
- `strict = true` - 启用严格模式
- `disallow_untyped_defs = true` - 禁止无类型注解的函数

---

### Bandit - 安全漏洞检测

Bandit 检测常见的安全问题，如硬编码密码、SQL 注入风险等。

**使用命令：**
```bash
uv run bandit -r src/
```

**检测内容：**
- 硬编码密码和密钥
- 不安全的函数使用
- SQL 注入风险
- YAML 解析安全问题
- 更多...

---

### Pre-commit - Git 提交钩子

Pre-commit 在 `git commit` 前自动运行代码检测。

**安装钩子：**
```bash
uv run pre-commit install
```

**手动运行所有检测：**
```bash
uv run pre-commit run --all-files
```

**跳过钩子（不推荐）：**
```bash
git commit --no-verify -m "message"
```

**配置位置：** `.pre-commit-config.yaml`

---

## 本地开发流程

### 1. 安装依赖

```bash
uv sync --extra dev
```

### 2. 启动开发服务器

```bash
uv run uvicorn src.fastapi_quality.main:app --reload
```

访问 http://localhost:8000 查看 API
访问 http://localhost:8000/docs 查看 Swagger 文档

### 3. 运行测试

```bash
uv run pytest tests/ -v
```

### 4. 代码质量检测

运行所有检测：
```bash
uv run ruff check . && uv run ruff format . --check && uv run mypy src/ && uv run bandit -r src/
```

### 5. 提交代码

安装 pre-commit 钩子后，每次提交会自动运行检测：
```bash
git add .
git commit -m "feat: add new feature"
```

如果检测失败，修复后重新提交：
```bash
git add .
git commit -m "feat: add new feature"
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

# 运行模块
uv run uvicorn src.fastapi_quality.main:app --reload
```

### 质量检测命令

```bash
# Ruff
uv run ruff check .              # 检查
uv run ruff check . --fix        # 检查并修复
uv run ruff format .             # 格式化

# Mypy
uv run mypy src/                 # 类型检查

# Bandit
uv run bandit -r src/            # 安全检查

# Pre-commit
uv run pre-commit install        # 安装钩子
uv run pre-commit run --all-files # 手动运行

# 测试
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

## 常见问题

### Q: Ruff 检测失败怎么办？

A: 运行 `uv run ruff check . --fix` 自动修复大部分问题。

### Q: Mypy 报类型错误？

A: 检查函数参数和返回值是否有类型注解。如需忽略某行，添加 `# type: ignore`。

### Q: Pre-commit 太慢？

A: 只在提交关键代码时使用，或跳过某些检测。

### Q: 如何添加新的规则？

A: 编辑 `pyproject.toml` 中 `[tool.ruff.lint]` 的 `select` 列表。

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
