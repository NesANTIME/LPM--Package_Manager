# ~~~ modulos internos de lpm ~~~
from source.animations.message import message
from source.controller.conection_auth import autentificacion_server, requestsDelivery



def main_search(id_client, token_client, name_package):
    session_id = autentificacion_server(id_client, token_client, "sea")

    data = requestsDelivery(
        { 
            "client_uuidSession": session_id, 
            "client_namePackage": name_package
        },
        10,
        "fS_search"
    )

    message(f"[!] Consultando por el paquete [{name_package}]", f"[ OK ] El paquete existe!", 2, 4)

    version_package = f"{data.get('version_pkg')} (lastest)"

    print(f"\n{' '*6}Package      : {data.get('name_pkg')}\n{' '*6}Version      : {version_package}")
    print(f"{' '*6}Developer    : {data.get('creador')}\n{' '*6}Description  : {data.get('description')}")
    