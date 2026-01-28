# 测试表生成器 Skill 使用指南

## Skill 配置完成 ✅

你的 `test-table-generator` 已经成功配置为 Claude Code skill！

## 在 Claude Code 中使用

### 方式 1：在项目中直接使用（推荐）

由于 skill 已经在项目目录中，Claude Code 会自动发现它。你可以直接通过以下方式调用：

```bash
/test-table 你的需求描述
```

### 方式 2：通过命令行参数调用

```bash
# 基础用法：生成混合类型测试表（只显示 SQL）
/test-table --tableName=test_users --dataType=mixed --rowCount=10

# 直接执行到数据库（使用预配置环境）
/test-table --tableName=test_orders --dataType=string --rowCount=50 --execute=true --env=cjjcommon

# 生成并保存到文件
/test-table --tableName=test_products --dataType=number --rowCount=100 --output=products.sql

# 包含 DROP TABLE 语句
/test-table --tableName=test_demo --includeDrop=true --rowCount=20
```

## 参数说明

| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `tableName` | ✅ 是 | - | 表名称 |
| `dataType` | 否 | mixed | 数据类型：string, number, date, boolean, mixed |
| `rowCount` | 否 | 10 | 生成的测试数据行数 |
| `dbType` | 否 | mysql | 数据库类型：mysql, tidb, adb |
| `env` | 否 | - | 预配置环境名称（cjjcommon, tidb-ares 等）|
| `execute` | 否 | false | 是否直接执行到数据库 |
| `output` | 否 | - | 保存 SQL 文件路径 |
| `tableComment` | 否 | - | 表注释 |
| `includeDrop` | 否 | false | 是否包含 DROP TABLE 语句 |

## 可用的预配置环境

使用以下命令查看所有可用环境：

```bash
python3 index.py list-envs
```

当前配置的环境：
- `cjjcommon` - MySQL 入仓测试环境
- `bigdata-biz` - MySQL 入仓测试环境
- `datagovernor` - MySQL 数据治理环境
- `cjjloan` - MySQL 入仓测试环境
- `tidb-ares` - TiDB 测试环境
- `adb-realtime` - ADB 实时数仓环境

## 使用示例

### 示例 1：生成字符串类型测试表
```bash
/test-table --tableName=test_users --dataType=string --rowCount=50
```

### 示例 2：生成数值类型表并执行到 TiDB
```bash
/test-table --tableName=test_prices --dataType=number --rowCount=100 --execute=true --env=tidb-ares --dbType=tidb
```

### 示例 3：生成混合类型表并保存到文件
```bash
/test-table --tableName=test_orders --dataType=mixed --rowCount=200 --output=/Users/wendy/PycharmProjects/ClaudeCode的脚本/orders.sql --tableComment=订单测试表
```

### 示例 4：生成日期类型表（包含 DROP）
```bash
/test-table --tableName=test_events --dataType=date --rowCount=30 --includeDrop=true
```

## 数据类型说明

### string（字符串类型）
包含字段：user_name, email, description

### number（数值类型）
包含字段：int_value, bigint_value, decimal_value (多种精度), float_value

### date（日期类型）
包含字段：date_value, datetime_value, timestamp_value, year_value

### boolean（布尔类型）
包含字段：is_active, is_deleted, is_verified

### mixed（混合类型，默认）
包含上述所有类型的综合字段

## 独立运行（不使用 Claude Code）

你也可以直接在 PyCharm 或命令行中运行：

```bash
cd /Users/wendy/PycharmProjects/cc_free_coder/test-table-generator

# 查看所有环境
python3 index.py list-envs

# 生成测试表
python3 index.py generate --tableName=test_demo --dataType=mixed --rowCount=10

# 执行到数据库
python3 index.py generate --tableName=test_users --execute --env=cjjcommon --rowCount=50
```

## 注意事项

1. ⚠️ 使用 `--execute=true` 会直接在数据库中创建表和插入数据
2. 📝 所有生成的表都严格遵守 MySQL 建表规范
3. 🔐 数据库密码存储在 `db_config.ini` 中，请勿提交到公共仓库
4. 🐍 确保已安装 `pymysql` 库：`pip install pymysql`

## 文件结构

```
test-table-generator/
├── index.py           # 主程序（可直接在 PyCharm 运行）
├── skill.json         # Skill 配置文件
├── db_config.ini      # 数据库环境配置
├── README.md          # 详细使用说明
├── SKILL_USAGE.md     # Skill 使用指南（本文件）
└── .gitignore         # Git 忽略配置
```

## 故障排除

### 问题：找不到 pymysql 库
**解决方案：**
```bash
pip install pymysql
```

### 问题：连接数据库失败
**解决方案：**
1. 检查 `db_config.ini` 中的配置是否正确
2. 确认网络可以访问目标数据库
3. 验证用户名和密码是否正确

### 问题：Claude Code 找不到 skill
**解决方案：**
1. 确认 `skill.json` 格式正确（JSON 格式）
2. 确认 `index.py` 有执行权限：`chmod +x index.py`
3. 重启 Claude Code 或重新加载项目

## 版本信息

- **Skill 版本**: v1.0.0
- **Python 版本要求**: Python 3.9+
- **支持的数据库**: MySQL 5.7+, TiDB, ADB
- **最后更新**: 2026-01-28
