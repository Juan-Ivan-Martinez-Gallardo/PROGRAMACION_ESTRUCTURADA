#cooppel.py
#sistema de gestión de productos para COOPPEL

def borrarPantalla():
    import os
    os.system("cls" if os.name == "nt" else "clear")

def esperarTecla():
    input("\n\t ⌨ Oprima cualquier tecla para continuar...\n\t")

def menu_principal():
    print("\n\t..::: Sistema de Gestión de Productos COOPPEL :::..\n")
    print("\t1. 📥Agregar Producto📥")
    print("\t2. 📝Mostrar Productos📝")
    print("\t3. ⚙ Modificar Producto⚙")
    print("\t4. 💲Checar Precio💲")
    print("\t5. 📛Eliminar Producto📛")
    print("\t6. 🚪Salir🚪")
    opcion = input("\n\tSelecciona una opción (1-6): ")
    return opcion

def agregar_producto(lista):
    borrarPantalla()
    print("\n\t..::: 📝Agregar Producto📝 :::..\n")
    nombre = input("Nombre del producto: ").capitalize().strip()
    while True:
        try:
            precio = float(input("💲Precio del producto💲: "))        
            if precio >= 0:
                lista.append([nombre, precio])
                print("✅Producto agregado exitosamente.✅")
                break
            else:
                print("⚠El precio no puede ser negativo.⚠")
        except ValueError:
            print("⚠Ingrese un valor numérico válido.⚠")

def mostrar_productos(lista):
    borrarPantalla()
    print("\n\t..::: 📝Lista de Productos📝 :::..\n")
    if lista:
        print(f"{'ID':<5}{'💲 Producto':<20}{' 💲 Precio':<10}")
        print("-" * 40)
        for idx, (nombre, precio) in enumerate(lista, start=1):
            print(f"{idx:<5}{nombre:<20}${ precio:<10.2f}")
        print("-" * 40)
        print(f"Total: {len(lista)} productos.")
    else:
        print("⚠No hay productos registrados.⚠")

def modificar_producto(lista):
    mostrar_productos(lista)
    if lista:
        try:
            idx = int(input("🔢Número de producto a modificar🔢: ")) - 1
            if 0 <= idx < len(lista):
                nuevo_nombre = input("🔄Nuevo nombre🔄: ").capitalize().strip()
                nuevo_precio = float(input("💲Nuevo precio💲: "))
                lista[idx][0] = nuevo_nombre
                lista[idx][1] = nuevo_precio
                print("✅Producto modificado correctamente.✅")
            else:
                print("⚠Índice fuera de rango.⚠")
        except ValueError:
            print("❌Entrada inválida.❌")
    else:
        print("⚠No hay productos para modificar.⚠")

def checar_precio(lista):
    nombre = input("\n\t..::: 📝Nombre del producto: 📝 :::..\n").capitalize().strip()
    encontrado = False
    for producto in lista:
        if producto[0] == nombre:
            print(f"El precio de {nombre} es ${producto[1]:.2f}")
            encontrado = True
            break
    if not encontrado:
        print("⚠Producto no encontrado.⚠")

def eliminar_producto(lista):
    mostrar_productos(lista)
    if lista:
        try:
            idx = int(input("🔎Número de producto a eliminar:🔎 ")) - 1
            if 0 <= idx < len(lista):
                eliminado = lista.pop(idx)
                print(f"📛Producto '{eliminado[0]}' eliminado.📛")
            else:
                print("❌Opcion no encontrada.❌")
        except ValueError:
            print("❌Entrada inválida.❌")
    else:
        print("⚠No hay productos para eliminar.⚠")