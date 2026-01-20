import sys
import json
import time
import requests

# funciones internas de lpm
from source.animations.message import message
from source.controller.credentials.credential import return_userConfig
from source.modules.chargate_config import returnURL_ServidoresConexion


# Variables Globales
URL_BASEDATA = returnURL_ServidoresConexion().rstrip('/')



# funciones principales
def autentificacion_server(id_client, token_secret, type_consulta):
    message(
        "[!] Conectando con el Servidor...", 
        "[ OK ] Conectado con el Servidor...", 
        1,
        4
    )
    print(f"{' '*6} Iniciando autentificacion con el dominio: {id_client[:5]}...")

    auth_response = requests.post(
        f"{URL_BASEDATA}/auth",
        json={
            "client_id": id_client,
            "client_typeConsult": type_consulta,
            "client_token": token_secret
        },
        timeout=10
    )

    auth_response.raise_for_status()
    auth_data = auth_response.json()

    if not auth_data.get("authorized"):
        message(
            "[!] Conectado a lpm_DATABASE",
            f"[ ERROR ] autentificacion fallida con el dominio: {id_client[:5]}",
            2,
            4
        )
        sys.exit(1)

    session_id = auth_data["session"]

    message(
        "[!] Conectado a lpm_DATABASE",
        f"[ OK ] Conectado a lpm_DATABASE, Bienvenido {auth_data.get('username')}!",
        3,
        4
    )
    print(f"{' '*6} Conexión autenticada con éxito...")

    return session_id





# funciones externas
def requestsDelivery(peticion, timeoutt, autorModule_):

    def auxiliary_controller(mode_, detalles):

        if autorModule_ == "fS_install":
            if mode_:
                message(
                    "[!] Consultando por el paquete!",
                    "[ ERROR ] El paquete o la versión no existe",
                    3,
                    4
                )
                sys.exit(1)
            terminate_url = "/client/search/install_package"

        elif autorModule_ == "fI_install":
            if mode_:
                print(f"❌ Error de conexión: {detalles}")
                if hasattr(detalles, "response") and detalles.response is not None:
                    print(f"   Detalles: {detalles.response.text}")
                sys.exit(1)
            terminate_url = "/client/install_package"

        elif autorModule_ == "fS_search":
            if mode_:
                message(
                    "[!] Consultando por el paquete!",
                    "[ ERROR ] El paquete no existe",
                    3,
                    4
                )
                sys.exit(1)
            terminate_url = "/client/search_package"

        elif autorModule_ == "fS_update":
            if mode_:
                print("    [!] Error en la petición al servidor")
                if hasattr(detalles, "response") and detalles.response is not None:
                    print(f"        {detalles.response.text}")
                sys.exit(1)
            terminate_url = "/client/search/update_package"

        elif autorModule_ == "fI_update":
            if mode_:
                print(f"    ❌ Error de conexión: {detalles}")
                if hasattr(detalles, "response") and detalles.response is not None:
                    print(f"       {detalles.response.text}")
                sys.exit(1)
            terminate_url = "/client/update_package"

        else:
            raise ValueError(f"autorModule_ desconocido: {autorModule_}")

        return terminate_url


    url = auxiliary_controller(False, None)

    try:
        response = requests.post(
            f"{URL_BASEDATA}{url}",
            json=peticion,
            timeout=timeoutt
        )
        response.raise_for_status()
        data = response.json()

    except requests.exceptions.RequestException as e:
        auxiliary_controller(True, e)

    return data




def descarga_files(url, localFile):
    response = requests.get(url, stream=True)
    total_length = int(response.headers.get('content-length', 0))
    chunk_size = 1024
    downloaded = 0
    start_time = time.time()
    with open(localFile, "wb") as f:
        for chunk in response.iter_content(chunk_size=chunk_size):
            if chunk:
                f.write(chunk)
                downloaded += len(chunk)
                percent = downloaded / total_length * 100
                elapsed_time = time.time() - start_time
                speed = downloaded / 1024 / elapsed_time
                sys.stdout.write(f"\r{' '*4}Descargando: {percent:.2f}% - {speed:.2f} KB/s")
                sys.stdout.flush()
    sys.stdout.write("")




def get_firmaForCreador(name):
    file_path = return_userConfig()
    timeoutt = 10

    with open(file_path, "r", encoding="utf-8") as f:
        bd = json.load(f)

    id_client = bd["credentials"]["id_client"]

    try:
        response = requests.post(
            f"{URL_BASEDATA}/get/consult",
            json={"client_id": id_client, "client_GetConsult": name},
            timeout=timeoutt
        )

        response.raise_for_status()
        data = response.json()

    except requests.exceptions.RequestException as e:
        print(e)

    return data