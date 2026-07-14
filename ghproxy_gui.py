import tkinter as tk
from tkinter import ttk
import configparser
import os

CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.ini")

DEFAULT_NODES = [
    "https://gh-proxy.com/",
    "https://ghproxy.net/",
    "https://github.akams.cn/",
    "https://ghproxy.cfd/",
]

def load_config():
    config = configparser.ConfigParser()
    nodes = DEFAULT_NODES.copy()
    selected = nodes[0]
    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE, encoding="utf-8")
        if "nodes" in config:
            saved = config["nodes"].get("list", "")
            if saved:
                nodes = saved.split("\n")
            selected = config["nodes"].get("selected", nodes[0])
    return nodes, selected

def save_config(nodes, selected):
    config = configparser.ConfigParser()
    config["nodes"] = {"list": "\n".join(nodes), "selected": selected}
    config["ui"] = {"last_custom": custom_var.get() if custom_var else ""}
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        config.write(f)

def on_node_change(event=None):
    sel = node_combo.get()
    if sel == "自定义...":
        node_combo.set("")
        node_combo.configure(state="normal")
        node_combo.delete(0, tk.END)
        node_combo.insert(0, custom_var.get())
        node_combo.focus()
    else:
        custom_var.set("")

def on_focus_out(event=None):
    val = node_combo.get().strip()
    if val:
        custom_var.set(val)

def on_combo_return(event=None):
    convert()

def convert():
    raw = entry.get().strip()
    if not raw:
        return
    prefix = node_combo.get().strip()
    if not prefix:
        prefix = DEFAULT_NODES[0]
    result = prefix + raw
    result_var.set(result)
    root.clipboard_clear()
    root.clipboard_append(result)
    status_var.set("已复制到剪贴板")
    # save current node
    nodes = [node_combo.cget("values")[i] for i in range(len(node_combo.cget("values")) - 1)] if node_combo.cget("values") else list(node_combo["values"])
    all_items = list(node_combo["values"]) if node_combo["values"] else DEFAULT_NODES.copy()
    current_node = prefix
    save_config(list(all_items[:-1]) + ([current_node] if current_node not in all_items[:-1] else []), current_node)

def clear_all():
    entry.delete(0, tk.END)
    result_var.set("")
    status_var.set("")

def manage_nodes():
    mw = tk.Toplevel(root)
    mw.title("管理节点")
    mw.geometry("460x280")
    mw.resizable(False, False)
    mw.transient(root)
    mw.grab_set()

    lb = tk.Listbox(mw, font=("", 10))
    lb.pack(fill="both", expand=True, padx=10, pady=(10, 5))
    for n in node_combo["values"]:
        if n != "自定义...":
            lb.insert(tk.END, n)

    def add_node():
        val = add_entry.get().strip()
        if val and val not in lb.get(0, tk.END):
            lb.insert(tk.END, val)
            add_entry.delete(0, tk.END)

    def delete_node():
        sel = lb.curselection()
        if sel:
            lb.delete(sel[0])

    def save_nodes():
        items = list(lb.get(0, tk.END))
        items.append("自定义...")
        node_combo["values"] = items
        if items:
            node_combo.set(items[0])
        save_config(list(lb.get(0, tk.END)), node_combo.get())
        mw.destroy()

    add_frame = ttk.Frame(mw)
    add_frame.pack(fill="x", padx=10, pady=(0, 5))
    add_entry = ttk.Entry(add_frame, font=("", 9))
    add_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
    ttk.Button(add_frame, text="添加", command=add_node, width=6).pack(side="left")
    ttk.Button(add_frame, text="删除", command=delete_node, width=6).pack(side="left", padx=(5, 0))

    btn_frame = ttk.Frame(mw)
    btn_frame.pack(fill="x", padx=10, pady=(0, 10))
    ttk.Button(btn_frame, text="保存", command=save_nodes).pack(side="right", padx=(5, 0))
    ttk.Button(btn_frame, text="取消", command=mw.destroy).pack(side="right")


nodes, selected = load_config()

root = tk.Tk()
root.title("GitHub 加速下载")
root.geometry("640x260")
root.resizable(False, False)

main = ttk.Frame(root, padding=16)
main.pack(fill="both", expand=True)

ttk.Label(main, text="加速节点:", font=("", 10)).pack(anchor="w")
node_frame = ttk.Frame(main)
node_frame.pack(fill="x", pady=(2, 8))

node_values = nodes + ["自定义..."]
custom_var = tk.StringVar()
node_combo = ttk.Combobox(node_frame, values=node_values, font=("", 10), state="readonly")
node_combo.set(selected if selected in node_values else node_values[0])
node_combo.pack(side="left", fill="x", expand=True, padx=(0, 5))
node_combo.bind("<<ComboboxSelected>>", on_node_change)

ttk.Button(node_frame, text="管理节点", command=manage_nodes, width=8).pack(side="left")

ttk.Label(main, text="GitHub 原始链接:", font=("", 10)).pack(anchor="w")
entry = ttk.Entry(main, font=("", 10))
entry.pack(fill="x", pady=(4, 8))
entry.focus()

frame = ttk.Frame(main)
frame.pack(fill="x", pady=(0, 8))
ttk.Button(frame, text="转换", command=convert).pack(side="left", padx=(0, 8))
ttk.Button(frame, text="清空", command=clear_all).pack(side="left")

result_var = tk.StringVar()
ttk.Label(main, text="加速链接:", font=("", 10)).pack(anchor="w")
result_entry = ttk.Entry(main, textvariable=result_var, font=("", 9), state="readonly")
result_entry.pack(fill="x", pady=(4, 4))

result_entry.bind("<Button-1>", lambda e: root.clipboard_append(result_var.get()) or status_var.config(text="已复制"))

status_var = tk.StringVar()
ttk.Label(main, textvariable=status_var, foreground="gray").pack()

root.mainloop()