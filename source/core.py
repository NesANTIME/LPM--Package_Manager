import time

# ~~~ modulos internos de lpm ~~~
from source.controller.functions.func_use import main_use
from source.controller.functions.func_list import main_list
from source.controller.functions.func_remove import main_remove
from source.controller.functions.func_search import main_search
from source.controller.functions.func_update import main_update
from source.controller.functions.func_install import main_install

from source.controller.credentials.credential import verify_userConfig
from source.modules.system_controller import func_restartConfig
from source.modules.chargate_config import load_config
from source.animations.icon import check_newVersion
from source.animations.bar import BarAnimation




# ~~~~ Funciones Principales ~~~~

def init_(function, name_package):

    id_client, token_client = verify_userConfig()

    if (function == "install"):
        main_install(id_client, token_client, name_package)

    elif (function == "search"):
        main_search(id_client, token_client, name_package)

    elif (function == "list"):
        main_list()

    elif (function == "update"):
        main_update(id_client, token_client)

    elif (function == "remove"):
        main_remove()

    elif (function == "use"):
        main_use(name_package)


def lpm_restart():
    print(f"{' '*4}Programa de restauracion de lpm!")
    print(f"{' '*6}[!] Advertencia: este programa eliminara los siguientes directorios o archivos!")
    print(f"{' '*7}=> Archivos de configuracion de LPM\n{' '*7}=> Todos los paquetes intalados via LPM")

    validate = input("[*] Desea realizar los cambios en el disco y lpm? (y/n): ")
    if (validate != "y"):
        print(f"{' '*6}[!] Operacion cancelada por el usuario!")

    else:
        bar = BarAnimation("Restaurando...", "modern")

        func_restartConfig()

        bar.new_valor(80, "Finalizando...")

        time.sleep(2)
        
        bar.new_valor(80, "Completado...")
    



def lpm_version():
    config_json = load_config()

    version = config_json["info"]["version"]
    info_newVersion = check_newVersion()

    print(f"{' '*4}Version: {version}")

    if (info_newVersion != False):
        print(f"{' '*4} {info_newVersion}")
    
    print(f"{' '*6}lpm packages by nesantime")