import http.server
import http.client
import socketserver
import json

# Puerto donde lanzar el servidor
PORT = 8000
socketserver.TCPServer.allow_reuse_address = True


# Cabecera de cliente y páginas web varias
headers = {'User-Agent': 'http-client'}
pagina_inicio = "index.html"
pagina_error = "index_error.html"
pagina_auth = "index_auth.html"


class TestHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    # Mediante get_info, pasándole el recurso como argumento, conseguiremos obtener la información que queremos
    # y la guardaremos en forma de diccionario en drugs
    def get_info(self, recurso):
        connect = http.client.HTTPSConnection("api.fda.gov")
        connect.request("GET", "/drug/label.json?{}".format(recurso), None, headers)

        response = connect.getresponse()
        print(response.status, response.reason)
        drugs_json = response.read().decode("utf-8")
        connect.close()
        drugs = json.loads(drugs_json)

        return drugs


    # Así podremos elegir qué página web proporcionará el servidor directamente poniendo la elección
    def pagina (self, eleccion):
        with open (eleccion, "r") as f:
            contenido = f.read()

        return contenido

    # Obtenemos la lista de medicamentos con la extensión deseada (mediante recurso)
    def list_drugs(self, recurso):

        # Recogemos la información llamando a get_info con el recurso introducido
        drugs = self.get_info(recurso)

        # Crearemos una lista donde meteremos la información
        info = []

        # Vamos a procesar la info del número de medicamentos que noa hayan dicho
        # El cual es el número de la derecha del símbolo igual en "limit=n"
        repet = recurso.split("=")[1]

        # Para cada medicamento, comprobamos si a openfda solo le corresponde un diccionario vacío o no
        # En cada caso o se informa de ello o se le aporta el nombre utilizando el diccionario drugs
        # Y cada línea de información se guarda como un elemento de una lista
        # <b> se utiliza para poner en negrita
        for num in range(int(repet)):
            if not drugs["results"][num]["openfda"] == {}:
                info.append("El medicamento {}, que tiene id <b>{}</b>,"
                            " se llama: <b>{}</b>".format(num + 1, drugs["results"][num]["id"],
                                                          drugs["results"][num]["openfda"]["brand_name"][0]))
            else:
                info.append("El medicamento {}, que tiene id <b>{}</b>,"
                            " no muestra su nombre.".format(num + 1, drugs["results"][num]["id"]))

        # Creamos el texto del archivo HTML y hacemos que contenga ese inicio (necesario)
        contenido = "<!doctype html>\n<html>\n<body>"
        # Ponemos un título
        contenido += "\n<h1>Lista de medicamentos</h1>"
        # Creamos una lista con un tamaño de letra un poco mayor
        contenido += "\n<ul style='font-size:110%;'>"

        # Añadimos cada elemento de la lista anterior en el archvio HTML que estamos creando
        for i in info:
            contenido += ("<li>" + i + "</li>")

        contenido += "\n</ul>"
        # Añadimos un link con texto
        contenido += "\nDatos obtenidos a partir de <a href='https://api.fda.gov/drug/label.json'>esta web</a>"
        # Añadimos el final (necesario) y ya tendríamos creado el código de la web
        contenido += "\n</body>\n</html>"

        return contenido

    def list_companies(self, recurso):

        drugs = self.get_info(recurso)

        info = []

        for num in range(int(recurso.split("=")[1])):
            if not drugs["results"][num]["openfda"] == {}:
                info.append(
                    "Un fabricante es: <b>{}</b>".format(drugs["results"][num]["openfda"]["manufacturer_name"][0]))
            else:
                info.append("El medicamento cuya id es <b>{}</b> es Desconocida".format(drugs["results"][num]["id"]))

        contenido = "<!doctype html>\n<html>\n<body>"
        contenido += "\n<h1>Lista de empresas</h1>"
        contenido += "\n<ul style='font-size:110%;'>"

        for i in info:
            contenido += ("<li>" + i + "</li>")

        contenido += "\n</ul>\n</body>\n</html>"

        return contenido

    def search_drug(self, recurso):

        drugs = self.get_info(recurso)

        info = []

        # Pasamos por cada uno de los medicamentos que se hayan recibido
        for num in range(len(drugs["results"])):
            if not drugs["results"][num]["openfda"] == {}:
                info.append("El medicamento con id <b>{}</b> tiene el ingrediente activo: <b>{}</b>".format(
                    drugs["results"][num]["id"],
                    recurso.split("=")[1].rstrip("&limit").lstrip("active_ingredient:")))

            else:
                info.append(
                    "El medicamento que tiene id <b>{}</b> no muestra datos.".format(drugs["results"][num]["id"]))

        contenido = "<!doctype html>\n<html>\n<body>"
        contenido += "\n<h1>Lista de medicamentos</h1>"
        contenido += "\n<ul style='font-size:110%;'>"
        for i in info:
            contenido += ("<li>" + i + "</li>")

        contenido += "\n</ul>\n</body>\n</html>"

        return contenido

    def search_company(self, recurso):

        drugs = self.get_info(recurso)

        info = []

        for num in range(len(drugs["results"])):
            if not drugs["results"][num]["openfda"] == {}:
                info.append(
                    "El fabricante del medicamento con id <b>{}</b> es: <b>{}</b>".format(drugs["results"][num]["id"],
                                                                                          drugs["results"][num][
                                                                                              "openfda"][
                                                                                              "manufacturer_name"][0]))
            else:
                info.append(
                    "El medicamento que tiene id <b>{}</b> no muestra datos.".format(drugs["results"][num]["id"]))

        contenido = "<!doctype html>\n<html>\n<body>"
        contenido += "\n<h1>Lista de empresas</h1>"
        contenido += "\n<ul style='font-size:110%;'>"

        for i in info:
            contenido += ("<li>" + i + "</li>")

        contenido += "\n</ul>\n</body>\n</html>"

        return contenido

    def list_warnings(self, recurso):

        drugs = self.get_info(recurso)

        info = []
        n = int(recurso.split("=")[1])

        for num in range(n):

            # En caso de existir el campo "warnings" en cada medicamento específico, se aportan sus datos o no
            if "warnings" in drugs["results"][num]:
                info.append("El medicamento con id <b>{}</b> tiene como advertencia: {}".format
                            (drugs["results"][num]["id"], drugs["results"][num]["warnings"][0]))

            else:
                info.append("El medicamento con id <b>{}</b> no tiene advertencias".format(drugs["results"][num]["id"]))

        contenido = "<!doctype html>\n<html>\n<body>"
        contenido += "\n<h1>Lista de advertencias</h1>"
        contenido += "\n<ul style='font-size:110%;'>"

        for i in info:
            contenido += ("<li>" + i + "</li>")

        contenido += "\n</ul>\n</body>\n</html>"

        return contenido


    # Se entra en do_Get cada vez que se realiza una petición GET por http
    def do_GET(self):

        redirigir = False

        # self.path es el recurso al que se ha intentado acceder
        if "?" in self.path:

            if self.path.split("=")[0] == "/listDrugs?limit":

                # Así evitamos entradas de caracteres no numéricos y creamos el recurso que se pasará a uno de los anteriores
                # En cualquier caso, si se introcude algo no válido, enviamos una página de error
                if (self.path.split("=")[1]).isdigit():
                    recurso = "limit=" + self.path.split("=")[1]
                    contenido = self.list_drugs(recurso)

                else:
                    contenido = self.pagina(pagina_error)

            elif self.path.split("=")[0] == "/listCompanies?limit":

                if (self.path.split("=")[1]).isdigit():
                    recurso = "limit=" + self.path.split("=")[1]
                    contenido = self.list_companies(recurso)

                else:
                    contenido = self.pagina(pagina_error)

            elif self.path.split("=")[0] == "/listWarnings?limit":

                if (self.path.split("=")[1]).isdigit():
                    recurso = "limit=" + self.path.split("=")[1]
                    contenido = self.list_warnings(recurso)

                else:
                    contenido = self.pagina(pagina_error)

            # Añadiendo el limit hacemos que nos dé más de 1 medicamento
            elif self.path.split("=")[0] == "/searchDrug?active_ingredient":
                recurso = "search=active_ingredient:" + self.path.split("=")[1] + "&limit=10"
                contenido = self.search_drug(recurso)

            elif self.path.split("=")[0] == "/searchCompany?company":
                recurso = "search=manufacturer_name:" + self.path.split("=")[1] + "&limit=10"
                contenido = self.search_company(recurso)

            else:
                contenido = self.pagina(pagina_error)

        # En caso de acceder a los siguientes por la URL directamente y no por el formulario
        # Podemos acceder sin tener que poner el símbolo de interrogación
        # En cualquiera de los casos, creamos el recurso que pasamos
        elif self.path == "/listDrugs":
            recurso = "limit=1"
            contenido = self.list_drugs(recurso)

        elif self.path == "/listCompanies":
            recurso = "limit=10"
            contenido = self.list_companies(recurso)

        elif self.path == "/listWarnings":
            recurso = "limit=10"
            contenido = self.list_warnings(recurso)

        elif self.path == "/secret":
            contenido = self.pagina(pagina_auth)

        elif self.path == "/redirect":
            contenido = self.pagina(pagina_inicio)
            redirigir = True

        elif self.path == "/":
            contenido = self.pagina(pagina_inicio)

        else:
            contenido = self.pagina(pagina_error)

        # Para saber con qué cabecera y qué código tenemos que responder al cliente
        # Nos fijamos en la página web que le pasamos
        if contenido == self.pagina(pagina_error):
            self.send_response(404)
            self.send_header('Content-type', 'text/html')

        elif contenido == self.pagina(pagina_auth):
            self.send_response(401)
            self.send_header("WWW-Authenticate", "Basic realm='nmrs_m7VKmomQ2YM3:'")

        # Primero le redirigimos y le mandamos una cabecera, y después
        # Le mandamos la cabecera normal al haber sido redirigido
        elif redirigir:
            self.send_response(200)
            self.send_header("Location", "localhost:8000")
            self.send_header('Content-type', 'text/html')

        # En caso contrario a cualquiera especial, le pasamos la cabecera y el código normales
        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')

        self.end_headers()

        # Enviamos el mensaje (código HTML) codificándolo a utf-8 primero
        self.wfile.write(bytes(contenido, "utf8"))
        return


# ----------------------------------
# El servidor comienza a aqui
# ----------------------------------
# Establecemos como manejador nuestra propia clase
Handler = TestHTTPRequestHandler

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
