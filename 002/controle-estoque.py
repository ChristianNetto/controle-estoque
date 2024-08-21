import tkinter as tk
from tkinter import messagebox
import sqlite3

#criando banco de dados, ou utilizando um já criado(conexão)
conn = sqlite3.connect('estoque.db')
cursor = conn.cursor()

#tabela produtos
cursor.execute('''
CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    preco REAL NOT NULL,
    quantidade INTEGER NOT NULL
)
''')
conn.commit()
conn.close()

#janela prin
root = tk.Tk()
root.title("Controle de Estoque")
root.geometry("300x250")

#nome_prod
tk.Label(root, text="Nome do Produto").grid(row=0, column=0)
entry_nome = tk.Entry(root)
entry_nome.grid(row=0, column=1)

#preço_prod
tk.Label(root, text="Preço").grid(row=1, column=0)
entry_preco = tk.Entry(root)
entry_preco.grid(row=1, column=1)

#quant_prod
tk.Label(root, text="Quantidade").grid(row=2, column=0)
entry_quantidade = tk.Entry(root)
entry_quantidade.grid(row=2, column=1)

#excluir produto
tk.Label(root, text="ID do Produto").grid(row=5, column=0)
entry_id = tk.Entry(root)
entry_id.grid(row=5, column=1)

#adc produtos no banco de dados
def adicionar_produto():
    nome = entry_nome.get()
    preco = float(entry_preco.get())
    quantidade = int(entry_quantidade.get())

    conn = sqlite3.connect('estoque.db')
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO produtos (nome, preco, quantidade) VALUES (?, ?, ?)
    ''', (nome, preco, quantidade))

    conn.commit()
    conn.close()

    messagebox.showinfo("Sucesso", f"Produto {nome} adicionado com sucesso!")

    entry_nome.delete(0, tk.END)
    entry_preco.delete(0, tk.END)
    entry_quantidade.delete(0, tk.END)

#listar produtos
def listar_produtos():
    conn = sqlite3.connect('estoque.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM produtos')
    produtos = cursor.fetchall()

    conn.close()

    lista_produtos = ""
    for produto in produtos:
        lista_produtos += f"ID: {produto[0]}, Nome: {produto[1]}, Preço: R${produto[2]}, Quantidade: {produto[3]}\n"

    messagebox.showinfo("Produtos em Estoque", lista_produtos)

#Excluir produto banco de dados
def excluir_produto():
    produto_id = entry_id.get()

    if not produto_id:
        messagebox.showerror("Erro", "Por favor, insira o ID do produto a ser excluído.")
        return

    conn = sqlite3.connect('estoque.db')
    cursor = conn.cursor()

    # Verifica se o produto existe
    cursor.execute('SELECT * FROM produtos WHERE id = ?', (produto_id,))
    produto = cursor.fetchone()

    if produto is None:
        conn.close()
        messagebox.showerror("Erro", "Produto não encontrado.")
    else:
        cursor.execute('DELETE FROM produtos WHERE id = ?', (produto_id,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Sucesso", f"Produto com ID {produto_id} excluído com sucesso!")
        entry_id.delete(0, tk.END)


# Botão para adicionar produto
tk.Button(root, text="Adicionar Produto", command=adicionar_produto).grid(row=3, column=1)

# Botão para listar produtos
tk.Button(root, text="Listar Produtos", command=listar_produtos).grid(row=4, column=1)

# Botão para excluir produto
tk.Button(root, text="Excluir Produto", command=excluir_produto).grid(row=6, column=1)

# Iniciando o loop da aplicação
root.mainloop()
