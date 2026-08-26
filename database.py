import sqlite3 #Biblioteca 
conexao = sqlite3.connect('/home/ckalves/OneDrive/Caike/Estudos/controle_ronda/banco.db') #caminho do banco de dados
cursor = conexao.cursor() #executar algo no banco de dados

#cria o banco de dados de nao tiver e cria a tabela  usuario e suas linhas com os atributos
cursor.execute("""
CREATE TABLE IF NOT EXISTS carros(
    id INTEGER PRIMARY KEY,
    nome TEXT,
    marca TEXT,
    modelo TEXT,
    odometro_atual INTWGER,
    ano INTEGER
)
""")

conexao.commit() #salva a alteração

#inserir valor nas linhas
cursor.execute(""" 
INSERT INTO carros (nome, marca)
VALUES (?,?)
""", ("City", 2017))

conexao.commit()

#selecionar linha x
cursor.execute("""
SELECT * FROM usuario WHERE idade = 25
""")
pesquisa = cursor.fetchall() #resposta da pesquisa

print(pesquisa) 