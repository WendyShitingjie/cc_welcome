# 测试表生成器

一个用于快速生成符合 MySQL 建表规范的测试表工具，支持 MySQL、TiDB、ADB 等数据库。

## 特性

- ✅ 严格遵守 MySQL 建表规范
- ✅ 支持从配置文件管理数据库连接
- ✅ 自动生成测试数据
- ✅ 支持多种数据类型模板
- ✅ 可直接执行到数据库或导出 SQL 文件
- ✅ 支持命令行和自然语言交互

## 安装

### 1. 安装依赖

```bash
pip install pymysql
```

### 2. 配置数据库连接

编辑 `db_config.ini` 文件，添加你的数据库环境：

```ini
[环境名称]
type = mysql
host = 数据库主机地址
port = 端口号
database = 数据库名
username = 用户名
password = 密码
description = 环境描述
```

## 使用方法

### 查看所有配置的环境

```bash
python index.py list-envs
```

### 生成测试表

```bash
# 基本用法：生成 SQL 并显示
python index.py generate --tableName=test_users --dataType=mixed --rowCount=10

# 直接执行到数据库
python index.py generate --tableName=test_users --dataType=string --rowCount=50 --execute --env=cjjcommon

# 保存到文件
python index.py generate --tableName=test_orders --dataType=number --rowCount=100 --output=orders.sql
```

## 参数说明

| 参数 | 必填 | 说明 | 示例 |
|------|------|------|------|
| `--tableName` | 是 | 表名称 | `--tableName=test_users` |
| `--dataType` | 否 | 数据类型（string/number/date/boolean/mixed） | `--dataType=mixed` |
| `--rowCount` | 否 | 插入记录数（默认 10） | `--rowCount=100` |
| `--env` | 否 | 使用配置的环境名称 | `--env=cjjcommon` |
| `--execute` | 否 | 直接执行到数据库 | `--execute` |
| `--output` | 否 | 保存到文件 | `--output=test.sql` |
| `--tableComment` | 否 | 表注释 | `--tableComment=用户表` |
| `--includeDrop` | 否 | 包含 DROP TABLE 语句 | `--includeDrop` |

## 数据类型模板

### string - 字符串类型
包含 user_name、email、description 等字段

### number - 数值类型
包含 int、bigint、多种精度的 decimal、float 等字段

### date - 日期类型
包含 date、datetime、timestamp、year 等字段

### boolean - 布尔类型
包含 is_active、is_deleted、is_verified 等字段

### mixed - 混合类型（默认）
包含上述所有类型的综合字段

## 添加新环境

1. 打开 `db_config.ini`
2. 在文件末尾添加新环境配置：

```ini
[my-new-env]
type = mysql
host = my-host.example.com
port = 3306
database = my_database
username = my_user
password = my_password
description = 我的新环境
```

3. 验证配置：`python index.py list-envs`

## 使用示例

### 示例 1：生成并查看 SQL
```bash
python index.py generate --tableName=test_demo --dataType=mixed --rowCount=5
```

### 示例 2：生成并执行到数据库
```bash
python index.py generate --tableName=test_users --dataType=string --rowCount=100 --execute --env=cjjcommon
```

### 示例 3：生成数值表（包含多种 decimal 精度）
```bash
python index.py generate --tableName=test_prices --dataType=number --rowCount=50 --execute --env=datagovernor
```

### 示例 4：生成并保存到文件
```bash
python index.py generate --tableName=test_orders --dataType=mixed --rowCount=200 --output=orders.sql --tableComment=订单测试表
```

## MySQL 建表规范

本工具生成的表严格遵守以下规范：

- 主键为 `id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT`
- 必须包含 `created_at` 和 `updated_at` 字段
- `updated_at` 自动更新且有索引
- 所有字段和表都有中文注释
- 使用 InnoDB 引擎和 utf8mb4 字符集
- 表名、字段名全部小写，使用下划线命名

## 安全提示

⚠️ `db_config.ini` 包含数据库密码，请勿提交到公共代码仓库

建议：
- 将 `db_config.ini` 添加到 `.gitignore`
- 提供 `db_config.ini.example` 作为模板
- 团队成员各自维护自己的配置文件

## 常见问题

**Q: 提示需要安装 pymysql 库？**
A: 运行 `pip install pymysql`

**Q: 连接数据库失败？**
A: 检查 `db_config.ini` 中的配置是否正确

**Q: 如何自定义字段？**
A: 通过自然语言告诉 Claude 你的需求，或修改代码中的 `DATA_TYPE_SCHEMAS`

## 文件说明

- `index.py` - 主程序
- `db_config.ini` - 数据库配置文件（需自行配置）
- `skill.json` - Claude Code skill 配置
- `README.md` - 使用说明

## 版本

v1.0.0 (2026-01-28)
