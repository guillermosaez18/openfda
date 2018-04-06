import http.client
import json

headers = {'User-Agent': 'http-client'}
n = 10

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json?limit={}".format(n), None, headers)
r2 = conn.getresponse()
print(r2.status, r2.reason)
# Se lee el archivo json recibido y se pasa a string
r2 = r2.read().decode("utf-8")
# Lo pasa a diccionario
drugs = json.loads(r2)

for num in range(n):
    print ("El medicamento número {} tiene id: {}".format(num+1, drugs["results"][num]["id"]))