import tkinter as tk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox
import time

#ĐỒ THỊ
G = nx.Graph()

#CẬP NHẬT MA TRẬN KỀ
def update_matrix():
    text_matrix.delete("1.0", tk.END)

    nodes = list(G.nodes())
    n = len(nodes)

    if n == 0:
        return

    matrix = nx.to_numpy_array(G, nodelist=nodes, dtype=int)

    for row in matrix:
        text_matrix.insert(tk.END, " ".join(map(str, row)) + "\n")

#THUẬT TOÁN
def greedy():
    color = {}
    for v in G.nodes():
        used = {color.get(u) for u in G.neighbors(v)}
        c = 0
        while c in used:
            c += 1
        color[v] = c
    return color

def welch_powell():
    color = {}
    nodes = sorted(G.nodes(), key=lambda x: G.degree(x), reverse=True)
    for v in nodes:
        used = {color.get(u) for u in G.neighbors(v)}
        c = 0
        while c in used:
            c += 1
        color[v] = c
    return color

#VẼ ĐỒ THỊ
def draw(color=None):
    ax.clear()
    ax.axis("off")

    if G.number_of_nodes() == 0:
        canvas.draw()
        return

    pos = nx.spring_layout(G, seed=42)

    if color:
        nx.draw(G, pos, ax=ax,
                with_labels=True,
                node_color=list(color.values()),
                cmap=plt.cm.Set3,
                node_size=800)
    else:
        nx.draw(G, pos, ax=ax,
                with_labels=True,
                node_color="lightgray",
                node_size=800)

    canvas.draw()

#SỰ KIỆN
def add_edge():
    u = entry_dinh.get().strip()
    v = entry_canh.get().strip()

    if u and v:
        G.add_edge(u, v)
        entry_dinh.delete(0, tk.END)
        entry_canh.delete(0, tk.END)

        draw()
        update_matrix()   

def run_greedy():
    if G.number_of_nodes() > 0:
        start = time.perf_counter()
        colors = greedy()
        end = time.perf_counter()

        draw(colors)

        num_colors = len(set(colors.values()))
        elapsed = (end - start) * 1000

        label_info.config(text=f"Greedy: {num_colors} màu | {elapsed:.2f} ms")

def run_welch():
    if G.number_of_nodes() > 0:
        start = time.perf_counter()
        colors = welch_powell()
        end = time.perf_counter()

        draw(colors)

        num_colors = len(set(colors.values()))
        elapsed = (end - start) * 1000

        label_info.config(text=f"Welch-Powell: {num_colors} màu | {elapsed:.2f} ms")

def add_matrix():
    try:
        G.clear()
        rows = [r for r in text_matrix.get("1.0", tk.END).split("\n") if r.strip()]
        matrix = [list(map(int, r.split())) for r in rows]

        n = len(matrix)
        for r in matrix:
            if len(r) != n:
                messagebox.showerror("Lỗi", "Ma trận không vuông")
                return

        for i in range(n):
            G.add_node(str(i + 1))

        for i in range(n):
            for j in range(i + 1, n):
                if matrix[i][j] == 1:
                    G.add_edge(str(i + 1), str(j + 1))

        draw()
        update_matrix()   
    except:
        messagebox.showerror("Lỗi", "Ma trận không hợp lệ")

def reset():
    G.clear()
    ax.clear()
    ax.axis("off")
    canvas.draw()
    text_matrix.delete("1.0", tk.END)
    label_info.config(text="")

#GIAO DIỆN
root = tk.Tk()
root.title("Giải thuật tô màu đồ thị")
root.geometry("1000x550")

tk.Label(root, text="Giải thuật tô màu đồ thị",
         font=("Arial", 18, "bold")).pack(pady=10)

main = tk.Frame(root)
main.pack(fill=tk.BOTH, expand=True)

#BÊN TRÁI
left = tk.Frame(main, bg="white")
left.pack(side=tk.LEFT, padx=10)

fig, ax = plt.subplots(figsize=(6, 4))
ax.axis("off")
canvas = FigureCanvasTkAgg(fig, master=left)
canvas.get_tk_widget().pack()

#BÊN PHẢI
right = tk.Frame(main)
right.pack(side=tk.RIGHT, padx=30)

tk.Label(right, text="Đỉnh").grid(row=0, column=0)
tk.Label(right, text="Cạnh").grid(row=0, column=1)

entry_dinh = tk.Entry(right, width=10)
entry_canh = tk.Entry(right, width=10)
entry_dinh.grid(row=1, column=0, padx=5)
entry_canh.grid(row=1, column=1, padx=5)

tk.Button(right, text="Thêm", width=8,
          command=add_edge).grid(row=1, column=2)

tk.Label(right, text="Tô màu:").grid(row=2, column=0, columnspan=3, pady=10)

label_info = tk.Label(right, text="", fg="blue", font=("Arial", 10, "bold"))
label_info.grid(row=4, column=0, columnspan=3, pady=5)

tk.Button(right, text="Greedy", width=10,
          command=run_greedy).grid(row=3, column=0)

tk.Button(right, text="Welch Powell", width=10,
          command=run_welch).grid(row=3, column=1)

tk.Label(right, text="Ma trận").grid(row=5, column=0, columnspan=3, pady=10)

text_matrix = tk.Text(right, width=25, height=8)
text_matrix.grid(row=6, column=0, columnspan=3)

tk.Button(right, text="Thêm ma trận", width=15,
          command=add_matrix).grid(row=7, column=0, columnspan=3, pady=5)

tk.Button(right, text="RESET", width=10,
          command=reset).grid(row=8, column=0, columnspan=3, pady=10)

root.mainloop()
