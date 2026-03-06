# YAML格式测试用例生成规范

## 📋 概述

本规范用于指导AI基于**MD格式测试用例集 + 知识库**生成YAML格式的可执行测试用例。YAML格式用例是测试用例的**第二层**，主要用于**自动化执行**，强调技术准确性和可执行性。

**核心原则**:
- ✅ 基于MD用例集 + 知识库生成
- ✅ 包含完整的技术实现细节
- ✅ 使用原语调用，可直接执行
- ✅ 包含详细的注释说明

---

## 🎯 设计理念

### 为什么使用YAML格式？

1. **可执行性**: 测试框架可以直接解析和执行
2. **结构化**: 清晰的层次结构，易于解析
3. **技术完整**: 包含所有技术实现细节（原语、参数、断言）
4. **可追溯**: 关联知识库，便于维护和更新

### YAML文件组织模式

YAML测试用例支持两种组织模式：

| 维度 | 单文档模式 | 多文档套件模式 |
|------|-----------|---------------|
| **适用场景** | 流程测试（单个场景） | 接口测试（多个场景） |
| **文件结构** | 一个YAML文件 = 一个用例 | 一个YAML文件 = 多个用例（用 `---` 分隔） |
| **执行方式** | `python run_test.py <file>` | `python run_suite.py <file>` |
| **命名规范** | `TC_TKF001_001_xxx.yaml` | `TC_TKI001_图数据源保存接口测试.yaml` |
| **典型场景** | 端到端流程、多步骤 Job | 单接口正/反例覆盖 |

### YAML格式 vs MD格式

| 维度 | YAML格式（执行层） | MD格式（业务层） |
|------|-------------------|----------------|
| **目标用户** | 测试框架 | 业务人员、产品经理 |
| **内容** | 技术实现、原语调用 | 业务逻辑、测试目的 |
| **长度** | 不限（通常100-300行） | 100-150行 |
| **可读性** | ⭐⭐ 一般 | ⭐⭐⭐⭐⭐ 非常好 |
| **用途** | 自动化执行 | 评审、沟通 |

---

## 📝 文件结构规范

### 文件命名

**单文档模式**: `TC_<业务流程ID>_<序号>_<用例名称>.yaml`

**示例**:
- `TC_TKF001_001_离线剧本批量生成_正常流程.yaml`
- `TC_TKF001_002_离线剧本批量生成_断点续传.yaml`

**多文档套件模式**: `TC_<组件ID>_<组件名称>.yaml`

**示例**:
- `TC_TKI001_图数据源保存接口测试.yaml`（内含7个用例，用 `---` 分隔）

### 文件组织

**单文档模式**: 一个MD用例 = 一个YAML文件

- ✅ 适合流程测试、端到端测试
- ✅ 文件名包含业务流程ID、序号、用例名称
- ✅ 存放在 `ai_test_framework/test_cases/` 目录

**多文档套件模式**: 一个接口/组件 = 一个YAML文件（包含正例+反例）

- ✅ 适合接口测试（同一接口的多个测试场景）
- ✅ 第一个文档为套件元数据（front matter），后续文档为测试用例
- ✅ 用例间用 `---` 分隔
- ✅ 存放在 `ai_test_framework/graph_feature/` 或对应业务目录

---

## 📄 YAML用例文件结构

### 模式1：单文档模式（流程测试）

```yaml
# ============================================================================
# 测试用例：<用例名称>
# ============================================================================
# 知识来源: <关联的知识文档>
# 生成方式: AI基于Test Knowledge Tree自动生成
# 生成时间: YYYY-MM-DD
# ============================================================================

test_case_id: <用例ID>
test_name: <用例名称>
business_flow: <业务流程ID>
business_rules:
  - <业务规则ID>  # 规则名称注释

# 变量配置
owner_config:
  owner_id: <负责人ID>
  owner_name: <负责人姓名>
  owner_org_id: <负责组ID>
  owner_org_name: <负责组名称>

# 关联的知识文档
related_knowledge:
  flows:
    - <业务流程知识>
  rules:
    - <业务规则知识>
  data_components:
    - <数据组件知识>
  job_components:
    - <Job组件知识>
  integration_components:
    - <集成组件知识>

# 测试意图
test_intent:
  preconditions:
    - intent: "<前置条件说明>"
      primitive: <原语名称>
      params:
        <参数名>: <参数值>

  test_steps:
    - intent: "<步骤说明>"
      primitive: <原语名称>
      params:
        <参数名>: <参数值>

      assertions:
        - intent: "<断言说明>"
          primitive: <断言原语名称>
          params:
            <参数名>: <参数值>

expected_result:
  description: |
    <预期结果描述>
```

