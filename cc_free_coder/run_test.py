#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 测试框架执行入口

功能：
1. 加载 YAML 测试用例
2. 使用 AITestExecutor 执行测试
3. 生成 HTML 测试报告

使用方法：
    python run_test.py test_cases/TC_TKF001_001_JDBC批量新增入仓任务_全链路成功场景.yaml
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))
#修改前 from ai_test_framework.framwork.executor import AITestExecutor
# 修改导入
from ai_test_framework.framwork.executor import AITestExecutor

# 修改 sys.path 指向顶层
project_root = Path(__file__).resolve().parent.parent.parent # 指向 cc_free_coder
sys.path.insert(0, str(project_root))

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("=" * 70)
        print("AI 测试框架 - 执行器")
        print("=" * 70)
        print("\n用法:")
        print("  python run_test.py <yaml_file>")
        print("\n示例:")
        print("  python run_test.py test_cases/TC_TKF001_001_JDBC批量新增入仓任务_全链路成功场景.yaml")
        print("\n可用测试用例:")

        # 列出所有测试用例
        test_cases_dir = project_root / "ai_test_framework" / "test_cases"
        if test_cases_dir.exists():
            yaml_files = list(test_cases_dir.glob("*.yaml"))
            for i, yaml_file in enumerate(yaml_files, 1):
                print(f"  {i}. {yaml_file.name}")

        print("=" * 70)
        sys.exit(1)

    yaml_file = sys.argv[1]

    # 如果是相对路径，转换为绝对路径
    if not os.path.isabs(yaml_file):
        # 先尝试在当前目录查找
        if os.path.exists(yaml_file):
            yaml_file = os.path.abspath(yaml_file)
        else:
            # 再尝试在 test_cases 目录查找
            test_cases_path = project_root / "ai_test_framework" / "test_cases" / yaml_file
            if test_cases_path.exists():
                yaml_file = str(test_cases_path)
            else:
                print(f"❌ 测试用例文件不存在: {yaml_file}")
                sys.exit(1)

    if not os.path.exists(yaml_file):
        print(f"❌ 测试用例文件不存在: {yaml_file}")
        sys.exit(1)

    print("\n" + "=" * 70)
    print("🚀 AI 测试框架 - 开始执行")
    print("=" * 70)
    print(f"📄 测试用例: {os.path.basename(yaml_file)}")
    print(f"📂 文件路径: {yaml_file}")
    print("=" * 70 + "\n")

    # 读取 YAML 文件
    with open(yaml_file, 'r', encoding='utf-8') as f:
        test_case_yaml = f.read()

    # 创建执行器（启用 HTML 报告）
    executor = AITestExecutor(
        llm_client=None,  # 不使用 LLM 意图解析
        knowledge_base=None,
        enable_html_report=True
    )

    try:
        # 执行测试用例
        result = executor.execute_test_case(test_case_yaml)

        # 打印最终结果
        print("\n" + "=" * 70)
        if result.status == 'PASS':
            print("✅ 测试执行成功！")
        else:
            print("❌ 测试执行失败！")
        print("=" * 70)

        # 返回退出码
        sys.exit(0 if result.status == 'PASS' else 1)

    except Exception as e:
        print("\n" + "=" * 70)
        print(f"❌ 测试执行异常: {str(e)}")
        print("=" * 70)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
