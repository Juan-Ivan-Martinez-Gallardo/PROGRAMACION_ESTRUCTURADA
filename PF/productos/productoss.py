# productos/productoss.py
from conexionBD import conectar

def crear(codigo, nombre, categoria, precio, stock, usuario_id):
    conn = conectar()
    if not conn: return False
    try:
        cur = conn.cursor()
        sql = ("INSERT INTO productos (codigo, nombre, categoria, precio, stock, fecha_actualizacion, usuario_id) "
               "VALUES (%s, %s, %s, %s, %s, NOW(), %s)")
        cur.execute(sql, (codigo, nombre, categoria, precio, stock, usuario_id))
        conn.commit()
        return True
    except Exception as e:
        print(f"[Productos] Error al crear: {e}")
        conn.rollback()
        return False
    finally:
        cur.close(); conn.close()

def listar():
    conn = conectar()
    if not conn: return []
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT id, codigo, nombre, categoria, precio, stock FROM productos ORDER BY nombre")
        return cur.fetchall()
    except Exception as e:
        print(f"[Productos] Error al listar: {e}")
        return []
    finally:
        cur.close(); conn.close()

def buscar(codigo):
    conn = conectar()
    if not conn: return None
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT id, codigo, nombre, categoria, precio, stock FROM productos WHERE codigo=%s", (codigo,))
        return cur.fetchone()
    except Exception as e:
        print(f"[Productos] Error al buscar: {e}")
        return None
    finally:
        cur.close(); conn.close()

def obtener_por_id(pid):
    conn = conectar()
    if not conn: return None
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT id, codigo, nombre, categoria, precio, stock FROM productos WHERE id=%s", (pid,))
        return cur.fetchone()
    except Exception as e:
        print(f"[Productos] Error al obtener por id: {e}")
        return None
    finally:
        cur.close(); conn.close()

def actualizar_stock(codigo, nuevo_stock):
    conn = conectar()
    if not conn: return False
    try:
        cur = conn.cursor()
        cur.execute("UPDATE productos SET stock=%s, fecha_actualizacion=NOW() WHERE codigo=%s",
                    (nuevo_stock, codigo))
        conn.commit()
        return cur.rowcount > 0
    except Exception as e:
        print(f"[Productos] Error al actualizar stock: {e}")
        conn.rollback()
        return False
    finally:
        cur.close(); conn.close()

def modificar(codigo, nombre, categoria, precio):
    """Modifica nombre/categoría/precio por código."""
    conn = conectar()
    if not conn: return False
    try:
        cur = conn.cursor()
        cur.execute(
            "UPDATE productos SET nombre=%s, categoria=%s, precio=%s, fecha_actualizacion=NOW() WHERE codigo=%s",
            (nombre, categoria, precio, codigo)
        )
        conn.commit()
        return cur.rowcount > 0
    except Exception as e:
        print(f"[Productos] Error al modificar: {e}")
        conn.rollback()
        return False
    finally:
        cur.close(); conn.close()

def eliminar(codigo):
    """Borrado físico por código (si quieres baja lógica, cambia a un campo 'activo')."""
    conn = conectar()
    if not conn: return False
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM productos WHERE codigo=%s", (codigo,))
        conn.commit()
        return cur.rowcount > 0
    except Exception as e:
        print(f"[Productos] Error al eliminar: {e}")
        conn.rollback()
        return False
    finally:
        cur.close(); conn.close()
