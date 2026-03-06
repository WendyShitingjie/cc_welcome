# AI测试用例生成 - 快速参考卡

## 🎯 用户指令

```
请基于知识库中的 TKF_XXX_XXX.md 生成覆盖本流程的全部测试用例，用例格式为可执行的YAML格式
```

---

## 📋 执行清单

### ☑️ 步骤1：读取知识库（5分钟）

```bash
# 必读文件
□ flows/TKF_XXX_XXX.md                    # 业务流程（核心）
□ components/TKD_*.md                     # 数据组件
□ components/TKJ_*.md                     # Job组件
□ components/TKI_*.md                     # 集成组件
□ rules/TKR_*.md                          # 业务规则
```

### ☑️ 步骤2：识别测试场景（10分钟）

**识别规则**:
- ✅ 业务场景 → 测试场景（直接转换）
- ✅ 业务规则 → 异常场景（推导）
- ✅ 状态流转 → 状态场景（推导）
- ✅ 断点续传规则 → 断点续传场景（推导）

**输出**: 场景列表（3-10个）

### ☑️ 步骤3：生成YAML用例（每个场景15分钟）

**文件命名**: `TC_<流程ID>_<序号>_<用例名称>.yaml`

**必需内容**:
```yaml
# 文件头注释
test_case_id: TC_XXX_001
test_name: XXX
business_flow: XXX
priority: P0/P1/P2           # 根据场景自动判定
automation_level: L0/L1/L2/L3  # 根据知识库完整性自动判定
business_rules: [...]
related_knowledge: {...}
test_intent:
  preconditions: [...]      # 先清理后准备！
  test_steps: [...]         # 包含assertions
expected_result: |
  ...
```

**关键检查**:
- ✅ preconditions顺序：先clean_test_data，后prepare_datahub_data
- ✅ clean_test_data 使用 `where` 精确匹配（而非 `pattern` 模糊匹配）
- ✅ 每个用例必须有 `business_rules` 字段且非空
- ✅ 所有Job断言都有timeout和poll_interval
- ✅ 数据库断言添加 `wait` 参数（等待数据落库）
- ✅ 断言字段必须在目标表中实际存在
- ✅ common_job_status表用business_type，其他表用source
- ✅ JSON字段用JSON_UNQUOTE
- ✅ 不手动指定batch_no

### ☑️ 步骤4：生成MD总览（10分钟）

**文件命名**: `<流程ID>_测试用例集总览.md`

**必需内容**:
```markdown
# 业务流程
# 测试覆盖策略
# 测试用例清单（每个用例详细说明）
# 测试覆盖率统计
# 执行建议
```

---

## 🎯 场景识别速查表

| 来源 | 识别方法 | 示例 | 优先级 |
|------|---------|------|--------|
| 业务场景 | 直接转换 | 场景1：正常批量生成 → TC_001 | P0 |
| 业务规则 | 推导异常 | TKR_001（DP状态判断）→ DP未产出场景 | P1 |
| 状态流转 | 推导状态场景 | FAILURE状态 → 失败重试场景 | P1 |
| 状态流转 | 推导补偿场景 | PROCESSING状态 → 处理中补偿 | P1 |
| 断点续传规则 | 推导容错场景 | TKR_002 → 断点续传场景 | P0 |

---

## ⚠️ 9大常见错误

### ❌ 错误1：数据准备顺序错误
```yaml
# 错误
preconditions:
  - prepare_datahub_data  # 先准备
  - clean_test_data       # 后清理（会清掉刚准备的数据！）

# 正确
preconditions:
  - clean_test_data       # 先清理
  - prepare_datahub_data  # 后准备
```

### ❌ 错误2：数据清理用模糊匹配导致清理失败
```yaml
# 错误：sourceCode 是 'ds.grt.graph.risk'，pattern "test%" 匹配不到
params:
  tables: ["featurestore.source_basic_info"]
  pattern: "test%"

# 正确：使用精确 WHERE 条件
params:
  tables: ["featurestore.source_basic_info"]
  where: "source_code = 'ds.grt.graph.risk'"
```

### ❌ 错误3：缺少 business_rules 导致报告覆盖为空
```yaml
# 错误：测试报告中业务规则覆盖显示为空
test_case_id: TC_TKI001_001
business_flow: TKF_001
# 没有 business_rules

# 正确：每个用例必须关联业务规则
test_case_id: TC_TKI001_001
business_flow: TKF_001
business_rules:
  - TKR_001  # 图数据源编码命名规则
  - TKR_005  # 数据源类型校验规则
```

### ❌ 错误4：Job断言缺少超时参数
```yaml
# 错误
assertions:
  - primitive: assert_field_equals
    params:
      table: "copilot.common_job_status"
      field: "status"
      expected: "SUCCESS"
      # 缺少timeout和poll_interval！

# 正确
assertions:
  - primitive: assert_field_equals
    params:
      table: "copilot.common_job_status"
      field: "status"
      expected: "SUCCESS"
      timeout: 30
      poll_interval: 2
```

