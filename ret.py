import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# Имя файла для сохранения
FILE_NAME = "workouts.json"

class TrainingPlannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Training Planner")
        self.root.geometry("600x400")

        self.workouts = self.load_data()

        # Интерфейс
        self.create_widgets()
        self.update_list()

    def load_data(self):
        if os.path.exists(FILE_NAME):
            with open(FILE_NAME, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def save_data(self):
        with open(FILE_NAME, 'w', encoding='utf-8') as f:
            json.dump(self.workouts, f, indent=4, ensure_ascii=False)

    def create_widgets(self):
        # Поля ввода
        frame_input = tk.Frame(self.root)
        frame_input.pack(pady=10)

        tk.Label(frame_input, text="Упражнение:").grid(row=0, column=0)
        self.entry_name = tk.Entry(frame_input)
        self.entry_name.grid(row=0, column=1)

        tk.Label(frame_input, text="Тип:").grid(row=0, column=2)
        self.combo_type = ttk.Combobox(frame_input, values=["Силовая", "Кардио", "Йога"])
        self.combo_type.grid(row=0, column=3)
        self.combo_type.current(0)

        btn_add = tk.Button(frame_input, text="Добавить", command=self.add_workout)
        btn_add.grid(row=0, column=4, padx=5)

        # Фильтрация
        frame_filter = tk.Frame(self.root)
        frame_filter.pack(pady=5)
        tk.Label(frame_filter, text="Фильтр (тип):").pack(side=tk.LEFT)
        self.combo_filter = ttk.Combobox(frame_filter, values=["Все", "Силовая", "Кардио", "Йога"])
        self.combo_filter.pack(side=tk.LEFT)
        self.combo_filter.current(0)
        self.combo_filter.bind("<<ComboboxSelected>>", self.update_list)

        # Список тренировок
        self.tree = ttk.Treeview(self.root, columns=("Name", "Type"), show='headings')
        self.tree.heading("Name", text="Упражнение")
        self.tree.heading("Type", text="Тип")
        self.tree.pack(pady=10, fill=tk.BOTH, expand=True)

    def add_workout(self):
        name = self.entry_name.get()
        w_type = self.combo_type.get()
        if name:
            self.workouts.append({"name": name, "type": w_type})
            self.save_data()
            self.update_list()
            self.entry_name.delete(0, tk.END)
        else:
            messagebox.showwarning("Ошибка", "Введите название")

    def update_list(self, event=None):
        # Очистка списка
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Фильтрация
        filter_type = self.combo_filter.get()
        for w in self.workouts:
            if filter_type == "Все" or w["type"] == filter_type:
                self.tree.insert("", tk.END, values=(w["name"], w["type"]))

if __name__ == "__main__":
    root = tk.Tk()
    app = TrainingPlannerApp(root)
    root.mainloop()