### 模式2：多文档套件模式（接口测试）

**适用场景**: 同一接口的正例/反例测试，一个文件包含多个用例。

**关键规则**:
- ✅ 第一个文档为 **套件元数据**（front matter），包含 `test_suite_id`、`owner_config`、`graph_config` 等公共配置
- ✅ 后续每个文档为一个独立的 **测试用例**，用 `---` 分隔
- ✅ 测试用例中通过 `${变量名}` 引用 front matter 中定义的变量
- ✅ **每个用例必须包含 `business_rules` 字段**，关联该用例覆盖的业务规则
- ✅ 使用 `run_suite.py` 执行，支持 `--case` 参数指定单条用例

```yaml
---
# ============================================================================
# 套件元数据（front matter）— 公共配置，所有用例共享
# ============================================================================
test_suite_id: TC_TKI001
test_suite_name: "图数据源保存接口测试"
business_module: "特征平台-图特征管理"
related_component: TKI_001
version: v1.0
created_date: 2026-02-24

# 接口负责人配置（所有用例通过 ${owner_id} 等变量引用）
owner_config:
  owner_id: "71a5325d-f0e6-45e0-acdc-f317b81a3283"
  owner_name: "张雯"
  owner_org_id: "9fb7afdf-8444-4cdb-bd41-19ada5d8d246"
  owner_org_name: "风险中台测试组"

# 图空间配置（通过 ${graph_code} 引用）
graph_config:
  graph_code: "risk"
---

# ========================================
# 测试用例1: 正常创建图数据源（正例）
# ========================================
test_case_id: TC_TKI001_001
test_name: "正常创建图数据源_成功"
test_priority: P0
test_type: SIT0+
business_flow: TKF_001
business_rules:              # 必填：关联的业务规则
  - TKR_001                  # 图数据源编码命名规则
  - TKR_005                  # 数据源类型校验规则

test_intent:
  preconditions:
    - intent: "清理测试数据"
      primitive: clean_test_data
      params:
        tables:
          - "featurestore.source_graph"
          - "featurestore.source_basic_info"
        where: "source_code = 'ds.grt.graph.risk'"  # 精确匹配清理条件

  test_steps:
    - intent: "创建图数据源"
      primitive: create_graph_source
      params:
        sourceCode: "ds.grt.graph.risk"
        sourceName: "测试风控关系图数据源"
        sourceType: "GRAPH"
        graphCode: "${graph_code}"
        sourceOwnerId: "${owner_id}"
        sourceOwner: "${owner_name}"
        sourceOwnerOrgId: "${owner_org_id}"
        sourceOwnerOrg: "${owner_org_name}"

      assertions:
        - intent: "验证接口返回成功"
          primitive: assert_equals
          params:
            actual: "${response.code}"
            expected: 10000

        - intent: "验证数据源基本信息已保存"
          primitive: assert_database_record
          params:
            table: "featurestore.source_basic_info"
            where: "source_code='${context.sourceCode}'"
            wait: 3                        # 等待数据落库
            assertions:
              - field: "source_type"
                expected: "GRAPH"
              - field: "source_state"
                expected: "INIT"

---

# ========================================
# 测试用例2: sourceCode格式错误（反例）
# ========================================
test_case_id: TC_TKI001_002
test_name: "sourceCode格式错误_返回错误"
test_priority: P1
test_type: SIT1-
business_flow: TKF_001
business_rules:
  - TKR_001                  # 图数据源编码命名规则

test_intent:
  test_steps:
    - intent: "使用错误格式的sourceCode创建数据源"
      primitive: create_graph_source
      params:
        sourceCode: "invalid_format_${timestamp()}"  # 故意使用错误格式
        # ... 其他参数

      assertions:
        - intent: "验证接口返回格式错误"
          primitive: assert_equals
          params:
            actual: "${response.code}"
            expected: 20001
```

