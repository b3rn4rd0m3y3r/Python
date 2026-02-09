import tkinter as tk

# =========================
# Função auxiliar de log
# =========================
def registrar_log(mensagem):
    log_text.insert(tk.END, mensagem + "\n")
    log_text.see(tk.END)

# =========================
# Funções de resposta
# =========================

def atualizar_check():
    registrar_log("Função atualizar_check() executada")

    if notif_var.get() == 1:
        label_check.config(text="Status notificações: Ativadas")
    else:
        label_check.config(text="Status notificações: Desativadas")

def atualizar_lista(event):
    registrar_log("Função atualizar_lista() executada")

    selecao = listbox.curselection()
    if selecao:
        setor = listbox.get(selecao[0])
        label_lista.config(text=f"Setor escolhido: {setor}")

# =========================
# Janela principal
# =========================

janela = tk.Tk()
janela.title("Controles de Seleção")
janela.geometry("520x520")  # formulário maior

# Fonte padrão
fonte_padrao = ("Arial", 14)

# =========================
# Variável do CheckButton
# =========================

notif_var = tk.IntVar()

# =========================
# CheckButton
# =========================

check = tk.Checkbutton(
    janela,
    text="Receber notificações",
    variable=notif_var,
    command=atualizar_check,
    font=fonte_padrao
)
check.pack(pady=12)

# =========================
# Listbox
# =========================

tk.Label(
    janela,
    text="Escolha o setor:",
    font=fonte_padrao
).pack()

listbox = tk.Listbox(
    janela,
    height=4,
    font=fonte_padrao
)
listbox.pack(pady=8)

setores = ["Financeiro", "Comercial", "TI", "RH"]
for setor in setores:
    listbox.insert(tk.END, setor)

listbox.bind("<<ListboxSelect>>", atualizar_lista)

# =========================
# Labels de resultado
# =========================

label_check = tk.Label(
    janela,
    text="Status notificações: Desativadas",
    font=fonte_padrao
)
label_check.pack(pady=12)

label_lista = tk.Label(
    janela,
    text="Setor escolhido: Nenhum",
    font=fonte_padrao
)
label_lista.pack()

# =========================
# Área de log (tipo textarea)
# =========================

tk.Label(
    janela,
    text="Log de ações:",
    font=fonte_padrao
).pack(pady=8)

log_text = tk.Text(
    janela,
    height=7,
    width=48,
    font=fonte_padrao
)
log_text.pack(padx=12, pady=8)

janela.mainloop()

