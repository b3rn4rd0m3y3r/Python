import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# =========================
# Estrutura de Dados
# =========================

cadastros = []
proximo_id = 1

# =========================
# Função Incluir
# =========================

def incluir():
    global proximo_id

    nome = entry_nome.get().strip()
    fone = entry_fone.get().strip()
    prof = entry_prof.get().strip()
    cid = entry_cid.get().strip()

    # =========================
    # Validações
    # =========================

    if not nome:
        messagebox.showerror("Erro", "Nome é obrigatório.")
        return

    if len(nome) > 40:
        messagebox.showerror("Erro", "Nome deve ter no máximo 40 caracteres.")
        return

    if not fone:
        messagebox.showerror("Erro", "Telefone é obrigatório.")
        return

    if not fone.isdigit():
        messagebox.showerror("Erro", "Telefone deve conter apenas números.")
        return

    if len(fone) > 11:
        messagebox.showerror("Erro", "Telefone deve ter no máximo 11 caracteres.")
        return

    if len(prof) > 40:
        messagebox.showerror("Erro", "Profissão deve ter no máximo 40 caracteres.")
        return

    if len(cid) > 40:
        messagebox.showerror("Erro", "Cidade deve ter no máximo 40 caracteres.")
        return

    # =========================
    # Criação do Registro
    # =========================

    registro = {
        "id": proximo_id,
        "nome": nome,
        "fone": fone,
        "prof": prof,
        "cid": cid
    }

    cadastros.append(registro)

    print("\nLista atual de cadastros:")
    for item in cadastros:
        print(item)

    label_status.config(text=f"Registro {proximo_id} incluído com sucesso.")

    proximo_id += 1
    entry_id.config(state="normal")
    entry_id.delete(0, tk.END)
    entry_id.insert(0, proximo_id)
    entry_id.config(state="readonly")

    limpar_campos()

# =========================
# Limpar Campos
# =========================

def limpar_campos():
    entry_nome.delete(0, tk.END)
    entry_fone.delete(0, tk.END)
    entry_prof.delete(0, tk.END)
    entry_cid.delete(0, tk.END)

# =========================
# Interface
# =========================

janela = tk.Tk()
janela.title("Mini Sistema de Cadastro - Parte 1")
janela.geometry("600x420")

style = ttk.Style()
style.theme_use("clam")

fonte_padrao = ("Arial", 14)

style.configure("TLabel", font=fonte_padrao)
style.configure("TEntry", font=fonte_padrao)
style.configure("TButton", font=fonte_padrao, padding=6)

frame = ttk.Frame(janela, padding=20)
frame.pack()

# ID (readonly)

ttk.Label(frame, text="Id:").grid(row=0, column=0, sticky="e", pady=8)
entry_id = ttk.Entry(frame, width=10)
entry_id.grid(row=0, column=1, pady=8, sticky="w")
entry_id.insert(0, proximo_id)
entry_id.config(state="readonly")

# Nome

ttk.Label(frame, text="Nome:").grid(row=1, column=0, sticky="e", pady=8)
entry_nome = ttk.Entry(frame, width=40)
entry_nome.grid(row=1, column=1, pady=8)

# Telefone

ttk.Label(frame, text="Telefone:").grid(row=2, column=0, sticky="e", pady=8)
entry_fone = ttk.Entry(frame, width=40)
entry_fone.grid(row=2, column=1, pady=8)

# Profissão

ttk.Label(frame, text="Profissão:").grid(row=3, column=0, sticky="e", pady=8)
entry_prof = ttk.Entry(frame, width=40)
entry_prof.grid(row=3, column=1, pady=8)

# Cidade

ttk.Label(frame, text="Cidade:").grid(row=4, column=0, sticky="e", pady=8)
entry_cid = ttk.Entry(frame, width=40)
entry_cid.grid(row=4, column=1, pady=8)

# Botão

btn_incluir = ttk.Button(frame, text="Incluir", command=incluir)
btn_incluir.grid(row=5, column=0, columnspan=2, pady=20)

# Status

label_status = ttk.Label(janela, text="Aguardando inclusão...")
label_status.pack(pady=10)

janela.mainloop()