**执行方式**:
```bash
# 执行整个套件（所有用例）
python run_suite.py ai_test_framework/graph_feature/TC_TKI001_图数据源保存接口测试.yaml

# 执行单条用例
python run_suite.py ai_test_framework/graph_feature/TC_TKI001_图数据源保存接口测试.yaml --case TC_TKI001_001
```

---

## 📐 各部分生成规范

### 1. 文件头部注释

**要求**:
- ✅ 包含用例名称
- ✅ 标注知识来源（关联的知识文档）
- ✅ 标注生成方式和时间
- ✅ 使用分隔线美化

**示例**:
```yaml
# ============================================================================
# 测试用例：离线剧本批量生成 - 正常流程（首次执行）
# ============================================================================
# 知识来源: TKF_001_离线剧本批量生成.md
# 生成方式: AI基于Test Knowledge Tree自动生成
# 生成时间: 2026-02-10
# ============================================================================
```

---

### 2. 基本信息

**要求**:
- ✅ test_case_id: 唯一标识，格式 `TC_<业务流程ID>_<序号>`
- ✅ test_name: 用例名称，格式 `<业务流程>_<场景>_<特征>`
- ✅ business_flow: 业务流程ID
- ✅ **business_rules: 关联的业务规则列表（必填，带注释）**
- ✅ test_priority: 测试优先级（P0/P1/P2/P3）
- ✅ test_type: 测试类型标签（如 SIT0+、SIT1-）

**示例**:
```yaml
test_case_id: TC_TKI001_001
test_name: "正常创建图数据源_成功"
test_priority: P0
test_type: SIT0+
business_flow: TKF_001
business_rules:
  - TKR_001  # 图数据源编码命名规则
  - TKR_005  # 数据源类型校验规则
```

**business_rules 规则**:
- ❌ 不��省略 business_rules 字段（会导致测试报告中业务规则覆盖为空）
- ✅ 每个用例只关联与该用例测试场景直接相关的规则
- ✅ 规则ID必须在 `knowledge_mapping.yaml` 中有对应的名称映射

---

### 3. 变量配置（通用配置）

**生成规则**:
- ✅ **所有测试用例必须包含 owner_config 配置段**
- ✅ owner_config 包含：owner_id、owner_name、owner_org_id、owner_org_name
- ✅ 具体配置值参考：`测试用例变量使用规范.md`
- ✅ 特殊配置（如图特征测试的 graph_config）根据具体业务需求添加

**多文档套件模式注意**: owner_config 和 graph_config 定义在 front matter 中，所有用例共享。

**变量引用**:
- 测试步骤中通过 `${变量名}` 引用配置的变量
- owner_config 变量：`${owner_id}`、`${owner_name}`、`${owner_org_id}`、`${owner_org_name}`

**使用示例**:
```yaml
# 配置段（文件头部或 front matter）
owner_config:
  owner_id: "71a5325d-f0e6-45e0-acdc-f317b81a3283"
  owner_name: "张雯"
  owner_org_id: "9fb7afdf-8444-4cdb-bd41-19ada5d8d246"
  owner_org_name: "风险中台测试组"

# 测试步骤中引用变量
test_steps:
  - intent: "创建数据源"
    primitive: create_source
    params:
      sourceOwnerId: "${owner_id}"        # 引用owner_config
      sourceOwner: "${owner_name}"
      sourceOwnerOrgId: "${owner_org_id}"
      sourceOwnerOrg: "${owner_org_name}"
```

**注意事项**:
- ❌ 不要在测试步骤中硬编码负责人信息
- ✅ 统一在文件头部的配置段中定义，测试步骤中使用变量引用
- ✅ 生成测试用例时，如果文件中没有 owner_config 配置段，则必须新增

---

### 4. 关联知识文档

**要求**:
- ✅ 列出所有关联的知识文档
- ✅ 分类：flows、rules、data_components、job_components、integration_components
- ✅ 使用知识文档的完整ID

