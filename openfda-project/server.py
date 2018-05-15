import http.server
import http.client
import socketserver
import json

# -- Puerto donde lanzar el servidor
PORT = 8000
socketserver.TCPServer.allow_reuse_address = True


# -- Parametros de configuracion
headers = {'User-Agent': 'http-client'}
pagina_inicio = "index.html"
pagina_error = "index_error.html"
pagina_auth = "index_auth.html"


class TestHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    def get_info(self, recurso):

        connect = http.client.HTTPSConnection("api.fda.gov")
        connect.request("GET", "/drug/label.json?{}".format(recurso), None, headers)

        response = connect.getresponse()
        print(response.status, response.reason)
        drugs_json = response.read().decode("utf-8")
        connect.close()
        drugs = json.loads(drugs_json)

        return drugs

    def pagina (self, eleccion):
        with open (eleccion, "r") as f:
            contenido = f.read()

        return contenido


    def list_drugs(self, recurso):

        drugs = self.get_info(recurso)

        # Crearemos una lista donde meteremos la información
        info = []

        # Para los n medicamentos, comprobamos si a openfda solo le corresponde un diccionario vacío o no
        # En cada caso o se informa de ello o se le aporta el nombre utilizando el diccionario de OpenFDA
        # Y cada línea de información se guarda como un elemento de una lista
        # <b> se utiliza para poner en negrita

        if (recurso.split("=")[1]):
            repes = recurso.split("=")[1]
        else:
            repes = 1

        for num in range(int(repes)):
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
                    "El medicamento que tiene id <b>{}</b> no muestra info.".format(drugs["results"][num]["id"]))

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
        mas = 0
        n = int(recurso.split("=")[1])

        for num in range(n):

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

    def do_GET(self):

        redirigir = False

        if "?" in self.path:

            if self.path.split("=")[0] == "/listDrugs?limit":

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

            elif self.path.split("=")[0] == "/searchDrug?active_ingredient":
                recurso = "search=active_ingredient:" + self.path.split("=")[1] + "&limit=10"
                contenido = self.search_drug(recurso)

            elif self.path.split("=")[0] == "/searchCompany?company":
                recurso = "search=manufacturer_name:" + self.path.split("=")[1] + "&limit=10"
                contenido = self.search_company(recurso)

            else:
                contenido = self.pagina(pagina_error)

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


        if contenido == self.pagina(pagina_error):
            self.send_response(404)
            self.send_header('Content-type', 'text/html')

        elif contenido == self.pagina(pagina_auth):
            self.send_response(401)
            self.send_header("WWW-Authenticate", "Basic realm='nmrs_m7VKmomQ2YM3:'")

        elif redirigir:
            self.send_response(200)
            self.send_header("Location", "localhost:8000")
            self.send_header('Content-type', 'text/html')

        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')

        self.end_headers()

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
