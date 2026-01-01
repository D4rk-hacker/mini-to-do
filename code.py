import json
from datetime import datetime

class TodoApp:
    def __init__(self):
        self.tasks = []
        self.selected = 0
        self.view = "all"
        self.load_tasks()
    
    def clear_screen(self):
        print("\033[2J\033[H", end="")
    
    def print_header(self):
        print("\033[1;36m" + "="*50 + "\033[0m")
        print("\033[1;33m" + "           🚀 TODO MANAGER v4.0" + "\033[0m")
        print("\033[1;36m" + "="*50 + "\033[0m")
    
    def print_stats(self):
        pending = len([t for t in self.tasks if not t["done"]])
        done = len(self.tasks) - pending
        print(f"\033[1;32m📊 {pending} pending | {done} completed\033[0m")
    
    def print_tasks(self):
        visible_tasks = self.get_visible_tasks()
        if not visible_tasks:
            print("\033[1;33m📭 No tasks - add your first one! 🎯\033[0m")
            return
        
        for i, task in enumerate(visible_tasks):
            marker = "✅" if task["done"] else "○"
            prio_color = "🔴" if task["priority"] == 5 else "🟡" if task["priority"] >= 3 else "🟢"
            sel = " 👈" if i == self.selected else ""
            
            print(f"  {marker} {prio_color} P{task['priority']} {task['title']}{sel}")
    
    def get_visible_tasks(self):
        tasks = self.tasks
        if self.view == "pending":
            return [t for t in tasks if not t["done"]]
        elif self.view == "done":
            return [t for t in tasks if t["done"]]
        return tasks
    
    def print_menu(self):
        print("\n\033[1;32m[1] ➕ ADD    [2] ✅ COMPLETE  [3] 🗑️ DELETE")
        print("\033[1;34m[4] 🔼 PRIO   [5] 📅 DATE    [6] 👁️ VIEW")
        print("\033[1;36m[0] 💾 EXIT\033[0m")
        print("-"*50)
    
    def add_task(self):
        print("\n\033[1;32m➕ NEW TASK\033[0m")
        title = input("📝 Title (min 3 chars): ").strip()
        if len(title) < 3:
            print("\033[1;31m❌ Title too short!\033[0m")
            return
        
        priority_str = input("⭐ Priority 1-5 [default 3]: ").strip()
        try:
            priority = int(priority_str) if priority_str else 3
            priority = max(1, min(5, priority))
        except:
            priority = 3
        
        task = {
            "title": title,
            "priority": priority,
            "done": False,
            "date": datetime.now().strftime("%d.%m %H:%M")
        }
        self.tasks.append(task)
        print(f"\033[1;32m✅ Added: {title}\033[0m")
    
    def toggle_done(self):
        visible = self.get_visible_tasks()
        if not visible:
            print("\033[1;33mℹ️ No tasks\033[0m")
            return
        
        global_index = self.tasks.index(visible[self.selected])
        self.tasks[global_index]["done"] = not self.tasks[global_index]["done"]
        print("\033[1;32m✅ Status changed!\033[0m")
    
    def delete_task(self):
        visible = self.get_visible_tasks()
        if not visible:
            return
        
        global_index = self.tasks.index(visible[self.selected])
        print(f"\033[1;31m🗑️ Delete '{self.tasks[global_index]['title']}'? (y/n):\033[0m")
        if input().lower() in ['y', 'yes']:
            del self.tasks[global_index]
            print("\033[1;32m✅ Deleted!\033[0m")
    
    def sort_tasks(self, key):
        reverse = key == "priority"
        self.tasks.sort(key=lambda x: x[key], reverse=reverse)
        print(f"\033[1;34m🔄 Sorted by {key}\033[0m")
    
    def switch_view(self):
        views = {"all": "pending", "pending": "done", "done": "all"}
        self.view = views[self.view]
        self.selected = 0
        print(f"\033[1;35m👁️ View: {self.view}\033[0m")
    
    def save_tasks(self):
        try:
            data = json.dumps(self.tasks, indent=2, ensure_ascii=False)
            print("\n💾 DATA SAVED TO MEMORY (console + history)")
            print("📋 Copy this to notepad:")
            print(data)
        except:
            print("💾 Saved to program memory")
    
    def load_tasks(self):
        tasks_json = '''
        []
        '''
        try:
            self.tasks = json.loads(tasks_json.strip())
        except:
            self.tasks = []
    
    def run(self):
        input("⏎ Press Enter to start...")
        
        while True:
            self.clear_screen()
            self.print_header()
            self.print_stats()
            print()
            self.print_tasks()
            self.print_menu()
            
            choice = input("\n\033[1;36m➤ Choose (0-6): \033[0m").strip()
            
            if choice == "1":
                self.add_task()
            elif choice == "2":
                self.toggle_done()
            elif choice == "3":
                self.delete_task()
            elif choice == "4":
                self.sort_tasks("priority")
            elif choice == "5":
                self.sort_tasks("date")
            elif choice == "6":
                self.switch_view()
            elif choice == "0":
                self.save_tasks()
                print("\n\033[1;32m👋 Thanks! See you! 🚀\033[0m")
                break
            else:
                print("\033[1;31m❌ Unknown option! (0-6)\033[0m")
            
            input("\n\033[1;33m⏎ Enter = continue...\033[0m")

if __name__ == "__main__":
    app = TodoApp()
    app.run()