**示例**:
```yaml
related_knowledge:
  flows:
    - TKF_001_图数据源创建和上线
  rules:
    - TKR_001_图数据源编码命名规则
    - TKR_005_数据源类型校验规则
  data_components:
    - TKD_001_剧本推荐日志表
    - TKD_002_剧本推荐表
  job_components:
    - TKJ_001_AiScriptUidPullJob
  integration_components:
    - TKI_001_图数据源保存接口
```

---

### 5. 前置条件 (preconditions)

**要求**:
- ✅ 每个前置条件包含：intent（意图说明）、primitive（原语名称）、params（参数）
- ✅ intent使用业务语言描述目的
- ✅ 添加注释说明知识来源和业务逻辑
- ✅ 按照执行顺序排列（先清理数据，再准备数据）

**数据清理规范**:
- ✅ **使用精确 WHERE 条件**，而非模糊匹配 pattern
- ✅ 清理条件必须与测试步骤中使用的数据完全对应
- ❌ 避免使用 `pattern: "test%"` 这样的模糊匹配（可能清理不到目标数据）

**示例**:
```yaml
preconditions:
  # 前置1: 清空历史数据（精确匹配清理）
  - intent: "清理测试数据"
    primitive: clean_test_data
    params:
      tables:
        - "featurestore.source_graph"
        - "featurestore.source_basic_info"
      where: "source_code = 'ds.grt.graph.risk'"  # 精确 WHERE 条件
```

**错误示例**:
```yaml
# ❌ 错误：模糊匹配可能无法清理到 ds.grt.graph.risk
params:
  tables:
    - "featurestore.source_basic_info"
  pattern: "test%"

# ✅ 正确：精确指定 WHERE 条件
params:
  tables:
    - "featurestore.source_basic_info"
  where: "source_code = 'ds.grt.graph.risk'"
```

---

### 6. 测试步骤 (test_steps)

**要求**:
- ✅ 每个步骤包含：intent、primitive、params、assertions
- ✅ intent描述步骤的业务目的
- ✅ 添加详细的注释说明（知识来源、业务逻辑、数据链路）
- ✅ assertions包含该步骤的所有断言

**示例**:
```yaml
test_steps:
  # ===== 步骤1: 创建图数据源并验证 =====
  - intent: "创建图数据源"
    primitive: create_graph_source
    params:
      sourceCode: "ds.grt.graph.risk"       # 编码规则: ds.grt.graph.{graphCode}
      sourceName: "测试风控关系图数据源"
      sourceType: "GRAPH"
      graphCode: "${graph_code}"             # 引用 graph_config 变量
      sourceOwnerId: "${owner_id}"
      sourceOwner: "${owner_name}"
      sourceOwnerOrgId: "${owner_org_id}"
      sourceOwnerOrg: "${owner_org_name}"

    assertions:
      - intent: "验证接口返回成功"
        primitive: assert_equals
        params:
          actual: "${response.code}"
          expected: 10000

      - intent: "验证数据源基本信息已保存"
        primitive: assert_database_record
        params:
          table: "featurestore.source_basic_info"
          where: "source_code='${context.sourceCode}'"
          wait: 3                            # 等待数据落库
          assertions:
            - field: "source_type"
              expected: "GRAPH"
            - field: "source_state"
              expected: "INIT"
```

---

### 7. 断言 (assertions)

**要求**:
- ✅ 每个断言包含：intent、primitive、params
- ✅ intent描述断言的验证目的
- ✅ 使用合适的断言原语
- ✅ 数据库断言添加 `wait` 参数（数据落库等待）
- ✅ 异步操作断言添加 `timeout` 和 `poll_interval` 参数
- ✅ 只验证实际存在的数据库字段（先查表结构确认）

**常用断言原语**:
- `assert_equals`: 验证值相等（接口返回码等）
- `assert_not_null`: 验证值非空
- `assert_not_equal`: 验证值不等（反例验证）
- `assert_database_record`: 验证数据库记录多个字段值（支持 `wait` 参数）
- `assert_record_exists`: 验证记录存在
- `assert_record_count`: 验证记录数量
- `assert_field_equals`: 验证单个字段值（支持 `timeout` + `poll_interval` 超时轮询）
- `assert_all_records_match`: 验证所有记录的字段值都匹配
- `assert_all_json_fields_not_null`: 验证JSON字段非空

