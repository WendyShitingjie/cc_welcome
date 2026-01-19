# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

这是一个 Python 测试辅助脚本集合,主要用于数据平台相关的测试和数据处理任务。项目包含多个独立的 Python 脚本,用于不同场景的测试、数据生成和 API 调用。

## 主要目录结构

- `pythonProject/` - 主要项目目录
  - `test/` - 测试相关脚本
    - `api自动化辅助脚本/` - API 自动化测试辅助工具集
  - `feature/` - 特征平台相关测试脚本
  - `ecube/` - ecube 相关脚本
  - `数分/` - 数据分析相关脚本
- `oss2dp/` - OSS 到数据平台的数据格式转换脚本
- `ClaudeCode的脚本/` - **Claude Code 生成的脚本存放目录**（所有新生成的 Python 脚本默认存放于此）

## 核心功能模块

### 1. 数据库测试数据生成
项目包含多个批量生成和插入测试数据的脚本:
- `1e.py` - 生成大量测试数据并批量插入到 TiDB 数据库
- `每天插入15条数据到datagovernor表.py` - 定期插入测试数据到 datagovernor 表
- `每天插入20条数据到featurestore库表.py` - 定期插入测试数据到 featurestore 表

**数据库连接配置模式:**
```python
# TiDB 配置示例
config = {
    'host': 'sitpublic.tidb.ali-bj-sit01.shuheo.net',
    'port': 4000,
    'user': 'user_for_dp',
    'password': 'your_password',
    'database': 'dataops',
    'charset': 'utf8mb4'
}

# MySQL 配置示例
config = {
    'host': 'bigdata-biz.db.ali-bj-bdsit01.shuheo.net',
    'user': 'bdsit_user_datagovernor',
    'password': 'password',
    'database': 'datagovernor',
    'charset': 'utf8mb4'
}
```

使用 `mysql.connector` 或 `pymysql` 库进行数据库连接。

### 2. 消息队列测试
用于测试 RabbitMQ 和 Kafka 消息流:
- `test/api自动化辅助脚本/send_rabbitMQ.py` - 直接向 RabbitMQ 发送消息
- `bpm_send_mq.py` - 通过 API 发送 RabbitMQ 消息
- `test/api自动化辅助脚本/send_kafka.py` - 发送 Kafka 消息

**消息格式模式:**
```python
message = {
    "startUid": "uuid",
    "orderNo": "工单号",
    "dataMap": json.dumps({...}),
    "status": "STATUS_APPROVED"
}
```

### 3. API 压力测试
`接口并发.py` - HTTP 接口负载测试工具,支持:
- 自定义并发数和请求总数
- 支持 GET/POST 等 HTTP 方法
- 生成响应时间统计报告和分布图

**使用方式:**
```bash
python 接口并发.py <url> -m POST -c 10 -r 100 -d '{"key":"value"}'
```

### 4. 特征平台测试
`feature/` 目录包含特征平台相关测试:
- `模型特征测试.py` - 批量调用特征接口并对比结果
- `特征平台迁移旧-新.py` - 特征平台迁移对比测试
- 支持分块处理大量 UID 数据

**特征测试 API 模式:**
```python
url = 'http://moka.dmz.prod.caijj.net/featurestoreopr/featurestorejob/feature/test'
data = {
    'registerType': 'SQL_COMPUTE',
    'groupCode': 'fg.rt.usr.device_rta_model_feature_record',
    'logicVersion': '1',
    'inputList': uid_list
}
```

### 5. 数据格式转换
`oss2dp/` 目录包含多种数据格式处理:
- `testdata_json.py` - JSON 数据生成
- `testdata_csv.py` - CSV 数据处理
- `testdata_txt.py` - 文本数据处理
- `test_orc.py` - ORC 文件格式处理
- `解析orc文件.py` - 解析 ORC 文件

## 常用依赖库

项目主要使用以下 Python 库:
- `mysql.connector` / `pymysql` - 数据库连接
- `requests` - HTTP 请求
- `pika` - RabbitMQ 客户端
- `pandas` - 数据处理
- `concurrent.futures` - 并发处理
- `matplotlib` - 数据可视化

## 开发环境

- Python 3.9
- 虚拟环境位于 `pythonProject/venv/`

**激活虚拟环境:**
```bash
source pythonProject/venv/bin/activate
```

## 命名约定

- 测试数据生成脚本通常以目标表名或功能命名
- BPM 相关脚本命名格式: `bpm_send_mq_<场景描述>.py`
- 测试辅助脚本放在 `test/` 目录下
- API 自动化辅助脚本统一放在 `test/api自动化辅助脚本/` 目录

## 数据环境

项目主要针对以下测试环境:
- SIT 环境 (ali-bj-sit01, ali-bj-sit03)
- 生产模拟环境 (moka.dmz.prod.caijj.net, moka.dmz.sit.caijj.net)

## 脚本存放规则

**重要：所有通过 Claude Code 新生成的 Python 脚本都必须默认存放在 `ClaudeCode的脚本/` 目录下。**

路径：`/Users/wendy/PycharmProjects/ClaudeCode的脚本/`

## 注意事项

1. 数据库密码和敏感信息已在代码中明文存储,仅用于测试环境
2. 脚本独立运行,没有统一的项目入口
3. 大部分脚本需要根据实际测试场景修改参数后运行
4. 数据生成脚本使用随机数据,包含完整的字段逻辑关联处理
5. API 测试脚本包含环境特定的 URL 和 token 配置
