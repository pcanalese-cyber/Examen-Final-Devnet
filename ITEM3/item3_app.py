from flask import Flask, request, redirect, url_for
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

DB_NAME = "usuarios.db"

# ---------------------------
# Funciones de base de datos
# ---------------------------
def get_conn():
    return sqlite3.connect(DB_NAME)

def init_db_if_needed():
    """
    Crea la tabla usuarios si aún no existe.
    Permite que la app funcione incluso si db_setup.py no se ejecutó.
    """
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
    );
    """)
    conn.commit()
    conn.close()

# ---------------------------
# Ruta principal
# ---------------------------
@app.route("/")
def index():
    return """
    <h1>ITEM 3 - Sitio Web DEVNET</h1>
    <p>Servidor Flask funcionando correctamente en puerto 5800.</p>
    <ul>
        <li><a href="/registro">Registro de usuario</a></li>
        <li><a href="/login">Login</a></li>
    </ul>
    """

# ---------------------------
# Registro de usuarios
# ---------------------------
@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return "Debe completar todos los campos. <a href='/registro'>Volver</a>"

        password_hash = generate_password_hash(password)

        try:
            conn = get_conn()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO usuarios (username, password_hash) VALUES (?, ?)",
                (username, password_hash)
            )
            conn.commit()
            conn.close()
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            return "Usuario ya existe. <a href='/registro'>Volver</a>"

    return """
    <h2>Registro de Usuario</h2>
    <form method="post">
        Username:<br>
        <input type="text" name="username"><br><br>
        Password:<br>
        <input type="password" name="password"><br><br>
        <input type="submit" value="Registrar">
    </form>
    <br>
    <a href="/">Volver al inicio</a>
    """

# ---------------------------
# Login
# ---------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT password_hash FROM usuarios WHERE username = ?",
            (username,)
        )
        result = cursor.fetchone()
        conn.close()

        if result and check_password_hash(result[0], password):
            return f"<h2>Login exitoso</h2><p>Bienvenido, {username}</p><a href='/'>Volver al inicio</a>"
        else:
            return "Credenciales incorrectas. <a href='/login'>Volver</a>"

    return """
    <h2>Login</h2>
    <form method="post">
        Username:<br>
        <input type="text" name="username"><br><br>
        Password:<br>
        <input type="password" name="password"><br><br>
        <input type="submit" value="Ingresar">
    </form>
    <br>
    <a href="/">Volver al inicio</a>
    """

# ---------------------------
# Main
# ---------------------------
if __name__ == "__main__":
    init_db_if_needed()
    app.run(host="0.0.0.0", port=5800, debug=True)
