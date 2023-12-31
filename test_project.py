import unittest
from to_do_list import add_task, view_tasks, mark_complete, delete_task, save_tasks, load_tasks

class TestToDoList(unittest.TestCase):

    # Test adding tasks
    def test_add_valid_task(self):
        add_task("Finish assignment")
        tasks = view_tasks()
        self.assertEqual(tasks, ["1. Finish assignment - Due: None"])

    def test_add_task_with_due_date(self):
        add_task("Buy groceries", "2024-01-15")
        tasks = view_tasks()
        self.assertEqual(tasks, ["1. Buy groceries - Due: 2024-01-15"])

    # Test marking tasks complete
    def test_mark_task_complete(self):
        add_task("Task 1")
        add_task("Task 2")
        mark_complete(1)
        tasks = view_tasks()
        self.assertEqual(tasks, ["1. Task 1 - Due: None (Completed)", "2. Task 2 - Due: None"])

    # Test deleting tasks
    def test_delete_task(self):
        add_task("Task 1")
        delete_task(1)
        tasks = view_tasks()
        self.assertEqual(tasks, [])

    # Test saving and loading tasks
    def test_save_load_tasks(self):
        add_task("Task 1")
        add_task("Task 2")
        save_tasks()
        tasks = load_tasks()
        self.assertEqual(tasks, [{"task": "Task 1", "due_date": None, "completed": False},
                                 {"task": "Task 2", "due_date": None, "completed": False}])

if __name__ == "__main__":
    unittest.main()
