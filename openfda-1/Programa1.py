import http.client
import json

# Escribimos la cabecera del mensaje de solicitud
headers = {'User-Agent': 'http-client'}

# Se conecta a la API general de FDA, al servidor
connect = http.client.HTTPSConnection("api.fda.gov")
# Hace una solicitud mediante el verbo "GET" concretando el recurso desde donde obtendremos la información
connect.request("GET", "/drug/label.json", None, headers)
# Leemos la información que nos responde el servidor
response1 = connect.getresponse()
# Imprimimos por pantalla la línea de estado de la respuesta
print(response1.status, response1.reason)
# Se lee la respuesta recibida y la descodifica desde utf-8 al formato local
response1 = response1.read().decode("utf-8")
# Lo pasa a diccionario
drugs = json.loads(response1)

# Creamos un diccionario vacío
info = {}
# Vamos añadiendo claves con sus respectivos valores obtenidos del diccionario de la respuesta del servidor
info["id"] = drugs["results"][0]["id"]
info["propósito"] = drugs["results"][0]["purpose"][0]
info["fabricante"] = drugs["results"][0]["openfda"]["manufacturer_name"][0]

# Imprimimos por pantalla las claves con sus valores asociados
for feature,answer in info.items():
    print("El {} del medicamento es: {}".format(feature, answer))

# Finalmente cerramos la conexión
connect.close()
