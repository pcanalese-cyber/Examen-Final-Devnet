import requests

API_KEY = "e3da88b2-c37a-492c-b836-c7fe4b89e56a"  


def km_to_miles(km):
    return km * 0.621371


def segundos_a_hms(segundos):
    horas = int(segundos // 3600)
    minutos = int((segundos % 3600) // 60)
    segundos = int(segundos % 60)
    return horas, minutos, segundos


def geocode(ciudad, pais):
    """
    Convierte 'Ciudad, Pais' a coordenadas "lat,lon" usando GraphHopper Geocoding API.
    """
    url = "https://graphhopper.com/api/1/geocode"
    params = {
        "q": f"{ciudad}, {pais}",
        "locale": "es",
        "limit": 1,
        "key": API_KEY
    }

    r = requests.get(url, params=params, timeout=30)
    data = r.json()

    hits = data.get("hits", [])
    if len(hits) == 0:
        return None

    lat = hits[0]["point"]["lat"]
    lon = hits[0]["point"]["lng"]
    return f"{lat},{lon}"


print("=== GraphHopper: Rutas Chile -> Argentina ===")
print("Para salir escriba 'v' en cualquier opción.\n")

while True:
    origen = input("Ciudad de Origen (Chile): ").strip()
    if origen.lower() == "v":
        print("Saliendo del programa...")
        break

    destino = input("Ciudad de Destino (Argentina): ").strip()
    if destino.lower() == "v":
        print("Saliendo del programa...")
        break

    print("\nMedio de transporte:")
    print("1) Auto")
    print("2) Bicicleta")
    print("3) A pie")
    opcion = input("Seleccione opción (1/2/3) o 'v' para salir: ").strip().lower()

    if opcion == "v":
        print("Saliendo del programa...")
        break

    vehiculos = {"1": "car", "2": "bike", "3": "foot"}
    if opcion not in vehiculos:
        print("Opción inválida. Intente nuevamente.\n")
        continue

    vehiculo = vehiculos[opcion]

    # Geocodificar origen/destino (Chile -> Argentina)
    punto_origen = geocode(origen, "Chile")
    punto_destino = geocode(destino, "Argentina")

    if not punto_origen or not punto_destino:
        print("\nNo fue posible geocodificar el origen o destino.")
        print("Sugerencia: use nombres más específicos, por ejemplo: 'Santiago' o 'Mendoza'.\n")
        continue

    # Calcular ruta con coordenadas
    url = "https://graphhopper.com/api/1/route"
    params = {
        "point": [punto_origen, punto_destino],
        "vehicle": vehiculo,
        "locale": "es",
        "instructions": "true",
        "calc_points": "true",       # <-- CLAVE: habilita narrativa/instrucciones
        "points_encoded": "false",   # <-- opcional: evita polyline codificado
        "key": API_KEY
    }

    r = requests.get(url, params=params, timeout=30)
    data = r.json()

    if "paths" not in data or len(data["paths"]) == 0:
        print("\nNo fue posible calcular la ruta. Respuesta API:")
        print(data)
        print("")
        continue

    path = data["paths"][0]

    # Distancia
    distancia_km = path.get("distance", 0) / 1000
    distancia_millas = km_to_miles(distancia_km)

    # Tiempo
    tiempo_seg = path.get("time", 0) / 1000
    h, m, s = segundos_a_hms(tiempo_seg)

    print("\n===== RESULTADOS =====")
    print(f"Origen:   {origen}, Chile")
    print(f"Destino:  {destino}, Argentina")
    print(f"Distancia: {distancia_km:.2f} km / {distancia_millas:.2f} millas")
    print(f"Duración:  {h}h {m}m {s}s")

    # Narrativa (instrucciones)
    print("\n--- Narrativa del viaje (instrucciones) ---")
    instrucciones = path.get("instructions", [])

    if len(instrucciones) == 0:
        print("No se recibieron instrucciones (narrativa no disponible).")
    else:
        for i, inst in enumerate(instrucciones, 1):
            texto = inst.get("text", "")
            dist = inst.get("distance", 0) / 1000
            print(f"{i}. {texto} ({dist:.2f} km)")

    print("\n=========================================\n")
