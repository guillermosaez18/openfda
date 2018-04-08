import http.client
import json
# Escribimos la cabecera del mensaje de solicitud
headers = {'User-Agent': 'http-client'}
# Declaramos el número de medicamentos que deseamos ver
n = 10

# Se conecta a la API general de FDA, al servidor
connect = http.client.HTTPSConnection("api.fda.gov")
# Hace una solicitud mediante el verbo "GET" concretando el recurso desde donde obtendremos la información
# Mediante el parámetro limit=n hacemos posible ver la información de n medicamentos
connect.request("GET", "/drug/label.json?limit={}".format(n), None, headers)
# Leemos la información que nos responde el servidor
response2 = connect.getresponse()
# Imprimimos por pantalla la línea de estado de la respuesta
print(response2.status, response2.reason)
# Se lee la respuesta recibida y la descodifica desde utf-8 al formato local
response2 = response2.read().decode("utf-8")
# Lo pasa a diccionario 
drugs = json.loads(response2)

# Vamos pasando por los medicamentos en orden y extrayendo la información que queremos (del diccionario)
for num in range(n):
    print("El medicamento número {} tiene id: {}".format(num+1, drugs["results"][num]["id"]))

# Finalmente cerramos la conexión
connect.close()
