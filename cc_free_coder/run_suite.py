#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
运行测试套件（支持包含多个测试用例的YAML文件）

用法:
    python run_suite.py <测试套件路径>

示例:
    python run_suite.py ai_test_framework/graph_feature/TC_TKI001_图数据源保存接口测试.yaml
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime
import yaml

# 添加项目路径到sys.path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from ai_test_framework.framework.executor import AITestExecutor
from ai_test_framework.primitives.primitives_config import register_all_primitives


def parse_suite_yaml(yaml_content):
    """
    解析测试套件YAML文件

    Returns:
        tuple: (suite_config, test_cases)
    """
    documents = list(yaml.safe_load_all(yaml_content))

    if len(documents) < 2:
        raise ValueError("测试套件文件至少应包含套件配置和一个测试用例")

    # 第一个文档是套件配置（front matter）
    suite_config = documents[0]

    # 剩余文档是测试用例
    test_cases = documents[1:]

    return suite_config, test_cases


def merge_config(test_case, suite_config):
    """
    将套件级配置合并到测试用例中

    Args:
        test_case: 测试用例字典
        suite_config: 套件配置字典

    Returns:
        dict: 合并后的测试用例
    """
    # 复制测试用例，避免修改原始数据
    merged = test_case.copy()

    # 合并 owner_config
    if 'owner_config' in suite_config and 'owner_config' not in merged:
        merged['owner_config'] = suite_config['owner_config']

    # 合并 graph_config
    if 'graph_config' in suite_config and 'graph_config' not in merged:
        merged['graph_config'] = suite_config['graph_config']

    # 添加套件信息
    merged['test_suite_id'] = suite_config.get('test_suite_id', 'N/A')
    merged['test_suite_name'] = suite_config.get('test_suite_name', 'N/A')
    merged['business_module'] = suite_config.get('business_module', 'N/A')

    return merged


def execute_test_case_with_config(executor, test_case, suite_config, index, total):
    """
    执行单个测试用例

    Args:
        executor: 测试执行器
        test_case: 测试用例字典
        suite_config: 套件配置
        index: 当前索引
        total: 总数

    Returns:
        dict: 测试结果
    """
    print(f"\n{'='*70}")
    print(f"[{index}/{total}] 执行测试用例")
    print(f"{'='*70}")

    # 合并配置
    merged_test_case = merge_config(test_case, suite_config)

    # 转换回YAML格式
    test_case_yaml = yaml.dump(merged_test_case, allow_unicode=True)

    # 执行测试
    try:
        result = executor.execute_test_case(test_case_yaml)

        return {
            'test_case_id': result.test_case_id,
            'test_name': result.test_name,
            'status': result.status,
            'execution_time': result.execution_time,
            'assertions': executor.execution_details.get('assertions', [])
        }
    except Exception as e:
        print(f"❌ 执行失败: {e}")
        import traceback
        traceback.print_exc()

        return {
            'test_case_id': test_case.get('test_case_id', 'UNKNOWN'),
            'test_name': test_case.get('test_name', 'UNKNOWN'),
            'status': 'FAIL',
            'execution_time': 0,
            'assertions': [],
            'error': str(e)
        }


def main():
    """主函数"""
    # 解析命令行参数
    parser = argparse.ArgumentParser(
        description='运行测试套件（支持包含多个测试用例的YAML文件）',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python run_suite.py ai_test_framework/graph_feature/TC_TKI001_图数据源保存接口测试.yaml
        """
    )
    parser.add_argument(
        'suite_path',
        type=str,
        help='测试套件文件路径（相对于run_suite.py所在目录）'
    )
    parser.add_argument(
        '--case',
        type=str,
        default=None,
        help='指定执行的测试用例ID（如 TC_TKI001_001）'
    )

    args = parser.parse_args()

    # 注册所有原语
    register_all_primitives()

    # 获取路径
    suite_path = project_root / args.suite_path

    # 检查文件是否存在
    if not suite_path.exists():
        print(f"\n❌ 错误: 文件不存在: {args.suite_path}")
        print(f"   完整路径: {suite_path}")
        sys.exit(1)

    if not suite_path.is_file():
        print(f"\n❌ 错误: 路径不是文件: {args.suite_path}")
        sys.exit(1)

    print("="*70)
    print("  🧪 AI测试框架 - 运行测试套件")
    print("="*70)

    # 读取并解析测试套件
    print(f"\n📁 读取测试套件: {suite_path.name}")

    with open(suite_path, 'r', encoding='utf-8') as f:
        yaml_content = f.read()

    suite_config, test_cases = parse_suite_yaml(yaml_content)

    # 过滤指定用例
    if args.case:
        test_cases = [tc for tc in test_cases if tc.get('test_case_id') == args.case]
        if not test_cases:
            print(f"\n❌ 错误: 未找到用例 {args.case}")
            sys.exit(1)

    print(f"📋 套件ID: {suite_config.get('test_suite_id', 'N/A')}")
    print(f"📝 套件名称: {suite_config.get('test_suite_name', 'N/A')}")
    print(f"📦 业务模块: {suite_config.get('business_module', 'N/A')}")
    print(f"📊 测试用例数量: {len(test_cases)}")

    # 初始化执行器
    print("\n🔧 初始化测试执行器...")
    executor = AITestExecutor()

    # 执行所有测试用例
    results = []
    start_time = datetime.now()

    print("\n" + "="*70)
    print("开始执行测试用例...")
    print("="*70)

    for i, test_case in enumerate(test_cases, 1):
        result = execute_test_case_with_config(
            executor,
            test_case,
            suite_config,
            i,
            len(test_cases)
        )
        results.append(result)

    end_time = datetime.now()
    total_time = (end_time - start_time).total_seconds()

    # 打印汇总结果
    total_tests = len(results)
    passed_tests = sum(1 for r in results if r['status'] == 'PASS')
    failed_tests = total_tests - passed_tests
    pass_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0

    print("\n" + "="*70)
    print("📊 测试套件执行结果")
    print("="*70)
    print(f"套件ID: {suite_config.get('test_suite_id', 'N/A')}")
    print(f"套件名称: {suite_config.get('test_suite_name', 'N/A')}")
    print(f"总用例数: {total_tests}")
    print(f"✅ 通过: {passed_tests}")
    print(f"❌ 失败: {failed_tests}")
    print(f"📈 通过率: {pass_rate:.1f}%")
    print(f"⏱️  总耗时: {total_time:.2f}秒")
    print("="*70)

    # 列出所有测试用例结果
    print("\n📋 测试用例详情:")
    for result in results:
        status_icon = "✅" if result['status'] == 'PASS' else "❌"
        print(f"  {status_icon} [{result['test_case_id']}] {result['test_name']}")
        print(f"      执行时间: {result['execution_time']:.2f}秒")

        # 统计断言
        assertions = result.get('assertions', [])
        if assertions:
            passed_assertions = sum(1 for a in assertions if a.get('status') == 'PASS')
            total_assertions = len(assertions)
            print(f"      断言: {passed_assertions}/{total_assertions} 通过")

        if result['status'] == 'FAIL' and 'error' in result:
            print(f"      错误: {result['error']}")

    # 列出失败的用例
    if failed_tests > 0:
        print("\n❌ 失败的测试用例:")
        for result in results:
            if result['status'] == 'FAIL':
                print(f"  - {result['test_case_id']}: {result['test_name']}")

    print("\n" + "="*70)


if __name__ == '__main__':
    main()
