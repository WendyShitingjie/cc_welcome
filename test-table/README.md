# JDBC 测试表生成器

一个用于快速生成符合规范的测试表和测试数据的工具，支持 MySQL、TiDB、ADB 等多种数据库。

## 功能特性

- 🚀 **快速生成**：一条命令即可创建测试表并插入数据
- 🎯 **多种数据类型**：支持 mixed（混合）、numeric（数字）、string（字符串）、datetime（日期时间）
- 🔧 **多环境支持**：预配置了 6 个测试环境，开箱即用
- 📝 **符合规范**：自动生成符合 MySQL 建表规范的 SQL
- 🎨 **灵活配置**：支持自定义表名、数据行数、数据类型

## 支持的测试环境

| 环境名称 | 数据库类型 | 数据库名 |
|---------|----------|---------|
| cjjcommon | MySQL | dataops_shitingjie |
| bigdata-biz-dataops | MySQL | dataops |
| bigdata-biz-datagovernor | MySQL | datagovernor |
| cjjloan | MySQL | datahub |
| tidb-ares | TiDB | ares |
| adb-realtime | ADB | stjtestadb |

## 快速开始

### 1. 安装依赖

```bash
pip install pymysql
```

### 2. 基本使用

```bash
cd scripts
python index.py generate --tableName test_demo --rowCount 10 --env cjjcommon --execute
```

### 3. 参数说明

| 参数 | 说明 | 必需 | 默认值 |
|-----|------|------|--------|
| `--tableName` | 表名 | 是 | - |
| `--rowCount` | 数据行数 | 否 | 10 |
| `--dataType` | 数据类型（mixed/numeric/string/datetime） | 否 | mixed |
| `--env` | 目标环境 | 否 | - |
| `--execute` | 是否执行到数据库 | 否 | false |

## 使用示例

### 示例 1：生成 SQL 但不执行

```bash
python index.py generate --tableName test_users --dataType mixed --rowCount 50
```

### 示例 2：直接创建表并插入数据

```bash
python index.py generate --tableName test_orders --dataType mixed --rowCount 100 --execute --env cjjcommon
```

### 示例 3：生成纯数���类型的测试表

```bash
python index.py generate --tableName test_numbers --dataType numeric --rowCount 20 --execute --env tidb-ares
```

## 数据类型说明

- **mixed**（推荐）：包含多种字段类型（VARCHAR、INT、DECIMAL、DATETIME、TEXT 等）
- **numeric**：仅包含数字类型字段（INT、BIGINT、DECIMAL、FLOAT）
- **string**：仅包含字符串类型字段（VARCHAR、CHAR、TEXT）
- **datetime**：包含日期时间类型字段（DATE、DATETIME、TIMESTAMP）

## 配置文件

数据库连接配置位于 `scripts/db_config.ini`，包含所有测试环境的连接信息。

## 详细文档

查看 [SKILL.md](SKILL.md) 获取完整的使用文档和高级功能说明。

## 参考资料

- [JDBC 测试环境连接信息](references/JDBC_sit_connnect_info.md)
- [JDBC SQL 验证规则](references/JDBC_sql_verify_rules.md)
- [JDBC 入仓工作流梳理](references/JDBC入仓工作流梳理.md)

## 注意事项

1. 仅用于测试环境，请勿在生产环境使用
2. 建议表名以 `test_` 开头，便于识别测试表
3. 大量数据生成（>1000 行）可能需要较长时间
4. 执行前请确认目标环境和数据库名称

## 常见问题

**Q: 如何查看生成的 SQL 而不执行？**
A: 不使用 `--execute` 参数，脚本会将 SQL 输出到控制台。

**Q: 如何添加新的测试环境？**
A: 编辑 `scripts/db_config.ini` 文件，添加新的环境配置。

**Q: 支持哪些数据库？**
A: 目前支持 MySQL、TiDB、ADB（AnalyticDB）。

## 贡献者

- Wendy Shitingjie
- Claude Opus 4.6

## 许可证

内部使用，仅供公司测试人员使用。
