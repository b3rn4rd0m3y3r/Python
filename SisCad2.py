import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json
import os

# =========================
# Configuração
# =========================

ARQUIVO = "cadastros.json"

cadastros = []
proximo_id = 1

# =========================
# Funções de Persistência
# =========================

def carregar_dados():
    global cadastros, proximo_id

    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            cadastros = json.load(f)

        if cadastros:
            ultimo_id = max(reg["id"] for reg in cadastros)
            proximo_id = ultimo_id + 1

        label_status.config(text="Dados carregados do arquivo JSON.")
    else:
        cadastros = []
        label_status.config(text="Arquivo não encontrado. Novo banco criado.")

def salvar_dados():
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(cadastros, f, indent=4, ensure_ascii=False)

    label_status.config(text="Dados salvos automaticamente no JSON.")

# =========================
# Inclusão
# =========================

def incluir():
    global proximo_id
    # Limpeza dos "entries"
    nome = entry_nome.get().strip()
    fone = entry_fone.get().strip()
    prof = entry_prof.get().strip()
    cid = entry_cid.get().strip()

    # Validações

    if not nome or len(nome) > 40:
        messagebox.showerror("Erro", "Nome obrigatório (máx 40).")
        return

    if not fone or not fone.isdigit() or len(fone) > 11:
        messagebox.showerror("Erro", "Telefone obrigatório, até 11 números.")
        return

    if len(prof) > 40:
        messagebox.showerror("Erro", "Profissão máx 40.")
        return

    if len(cid) > 40:
        messagebox.showerror("Erro", "Cidade máx 40.")
        return

    registro = {
        "id": proximo_id,
        "nome": nome,
        "fone": fone,
        "prof": prof,
        "cid": cid,
        "stat": "A"
    }

    cadastros.append(registro)

    print("\nBase atual:")
    for r in cadastros:
        print(r)

    salvar_dados()

    label_status.config(text=f"Registro {proximo_id} incluído e persistido.")

    proximo_id += 1
    atualizar_id()
    limpar_campos()

# =========================
# Auxiliares
# =========================

def atualizar_id():
    entry_id.config(state="normal")
    entry_id.delete(0, tk.END)
    entry_id.insert(0, proximo_id)
    entry_id.config(state="readonly")

def limpar_campos():
    entry_nome.delete(0, tk.END)
    entry_fone.delete(0, tk.END)
    entry_prof.delete(0, tk.END)
    entry_cid.delete(0, tk.END)

# =========================
# Interface
# =========================

janela = tk.Tk()
janela.title("Mini Sistema - Parte 2 (Persistência)")
janela.geometry("650x450")

style = ttk.Style()
style.theme_use("clam")

fonte = ("Arial", 14)

style.configure("TLabel", font=fonte)
style.configure("TEntry", font=fonte)
style.configure("TButton", font=fonte, padding=6)

frame = ttk.Frame(janela, padding=20)
frame.pack()

# ID

ttk.Label(frame, text="Id:").grid(row=0, column=0, sticky="e", pady=8)
entry_id = ttk.Entry(frame, width=10)
entry_id.grid(row=0, column=1, sticky="w")
entry_id.config(state="readonly")

# Nome

ttk.Label(frame, text="Nome:").grid(row=1, column=0, sticky="e", pady=8)
entry_nome = ttk.Entry(frame, width=40)
entry_nome.grid(row=1, column=1)

# Telefone

ttk.Label(frame, text="Telefone:").grid(row=2, column=0, sticky="e", pady=8)
entry_fone = ttk.Entry(frame, width=40)
entry_fone.grid(row=2, column=1)

# Profissão

ttk.Label(frame, text="Profissão:").grid(row=3, column=0, sticky="e", pady=8)
entry_prof = ttk.Entry(frame, width=40)
entry_prof.grid(row=3, column=1)

# Cidade

ttk.Label(frame, text="Cidade:").grid(row=4, column=0, sticky="e", pady=8)
entry_cid = ttk.Entry(frame, width=40)
entry_cid.grid(row=4, column=1)

# Botão

btn_incluir = ttk.Button(frame, text="Incluir", command=incluir)
btn_incluir.grid(row=5, column=0, columnspan=2, pady=20)

# Status

label_status = ttk.Label(janela, text="Inicializando sistema...")
label_status.pack(pady=15)

# Inicialização

carregar_dados()
atualizar_id()

janela.mainloop()