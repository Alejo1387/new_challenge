import sqlite3

# create the archive if not is create or also is the conexion
conexion = sqlite3.connect("mi_base.db")

# it is for modificate archive
cursor = conexion.cursor()

# for create a table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        edad INTEGER
    )
""")

# for insert
cursor.execute("INSERT INTO usuarios (nombre, edad) VALUES (?, ?)", ("Alejandro", 20))
cursor.execute("INSERT INTO usuarios (nombre, edad) VALUES (?, ?)", ("Maria", 22))

# for select
print("\nUsuarios:")
cursor.execute("SELECT * FROM usuarios")
for fila in cursor.fetchall():
    print(fila)

# for update
cursor.execute("UPDATE usuarios SET edad = ? WHERE nombre = ?", (21, "Alejandro"))

# for delete
cursor.execute("DELETE FROM usuarios WHERE nombre = ?", ("Alejandro",))

print("\nUsuarios:")
cursor.execute("SELECT * FROM usuarios")
for fila in cursor.fetchall():
    print(fila)

# for save
conexion.commit()

# for close
conexion.close()