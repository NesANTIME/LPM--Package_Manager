import os
import sys
import subprocess


# ~~~ funciones internas de lpm ~~~
from source.modules.controller import func_userConfig
from source.modules.load_config import returnLocal_RutaPackagesLPM


# ~~~~ VARIABLES GLOBALES ~~~~
LOCAL_SOURCESPACKAGES = os.path.expanduser(returnLocal_RutaPackagesLPM())



# ~~~ funciones auxiliares ~~~
def verify_packageExists(name_package):
    data = func_userConfig("r", None)

    if (name_package in data.get("package_install", {})):
        package = data["package_install"][name_package]

        main = package.get("__main-use__")
        version = package.get("version_use")

        ruta = os.path.join(LOCAL_SOURCESPACKAGES, name_package, version, main)

        if os.path.isfile(ruta):
            return ruta
        else:
            print(f"{' '*4}[ ERROR ] Archivo principal no encontrado")
            return False
    else:
        print(f"{' '*4}[ ERROR ] El paquete no se encuentra instalado o no existe!")
        return False




def main_use(name):
    name_package = name[0]
    argumentos_package = name[1]
    rutas = verify_packageExists(name_package)

    if (verify_packageExists(name_package) != False):
        print("\n")
        subprocess.run([sys.executable, rutas] + argumentos_package)
    else:
        sys.exit(1)