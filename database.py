import sqlite3
import os

# Caminho do banco de dados (fica na mesma pasta deste arquivo)
CAMINHO_BANCO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "banco.db")


def conectar():
    """Abre uma conexão com o banco de dados."""
    conexao = sqlite3.connect(CAMINHO_BANCO)
    conexao.execute("PRAGMA foreign_keys = ON")  # ativa a checagem de chave estrangeira
    return conexao


def criar_tabelas():
    """Cria as tabelas do banco, se ainda não existirem."""
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS carros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            marca TEXT,
            modelo TEXT,
            ano INTEGER,
            odometro_atual REAL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS abastecimentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            carro_id INTEGER NOT NULL,
            data TEXT NOT NULL,
            km REAL NOT NULL,
            litros REAL NOT NULL,
            preco_litro REAL NOT NULL,
            total REAL NOT NULL,
            posto TEXT,
            tanque_cheio INTEGER DEFAULT 1,
            FOREIGN KEY (carro_id) REFERENCES carros(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS manutencoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            carro_id INTEGER NOT NULL,
            data TEXT NOT NULL,
            km REAL NOT NULL,
            tipo TEXT NOT NULL,
            descricao TEXT,
            custo REAL NOT NULL,
            FOREIGN KEY (carro_id) REFERENCES carros(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS gastos_gerais (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            carro_id INTEGER NOT NULL,
            data TEXT NOT NULL,
            categoria TEXT NOT NULL,
            descricao TEXT,
            valor REAL NOT NULL,
            FOREIGN KEY (carro_id) REFERENCES carros(id)
        )
    """)

    conexao.commit()
    conexao.close()


# ---------------- CARROS ----------------

def adicionar_carro(nome, marca, modelo, ano, odometro_atual):
    """Cadastra um carro novo e devolve o id dele."""
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        INSERT INTO carros (nome, marca, modelo, ano, odometro_atual)
        VALUES (?, ?, ?, ?, ?)
    """, (nome, marca, modelo, ano, odometro_atual))
    conexao.commit()
    novo_id = cursor.lastrowid
    conexao.close()
    return novo_id


def listar_carros():
    """Devolve todos os carros cadastrados."""
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM carros")
    resultado = cursor.fetchall()
    conexao.close()
    return resultado


# ---------------- ABASTECIMENTOS ----------------

def adicionar_abastecimento(carro_id, data, km, litros, preco_litro, posto, tanque_cheio=1):
    """Cadastra um abastecimento vinculado a um carro. O total é calculado aqui dentro."""
    total = round(litros * preco_litro, 2)
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        INSERT INTO abastecimentos (carro_id, data, km, litros, preco_litro, total, posto, tanque_cheio)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (carro_id, data, km, litros, preco_litro, total, posto, tanque_cheio))
    conexao.commit()
    conexao.close()
    return total


def listar_abastecimentos(carro_id):
    """Devolve os abastecimentos de um carro específico, do mais antigo pro mais novo."""
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT * FROM abastecimentos WHERE carro_id = ? ORDER BY km ASC
    """, (carro_id,))
    resultado = cursor.fetchall()
    conexao.close()
    return resultado


# ---------------- MANUTENÇÕES ----------------

def adicionar_manutencao(carro_id, data, km, tipo, descricao, custo):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        INSERT INTO manutencoes (carro_id, data, km, tipo, descricao, custo)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (carro_id, data, km, tipo, descricao, custo))
    conexao.commit()
    conexao.close()


def listar_manutencoes(carro_id):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT * FROM manutencoes WHERE carro_id = ? ORDER BY data DESC
    """, (carro_id,))
    resultado = cursor.fetchall()
    conexao.close()
    return resultado


# ---------------- GASTOS GERAIS ----------------

def adicionar_gasto(carro_id, data, categoria, descricao, valor):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        INSERT INTO gastos_gerais (carro_id, data, categoria, descricao, valor)
        VALUES (?, ?, ?, ?, ?)
    """, (carro_id, data, categoria, descricao, valor))
    conexao.commit()
    conexao.close()


def listar_gastos(carro_id):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT * FROM gastos_gerais WHERE carro_id = ? ORDER BY data DESC
    """, (carro_id,))
    resultado = cursor.fetchall()
    conexao.close()
    return resultado