### ❌ 错误5：数据库断言不等待数据落库
```yaml
# 错误：API 返回成功后立即查库，数据可能还没写入
- primitive: assert_database_record
  params:
    table: "featurestore.source_basic_info"
    where: "source_code='${context.sourceCode}'"
    assertions:
      - field: "source_type"
        expected: "GRAPH"

# 正确：添加 wait 参数
- primitive: assert_database_record
  params:
    table: "featurestore.source_basic_info"
    where: "source_code='${context.sourceCode}'"
    wait: 3  # 等待3秒
    assertions:
      - field: "source_type"
        expected: "GRAPH"
```

### ❌ 错误6：断言不存在的数据库字段
```yaml
# 错误：register_type 字段已从表中移除
assertions:
  - field: "register_type"
    expected: "GRAPH"

# 正确：只断言实际存在的字段
assertions:
  - field: "source_type"
    expected: "GRAPH"
```

### ❌ 错误7：字段映射错误
```yaml
# 错误：common_job_status表使用source字段
where: "job_name='XXX' AND source='postLoan'"  # 字段不存在！

# 正确：common_job_status表使用business_type字段
where: "job_name='XXX' AND business_type='postLoan'"
```

### ❌ 错误8：JSON字段处理错误
```yaml
# 错误：返回带引号的字符串 "1"
field: "JSON_EXTRACT(output_data, '$.resp_code')"

# 正确：返回不带引号的值 1
field: "JSON_UNQUOTE(JSON_EXTRACT(output_data, '$.resp_code'))"
```

### ❌ 错误9：手动指定batch_no
```yaml
# 错误：可能与其他测试冲突
params:
  batch_no: "20260210001"
  source: "postLoan"

# 正确：让原语自动生成
params:
  source: "postLoan"
  # batch_no不传，自动生成
```

---

## 🏆 自动化等级速查表

| 等级 | 名称 | 判定条件 | 示例场景 |
|------|------|---------|---------|
| **L3** ⭐⭐⭐ | 高成熟可自动化 | 知识完整（触发示例✅、验证示例✅、数据模板✅、关键知识点✅） | 正常流程、失败重试 |
| **L2** ⭐⭐ | 可自动化 | 知识基本完整，需少量人工调整 | 断点续传、处理中补偿 |
| **L1** ⭐ | 弱可自动化 | 知识不完整，需大量人工补充 | 复杂环境配置场景 |
| **L0** ⚪ | 不可自动化 | 依赖人工判断或主观经验 | 质量评估、用户体验 |

---

## 📊 测试数据量速查表

| 场景类型 | 数据量 | 说明 |
|---------|--------|------|
| 正常流程 | 2个用户 | 最小有效数据集 |
| 断点续传 | 4个用户 | 模拟2页数据（每页2个） |
| 失败重试 | 2条记录 | 验证批量处理 |
| 处理中补偿 | 2条记录 | 验证批量处理 |
| 异常场景 | 2个用户 | 验证异常处理逻辑 |

---

## ⏱️ 超时时间速查表

| 操作类型 | 参数 | 推荐值 | 说明 |
|---------|------|--------|------|
| Job1（名单拉取） | timeout / poll_interval | 60-120秒 / 5秒 | 数据量大，耗时长 |
| Job2（剧本生成） | timeout / poll_interval | 30-60秒 / 2-3秒 | AI调用，中等耗时 |
| 数据库异步查询 | timeout / poll_interval | 30秒 / 2-3秒 | 异步插入，需等待 |
| API后数据库验证 | wait | 3秒 | assert_database_record 等待数据落库 |

---

## 📝 生成输出示例

**输入**:
```
请基于知识库中的 TKF_001_离线剧本批量生成.md 生成覆盖本流程的全部测试用例
```

**输出**:
```
✅ 已生成 5 个YAML格式测试用例：
   - TC_TKF001_001_离线剧本批量生成_正常流程.yaml
   - TC_TKF001_002_离线剧本批量生成_断点续传.yaml
   - TC_TKF001_003_离线剧本批量生成_失败重试.yaml
   - TC_TKF001_004_离线剧本批量生成_处理中补偿.yaml
   - TC_TKF001_005_离线剧本批量生成_DP数据未产出.yaml

✅ 已生成 1 个MD格式总览文件：
   - TKF001_测试用例集总览.md

📊 覆盖率统计：
   - 业务场景：5个（100%）
   - 业务规则：3个（100%）
   - 核心组件：3个（100%）
```

---

## 🔗 相关文档

- **详细规范**: `ai_test_framework/docs/AI测试用例生成规范.md`
- **YAML格式规范**: `ai_test_framework/docs/YAML格式测试用例生成规范.md`
- **参考示例**: `ai_test_framework/graph_feature/TC_TKI001_图数据源保存接口测试.yaml`（已验证）、`ai_test_framework/test_cases/TC_TKF001_*.yaml`
- **总览示例**: `ai_test_framework/test_cases/TKF001_测试用例集总览.md`
- **知识映射配置**: `ai_test_framework/config/knowledge_mapping.yaml`

---

**版本**: v1.1
**日期**: 2026-02-28
**用途**: AI快速参考

