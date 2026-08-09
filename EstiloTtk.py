import tkinter as tk
from tkinter import ttk

# =========================
# Funções
# =========================

def salvar():
    nome = entry_nome.get()
    email = entry_email.get()
    cargo = entry_cargo.get()

    label_status.config(
        text=f"Dados salvos: {nome} - {cargo}"
    )

def limpar():
    entry_nome.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_cargo.delete(0, tk.END)
    label_status.config(text="Campos limpos")

# =========================
# Janela principal
# =========================

janela = tk.Tk()
janela.title("Sistema Corporativo")
janela.geometry("600x400")

# =========================
# Estilo ttk
# =========================

style = ttk.Style()
style.theme_use("clam")        # tema mais neutro e customizável

fonte_padrao = ("Arial", 14)

# Estilo geral
style.configure("TLabel", font=fonte_padrao)
style.configure("TEntry", font=fonte_padrao)
style.configure("TButton", font=fonte_padrao, padding=6)

# Estilo do cabeçalho
style.configure(
    "Header.TLabel",
    font=("Arial", 16, "bold"),
    foreground="white",
    background="#2c3e50"
)

# Estilo botão principal
style.configure(
    "Primary.TButton",
    background="#2980b9",
    foreground="white"
)

# Estilo botão secundário
style.configure(
    "Secondary.TButton",
    background="#7f8c8d",
    foreground="white"
)

# =========================
# Cabeçalho
# =========================

header_frame = tk.Frame(janela, bg="#2c3e50")
header_frame.pack(fill="x")

header = ttk.Label(
    header_frame,
    text="SISTEMA CORPORATIVO",
    style="Header.TLabel",
    anchor="center"
)
header.pack(fill="x", pady=15)

# =========================
# Frame principal
# =========================

frame = ttk.Frame(janela, padding=20)
frame.pack(pady=20)

# =========================
# Campos
# =========================

ttk.Label(frame, text="Nome:").grid(row=0, column=0, sticky="e", pady=8, padx=10)
entry_nome = ttk.Entry(frame, width=25)
entry_nome.grid(row=0, column=1, pady=8)

ttk.Label(frame, text="Email:").grid(row=1, column=0, sticky="e", pady=8, padx=10)
entry_email = ttk.Entry(frame, width=25)
entry_email.grid(row=1, column=1, pady=8)

ttk.Label(frame, text="Cargo:").grid(row=2, column=0, sticky="e", pady=8, padx=10)
entry_cargo = ttk.Entry(frame, width=25)
entry_cargo.grid(row=2, column=1, pady=8)

# =========================
# Botões
# =========================

btn_frame = ttk.Frame(janela, padding=10)
btn_frame.pack()

btn_salvar = ttk.Button(
    btn_frame,
    text="SALVAR",
    style="Primary.TButton",
    command=salvar
)
btn_salvar.grid(row=0, column=0, padx=15)

btn_limpar = ttk.Button(
    btn_frame,
    text="LIMPAR",
    style="Secondary.TButton",
    command=limpar
)
btn_limpar.grid(row=0, column=1, padx=15)

# =========================
# Status
# =========================

label_status = ttk.Label(
    janela,
    text="Aguardando ação..."
)
label_status.pack(pady=15)

janela.mainloop()
