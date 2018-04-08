import http.client
import json
# Escribimos la cabecera del mensaje de solicitud
headers = {'User-Agent': 'http-client'}

# Se conecta a la API general de FDA, al servidor
conn = http.client.HTTPSConnection("api.fda.gov")

# Hace una solicitud mediante el verbo "GET" concretando el recurso desde donde obtendremos la información
# Utilizamos el parámetro de búsqueda para el cual el principio activo es el ácido salicílico
# Ya que esto es propio de las aspirinas
# Y lo establecemos para obtener 100 porque es el máximo que podemos obtener en una solicitud de búsqueda
conn.request("GET", "/drug/label.json?search=active_ingredient:acetylsalicylic&limit=100", None, headers)

# Leemos la información que nos responde el servidor
r3 = conn.getresponse()
# Imprimimos por pantalla la línea de estado de la respuesta
print(r3.status, r3.reason)
# Se lee la respuesta recibida y la descodifica desde utf-8 al formato local
r3 = r3.read().decode("utf-8")
# Lo pasa a diccionario
aspirinas = json.loads(r3)

# Redeclaramos la variable aspirinas para estar dentro de results (dejando atrás meta)
aspirinas = aspirinas["results"]

# En algunos casos, openfda solo tiene asociado un diccionario vacío, sin información alguna
# Así que los separamos para expresar ambos posibles resultados
for i in aspirinas:
    if i["openfda"] == {}:
        print("La aspirina cuya identificación es {} no contiene información sobre el fabricante.".format(i["id"]))
    else:
        print ("El fabricante de la aspirina con id {} es: {}".format(i["id"], i["openfda"]["manufacturer_name"][0]))