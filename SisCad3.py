import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json
import os

ARQUIVO = "cadastros.json"

cadastros = []
proximo_id = 1
registro_selecionado = None

# =====================================================
# PERSISTÊNCIA
# =====================================================

def carregar_dados():
    global cadastros, proximo_id
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            cadastros = json.load(f)
        if cadastros:
            ultimo = max(r["id"] for r in cadastros)
            proximo_id = ultimo + 1
        label_status.config(text="Dados carregados do JSON.{os.path}")
    else:
        cadastros = []
        label_status.config(text="Arquivo não encontrado. Novo banco iniciado.")
    atualizar_lista()


def salvar_dados():

    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(cadastros, f, indent=4, ensure_ascii=False)

    label_status.config(text="Dados gravados no JSON.")

# =====================================================
# LISTAGEM
# =====================================================

def atualizar_lista():
    for item in tree.get_children():
        tree.delete(item)
    for r in cadastros:
        tree.insert(
            "", tk.END, values=(
                r["id"],r["nome"],r["fone"],r["prof"],r["cid"],r["stat"]
            )
        )

# =====================================================
# NOVO REGISTRO
# =====================================================

def novo_registro():
    global registro_selecionado
    registro_selecionado = None
    limpar_campos()
    atualizar_id()
    label_status.config(text="Preparado para novo registro.")

# =====================================================
# INCLUIR
# =====================================================

def incluir():
    global proximo_id
    nome = entry_nome.get().strip()
    fone = entry_fone.get().strip()
    prof = entry_prof.get().strip()
    cid = entry_cid.get().strip()
    if not nome:
        messagebox.showerror("Erro", "Nome obrigatório.")
        return
    registro = {"id": proximo_id,"nome": nome,"fone": fone,"prof": prof,"cid": cid,"stat": "A"}
    cadastros.append(registro)
    salvar_dados()
    atualizar_lista()
    print("\nBase atual:")
    for r in cadastros:
        print(r)
    label_status.config(text=f"Registro {proximo_id} incluído.")
    proximo_id += 1
    novo_registro()

# =====================================================
# ALTERAR
# =====================================================

def alterar():
    global registro_selecionado
    if not registro_selecionado:
        messagebox.showwarning("Aviso", "Selecione um registro para alterar.")
        return
    registro_selecionado["nome"] = entry_nome.get()
    registro_selecionado["fone"] = entry_fone.get()
    registro_selecionado["prof"] = entry_prof.get()
    registro_selecionado["cid"] = entry_cid.get()
    salvar_dados()
    atualizar_lista()
    label_status.config(text=f"Registro {registro_selecionado['id']} alterado.")

# =====================================================
# EXCLUIR (lógico)
# =====================================================

def excluir():
    global registro_selecionado
    if not registro_selecionado:
        messagebox.showwarning("Aviso", "Selecione um registro.")
        return
    confirmar = messagebox.askyesno("Confirmar", "Excluir registro?")
    if not confirmar:
        return
    registro_selecionado["stat"] = "I"
    salvar_dados()
    atualizar_lista()
    label_status.config(text=f"Registro {registro_selecionado['id']} marcado como inativo.")
    novo_registro()

# =====================================================
# SELEÇÃO NA LISTA
# =====================================================

def selecionar_registro(event):
    global registro_selecionado
    item = tree.selection()
    if not item:
        return
    valores = tree.item(item)["values"]
    id_registro = valores[0]
    for r in cadastros:
        if r["id"] == id_registro:
            registro_selecionado = r
            break
    carregar_campos()
    label_status.config(text=f"Registro {id_registro} selecionado.")


def carregar_campos():

    entry_id.config(state="normal")
    entry_id.delete(0, tk.END)
    entry_id.insert(0, registro_selecionado["id"])
    entry_id.config(state="readonly")

    entry_nome.delete(0, tk.END)
    entry_nome.insert(0, registro_selecionado["nome"])

    entry_fone.delete(0, tk.END)
    entry_fone.insert(0, registro_selecionado["fone"])

    entry_prof.delete(0, tk.END)
    entry_prof.insert(0, registro_selecionado["prof"])

    entry_cid.delete(0, tk.END)
    entry_cid.insert(0, registro_selecionado["cid"])

# =====================================================
# AUXILIARES
# =====================================================

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

# =====================================================
# INTERFACE
# =====================================================

janela = tk.Tk()
janela.title("Mini Sistema de Cadastro")
janela.geometry("900x600")

style = ttk.Style()
style.theme_use("clam")

fonte = ("Arial", 14)

style.configure("TLabel", font=fonte)
style.configure("TEntry", font=fonte)
style.configure("TButton", font=fonte)

frame = ttk.Frame(janela, padding=20)
frame.pack()

ttk.Label(frame, text="Id").grid(row=0, column=0, sticky="e", pady=8)

entry_id = ttk.Entry(frame, width=10)
entry_id.grid(row=0, column=1, sticky="w")
entry_id.config(state="readonly")

ttk.Label(frame, text="Nome").grid(row=1, column=0, sticky="e", pady=8)
entry_nome = ttk.Entry(frame, width=40)
entry_nome.grid(row=1, column=1)

ttk.Label(frame, text="Telefone").grid(row=2, column=0, sticky="e", pady=8)
entry_fone = ttk.Entry(frame, width=40)
entry_fone.grid(row=2, column=1)

ttk.Label(frame, text="Profissão").grid(row=3, column=0, sticky="e", pady=8)
entry_prof = ttk.Entry(frame, width=40)
entry_prof.grid(row=3, column=1)

ttk.Label(frame, text="Cidade").grid(row=4, column=0, sticky="e", pady=8)
entry_cid = ttk.Entry(frame, width=40)
entry_cid.grid(row=4, column=1)

# =====================================================
# BOTÕES
# =====================================================

frame_botoes = ttk.Frame(janela)
frame_botoes.pack(pady=10)

ttk.Button(frame_botoes, text="Novo Registro", command=novo_registro).grid(row=0, column=0, padx=10)
ttk.Button(frame_botoes, text="Incluir", command=incluir).grid(row=0, column=1, padx=10)
ttk.Button(frame_botoes, text="Alterar", command=alterar).grid(row=0, column=2, padx=10)
ttk.Button(frame_botoes, text="Excluir", command=excluir).grid(row=0, column=3, padx=10)

# =====================================================
# TABELA
# =====================================================

colunas = ("id","nome","fone","prof","cid","stat")
tree = ttk.Treeview(janela, columns=colunas, show="headings", height=12)
tree.heading("id", text="ID")
tree.heading("nome", text="Nome")
tree.heading("fone", text="Telefone")
tree.heading("prof", text="Profissão")
tree.heading("cid", text="Cidade")
tree.heading("stat", text="Status")
tree.column("id", width=60, anchor="center")
tree.column("stat", width=60, anchor="center")
tree.pack(pady=20)
tree.bind("<<TreeviewSelect>>", selecionar_registro)

# =====================================================
# STATUS
# =====================================================

label_status = ttk.Label(janela, text="Sistema iniciado.")
label_status.pack(pady=10)

# =====================================================
# INICIALIZAÇÃO
# =====================================================

carregar_dados()
atualizar_id()

janela.mainloop()