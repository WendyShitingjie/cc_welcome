import requests
import concurrent.futures
import time
import argparse
from statistics import mean, median, stdev
import matplotlib.pyplot as plt

class LoadTester:
    def __init__(self, args):
        self.url = args.ur
        self.method = args.method.upper()
        self.concurrency = args.concurrency
        self.total_requests = args.requests
        self.timeout = args.timeout
        self.headers = {'User-Agent': 'LoadTest/1.0'}
        self.results = []
        # 初始化参数
        self.request_data = None
        if args.data:
            self.request_data = eval(args.data)  # 将字符串转换为字典

    def send_request(self):
        """发送单个HTTP请求"""
        start_time = time.time()
        status_code = 0
        try:
            response = requests.request(
                method=self.method,
                url=self.url,
                json=self.request_data,
                headers=self.headers,
                timeout=self.timeout
            )
            status_code = response.status_code
        except Exception as e:
            print(f"Request failed: {str(e)}")
        finally:
            elapsed = (time.time() - start_time) * 1000  # 转为毫秒
            return elapsed, status_code

    def run_test(self):
        """执行压测并收集结果"""
        start_time = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.concurrency) as executor:
            futures = [executor.submit(self.send_request) for _ in range(self.total_requests)]
            for future in concurrent.futures.as_completed(futures):
                elapsed, status = future.result()
                self.results.append((elapsed, status))

        self.total_time = time.time() - start_time
        self._analyze_results()

    def _analyze_results(self):
        """结果统计与分析"""
        times = [r[0] for r in self.results]
        success_count = sum(1 for r in self.results if 200 <= r[1] < 300)
        self.metrics = {
            'total_time': round(self.total_time, 2),
            'requests': len(self.results),
            'success_rate': success_count / len(self.results),
            'rps': round(len(self.results) / self.total_time, 2),
            'avg_time': round(mean(times), 2),
            'min_time': round(min(times), 2),
            'max_time': round(max(times), 2),
            'median_time': round(median(times), 2),
            'stdev': round(stdev(times), 2) if len(times) > 1 else 0
        }

    def print_report(self):
        """控制台输出测试报告"""
        print("\n======= 压力测试报告 =======")
        print(f"目标URL:       {self.method} {self.url}")
        print(f"并发数:        {self.concurrency}")
        print(f"总请求数:      {self.metrics['requests']}")
        print(f"总耗时:        {self.metrics['total_time']}s")
        print(f"成功率:        {self.metrics['success_rate'] * 100:.2f}%")
        print(f"吞吐量(RPS):   {self.metrics['rps']}")
        print("\n--- 响应时间统计(ms) ---")
        print(f"平均值:        {self.metrics['avg_time']}")
        print(f"中位数:        {self.metrics['median_time']}")
        print(f"最小值:        {self.metrics['min_time']}")
        print(f"最大值:        {self.metrics['max_time']}")
        print(f"标准差:        {self.metrics['stdev']}")

    def plot_results(self):
        """生成响应时间分布图"""
        plt.figure(figsize=(10, 6))
        plt.hist([r[0] for r in self.results], bins=20, alpha=0.7)
        plt.title('Response Time Distribution')
        plt.xlabel('Response Time (ms)')
        plt.ylabel('Number of Requests')
        plt.grid(True)
        plt.savefig('response_time_distribution.png')
        print("\n已生成响应时间分布图: response_time_distribution.png")

    def parse_args():
       """解析命令行参数"""
        parser = argparse.ArgumentParser(description='HTTP接口压力测试工具')
        parser.add_argument('url', help='目标接口URL')
        parser.add_argument('-m', '--method', default='GET',
        help='HTTP方法(GET/POST/PUT等), 默认GET')
        parser.add_argument('-c', '--concurrency', type=int, default=10,help='并发用户数，默认10')
        parser.add_argument('-r', '--requests', type=int, default=100,help='总请求数，默认100')
        parser.add_argument('-d', '--data',help='POST数据(JSON格式)，示例: \'{"key":"value"}\'')
        parser.add_argument('-t', '--timeout', type=float, default=5.0, help='单个请求超时时间(秒)，默认5')
        return parser.parse_args()



if __name__ == '__main__':
   args = parse_args()
   tester = LoadTester(args)
   print(f"开始压力测试: {args.method} {args.url}")
   print(f"配置参数: 并发数={args.concurrency}, 总请求数={args.requests}")
   try:
       tester.run_test()
       tester.print_report()
       tester.plot_results()
   except KeyboardInterrupt:
       print("\n测试被用户中断")

