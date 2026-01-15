import os
import sys
import base64
import zipfile

from source.animations import BarAnimation
from source.logics.func_install import addPackage
from source.modules.controller import func_userConfig
from source.modules.conections_core import autentificacion_server, peticiones_requests



def main_update(id_client, token_client):
    config = func_userConfig("r", None)
    session_id = autentificacion_server(id_client, token_client, "upd")

    installed_packages = config.get("package_install", {})
    local_packages = list(installed_packages.keys())
    updates = []

    print(f"    [!] Verificando versiones de los paquetes instalados!\n")

    result = peticiones_requests(
        {
            "client_uuidSession": session_id,
            "client_listPackages": local_packages
        },
        10,
        "fS_update"
    )

    server_packages = result.get("list_packages", {})

    for name, latest_version in server_packages.items():
        local_info = installed_packages.get(name)
        if not local_info:
            continue

        local_version = local_info.get("version_use")
        if not local_version:
            continue

        if local_version != latest_version:
            updates.append((name, local_version, latest_version))

    if not updates:
        print(f"\n    [!] Todos los paquetes se encuentran actualizados!")
        sys.exit(0)


    print(f"{' '*6}Los siguientes paquetes pueden ser actualizados!\n")
    print(f"{' '*6}[Name Package]{' '*8}[Version]{' '*12}[Latest]\n{' '*6}{'-'*20}   {'-'*19}   {'-'*20}")

    for name, local_v, latest_v in updates:
        print(f"{' '*6}{name:<20}   {local_v:<19}   {latest_v:<20}")

    confirm = input(f"\n    [!] Desea continuar a la actualizar los {len(updates)} packages? (y/n): ").strip().lower()
    if (confirm not in ("y", "s")):
        print(f"      [ CANCELADO ] Instalación abortada por el usuario")
        sys.exit(0)

    for name, _, latest_version in updates:
        destino = os.path.expanduser(f"~/.lpm/packages/{name}/{latest_version}")
        os.makedirs(destino, exist_ok=True)
        zip_path = os.path.join(destino, f"{name}.zip")

        try: 

            data = peticiones_requests(
                    {
                        "client_uuidSession": session_id,
                        "client_listPackages": [name]
                    },
                    20,
                    "fI_update"
                )

            if (data.get("status") != "success"):
                print(f"      [ ERROR ] Fallo en la instalación de {name}")
                continue

            packages = data.get("list_package_base64", {})
            pkg = packages.get(name)

            if (not pkg):
                print(f"      [ ERROR ] Paquete {name} no encontrado en respuesta")
                continue

            nombre_archivo = pkg.get("nombre_archivo")
            tamaño_bytes = pkg.get("tamaño_bytes")
            contenido_base64 = pkg.get("contenido_base64")
            main_package = pkg.get("main_package")

            if (not contenido_base64):
                print(f"      [ ERROR ] Contenido inválido para {name}")
                continue

            contenido = base64.b64decode(contenido_base64)

            print()
            #bar_animation(4, f"Instalando {name}... ")

            with open(zip_path, "wb") as f:
                f.write(contenido)

            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(destino)

            os.remove(zip_path)

            addPackage(name, latest_version, main_package)

            print(f"\n    [ OK ] Name : {nombre_archivo} - Size : {tamaño_bytes} bytes\n")

        except Exception as e:
            print(f"    ❌ Error inesperado: {e}")
            sys.exit(1)
