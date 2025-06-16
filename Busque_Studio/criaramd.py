import mysql.connector

# Conectar e inserir direto
conexao = mysql.connector.connect(
    host="localhost",
    user="root", 
    password="",
    database="busquestudios2"
)

cursor = conexao.cursor()

# Inserir admin
sql = "INSERT INTO administrador (id_perfil, nome, email, login, senha) VALUES (%s, %s, %s, %s, %s)"
cursor.execute(sql, (1, "Admin BusqueStudios", "admin@busque.com", "admbusque", "123"))
conexao.commit()

print("Admin criado: login=admbusque, senha=123")

cursor.close()
conexao.close()