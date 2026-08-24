import sqlite3
conexao = sqlite3.connect('/home/ckalves/OneDrive/Caike/Estudos/controle_ronda/banco.db')
cursor = conexao.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS usuario(
    id INTEGER PRIMARY KEY,
    nome TEXT,
    idade INTEGER
)
""")

conexao.commit()

print('Tabela feita')

cursor.execute("""
INSERT INTO usuario (nome, idade)
VALUES (?, ?)
""", ("Caike", 25))

conexao.commit()

cursor.execute("""
SELECT * FROM usuario WHERE idade = 25
""")
pesquisa = cursor.fetchall()

print(pesquisa)