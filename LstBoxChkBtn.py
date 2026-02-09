import tkinter as tk

# =========================
# Funções de resposta
# =========================

def atualizar_check():
    if notif_var.get() == 1:
        label_check.config(text="Status notificações: Ativadas")
    else:
        label_check.config(text="Status notificações: Desativadas")

def atualizar_lista(event):
    selecao = listbox.curselection()
    if selecao:
        setor = listbox.get(selecao[0])
        label_lista.config(text=f"Setor escolhido: {setor}")

# =========================
# Janela principal
# =========================

janela = tk.Tk()
janela.title("Controles de Seleção")
janela.geometry("560x400")

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
    font=("Arial", 14, "bold"),
    variable=notif_var,
    command=atualizar_check
)
check.pack(pady=10)

# =========================
# Listbox
# =========================

tk.Label(janela, font=("Arial", 14, "bold"), text="Escolha o setor:").pack()

listbox = tk.Listbox(janela, font=("Arial", 14, "bold"), height=4)
listbox.pack(pady=5)

setores = ["Financeiro", "Comercial", "TI", "RH"]
for setor in setores:
    listbox.insert(tk.END, setor)

listbox.bind("<<ListboxSelect>>", atualizar_lista)

# =========================
# Labels de resultado
# =========================

label_check = tk.Label(janela, font=("Arial", 14, "bold"), text="Status notificações: Desativadas")
label_check.pack(pady=10)

label_lista = tk.Label(janela, font=("Arial", 14, "bold"), text="Setor escolhido: Nenhum")
label_lista.pack()

janela.mainloop()
