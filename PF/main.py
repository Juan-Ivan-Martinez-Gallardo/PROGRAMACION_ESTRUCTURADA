from funciones import *
from conexionBD import reiniciar_tabla
from usuarios import usuarioss
from productos import productoss
from ventas import ventass
from financiamiento import financiamientoss
import getpass

def imprimir_catalogo(productos):
    if not productos:
        print("\nNo hay productos registrados.")
        return
    print("\nCATÁLOGO DE PRODUCTOS:")
    print(f"{'ID':<5}{'Código':<15}{'Nombre':<22}{'Precio':>12}{'Stock':>8}")
    print("-" * 70)
    for p in productos:
        print(f"{p['id']:<5}{p['codigo']:<15}{p['nombre'][:20]:<22}{formatear_precio(p['precio']):>12}{p['stock']:>8}")

def _to_float_limpio(txt: str) -> float:
    """Convierte '2%', '$1,234.50', '1.234,50' a float 2.0, 1234.50, 1234.50."""
    t = txt.strip()
    # quitar símbolos comunes
    for ch in ['%', '$', ' ']:
        t = t.replace(ch, '')
    # estandarizar separadores decimales
    # si tiene coma y punto, asumo formato 1,234.56 -> quitar comas
    if ',' in t and '.' in t:
        t = t.replace(',', '')
    else:
        # si solo tiene coma, asumo decimal con coma -> cambiar a punto
        t = t.replace(',', '.')
    return float(t)

def _to_int_limpio(txt: str) -> int:
    return int(txt.strip().replace(',', '').replace(' ', ''))

def menu_inventario():
    borrar_pantalla()
    print("\n" + "=" * 50)
    print(" MENÚ PRINCIPAL - COOPPEL")
    print("=" * 50)
    print("1. Realizar venta")
    print("2. Registrar producto")
    print("3. Modificar producto")
    print("4. Eliminar producto")
    print("5. Listar productos")
    print("6. Financiar producto")
    print("7. Buscar producto")
    print("8. Actualizar stock")
    print("9. Menú de administración de tablas")
    print("10. Cerrar sesión")
    return input("\nSeleccione una opción: ")

