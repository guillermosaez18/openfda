import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json", None, headers)
r1 = conn.getresponse()
print(r1.status, r1.reason)
# Se lee el archivo json recibido y se pasa a string
r1 = r1.read().decode("utf-8")
# Lo pasa a diccionario
drugs = json.loads(r1) 

dicc = {}
dicc["id"] = drugs["results"][0]["id"]
dicc["propósito"] = drugs["results"][0]["purpose"][0]
dicc["fabricante"] = drugs["results"][0]["openfda"]["manufacturer_name"][0]

for feature,solution in dicc.items():
    print("El {} del medicamento es: {}".format(feature, solution))
conn.close()
