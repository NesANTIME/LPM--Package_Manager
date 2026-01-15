import os
import sys
import time
import base64
import zipfile

# ~~~ modulos internos de lpm ~~~
from source.animations import BarAnimation, message_animation
from source.modules.load_config import returnLocal_RutaPackagesLPM
from source.modules.controller import addPackage_userConfig, add_path
from source.modules.conections_core import autentificacion_server, peticiones_requests




# ~~~ flujo principal de instalación ~~~
def main_install(id_client, token_client, package):
    if isinstance(package, list):
        namePackage = package[0]
        versionPackage = package[1]
    else:
        namePackage = package
        versionPackage = "latest"

    session_id = autentificacion_server(id_client, token_client, "ins")

    data = peticiones_requests(
        {
            "client_uuidSession": session_id,
            "client_namePackage": namePackage,
            "client_versionPackage": versionPackage
        },
        10,
        "fS_install"
    )


    version_pkg = data.get("version_pkg")
    main_pkg = data.get("__main__")

    message_animation(f"[!] Consultando por el paquete [{namePackage}]", f"[ OK ] El paquete existe!", 2, 4)

    print(f"\n{' '*6}Package{' '*6}: {data.get('name_pkg')}\n{' '*6}Version{' '*6}: {version_pkg} \n{' '*6}Developer{' '*4}: {data.get('creador')}")

    if (not version_pkg) or (not main_pkg):
        print(f"{' '*6}[ ERROR ] Información incompleta del paquete")
        sys.exit(1)


    validation = input(f"\n{' '*4}[!] Desea continuar a la instalacion del package? (y/n): ").strip().lower()
    if (validation not in ("y", "s")):
        print(f"{' '*6}[ CANCELADO ] Instalacion abortada por el usuario")
        sys.exit(0)


    destino = os.path.expanduser(f"{returnLocal_RutaPackagesLPM()}{namePackage}/{version_pkg}")
    os.makedirs(destino, exist_ok=True)
    zip_path = os.path.join(destino, f"{namePackage}.zip")


    try:
        data = peticiones_requests(
            {
                "client_uuidSession": session_id,
                "client_namePackage": namePackage,
                "client_versionPackage": version_pkg
            },
            20,
            "fI_install"
        )

        if (data.get("status") != "success"):
            print(f"{' '*6}[ ERROR ] Fallo en la instalación")
            sys.exit(1)

        print()
        bar = BarAnimation(f"Instalando package {namePackage}...", "clasic", 4)
        bar.new_valor(0)

        contenido = base64.b64decode(data["contenido_base64"])

        with open(zip_path, "wb") as f:
            f.write(contenido)

        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(destino)

        os.remove(zip_path)

        bar.new_valor(60, "Cargando en el path...")

        addPackage_userConfig(namePackage, version_pkg, main_pkg)
        add_path(namePackage, version_pkg, main_pkg)

        bar.new_valor(100, "Completado...")

        time.sleep(2)

        print(
            f"\n{' '*4}[ OK ] Package instalado correctamente"
            f"\n{' '*4}[ OK ] Package añadido al path correctamente"
            f"\n{' '*5}Name   : {data.get('nombre_archivo')}"
            f"\n{' '*5}Size   : {data.get('tamaño_bytes')} bytes"
        )

    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        sys.exit(1)
