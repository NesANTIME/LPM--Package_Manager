import sys
import requests

# funciones internas de lpm
from source.animations import message_animation
from source.modules.load_config import returnURL_ServidoresConexion


URL_BASEDATA = returnURL_ServidoresConexion().rstrip('/')


# funcion principales
def autentificacion_server(id_client, token_secret, type_consulta):
    message_animation("[!] Conectando con el Servidor...", "[ OK ] Conectado con el Servidor...", 1, 4)
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
        message_animation(
            "[!] Conectado a lpm_DATABASE",
            f"[ ERROR ] autentificacion fallida con el dominio: {id_client[:5]}",
            2,
            4
        )
        sys.exit(1)

    session_id = auth_data["session"]

    message_animation(
        "[!] Conectado a lpm_DATABASE",
        f"[ OK ] Conectado a lpm_DATABASE, Bienvenido {auth_data.get('username')}!",
        3,
        4
    )
    print(f"{' '*6} Conexión autenticada con éxito...")

    return session_id




# funciones externas
def peticiones_requests(peticion, timeoutt, autorModule_):

    def auxiliary_controller(mode_, detalles):

        if autorModule_ == "fS_install":
            if mode_:
                message_animation(
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
                message_animation(
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