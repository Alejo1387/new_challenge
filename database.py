import sqlite3

# create the archive if not is create or also is the conexion
conexion = sqlite3.connect("mi_base.db")

# it is for modificate archive
cursor = conexion.cursor()

# for create a table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS companies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        api_key TEXT NOT NULL
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS qrs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tenant_id INTEGER NOT NULL,
        logo_name TEXT NOT NULL,
        qr_name TEXT NOT NULL,
        destination_url TEXT NOT NULL,
        server_url TEXT NOT NULL,
        unique_id TEXT NOT NULL UNIQUE,
               
        FOREIGN KEY (tenant_id) REFERENCES companies(id)
            ON DELETE CASCADE
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS users_scam (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_unique TEXT NOT NULL,
        ip TEXT NOT NULL,
        device TEXT,
        country TEXT,
        city TEXT,
        latitude REAL,
        longitude REAL,
        datetime TEXT DEFAULT CURRENT_TIMESTAMP,
        
        FOREIGN KEY (id_unique) REFERENCES qrs(unique_id)
            ON DELETE CASCADE
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS geo_registers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_users_scam INTEGER NOT NULL,
        country TEXT,
        city TEXT,
        latitude REAL,
        longitude REAL,
        
        FOREIGN KEY (id_users_scam) REFERENCES users_scam(id)
            ON DELETE CASCADE
    );
""")

"""Examples"""
# # for insert
# cursor.execute("INSERT INTO usuarios (nombre, edad) VALUES (?, ?)", ("Alejandro", 20))
# cursor.execute("INSERT INTO usuarios (nombre, edad) VALUES (?, ?)", ("Maria", 22))

# # for select
# print("\nUsuarios:")
# cursor.execute("SELECT * FROM usuarios")
# for fila in cursor.fetchall():
#     print(fila)

# # for update
# cursor.execute("UPDATE usuarios SET edad = ? WHERE nombre = ?", (21, "Alejandro"))

# # for delete
# cursor.execute("DELETE FROM usuarios WHERE nombre = ?", ("Alejandro",))

# print("\nUsuarios:")
# cursor.execute("SELECT * FROM usuarios")
# for fila in cursor.fetchall():
#     print(fila)

# for save
conexion.commit()

# for close
conexion.close()