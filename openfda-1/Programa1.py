import http.client
import json
# Escribimos la cabecera del mensaje de solicitud
headers = {'User-Agent': 'http-client'}

# Se conecta a la API general de FDA, al servidor
connect = http.client.HTTPSConnection("api.fda.gov")
# Hace una solicitud mediante el verbo "GET" concretando el recurso desde donde obtendremos la información
connect.request("GET", "/drug/label.json", None, headers)
# Leemos la información que nos responde el servidor
r1 = connect.getresponse()
# Imprimimos por pantalla línea de estado de la respuesta
print(r1.status, r1.reason)
# Se lee la respuesta recibido y la descodifica convirtiéndolo en un string
r1 = r1.read().decode("utf-8")
# Lo pasa a diccionario
drugs = json.loads(r1)


dicc = {}
dicc["id"] = drugs["results"][0]["id"]
dicc["propósito"] = drugs["results"][0]["purpose"][0]
dicc["fabricante"] = drugs["results"][0]["openfda"]["manufacturer_name"][0]

for feature,solution in dicc.items():
    print("El {} del medicamento es: {}".format(feature, solution))
connect.close()