**数据库断言关键参数**:
```yaml
# assert_database_record 支持 wait 参数（等待数据落库）
- primitive: assert_database_record
  params:
    table: "featurestore.source_basic_info"
    where: "source_code='${context.sourceCode}'"
    wait: 3                     # 等待3秒后再查询（默认3秒）
    assertions:
      - field: "source_type"    # 字段必须在表中实际存在
        expected: "GRAPH"

# assert_field_equals 支持超时轮询（异步Job验证）
- primitive: assert_field_equals
  params:
    table: "copilot.common_job_status"
    field: "status"
    expected: "SUCCESS"
    timeout: 30                 # 最大等待30秒
    poll_interval: 2            # 每2秒轮询一次
```

**断言字段验证规则**:
- ❌ 不要断言表中不存在的字段（如断言了已删除的 `register_type` 字段会导致断言失败）
- ✅ 生成断言前先确认表结构中实际存在哪些字段
- ✅ 使用 `${context.xxx}` 引用前步骤保存的上下文变量

---

### 8. 预期结果 (expected_result)

**要求**:
- ✅ 使用description字段描述整体预期结果
- ✅ 使用多行字符串（|）格式
- ✅ 列出所有关键验证点
- ✅ 使用业务语言描述

**示例**:
```yaml
expected_result:
  description: |
    1. 接口返回成功，code=10000
    2. 数据源编码正确返回
    3. source_basic_info 表记录状态为 INIT
    4. source_graph 表关联记录已创建
```

---

## 🔧 参数使用规范

### 1. 变量引用

**格式**: `${context.变量名}`

**用途**: 引用前面步骤保存到上下文中的变量

**示例**:
```yaml
params:
  sourceCode: "${context.sourceCode}"   # 引用 create_graph_source 保存的编码
  groupCode: "${context.groupCode}"     # 引用 save_graph_group 保存的编码
```

---

### 2. 函数调用

**格式**: `${函数名()}`

**常用函数**:
- `${uuid()}`: 生成UUID
- `${batch_no()}`: 生成批次号（yyyyMMdd001格式）
- `${serial_id()}`: 生成序列ID
- `${timestamp()}`: 生成时间戳（格式: YYYYMMDDHHmmss）

**示例**:
```yaml
params:
  uid: "${uuid()}"              # 自动生成UUID
  batch_no: "${batch_no()}"     # 自动生成批次号
  bizSerial: "${serial_id()}"   # 自动生成流水号
```

---

### 3. 字符串拼接

**格式**: `"前缀_${变量}_后缀"`

**示例**:
```yaml
params:
  sourceCode: "ds.grt.graph.${graph_code}"  # 拼接图空间编码
```

---

## 📝 注释规范

### 1. 用例分隔注释（多文档套件模式必需）

```yaml
# ========================================
# 测试用例1: 正常创建图数据源（正例）
# ========================================
```

### 2. 逻辑块分隔注释

```yaml
# ========== 前置条件（准备测试数据） ==========
# ===== 步骤1: 创建图数据源并验证 =====
```

### 3. 说明注释

**用途**: 解释业务逻辑、数据链路、注意事项

**格式**:
```yaml
# 前置1: 清空历史数据（知识来源: TKD_001, TKD_002）
# 说明: 必须按照从下游到上游的顺序清理，避免外键约束错误

# 数据链路: result_df → common_job_status (batch_no + source)
#          base_df → recommendation_log (queue + ai_execute_code + source)

# 字段映射: common_job_status.business_type = 其他表.source
```

### 4. 行内注释

**用途**: 解释参数含义

**格式**:
```yaml
params:
  sourceCode: "ds.grt.graph.risk"   # 编码规则: ds.grt.graph.{graphCode}
  wait: 3                           # 等待数据落库
  graphCode: "invalid_graph"        # 故意使用不存在的图空间
  timeout: 30  # 最大等待30秒
  poll_interval: 2  # 每2秒查询一次
  batch_status: "1"  # DP数据已产出
```

---

## ✅ 生成检查清单

### 结构检查

