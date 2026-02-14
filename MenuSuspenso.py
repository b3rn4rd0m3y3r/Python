import tkinter as tk

# =========================
# Função de resposta ao clique
# =========================

def menu_clicado(ordem_menu, ordem_item):
    if ordem_menu == 1:
        texto_menu = "primeiro"
    else:
        texto_menu = "segundo"

    label_resultado.config(
        text=f"Você clicou no {texto_menu} menu, item {ordem_item}"
    )

# =========================
# Janela principal
# =========================

janela = tk.Tk()
janela.title("Aula 34 - Menu Suspenso")
janela.geometry("600x400")

fonte_padrao = ("Arial", 14)

# =========================
# Barra de Menu
# =========================

barra_menu = tk.Menu(janela)
janela.config(menu=barra_menu)

# =========================
# Primeiro Menu (3 itens)
# =========================

menu1 = tk.Menu(barra_menu, tearoff=0, font=fonte_padrao)
barra_menu.add_cascade(label="Menu 1", menu=menu1)

menu1.add_command(label="1.1", command=lambda: menu_clicado(1, 1))
menu1.add_command(label="1.2", command=lambda: menu_clicado(1, 2))
menu1.add_command(label="1.3", command=lambda: menu_clicado(1, 3))

# =========================
# Segundo Menu (4 itens)
# =========================

menu2 = tk.Menu(barra_menu, tearoff=0, font=fonte_padrao)
barra_menu.add_cascade(label="Menu 2", menu=menu2)

menu2.add_command(label="2.1", command=lambda: menu_clicado(2, 1))
menu2.add_command(label="2.2", command=lambda: menu_clicado(2, 2))
menu2.add_command(label="2.3", command=lambda: menu_clicado(2, 3))
menu2.add_command(label="2.4", command=lambda: menu_clicado(2, 4))

# =========================
# Label de Resultado
# =========================

label_resultado = tk.Label(
    janela,
    text="Clique em um item do menu acima",
    font=fonte_padrao
)

label_resultado.pack(expand=True)

janela.mainloop()
