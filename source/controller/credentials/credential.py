import os
import sys
import json
import uuid
import keyring

# funciones internas de lpm
from source.animations.message import message
from source.modules.chargate_config import (
    returnLocal_FileSources,
    returnLocal_RutaLPM,
    returnLocal_RutaPATH,
    returnLocal_RutaPackagesLPM
)

# variables globales
DIR_SOURCES = os.path.expanduser(returnLocal_RutaLPM())
FILE_REGISTRY = returnLocal_FileSources()


# funciones auxiliares
def return_userConfig():
    os.makedirs(DIR_SOURCES, exist_ok=True)
    return os.path.join(DIR_SOURCES, FILE_REGISTRY)


def func_userConfig(modo, data):
    path_registros = return_userConfig()
    with open(path_registros, modo, encoding="utf-8") as f:
        if modo == "w":
            json.dump(data, f, ensure_ascii=False, indent=4)
        else:
            return json.load(f)


# funciones de validacion de credentials
def is_valid_client_id(id) -> bool:
    if len(id) != 16:
        return False
    if id[0] != "l" or id[8] != "p" or id[-1] != "m":
        return False
    return True


def is_valid_client_token(token) -> bool:
    return token.startswith("L") and len(token) >= 30


def split_at_symbol(text: str):
    before, _, after = text.partition("@")
    return before, after



def create_credentials(file_path):
    print(f"{' '*4}[!] Iniciando configuración de LPM\n")

    password_account = input(f"{' '*6}[PASSWORD_ACCOUNT]: ").strip()
    id_client, token_client = split_at_symbol(password_account)

    if not is_valid_client_id(id_client):
        print(f"{' '*4}[lpm][user] Error ==> ID inválido")
        sys.exit(1)

    if not is_valid_client_token(token_client):
        print(f"{' '*4}[lpm][user] Error ==> TOKEN inválido")
        sys.exit(1)

    huella_system = f"LPM@{uuid.uuid4()}"
    huella_user = str(uuid.uuid4())

    print(f"{' '*7}[lpm][user] Credenciales ==> [ OK ]\n")

    data = {
        "credentials": {
            "user": huella_user,
            "huella_system": huella_system,
            "id_client": id_client
        },
        "package_install": {}
    }

    keyring.set_password(huella_system, huella_user, token_client)

    message(
        "[!] Estableciendo credenciales",
        "[ OK ] Credenciales establecidas",
        3,
        6
    )

    func_userConfig("w", data)
    os.chmod(file_path, 0o600)

    return data




def verify_userConfig():
    file_path = return_userConfig()

    if not os.path.isfile(file_path):
        data = create_credentials(file_path)
    else:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, ValueError):
            print(f"{' '*6}[!] Credenciales corruptas, recreando…")
            data = create_credentials(file_path)

    huella_system = data["credentials"]["huella_system"]
    huella_user = data["credentials"]["user"]
    id_client = data["credentials"]["id_client"]

    token_client = keyring.get_password(huella_system, huella_user)

    if token_client is None:
        print(f"{' '*6}[!] Token no encontrado en keyring")
        sys.exit(1)

    return id_client, token_client