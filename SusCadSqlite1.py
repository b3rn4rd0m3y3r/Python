import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

# =====================================================
# CONFIGURAÇÃO DE BANCO
# =====================================================

def obter_nome_banco():
    return "cadastros.db"


def obter_conexao():
    banco = obter_nome_banco()
    return sqlite3.connect(banco)


def criar_tabela():

    conn = obter_conexao()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cadastros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        fone TEXT,
        prof TEXT,
        cid TEXT,
        stat TEXT
    )
    """)

    conn.commit()
    conn.close()

# =====================================================
# FUNÇÕES DE ACESSO AO BANCO
# =====================================================

def db_inserir(nome, fone, prof, cid):

    conn = obter_conexao()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO cadastros (nome, fone, prof, cid, stat)
        VALUES (?, ?, ?, ?, 'A')
    """, (nome, fone, prof, cid))

    conn.commit()
    conn.close()


def db_atualizar(id_registro, nome, fone, prof, cid):

    conn = obter_conexao()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE cadastros
        SET nome=?, fone=?, prof=?, cid=?
        WHERE id=?
    """, (nome, fone, prof, cid, id_registro))

    conn.commit()
    conn.close()


def db_excluir(id_registro):

    conn = obter_conexao()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE cadastros
        SET stat='I'
        WHERE id=?
    """, (id_registro,))

    conn.commit()
    conn.close()


def db_listar():

    conn = obter_conexao()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nome, fone, prof, cid, stat
        FROM cadastros
        ORDER BY id
    """)

    dados = cursor.fetchall()

    conn.close()

    return dados


def db_buscar(id_registro):

    conn = obter_conexao()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nome, fone, prof, cid, stat
        FROM cadastros
        WHERE id=?
    """, (id_registro,))

    registro = cursor.fetchone()

    conn.close()

    return registro

# =====================================================
# VARIÁVEIS DO SISTEMA (mantidas)
# =====================================================

cadastros = []
registro_selecionado = None

# =====================================================
# PERSISTÊNCIA (adaptada para banco)
# =====================================================

def carregar_dados():

    global cadastros

    dados = db_listar()

    cadastros = []

    for r in dados:
        cadastros.append({
            "id": r[0],
            "nome": r[1],
            "fone": r[2],
            "prof": r[3],
            "cid": r[4],
            "stat": r[5]
        })

    atualizar_lista()

    label_status.config(text="Dados carregados do SQLite.")


def salvar_dados():
    # Mantida apenas para compatibilidade didática
    pass

# =====================================================
# LISTAGEM
# =====================================================

def atualizar_lista():

    for item in tree.get_children():
        tree.delete(item)

    for r in cadastros:

        tree.insert(
            "",
            tk.END,
            values=(
                r["id"],
                r["nome"],
                r["fone"],
                r["prof"],
                r["cid"],
                r["stat"]
            )
        )

# =====================================================
# NOVO REGISTRO
# =====================================================

def novo_registro():

    global registro_selecionado

    registro_selecionado = None

    limpar_campos()

    entry_id.config(state="normal")
    entry_id.delete(0, tk.END)
    entry_id.insert(0, "")
    entry_id.config(state="readonly")

    label_status.config(text="Preparado para novo registro.")

# =====================================================
# INCLUIR
# =====================================================

def incluir():

    nome = entry_nome.get().strip()
    fone = entry_fone.get().strip()
    prof = entry_prof.get().strip()
    cid = entry_cid.get().strip()

    if not nome:
        messagebox.showerror("Erro", "Nome obrigatório.")
        return

    db_inserir(nome, fone, prof, cid)

    carregar_dados()

    label_status.config(text="Registro incluído.")

    novo_registro()

# =====================================================
# ALTERAR
# =====================================================

def alterar():

    global registro_selecionado

    if not registro_selecionado:
        messagebox.showwarning("Aviso", "Selecione um registro.")
        return

    id_registro = registro_selecionado["id"]

    nome = entry_nome.get()
    fone = entry_fone.get()
    prof = entry_prof.get()
    cid = entry_cid.get()

    db_atualizar(id_registro, nome, fone, prof, cid)

    carregar_dados()

    label_status.config(text=f"Registro {id_registro} alterado.")

# =====================================================
# EXCLUIR
# =====================================================

def excluir():

    global registro_selecionado

    if not registro_selecionado:
        messagebox.showwarning("Aviso", "Selecione um registro.")
        return

    confirmar = messagebox.askyesno("Confirmar", "Excluir registro?")

    if not confirmar:
        return

    id_registro = registro_selecionado["id"]

    db_excluir(id_registro)

    carregar_dados()

    label_status.config(text=f"Registro {id_registro} marcado como inativo.")

    novo_registro()

# =====================================================
# SELEÇÃO NA TABELA
# =====================================================

def selecionar_registro(event):

    global registro_selecionado

    item = tree.selection()

    if not item:
        return

    valores = tree.item(item)["values"]

    id_registro = valores[0]

    registro = db_buscar(id_registro)

    registro_selecionado = {
        "id": registro[0],
        "nome": registro[1],
        "fone": registro[2],
        "prof": registro[3],
        "cid": registro[4],
        "stat": registro[5]
    }

    carregar_campos()

    label_status.config(text=f"Registro {id_registro} selecionado.")

# =====================================================
# AUXILIARES
# =====================================================

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


def limpar_campos():

    entry_nome.delete(0, tk.END)
    entry_fone.delete(0, tk.END)
    entry_prof.delete(0, tk.END)
    entry_cid.delete(0, tk.END)

# =====================================================
# INTERFACE
# =====================================================

janela = tk.Tk()
janela.title("Mini Sistema de Cadastro - SQLite")
janela.geometry("900x600")

style = ttk.Style()
style.theme_use("clam")

fonte = ("Arial", 14)

style.configure("TLabel", font=fonte)
style.configure("TEntry", font=fonte)

# estilos de botões
style.configure("Novo.TButton", font=fonte, background="#4CAF50")
style.configure("Incluir.TButton", font=fonte, background="#2196F3")
style.configure("Alterar.TButton", font=fonte, background="#FFC107")
style.configure("Excluir.TButton", font=fonte, background="#F44336")

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

# BOTÕES

frame_botoes = ttk.Frame(janela)
frame_botoes.pack(pady=10)

ttk.Button(frame_botoes, text="Novo Registro", command=novo_registro, style="Novo.TButton").grid(row=0,column=0,padx=10)
ttk.Button(frame_botoes, text="Incluir", command=incluir, style="Incluir.TButton").grid(row=0,column=1,padx=10)
ttk.Button(frame_botoes, text="Alterar", command=alterar, style="Alterar.TButton").grid(row=0,column=2,padx=10)
ttk.Button(frame_botoes, text="Excluir", command=excluir, style="Excluir.TButton").grid(row=0,column=3,padx=10)

# TABELA

colunas = ("id","nome","fone","prof","cid","stat")

tree = ttk.Treeview(janela, columns=colunas, show="headings", height=12)

for c in colunas:
    tree.heading(c, text=c.upper())

tree.column("id", width=60, anchor="center")
tree.column("stat", width=60, anchor="center")

tree.pack(pady=20)

tree.bind("<<TreeviewSelect>>", selecionar_registro)

# STATUS

label_status = ttk.Label(janela, text="Sistema iniciado.")
label_status.pack(pady=10)

# INICIALIZAÇÃO

criar_tabela()
carregar_dados()

janela.mainloop()