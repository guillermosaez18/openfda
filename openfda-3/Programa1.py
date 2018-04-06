import http.client
import json

headers = {'User-Agent': 'http-client'}
n = 10

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json?limit={}".format(n), None, headers)
r2 = conn.getresponse()

# Se lee el archivo json recibido y se pasa a string
r2 = r2.read().decode("utf-8")

# Lo pasa a diccionario
drugs = json.loads(r2)

contenido = ""
lista = []

for num in range(n):
    try:
        lista.append("El medicamento {}, que tiene id <b>{}</b>, se llama: <b>{}</b>".format(num + 1, drugs["results"][num]["id"],
                                                            drugs["results"][num]["openfda"]["brand_name"][0]))
    except KeyError:
        lista.append("El medicamento {}, que tiene id <b>{}</b>, no muestra su nombre.".format(num + 1, drugs["results"][num]["id"]))

contenido = "<!doctype html>\n<html>\n<body>"

for i in lista:
    contenido += ("\n" + "<p>" + i + "</p>")

contenido += "\n</body>\n</html>"

import http.server
import socketserver


# -- Puerto donde lanzar el servidor
PORT = 8001


# Clase con nuestro manejador. Es una clase derivada de BaseHTTPRequestHandler
# Esto significa que "hereda" todos los metodos de esta clase. Y los que
# nosotros consideremos los podemos reemplazar por los nuestros
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    # GET. Este metodo se invoca automaticamente cada vez que hay una
    # peticion GET por HTTP. El recurso que nos solicitan se encuentra
    # en self.path
    def do_GET(self):

        # La primera linea del mensaje de respuesta es el
        # status. Indicamos que OK
        self.send_response(200)

        # En las siguientes lineas de la respuesta colocamos las
        # cabeceras necesarias para que el cliente entienda el
        # contenido que le enviamos (que sera HTML)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Este es el mensaje que enviamos al cliente: un texto y
        # el recurso solicitado

        message = contenido

        # Enviar el mensaaje completo
        self.wfile.write(bytes(message, "utf8"))
        print("File served!")
        return


# ----------------------------------
# El servidor comienza a aqui
# ----------------------------------
# Establecemos como manejador nuestra propia clase
Handler = testHTTPRequestHandler

# -- Configurar el socket del servidor, para esperar conexiones de clientes
httpd = socketserver.TCPServer(("", PORT), Handler)
print("serving at port", PORT)

# Entrar en el bucle principal
# Las peticiones se atienden desde nuestro manejador
# Cada vez que se ocurra un "GET" se invoca al metodo do_GET de
# nuestro manejador
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print("")
    print("Interrumpido por el usuario")

print("")
print("Servidor parado")