- [ ] 文件头部包含完整注释（用例名称、知识来源、生成方式、生成时间）
- [ ] 包含基本信息（test_case_id、test_name、business_flow、**business_rules**）
- [ ] 包含通用变量配置（owner_config）
- [ ] 多文档套件模式：front matter 包含 test_suite_id、owner_config、graph_config
- [ ] 包含test_intent（preconditions、test_steps）
- [ ] 包含expected_result（单文档模式）

### 内容检查

- [ ] owner_config 包含完整的四个字段（owner_id、owner_name、owner_org_id、owner_org_name）
- [ ] **每个用例都有 business_rules 字段且非空**
- [ ] **business_rules 中的规则ID在 knowledge_mapping.yaml 中有映射**
- [ ] 每个前置条件包含intent、primitive、params
- [ ] 每个测试步骤包含intent、primitive、params、assertions
- [ ] 每个断言包含intent、primitive、params
- [ ] 数据库断言包含 `wait` 参数
- [ ] 异步操作的断言包含 `timeout` 和 `poll_interval` 参数
- [ ] 所有原语名称正确（参考原语文档）

### 数据清理检查

- [ ] **clean_test_data 使用 `where` 参数精确匹配**（而非 `pattern` 模糊匹配）
- [ ] 清理条件与测试步骤中使用的数据完全对应
- [ ] 前置条件按执行顺序排列（先清理数据，再准备数据）

### 断言字段检查

- [ ] **断言的字段必须在目标表中实际存在**（避免断言已删除或不存在的字段）
- [ ] 使用 `${context.xxx}` 引用上下文变量，而非硬编码
- [ ] WHERE 条件拼接正确，引号闭合

### 注释检查

- [ ] 前置条件有注释说明知识来源和业务逻辑
- [ ] 测试步骤有注释说明数据链路和字段映射
- [ ] 断言有注释说明验证逻辑
- [ ] 复杂参数有行内注释

### 参数检查

- [ ] owner_config 变量引用格式正确（`${owner_id}`、`${owner_name}`、`${owner_org_id}`、`${owner_org_name}`）
- [ ] 上下文变量引用格式正确（`${context.变量名}`）
- [ ] 函数调用格式正确（`${函数名()}`）
- [ ] 测试步骤中没有硬编码负责人信息

---

## 📚 参考示例

### 已验证通过的示例（推荐参考）

**多文档套件模式**（已端到端验证通过）:
- `ai_test_framework/graph_feature/TC_TKI001_图数据源保存接口测试.yaml`（7个用例，4/4断言通过）

**单文档模式**:
- `ai_test_framework/test_cases/TC_TKF001_001_离线剧本批量生成_正常流程.yaml`
- `ai_test_framework/test_cases/TC_TKF001_002_离线剧本批量生成_断点续传.yaml`
- `ai_test_framework/test_cases/TC_TKF001_003_离线剧本批量生成_失败重试.yaml`

---

## 🔄 生成流程

### 输入

1. **MD格式测试用例集**: 包含业务逻辑和测试目的
2. **知识库**: 包含业务流程、业务规则、数据组件、Job组件等

### 处理步骤

1. **解析MD用例**: 提取测试目的、测试数据、测试步骤、预期结果
2. **查询知识库**: 根据业务流程ID查询相关知识
3. **映射原语**: 将业务步骤映射到具体的原语调用
4. **生成参数**: 根据知识库生成原语参数
5. **生成断言**: 根据预期结果生成断言（确认字段存在性）
6. **添加注释**: 添加知识来源、业务逻辑、数据链路等注释
7. **配置 knowledge_mapping**: 确保 business_rules 中的规则ID在映射文件中有定义

### 输出

- 完整的YAML格式测试用例文件
- 可直接被测试框架执行（`run_test.py` 或 `run_suite.py`）

---

## 💡 最佳实践

### 1. 数据清理用精确条件

```yaml
# ✅ 精确 WHERE 条件
where: "source_code = 'ds.grt.graph.risk'"

# ❌ 模糊匹配可能清理不到目标数据
pattern: "test%"
```

### 2. 数据库断言加等待时间

```yaml
# ✅ API 调用后数据写入数据库有延迟，需等待
- primitive: assert_database_record
  params:
    wait: 3  # 等待3秒后再查
    # ...

# ❌ 不加等待，查询时数据可能还没落库
- primitive: assert_database_record
  params:
    # 没有 wait 参数
```

