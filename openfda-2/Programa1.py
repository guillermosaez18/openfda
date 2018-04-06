import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json?search=active_ingredient:acetylsalicylic&limit=100", None, headers)
r3 = conn.getresponse()
print(r3.status, r3.reason)

r3 = r3.read().decode("utf-8")
# Lo pasa a diccionario
aspirinas = json.loads(r3)
aspirinas = aspirinas["results"]

for i in aspirinas:
    if i["openfda"] == {}:
        print("La aspirina cuya identificación es {} no contiene información sobre el fabricante.".format(i["id"]))
    else:
        print ("El fabricante de la aspirina con id {} es: {}".format(i["id"], i["openfda"]["manufacturer_name"][0]))