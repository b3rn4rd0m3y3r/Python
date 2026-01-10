import tkinter as tk

janela = tk.Tk()
janela.title("Sistema Corporativo")
janela.geometry("800x500")

# =========================
# Frame do cabeçalho
# =========================
frame_topo = tk.Frame(janela, bg="#dddddd", height=50)
frame_topo.pack(fill="x")

titulo = tk.Label(
    frame_topo,
    text="Painel do Usuário",
    font=("Arial", 24, "bold"),
    bg="#dddddd"
)
titulo.pack(pady=10)

# =========================
# Frame central
# =========================
frame_meio = tk.Frame(janela)
frame_meio.pack(expand=True)

tk.Label(frame_meio, text="Nome:", font=("Arial", 14, "bold")).grid(row=0, column=0, padx=5, pady=5)
tk.Entry(frame_meio, font=("Arial", 12, "normal")).grid(row=0, column=1)

tk.Label(frame_meio, text="Cargo:", font=("Arial", 14, "bold")).grid(row=1, column=0, padx=5, pady=5)
tk.Entry(frame_meio, font=("Arial", 12, "normal")).grid(row=1, column=1)

# =========================
# Frame inferior
# =========================
frame_base = tk.Frame(janela)
frame_base.pack(pady=10)

tk.Button(frame_base, text="Salvar", font=("Arial", 12, "normal")).pack(side="left", padx=5)
tk.Button(frame_base, text="Cancelar", font=("Arial", 12, "normal")).pack(side="left", padx=5)

janela.mainloop()