### 3. 断言只验证存在的字段

```yaml
# ✅ 确认字段存在后再断言
assertions:
  - field: "source_type"
    expected: "GRAPH"
  - field: "source_state"
    expected: "INIT"

# ❌ register_type 字段已从表中移除，断言会失败
assertions:
  - field: "register_type"   # 字段不存在!
    expected: "GRAPH"
```

### 4. 每个用例关联业务规则

```yaml
# ✅ 每个用例明确关联业务规则（报告中会显示覆盖情况）
business_rules:
  - TKR_001  # 图数据源编码命名规则
  - TKR_005  # 数据源类型校验规则

# ❌ 缺少 business_rules 导致报告中业务规则覆盖为空
# business_rules: []  或完全不写
```

### 5. 测试报告 knowledge_mapping 同步

`business_rules` 和 `business_flow` 的ID需要在 `config/knowledge_mapping.yaml` 中有对应的名称映射，否则测试报告中只显示ID不显示名称。

```yaml
# config/knowledge_mapping.yaml
business_flows:
  TKF_001: "图数据源创建和上线"

business_rules:
  TKR_001: "图数据源编码命名规则"
  TKR_005: "数据源类型校验规则"
```

---

## 🚫 常见错误

### 1. 数据清理用模糊匹配导致清理失败

**错误**:
```yaml
# sourceCode 是 'ds.grt.graph.risk'，pattern "test%" 匹配不到
params:
  pattern: "test%"
```

**正确**:
```yaml
# 使用精确 WHERE 条件
params:
  where: "source_code = 'ds.grt.graph.risk'"
```

---

### 2. 缺少 business_rules 导致报告覆盖为空

**错误**:
```yaml
test_case_id: TC_TKI001_001
test_name: "正常创建图数据源_成功"
business_flow: TKF_001
# 没有 business_rules 字段
```

**正确**:
```yaml
test_case_id: TC_TKI001_001
test_name: "正常创建图数据源_成功"
business_flow: TKF_001
business_rules:
  - TKR_001  # 图数据源编码命名规则
  - TKR_005  # 数据源类型校验规则
```

---

### 3. 断言不存在的数据库字段

**错误**:
```yaml
# register_type 字段已从 source_basic_info 表中移除
assertions:
  - field: "register_type"
    expected: "GRAPH"
```

**正确**:
```yaml
# 只断言实际存在的字段
assertions:
  - field: "source_type"
    expected: "GRAPH"
  - field: "source_state"
    expected: "INIT"
```

---

### 4. 数据库查询不等待数据落库

**错误**:
```yaml
# API返回成功后立即查库，数据可能还没写入
- primitive: assert_database_record
  params:
    table: "featurestore.source_basic_info"
    where: "source_code='${context.sourceCode}'"
    assertions:
      - field: "source_type"
        expected: "GRAPH"
```

**正确**:
```yaml
# 添加 wait 参数等待数据落库
- primitive: assert_database_record
  params:
    table: "featurestore.source_basic_info"
    where: "source_code='${context.sourceCode}'"
    wait: 3  # 等待3秒
    assertions:
      - field: "source_type"
        expected: "GRAPH"
```

---

### 5. 缺少超时参数（异步操作）

**错误**:
```yaml
- intent: "验证Job执行成功"
  primitive: assert_field_equals
  params:
    table: "copilot.common_job_status"
    field: "status"
    expected: "SUCCESS"
```

**正确**:
```yaml
- intent: "验证Job执行成功（使用超时轮询）"
  primitive: assert_field_equals
  params:
    table: "copilot.common_job_status"
    field: "status"
    expected: "SUCCESS"
    timeout: 30  # 添加超时参数
    poll_interval: 2  # 添加轮询间隔
```

---

### 6. 硬编码批次号

**错误**:
```yaml
params:
  batch_no: "20260210001"  # 硬编码
```

**正确**:
```yaml
params:
  batch_no: "${context.batch_no}"  # 使用变量引用
  # 或
  batch_no: "${batch_no()}"  # 使用函数生成
```

---

**规范版本**: v2.0
**创建日期**: 2026-02-10
**最后更新**: 2026-02-28
**维护人员**: AI测试团队
