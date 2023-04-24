import redis

# Crear una conexión con la base de datos Redis
redis_db = redis.Redis(host='localhost', port=6379, db=0)

def menu():
    while True:
        print("\n-------SISTEMA DE INVENTARIO-------\n")
        print("1. Registrar un artículo")
        print("2. Buscar un artículo")
        print("3. Editar un artículo")
        print("4. Eliminar un artículo")
        print("5. Salir")

        opcion = input("\nIngrese una opción: ")

        if opcion == '1':
            registrar_articulo()
        elif opcion == '2':
            buscar_articulo()
        elif opcion == '3':
            editar_articulo()
        elif opcion == '4':
            eliminar_articulo()
        elif opcion == '5':
            print("\nHasta luego.")
            break
        else:
            print("\nOpción inválida. Intente de nuevo.")

def registrar_articulo():
    print("\n-------REGISTRAR ARTÍCULO-------\n")

    nombre = input("Ingrese el nombre del artículo: ")
    precio = input("Ingrese el precio del artículo: ")
    cantidad = input("Ingrese la cantidad del artículo: ")

    # Crear un hash con los datos del artículo
    redis_db.hmset(nombre, {'nombre': nombre, 'precio': precio, 'cantidad': cantidad})

    print(f"\nEl artículo '{nombre}' ha sido registrado exitosamente.")

def buscar_articulo():
    print("\n-------BUSCAR ARTÍCULO-------\n")

    nombre = input("Ingrese el nombre del artículo: ")

    # Obtener el hash con los datos del artículo
    articulo = redis_db.hgetall(nombre)

    if not articulo:
        print("\nEl artículo no se encuentra en el inventario.")
    else:
        print("\nDatos del artículo:")
        print(f"Nombre: {articulo[b'nombre'].decode('utf-8')}")
        print(f"Precio: {articulo[b'precio'].decode('utf-8')}")
        print(f"Cantidad: {articulo[b'cantidad'].decode('utf-8')}")

def editar_articulo():
    print("\n-------EDITAR ARTÍCULO-------\n")

    nombre = input("Ingrese el nombre del artículo a editar: ")

    # Verificar si el artículo existe en el inventario
    if not redis_db.exists(nombre):
        print("\nEl artículo no se encuentra en el inventario.")
    else:
        nuevo_nombre = input("Ingrese el nuevo nombre del artículo (deje en blanco si no desea cambiarlo): ")
        nuevo_precio = input("Ingrese el nuevo precio del artículo (deje en blanco si no desea cambiarlo): ")
        nueva_cantidad = input("Ingrese la nueva cantidad del artículo (deje en blanco si no desea cambiarlo): ")

        # Actualizar los datos del artículo
        if nuevo_nombre:
            redis_db.hset(nombre, 'nombre', nuevo_nombre)
        if nuevo_precio:
            redis_db.hset(nombre, 'precio', nuevo_precio)
        if nueva_cantidad:
            redis_db.hset(nombre, 'cantidad', nueva_cantidad)

        print(f"\nEl artículo '{nombre}' ha sido editado exitosamente.")

def eliminar_articulo():
    """
    Elimina un artículo del inventario.
    """
    # Obtener el nombre del artículo a eliminar
    nombre = input("Ingrese el nombre del artículo a eliminar: ")

    # Verificar si el artículo existe
    if redis_db.exists(nombre):
        # Eliminar el artículo de la base de datos
        redis_db.delete(nombre)
        print(f"El artículo '{nombre}' ha sido eliminado del inventario.")
    else:
        print(f"No se encontró el artículo '{nombre}' en el inventario.")

menu()