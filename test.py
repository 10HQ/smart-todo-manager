#!/usr/bin/env python3
"""测试脚本"""
import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import TodoManager

def test():
    print("=" * 50)
    print("🧪 开始测试")
    print("=" * 50)
    
    # 使用临时文件
    test_file = "test_temp.json"
    manager = TodoManager(test_file)
    
    # 测试1: 添加
    print("\n1️⃣ 测试添加功能...")
    t1 = manager.add("完成项目报告", "周五前提交给经理", "高", "2026-06-01")
    t2 = manager.add("学习Python", "每天1小时练习", "中", "2026-06-15")
    t3 = manager.add("买菜", "西红柿、鸡蛋、青菜", "低", "2026-05-29")
    print(f"   ✅ 添加: [{t1.id}] {t1.title}")
    print(f"   ✅ 添加: [{t2.id}] {t2.title}")
    print(f"   ✅ 添加: [{t3.id}] {t3.title}")
    
    # 测试2: 统计
    print("\n2️⃣ 测试统计功能...")
    stats = manager.get_stats()
    for k, v in stats.items():
        print(f"   📊 {k}: {v}")
    
    # 测试3: 搜索
    print("\n3️⃣ 测试搜索功能...")
    results = manager.search("Python")
    print(f"   🔍 搜索'Python': 找到 {len(results)} 条")
    for r in results:
        print(f"      - [{r.id}] {r.title}")
    
    # 测试4: 完成
    print("\n4️⃣ 测试完成功能...")
    manager.complete(1)
    print(f"   ✅ 标记完成: [1] 完成项目报告")
    stats = manager.get_stats()
    print(f"   📊 完成率: {stats['完成率']}")
    
    # 测试5: 排序
    print("\n5️⃣ 测试排序功能...")
    sorted_todos = manager.get_sorted("priority")
    print("   按优先级排序:")
    for t in sorted_todos:
        status = "✅" if t.completed else "⏳"
        print(f"      {status} [{t.id}] {t.priority} - {t.title}")
    
    # 测试6: 删除
    print("\n6️⃣ 测试删除功能...")
    manager.delete(3)
    print(f"   🗑️ 删除: [3] 买菜")
    stats = manager.get_stats()
    print(f"   📊 剩余: {stats['总数']} 条")
    
    # 清理
    os.remove(test_file)
    
    print("\n" + "=" * 50)
    print("✅ 所有测试通过！")
    print("=" * 50)

if __name__ == "__main__":
    test()