def main():
    usuario_actual = None

    while True:
        if not usuario_actual:
            # --- Menú de bienvenida ---
            borrar_pantalla()
            print("\n" + "=" * 50)
            print(" SISTEMA GESTIÓN COOPPEL ")
            print("=" * 50)
            print("1. Iniciar sesión")
            print("2. Registrar usuario")
            print("3. Salir")
            opcion = input("\nSeleccione una opción: ")

            if opcion == "1":
                borrar_pantalla()
                print("\n" + "=" * 50)
                print(" INICIO DE SESIÓN")
                print("=" * 50)
                email = input("Email: ").strip()
                contrasena = getpass.getpass("Contraseña: ").strip()
                usuario_actual = usuarioss.autenticar_usuario(email, contrasena)
                if usuario_actual:
                    print(f"\nBienvenido {usuario_actual['nombre']}!")
                else:
                    print("\n❌ Credenciales incorrectas")
                esperar_tecla()

            elif opcion == "2":
                borrar_pantalla()
                print("\n" + "=" * 50)
                print(" REGISTRO DE USUARIO")
                print("=" * 50)
                nombre = input("Nombre: ").strip().title()
                apellido = input("Apellido: ").strip().title()
                email = input("Email: ").strip().lower()
                contrasena = getpass.getpass("Contraseña: ").strip()
                ok = usuarioss.registrar_usuario(nombre, apellido, email, contrasena)
                print("\n✅ Usuario registrado exitosamente!" if ok else "\n❌ Error al registrar usuario")
                esperar_tecla()

            elif opcion == "3":
                print("\n¡Hasta pronto! 🍻")
                break
            else:
                print("\n❌ Opción inválida"); esperar_tecla()

        else:
            # --- Menú principal autenticado ---
            opcion = menu_inventario()

            if opcion == "1":  # Realizar venta
                borrar_pantalla()
                print("\n" + "=" * 50)
                print(" REGISTRAR VENTA")
                print("=" * 50)
                productos = productoss.listar()
                print("\nPRODUCTOS DISPONIBLES:")
                print(f"{'ID':<5}{'Nombre':<20}{'Precio':<10}{'Stock':<10}")
                print("-" * 45)
                for p in productos:
                    print(f"{p['id']:<5}{p['nombre'][:18]:<20}{formatear_precio(p['precio']):<10}{p['stock']:<10}")

                seleccion = []
                while True:
                    try:
                        print("\n" + "-" * 50)
                        pid = int(input("ID del producto (0 para terminar): "))
                        if pid == 0:
                            break
                        prod = next((x for x in productos if x['id'] == pid), None)
                        if not prod:
                            print("❌ ID no válido"); continue
                        cant = int(input(f"Cantidad de {prod['nombre']} (disp {prod['stock']}): "))
                        if cant <= 0: print("❌ Cantidad inválida"); continue
                        if cant > prod['stock']: print(f"❌ Stock insuficiente ({prod['stock']})"); continue
                        prod['stock'] -= cant
                        seleccion.append({'id': prod['id'], 'cantidad': cant, 'precio': prod['precio']})
                        print(f"✅ Añadido: {cant} x {prod['nombre']}")
                    except ValueError:
                        print("❌ Ingresa un número"); continue

                if seleccion:
                    ok = ventass.registrar_venta(usuario_actual['id'], seleccion)
                    if ok:
                        print("\n✅ Venta registrada!")
                        total = sum(x['cantidad']*x['precio'] for x in seleccion)
                        print(f"TOTAL: {formatear_precio(total)}")
                    else:
                        print("\n❌ Error al registrar venta")
                else:
                    print("\n⚠️ No se seleccionaron productos")
                esperar_tecla()

            elif opcion == "2":  # Registrar producto
                borrar_pantalla()
                print("\n" + "=" * 50)
                print(" REGISTRO DE PRODUCTO")
                print("=" * 50)
                codigo = input("Código de barras: ").strip()
                nombre = input("Nombre del producto: ").strip().title()
                categoria = input("Categoría: ").strip().title()
                precio = float(input("Precio unitario: $"))
                stock = int(input("Stock inicial: "))
                ok = productoss.crear(codigo, nombre, categoria, precio, stock, usuario_actual['id'])
                print("\n✅ Producto registrado!" if ok else "\n❌ Error al registrar producto")
                esperar_tecla()

            elif opcion == "3":  # Modificar producto
                borrar_pantalla()
                print("\n" + "=" * 50)
                print(" MODIFICAR PRODUCTO")
                print("=" * 50)
                # Mostrar catálogo antes
                lista = productoss.listar()
                imprimir_catalogo(lista)
                codigo = input("\nCódigo de barras a modificar: ").strip()
                prod = productoss.buscar(codigo)
                if not prod:
                    print("\n❌ Producto no encontrado"); esperar_tecla(); continue
                print(f"\nActual: {prod['nombre']} | {prod['categoria']} | {formatear_precio(prod['precio'])}")
                nuevo_nombre = input(f"Nuevo nombre ({prod['nombre']}): ").strip() or prod['nombre']
                nueva_cat    = input(f"Nueva categoría ({prod['categoria']}): ").strip() or prod['categoria']
                precio_in    = input(f"Nuevo precio ({prod['precio']}): ").strip()
                nuevo_precio = float(precio_in) if precio_in else float(prod['precio'])
                ok = productoss.modificar(codigo, nuevo_nombre, nueva_cat, nuevo_precio)
                print("\n✅ Producto actualizado!" if ok else "\n❌ No se pudo actualizar")
                esperar_tecla()

            elif opcion == "4":  # Eliminar producto
                borrar_pantalla()
                print("\n" + "=" * 50)
                print(" ELIMINAR PRODUCTO")
                print("=" * 50)

                lista = productoss.listar()
                if not lista:
                    print("\nNo hay productos registrados.")
                    esperar_tecla()
                    continue

                termino = input("\nFiltrar por nombre o código (ENTER para ver todos): ").strip().lower()
                if termino:
                    lista = [p for p in lista if termino in p['nombre'].lower() or termino in p['codigo'].lower()]
                    if not lista:
                        print("\nNo hay coincidencias con ese filtro.")
                        esperar_tecla()
                        continue

                imprimir_catalogo(lista)

                codigo = input("\nCódigo de barras a eliminar: ").strip()
                prod = productoss.buscar(codigo)
                if not prod:
                    print("\n❌ Producto no encontrado")
                    esperar_tecla()
                    continue

                print(f"\nVas a eliminar: {prod['nombre']} ({codigo})")
                conf = input("¿Confirmar? (s/n): ").lower().startswith("s")
                if not conf:
                    print("\nOperación cancelada.")
                else:
                    ok = productoss.eliminar(codigo)
                    print("\n✅ Eliminado" if ok else "\n❌ No se pudo eliminar (revisa ventas/detalles vinculados)")
                esperar_tecla()

            elif opcion == "5":  # Listar productos  🔹 (agregado)
                borrar_pantalla()
                print("\n" + "=" * 90)
                print(" LISTAR PRODUCTOS")
                print("=" * 90)
                # filtro opcional
                lista = productoss.listar()
                termino = input("\nFiltrar por nombre o código (ENTER para ver todos): ").strip().lower()
                if termino:
                    lista = [p for p in lista if termino in p['nombre'].lower() or termino in p['codigo'].lower()]
                imprimir_catalogo(lista)
                print("=" * 90)
                esperar_tecla()

            elif opcion == "6":  # Financiar producto
                borrar_pantalla()
                print("\n" + "=" * 50)
                print(" FINANCIAR PRODUCTO")
                print("=" * 50)
                lista = productoss.listar()
                if not lista:
                    print("\nNo hay productos para financiar."); esperar_tecla(); continue

                print("\nPRODUCTOS:")
                for p in lista:
                    print(f"[{p['id']}] {p['nombre']}  ${p['precio']}  stock={p['stock']}")
                try:
                    pid   = _to_int_limpio(input("\nID del producto a financiar: "))
                    eng   = _to_float_limpio(input("Enganche: "))
                    meses = _to_int_limpio(input("Meses: "))
                    tasa  = _to_float_limpio(input("Tasa anual (%): "))
                except ValueError:
                    print("\n❌ Datos inválidos (usa números, puedes escribir 2 o 2%)")
                    esperar_tecla()
                    continue

                # Validaciones de cortesía
                prod = next((x for x in lista if x['id'] == pid), None)
                if not prod:
                    print("\n❌ Producto no encontrado"); esperar_tecla(); continue
                if eng < 0 or eng >= float(prod['precio']):
                    print("\n❌ Enganche debe ser >= 0 y menor al precio del producto")
                    esperar_tecla(); continue
                if meses <= 0:
                    print("\n❌ Meses debe ser mayor a 0")
                    esperar_tecla(); continue
                if tasa < 0:
                    print("\n❌ La tasa no puede ser negativa")
                    esperar_tecla(); continue

                ok, info = financiamientoss.financiar_producto(usuario_actual['id'], pid, eng, meses, tasa)
                if ok:
                    print(f"\n✅ Financiamiento registrado. Mensualidad: {formatear_precio(info)}")
                else:
                    print(f"\n❌ Error: {info}")
                esperar_tecla()


            elif opcion == "7":  # Buscar producto
                borrar_pantalla()
                print("\n" + "=" * 50)
                print(" BUSCAR PRODUCTO")
                print("=" * 50)
                codigo = input("Código de barras: ").strip()
                prod = productoss.buscar(codigo)
                if prod:
                    print(f"\nCódigo: {prod['codigo']}")
                    print(f"Nombre: {prod['nombre']}")
                    print(f"Categoría: {prod['categoria']}")
                    print(f"Precio: {formatear_precio(prod['precio'])}")
                    print(f"Stock: {prod['stock']}")
                else:
                    print("\n❌ Producto no encontrado")
                esperar_tecla()

            elif opcion == "8":  # Actualizar stock
                borrar_pantalla()
                print("\n" + "=" * 50)
                print(" ACTUALIZAR STOCK")
                print("=" * 50)
                # mostrar catálogo para ayudar
                imprimir_catalogo(productoss.listar())
                codigo = input("\nCódigo de barras: ").strip()
                try:
                    nuevo_stock = int(input("Nuevo stock: "))
                except ValueError:
                    print("\n❌ Stock inválido"); esperar_tecla(); continue
                ok = productoss.actualizar_stock(codigo, nuevo_stock)
                print("\n✅ Stock actualizado!" if ok else "\n❌ Error al actualizar")
                esperar_tecla()

            elif opcion == "9":  # Administración
                while True:
                    op = menu_admin()
                    if op == "1":
                        print("\nReiniciando tabla productos (detalle_venta -> ventas -> productos)...")
                        ok = reiniciar_tabla("detalle_venta") and reiniciar_tabla("ventas") and reiniciar_tabla("productos")
                        print("\n✅ Tabla(s) reiniciada(s)" if ok else "\n❌ Error al reiniciar"); esperar_tecla()
                    elif op == "2":
                        print("\nReiniciando tabla ventas (detalle_venta -> ventas)...")
                        ok = reiniciar_tabla("detalle_venta") and reiniciar_tabla("ventas")
                        print("\n✅ Tabla(s) reiniciada(s)" if ok else "\n❌ Error al reiniciar"); esperar_tecla()
                    elif op == "3":
                        print("\nReiniciando tabla detalle_venta...")
                        ok = reiniciar_tabla("detalle_venta")
                        print("\n✅ Tabla reiniciada" if ok else "\n❌ Error al reiniciar"); esperar_tecla()
                    elif op == "4":
                        print("\nReiniciando tabla usuarios...")
                        ok = reiniciar_tabla("usuarios")
                        print("\n✅ Tabla reiniciada" if ok else "\n❌ Error al reiniciar"); esperar_tecla()
                    elif op == "5":
                        borrar_pantalla()
                        print("\n" + "=" * 50)
                        print(" EXPORTAR DATOS")
                        print("=" * 50)
                        print("1. Usuarios\n2. Productos\n3. Ventas\n4. Detalle de Ventas\n5. Volver")
                        sub = input("\nSeleccione tabla: ")
                        if sub == "5": continue
                        mapa = {"1":"usuarios","2":"productos","3":"ventas","4":"detalle_venta"}
                        tabla = mapa.get(sub)
                        if not tabla: print("\n❌ Opción inválida"); esperar_tecla(); continue
                        print("\nFormato: 1=Excel  2=PDF")
                        fmt = input("Seleccione formato: ")
                        formatos = {"1":"excel","2":"pdf"}
                        archivo = exportar_tabla(tabla, formatos.get(fmt))
                        if archivo: print(f"\n✅ Exportado: {archivo}")
                        else: print("\n❌ Error al exportar (¿tabla vacía?)")
                        esperar_tecla()
                    elif op == "6":
                        break
                    else:
                        print("\n❌ Opción inválida"); esperar_tecla()

            elif opcion == "10":
                usuario_actual = None
                print("\nSesión cerrada correctamente"); esperar_tecla()

            else:
                print("\n❌ Opción inválida"); esperar_tecla()

if __name__ == "__main__":
    main()
