import os
import sys
import json
import stat

# ~~ modulos internos lpm ~~
from source.animations import message_animation
from source.modules.load_config import returnLocal_FileSources, returnLocal_RutaLPM, returnLocal_RutaPATH, returnLocal_RutaPackagesLPM


# ~~~~ VARIABLES GLOBALES ~~~~
LOCAL_SOURCES = os.path.expanduser(returnLocal_RutaLPM())
SOURCE_REGISTRY = returnLocal_FileSources()



# ~~~ funciones auxiliaries para userConfig ~~~

def return_userConfig():
    os.makedirs(LOCAL_SOURCES, exist_ok=True)
    return os.path.join(LOCAL_SOURCES, SOURCE_REGISTRY)


def func_userConfig(modo, data):
    path_registros = return_userConfig()

    with open(path_registros, modo, encoding="utf-8") as f:
        if (modo == "w"):
            json.dump(data, f, ensure_ascii=False, indent=4)
        else:
            return json.load(f)
        



# ~~~ funciones auxiliaries para credentials ~~~

def create_credentials(file_path): 

    def validate_idClient(id):
        if (len(id) != 14):
            return False
        if (id[0] != "l"):
            return False
        if (id[7] != "p"):
            return False
        if (id[-1] != "m"):
            return False
        return True
    
    def validate_tokenClient(token):
        return token.startswith("L") and len(token) >= 30
    

    print(f"{' '*4}[!] Iniciando configuración de LPM\n")

    id_client = input(f"{' '*6}[ID Client]: ").strip()

    if (not validate_idClient(id_client)):
        print(f"{' '*4}[LPM][CONFIG][ID_CLIENT] --> ID_Client inválido")
        sys.exit(1)

    print(f"{' '*7}[LPM][CONFIG]>[ID_CLIENT] --> [ {id_client} ]")

    token_client = input(f"\n{' '*6}[TOKEN Client]: ").strip()

    if (not validate_tokenClient(token_client)):
        print(f"{' '*4}[LPM][CONFIG][TOKEN_CLIENT] --> Token inválido")
        sys.exit(1)
    print(f"{' '*7}[LPM][CONFIG]>[TOKEN_CLIENT] --> [ OK ]\n")

    message_animation("[!] Configurando credenciales locales", "[ OK ] Credenciales establecidas", 3 ,6)

    data = {
        "credentials": {
            "id_client": id_client, 
            "token_secret": token_client
        }, "package_install": {}
    }

    func_userConfig("w", data)
    os.chmod(file_path, 0o600)

    return data




# ~~~ funciones principales ~~~

def verify_userConfig():
    file_path = return_userConfig()
    if (not os.path.isfile(file_path)):
        data = create_credentials(file_path)

    else:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

        except (json.JSONDecodeError, ValueError):
            print(f"{' '*6} [!] Credenciales corruptas, recreando…")
            data = create_credentials(file_path)

    return data["credentials"]["id_client"], data["credentials"]["token_secret"]



def addPackage_userConfig(name_package, version_package, main):
    data = func_userConfig("r", None)

    data.setdefault("package_install", {})

    if name_package in data["package_install"]:
        pkg = data["package_install"][name_package]

        if version_package not in pkg["version_instaladas"]:
            pkg["version_instaladas"].append(version_package)

        pkg["version_use"] = version_package
        pkg["__main-use__"] = main

    else:
        data["package_install"][name_package] = {
            "version_use": version_package,
            "version_instaladas": [version_package],
            "__main-use__": main
        }

    func_userConfig("w", data)



def add_path(package_name, version, entrypoint):
    bin_dir = os.path.expanduser(returnLocal_RutaPATH())
    os.makedirs(bin_dir, exist_ok=True)

    src = os.path.join(os.path.expanduser(returnLocal_RutaPackagesLPM()), package_name, version, entrypoint)

    if not os.path.isfile(src):
        raise FileNotFoundError(f"Entrypoint no encontrado: {src}")

    if not os.access(src, os.X_OK):
        os.chmod(src, 0o755)

    venv_python = os.path.expanduser("~/.local/share/lpm/packages/airsend/1.0.4/lpm_venv/bin/python")

    launcher_path = os.path.join(bin_dir, package_name)

    content = f"""#!/bin/sh
exec "{venv_python}" "{src}" "$@"
"""

    with open(launcher_path, "w", encoding="utf-8") as f:
        f.write(content)

    os.chmod(
        launcher_path,
        os.stat(launcher_path).st_mode
        | stat.S_IXUSR
        | stat.S_IXGRP
        | stat.S_IXOTH
    )


def func_restartConfig():
    file_path = return_userConfig()

    if os.path.isfile(file_path):
            os.remove(file_path)