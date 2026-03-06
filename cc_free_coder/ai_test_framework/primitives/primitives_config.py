"""原语配置 - 注册所有原语

此文件负责导入和注册所有原语到注册表。

三层原语架构：
1. 通用原语层 (Generic Primitives) - 高度抽象，跨业务复用
2. 业务原语层 (Business Primitives) - 针对特定业务，封装业务逻辑
3. 基础设施层 (Infrastructure) - 数据库连接、HTTP客户端等
"""
from .primitive_registry import primitive_registry
# 1. 导入 Skill 桥接原语 (Generic 层)
from .generic.skill_bridge import SkillBridgePrimitive

# 2. 导入 JDBC 业务 API 原语 (Business 层)
# 假设你在 api.py 里的类名分别是这些
from .business.dataops.api import (
    BatchUploadValidatePrimitive,
    QueryBatchResultPrimitive,
    SubmitBatchTaskPrimitive,
    CancelBatchTaskPrimitive
)

# ========== 导入通用原语 (Generic Primitives) ==========
# 通用原语：高度抽象，参数灵活，跨业务复用

# Job操作原语
from .generic.job import (
    TriggerScheduledJobPrimitive
)
# 注意：WaitForJobCompletePrimitive 已删除
# 原因：不同Job的执行完成判断逻辑高度业务化，无法通用化
# 建议：在业务原语中实现特定Job的等待逻辑，或使用数据库断言原语验证执行结果

# 注意：AssertJobTriggeredPrimitive 已删除
# 原因1：逻辑错误 - 检查status in ['RUNNING', 'SUCCESS']，但trigger_scheduled_job设置status='TRIGGERED'
# 原因2：功能重复 - trigger_scheduled_job已经返回SUCCESS/FAIL状态，无需额外断言
# 原因3：语义混淆 - "Job触发成功"只表示"提交到调度平台成功"，不表示"Job执行成功"

# 断言原语
from .generic.assertion import (
    AssertEqualsPrimitive,
    AssertBusinessRulePrimitive
)

# 数据库断言原语
from .generic.database_assertion import (
    AssertFieldEqualsPrimitive,
    AssertRecordCountPrimitive,
    AssertAllRecordsMatchPrimitive,
    AssertAllJsonFieldsNotNullPrimitive,
    AssertAllFieldsNotNullPrimitive
)

# 数据库操作原语
from .generic.database import (
    DatabaseInsertPrimitive
)

# Skill 桥接原语
from .generic.skill_bridge import (
    SkillBridgePrimitive
)
# JDBC入仓数据断言原语
from .generic.database_assertion import (
    AssertDatabaseRecordPrimitive
)
# ========== 导入业务原语 (Business Primitives) ==========
# 业务原语：针对特定业务，封装业务逻辑，不追求通用性

# DataHub业务原语
from .business.datahub.data_preparation import (
    PrepareDatahubDataPrimitive,
    CleanTestDataPrimitive
)


# 注意：PrepareDataPrimitive 和 CleanupDataPrimitive 已删除
# 原因：这两个是空壳原语，没有实际功能，只返回成功状态
# 建议：直接使用 prepare_datahub_data 和 clean_test_data


# 注意：Mock原语已删除
# 公司有独立的Mock平台并提供API，测试时直接调用Mock平台API即可
# 如需Mock原语，可在business/目录下创建mock_platform.py封装Mock平台API调用


def register_all_primitives():
    """注册所有原语到注册表

    按照三层原语架构注册：
    1. 通用原语 - 高复用性，参数灵活
    2. 业务原语 - 业务特定，封装复杂逻辑
    """

    # ========== 注册通用原语 (Generic Primitives) ==========

    # Job操作原语
    primitive_registry.register(TriggerScheduledJobPrimitive)

    # 断言原语
    primitive_registry.register(AssertEqualsPrimitive)
    primitive_registry.register(AssertBusinessRulePrimitive)

    # 数据库断言原语
    primitive_registry.register(AssertFieldEqualsPrimitive)
    primitive_registry.register(AssertRecordCountPrimitive)
    primitive_registry.register(AssertAllRecordsMatchPrimitive)
    primitive_registry.register(AssertAllJsonFieldsNotNullPrimitive)
    primitive_registry.register(AssertAllFieldsNotNullPrimitive)

    # 数据库操作原语
    primitive_registry.register(DatabaseInsertPrimitive)


    # ========== 注册业务原语 (Business Primitives) ==========

    # DataHub业务原语
    primitive_registry.register(PrepareDatahubDataPrimitive)
    primitive_registry.register(CleanTestDataPrimitive)

    # --- 注册：Skill 桥接器 ---
    # 注册后，Registry 里的名字就是 'skill_bridge'
    primitive_registry.register(SkillBridgePrimitive)

    # --- 注册：JDBC 业务 API ---
    # 注册后，Registry 里的名字将是 TKI_003, TKI_004 等（取决于你 api.py 里的 metadata.name）
    primitive_registry.register(BatchUploadValidatePrimitive)
    primitive_registry.register(QueryBatchResultPrimitive)
    primitive_registry.register(SubmitBatchTaskPrimitive)
    primitive_registry.register(CancelBatchTaskPrimitive)

    # -- 注册：JDBC数据库断言 --
    primitive_registry.register(AssertDatabaseRecordPrimitive)

    print(f"✅ 已注册 {len(primitive_registry.list_all())} 个原语（通用原语 + 业务原语）")


# 自动注册
register_all_primitives()
