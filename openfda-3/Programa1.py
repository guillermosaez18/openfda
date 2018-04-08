import http.client
import json
import http.server
import socketserver

# -- COMIENZA AQUÍ EL CÓDIGO DEL CLIENTE --

# Escribimos la cabecera del mensaje de solicitud
headers = {'User-Agent': 'http-client'}
# Declaramos "n" como el número de medicamentos de los que queremos información
n = 10

# Se conecta a la API general de FDA, al servidor
connect = http.client.HTTPSConnection("api.fda.gov")
# Hace una solicitud mediante el verbo "GET" concretando el recurso desde donde obtendremos la información
# Mediante el parámetro limit=n hacemos posible ver la información de n medicamentos
connect.request("GET", "/drug/label.json?limit={}".format(n), None, headers)
# Leemos la información que nos responde el servidor
response4 = connect.getresponse()
# Imprimimos por pantalla la línea de estado de la respuesta del servidor de FDA
print(response4.status, response4.reason)
# Se lee la respuesta recibida y la descodifica desde utf-8 al formato local
response4 = response4.read().decode("utf-8")
# Lo pasa a diccionario
drugs = json.loads(response4)

# Crearemos una lista donde meteremos la información
info = []

# Para los n medicamentos, comprobamos si a openfda solo le corresponde un diccionario vacío o no
# En cada caso o se informa de ello o se le aporta el nombre utilizando el diccionario de OpenFDA
# Y cada línea de información se guarda como un elemento de una lista
# <b> se utiliza para poner en negrita
for num in range(n):
    if not drugs["results"][num]["openfda"] == {}:
        info.append("El medicamento {}, que tiene id <b>{}</b>, se llama: <b>{}</b>".format(num + 1, drugs["results"][num]["id"],
                                                            drugs["results"][num]["openfda"]["brand_name"][0]))
    else:
        info.append("El medicamento {}, que tiene id <b>{}</b>, no muestra su nombre.".format(num + 1, drugs["results"][num]["id"]))

# Creamos el texto del archivo HTML y hacemos que contenga ese inicio (necesario)
contenido = "<!doctype html>\n<html>\n<body>"

# Añadimos cada elemento de la lista anterior poniéndolo en línas separadas en el archvio HTML que estamos creando
for i in info:
    contenido += ("\n" + "<p>" + i + "</p>")

# Añadimos el final (necesario) y ya tendríamos creado el código de la web
contenido += "\n</body>\n</html>"

# Finalmente cerramos la conexión
connect.close()


# -- COMIENZA AQUÍ EL CÓDIGO DEL SERVIDOR --

# Puerto donde lanzar el servidor
PORT = 8001


# Clase con nuestro manejador. Es una clase derivada de BaseHTTPRequestHandler
# Por lo que hereda sus métodos, aunque podemos reemplazarlos
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    # Este método se invoca automáticamente cada vez que hay una petición GET por HTTP
    def do_GET(self):

        # La primera línea del mensaje de respuesta es el status. Indicamos que OK
        self.send_response(200)

        # En las siguientes líneas de la respuesta colocamos la cabecera necesaria para que el cliente entienda el
        # contenido que le enviamos (que será HTML)
        self.send_header('Content-type', 'text/html')
        # Indicamos que termina la cabecera
        self.end_headers()

        # Enviamos el mensaje (código HTML) codificándolo a utf-8 primero
        self.wfile.write(bytes(contenido, "utf8"))
        print("Enviado!")
        return


# El servidor comienza aquí

# Establecemos como manejador nuestra propia clase
Handler = testHTTPRequestHandler

# Configurar el socket del servidor (nuestro) para esperar conexiones de clientes
httpd = socketserver.TCPServer(("", PORT), Handler)
print("Serving at port", PORT)

# Las peticiones se atienden desde nuestro manejador
# Cada vez que ocurra un "GET", se invoca al método do_GET de nuestro manejador
# Si lo interrumpimos adrede, nos saldrá un mensaje y terminará el código
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print("Interrumpido por el usuario")
    print ("")

print("Servidor parado")
