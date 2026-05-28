#!/usr/bin/env python3
"""
智能待办事项管理系统
作者：洹（灵台未央）
功能：添加/删除/完成/查看/搜索/排序待办事项
"""

import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from enum import Enum


class Priority(Enum):
    """优先级枚举"""
    HIGH = "高"
    MEDIUM = "中"
    LOW = "低"


@dataclass
class TodoItem:
    """待办事项数据类"""
    id: int
    title: str
    description: str
    priority: str
    due_date: str
    completed: bool
    created_at: str
    completed_at: Optional[str] = None

    def to_dict(self) -> Dict:
        return asdict(self)


class TodoManager:
    """待办事项管理器"""
    
    def __init__(self, data_file: str = "todos.json"):
        self.data_file = data_file
        self.todos: List[TodoItem] = []
        self.next_id = 1
        self.load()
    
    def load(self):
        """从JSON文件加载数据"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.todos = [TodoItem(**item) for item in data.get('todos', [])]
                    self.next_id = data.get('next_id', 1)
            except (json.JSONDecodeError, KeyError):
                self.todos = []
                self.next_id = 1
    
    def save(self):
        """保存数据到JSON文件"""
        data = {
            'todos': [todo.to_dict() for todo in self.todos],
            'next_id': self.next_id
        }
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def add(self, title: str, description: str = "", 
            priority: str = "中", due_date: str = "") -> TodoItem:
        """添加待办事项"""
        if not due_date:
            due_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
        
        todo = TodoItem(
            id=self.next_id,
            title=title,
            description=description,
            priority=priority,
            due_date=due_date,
            completed=False,
            created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        
        self.todos.append(todo)
        self.next_id += 1
        self.save()
        return todo
    
    def delete(self, todo_id: int) -> bool:
        """删除待办事项"""
        for i, todo in enumerate(self.todos):
            if todo.id == todo_id:
                self.todos.pop(i)
                self.save()
                return True
        return False
    
    def complete(self, todo_id: int) -> bool:
        """标记完成"""
        for todo in self.todos:
            if todo.id == todo_id:
                todo.completed = True
                todo.completed_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.save()
                return True
        return False
    
    def search(self, keyword: str) -> List[TodoItem]:
        """搜索待办事项"""
        keyword = keyword.lower()
        return [
            todo for todo in self.todos
            if keyword in todo.title.lower() or keyword in todo.description.lower()
        ]
    
    def get_sorted(self, sort_by: str = "due_date") -> List[TodoItem]:
        """获取排序后的待办事项"""
        priority_order = {"高": 0, "中": 1, "低": 2}
        
        if sort_by == "priority":
            return sorted(self.todos, key=lambda t: priority_order.get(t.priority, 1))
        elif sort_by == "due_date":
            return sorted(self.todos, key=lambda t: t.due_date)
        else:
            return self.todos
    
    def get_pending(self) -> List[TodoItem]:
        """获取未完成的待办事项"""
        return [todo for todo in self.todos if not todo.completed]
    
    def get_completed(self) -> List[TodoItem]:
        """获取已完成的待办事项"""
        return [todo for todo in self.todos if todo.completed]
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        total = len(self.todos)
        completed = len(self.get_completed())
        pending = total - completed
        
        high_priority = len([t for t in self.todos if t.priority == "高" and not t.completed])
        
        return {
            "总数": total,
            "已完成": completed,
            "待完成": pending,
            "高优先级": high_priority,
            "完成率": f"{completed/total*100:.1f}%" if total > 0 else "0%"
        }


def display_todo(todo: TodoItem):
    """显示单个待办事项"""
    status = "✅" if todo.completed else "⏳"
    priority_icon = {"高": "🔴", "中": "🟡", "低": "🟢"}.get(todo.priority, "⚪")
    
    print(f"{status} [{todo.id}] {priority_icon} {todo.title}")
    if todo.description:
        print(f"    📝 {todo.description}")
    print(f"    📅 截止: {todo.due_date} | ⏰ 创建: {todo.created_at}")
    if todo.completed_at:
        print(f"    ✅ 完成于: {todo.completed_at}")
    print()


def display_todos(todos: List[TodoItem], title: str = "待办事项"):
    """显示待办事项列表"""
    print(f"\n{'='*50}")
    print(f"📋 {title}")
    print(f"{'='*50}")
    
    if not todos:
        print("  (空)")
        return
    
    for todo in todos:
        display_todo(todo)


def main():
    """主函数"""
    manager = TodoManager()
    
    while True:
        print("\n" + "="*50)
        print("📝 智能待办事项管理系统")
        print("="*50)
        print("1. 添加待办事项")
        print("2. 查看所有待办")
        print("3. 查看未完成")
        print("4. 查看已完成")
        print("5. 标记完成")
        print("6. 删除待办")
        print("7. 搜索")
        print("8. 按优先级排序")
        print("9. 按截止日期排序")
        print("10. 统计信息")
        print("0. 退出")
        print("-"*50)
        
        choice = input("请选择操作 (0-10): ").strip()
        
        if choice == "1":
            print("\n--- 添加待办事项 ---")
            title = input("标题: ").strip()
            if not title:
                print("❌ 标题不能为空")
                continue
            
            description = input("描述 (可选): ").strip()
            
            print("优先级: 1.高 2.中 3.低")
            priority_choice = input("选择优先级 (1-3, 默认2): ").strip()
            priority_map = {"1": "高", "2": "中", "3": "低"}
            priority = priority_map.get(priority_choice, "中")
            
            due_date = input("截止日期 (YYYY-MM-DD, 默认7天后): ").strip()
            
            todo = manager.add(title, description, priority, due_date)
            print(f"\n✅ 已添加: [{todo.id}] {todo.title}")
        
        elif choice == "2":
            todos = manager.get_sorted("due_date")
            display_todos(todos, "所有待办事项")
        
        elif choice == "3":
            todos = manager.get_pending()
            display_todos(todos, "未完成事项")
        
        elif choice == "4":
            todos = manager.get_completed()
            display_todos(todos, "已完成事项")
        
        elif choice == "5":
            todo_id = input("\n输入待办事项ID: ").strip()
            if todo_id.isdigit():
                if manager.complete(int(todo_id)):
                    print("✅ 已标记为完成")
                else:
                    print("❌ 未找到该ID")
            else:
                print("❌ 无效的ID")
        
        elif choice == "6":
            todo_id = input("\n输入待办事项ID: ").strip()
            if todo_id.isdigit():
                if manager.delete(int(todo_id)):
                    print("🗑️ 已删除")
                else:
                    print("❌ 未找到该ID")
            else:
                print("❌ 无效的ID")
        
        elif choice == "7":
            keyword = input("\n输入搜索关键词: ").strip()
            if keyword:
                results = manager.search(keyword)
                display_todos(todos=results, title=f"搜索结果: {keyword}")
            else:
                print("❌ 关键词不能为空")
        
        elif choice == "8":
            todos = manager.get_sorted("priority")
            display_todos(todos, "按优先级排序")
        
        elif choice == "9":
            todos = manager.get_sorted("due_date")
            display_todos(todos, "按截止日期排序")
        
        elif choice == "10":
            stats = manager.get_stats()
            print("\n" + "="*50)
            print("📊 统计信息")
            print("="*50)
            for key, value in stats.items():
                print(f"  {key}: {value}")
            print()
        
        elif choice == "0":
            print("\n👋 再见！")
            break
        
        else:
            print("❌ 无效的选择，请重试")


if __name__ == "__main__":
    main()
