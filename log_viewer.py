import tkinter as tk
from tkinter import ttk, filedialog, messagebox

def parse_log_line(line):
    try:
        parts = line.split()
        ip = parts[0]
        method = parts[5].strip('"')
        endpoint = parts[6]
        status = parts[8]
        return ip, method, endpoint, status
    except IndexError:
        return None

def load_log_file(file_path):
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
            return [parse_log_line(line) for line in lines if parse_log_line(line)]
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load file:\n{e}")
        return []

def choose_file():
    file_path = filedialog.askopenfilename(title="Select a Log File",
                                           filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        global log_data
        log_data = load_log_file(file_path)
        update_table()

def update_table(method_filter="All"):
    for row in tree.get_children():
        tree.delete(row)

    for index, entry in enumerate(log_data):
        ip, method, endpoint, status = entry
        if method_filter == "All" or method == method_filter:
            tag = 'even' if index % 2 == 0 else 'odd'
            tree.insert("", tk.END, values=(ip, method, endpoint, status), tags=(tag,))

def on_filter_change(event):
    selected_method = filter_var.get()
    update_table(selected_method)

# --- GUI Setup ---
root = tk.Tk()
root.title("🌐 Colorful Log File Viewer")
root.geometry("1000x600")
root.configure(bg="#1e1e2f")

style = ttk.Style(root)
style.theme_use("clam")

# General styling
style.configure("Treeview",
                background="#fefefe",
                foreground="#222222",
                rowheight=28,
                fieldbackground="#fefefe",
                font=("Segoe UI", 10))
style.configure("Treeview.Heading",
                background="#4a90e2",
                foreground="white",
                font=("Segoe UI", 10, "bold"))

# Alternating row colors
tree_tag_even = {'background': '#f1f1f1'}
tree_tag_odd = {'background': '#ffffff'}

# --- Top Controls ---
top_frame = tk.Frame(root, bg="#1e1e2f", pady=15)
top_frame.pack(fill=tk.X)

title_label = tk.Label(top_frame, text="🧾 Log File Viewer", font=("Segoe UI", 16, "bold"), bg="#1e1e2f", fg="#4a90e2")
title_label.pack(side=tk.LEFT, padx=20)

file_btn = tk.Button(top_frame, text="📁 Choose File", command=choose_file,
                     bg="#4a90e2", fg="white", font=("Segoe UI", 10, "bold"),
                     activebackground="#357ABD", activeforeground="white",
                     bd=0, padx=10, pady=5)
file_btn.pack(side=tk.RIGHT, padx=(0, 20))

# --- Filter Controls ---
filter_frame = tk.Frame(root, bg="#1e1e2f")
filter_frame.pack(fill=tk.X, padx=20)

filter_label = tk.Label(filter_frame, text="Filter by Method:", font=("Segoe UI", 10), bg="#1e1e2f", fg="#ffffff")
filter_label.pack(side=tk.LEFT)

filter_var = tk.StringVar(value="All")
filter_menu = ttk.Combobox(filter_frame, textvariable=filter_var, width=12, state="readonly")
filter_menu['values'] = ["All", "GET", "POST", "PUT"]
filter_menu.bind("<<ComboboxSelected>>", on_filter_change)
filter_menu.pack(side=tk.LEFT, padx=10, pady=10)

# --- Table Display ---
table_frame = tk.Frame(root, padx=20, pady=10, bg="#1e1e2f")
table_frame.pack(fill=tk.BOTH, expand=True)

columns = ("IP Address", "Method", "Endpoint", "Status")
tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=240, anchor=tk.W)

# Apply alternating row tags
tree.tag_configure('even', background="#e8f0ff")
tree.tag_configure('odd', background="#ffffff")

# Scrollbar
vsb = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=vsb.set)
vsb.pack(side=tk.RIGHT, fill=tk.Y)
tree.pack(fill=tk.BOTH, expand=True)

# --- Load and display ---
log_data = []
update_table()

root.mainloop()
