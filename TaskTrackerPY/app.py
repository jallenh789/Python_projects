import json
import os
from datetime import datetime

TASK_FILE = "tasks.json"

# ------------------ Task Class ------------------

class Task:
    def __init__(self, task_id, description, status, created_at=None, updated_at=None):
        self.task_id = task_id
        self.description = description
        self.status = status
        self.created_at = created_at or datetime.now().isoformat()
        self.updated_at = updated_at or datetime.now().isoformat()

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    @staticmethod
    def from_dict(data):
        return Task(
            data["task_id"],
            data["description"],
            data["status"],
            data["created_at"],
            data["updated_at"]
        )

# ------------------ Helper Functions ------------------

def reset_ids(tasks):
    """Resets task IDs starting from 1"""
    for index, task in enumerate(tasks):
        task.task_id = index + 1

# ------------------ File Functions ------------------

def load_tasks():
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, "r") as f:
            tasks = [Task.from_dict(t) for t in json.load(f)]
            reset_ids(tasks)
            return tasks
    return []

def save_tasks(tasks):
    with open(TASK_FILE, "w") as f:
        json.dump([t.to_dict() for t in tasks], f, indent=4)

# ------------------ Task Operations ------------------

def add_task(tasks):
    description = input("Enter task description: ")
    task = Task(0, description, "todo")  # temporary ID
    tasks.append(task)
    reset_ids(tasks)
    save_tasks(tasks)
    print("Task added and IDs updated.\n")

def update_task(tasks):
    prnt_all(tasks)
    try:
        task_id = int(input("Enter task ID to update: "))
    except ValueError:
        print("Invalid input.\n")
        return

    for task in tasks:
        if task.task_id == task_id:
            new_desc = input("Enter new description: ")
            task.description = new_desc
            task.updated_at = datetime.now().isoformat()
            save_tasks(tasks)
            print("Task updated.\n")
            return
    print("Task not found.\n")

def delete_task(tasks):
    prnt_all(tasks)
    try:
        task_id = int(input("Enter task ID to delete: "))
    except ValueError:
        print("Invalid input.\n")
        return

    for i, task in enumerate(tasks):
        if task.task_id == task_id:
            del tasks[i]
            reset_ids(tasks)
            save_tasks(tasks)
            print("Task deleted and IDs updated.\n")
            return
    print("Task not found.\n")

def mark_task(tasks, status):
    prnt_all(tasks)
    try:
        task_id = int(input(f"Enter task ID to mark as {status}: "))
    except ValueError:
        print("Invalid input.\n")
        return

    for task in tasks:
        if task.task_id == task_id:
            task.status = status
            task.updated_at = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task marked as {status}.\n")
            return
    print("Task not found.\n")

# ------------------ Print Functions ------------------

def prnt_all(tasks):
    print("\n--- All Tasks ---")
    for task in tasks:
        print(f"{task.task_id}: {task.description} [{task.status}]")
    print()

def prnt_by_status(tasks, status):
    print(f"\n--- Tasks with status '{status}' ---")
    for task in tasks:
        if task.status == status:
            print(f"{task.task_id}: {task.description}")
    print()

def prnt_not_done(tasks):
    print("\n--- Tasks not done ---")
    for task in tasks:
        if task.status in ["todo", "in-progress"]:
            print(f"{task.task_id}: {task.description} [{task.status}]")
    print()

# ------------------ Menu ------------------

def print_menu():
    print("1. Add a Task")
    print("2. Update a Task")
    print("3. Delete a Task")
    print("4. Mark as in progress")
    print("5. Mark as done")
    print("6. List all tasks")
    print("7. List all tasks that are done")
    print("8. List all tasks that are not done (todo, in-progress)")
    print("9. List all tasks that are in progress")
    print("10. Quit")
    print()

# ------------------ Main CLI ------------------

def main():
    tasks = load_tasks()
    while True:
        print_menu()
        choice = input("Enter your choice: ").strip()
        print()
        match choice:
            case "1":
                add_task(tasks)
            case "2":
                update_task(tasks)
            case "3":
                delete_task(tasks)
            case "4":
                mark_task(tasks, "in-progress")
            case "5":
                mark_task(tasks, "done")
            case "6":
                prnt_all(tasks)
            case "7":
                prnt_by_status(tasks, "done")
            case "8":
                prnt_not_done(tasks)
            case "9":
                prnt_by_status(tasks, "in-progress")
            case "10":
                print("Goodbye!")
                break
            case _:
                print("Invalid input. Please try again.\n")

if __name__ == "__main__":
    main()