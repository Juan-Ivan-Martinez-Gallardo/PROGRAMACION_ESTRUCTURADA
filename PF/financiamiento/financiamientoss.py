from conexionBD import conectar

def _obtener_producto_por_id(pid):
    conn = conectar()
    if not conn: return None
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT id, nombre, precio, stock FROM productos WHERE id=%s", (pid,))
        return cur.fetchone()
    finally:
        cur.close(); conn.close()

def _calcular_mensualidad(precio, enganche, meses, tasa_anual):
    monto = max(precio - enganche, 0.0)
    if meses <= 0: 
        return round(monto, 2)
    i = (tasa_anual / 100.0) / 12.0
    if i == 0:
        return round(monto / meses, 2)
    cuota = monto * (i * (1 + i) ** meses) / ((1 + i) ** meses - 1)
    return round(cuota, 2)

def financiar_producto(usuario_id, producto_id, enganche, meses, tasa):
    """Registra un financiamiento y devuelve (True, mensualidad) o (False, mensaje_error)."""
    prod = _obtener_producto_por_id(producto_id)
    if not prod:
        return False, "Producto no encontrado."
    if meses <= 0 or tasa < 0:
        return False, "Datos inválidos."
    mensualidad = _calcular_mensualidad(float(prod["precio"]), float(enganche), int(meses), float(tasa))

    conn = conectar()
    if not conn: 
        return False, "Sin conexión a BD."
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO financiamientos (usuario_id, producto_id, enganche, meses, tasa, mensualidad) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (usuario_id, producto_id, enganche, meses, tasa, mensualidad)
        )
        conn.commit()
        return True, mensualidad
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        cur.close(); conn.close()

    if meses <= 0 or tasa < 0 or enganche < 0:
        return False, "Datos inválidos."
    if enganche >= float(prod["precio"]):
        return False, "Enganche debe ser menor al precio."

