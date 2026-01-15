import os
import sys
import shutil
import tempfile
import subprocess

# ~~~ modulos internos de lpm ~~~
from source.logics.func_use import main_use
from source.logics.func_list import main_list
from source.logics.func_remove import main_remove
from source.logics.func_search import main_search
from source.logics.func_update import main_update
from source.logics.func_install import main_install

from source.animations import BarAnimation
from source.modules.controller import verify_userConfig
from source.modules.load_config import load_config, load_configRepo, check_newVersion



# ~~ VARIABLES GLOBALES ~~
CONFIG_JSON = load_config()


# ~~~~ Funciones Principales ~~~~

def verify_credentials(function, name_package):

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



def lpm_version():
    version = CONFIG_JSON["info"]["version"]
    info_newVersion = check_newVersion()

    print(f"{' '*4}Version: {version}")

    if (info_newVersion != False):
        print(f"{' '*4} {info_newVersion}")
    
    print(f"{' '*6}lpm packages by nesantime")
    



def lpm_upgrade(mode):
    # cargar BD
    config_jsonREPO = load_configRepo()

    version_local = CONFIG_JSON['info']['version']
    version_lastest = config_jsonREPO['info']['version']

    # rutas
    ruta_principal = os.path.expanduser(CONFIG_JSON['urls']['sources']['rutaHOME'])
    ruta_urlOficialLPM = CONFIG_JSON["urls"]["logic"]["repo_oficial"]


    print(f"{' '*4}[!] Iniciando Autoinstalacion de LPM [!]")
    print(f"{' '*6}Version actual =====> {version_local}")
    print(f"{' '*6}Version lastest ====> {version_lastest}")
    print(f"\n{' '*6}[{ruta_urlOficialLPM}]")


    if (mode == "normal"):
        if (version_local == version_lastest):
            print(f"{' '*4}[!] Ya se encuentra en la ultima version!")
            sys.exit(0)

    dir_carLPM = os.path.join(ruta_principal, "lpm_")
    dir_pyLPM = os.path.join(ruta_principal, "lpm_", "lpm.py")
    dir_sourceLPM = os.path.join(ruta_principal, "lpm_", "source")
    dir_LPMvenv = os.path.join(ruta_principal, "lpm_", "lpm_venv")

    dir_temp = tempfile.mkdtemp(prefix="lpm_install_")
    cwd = os.getcwd()

    try:
        subprocess.run(["git", "clone", "--depth", "1", ruta_urlOficialLPM, dir_temp], check=True)

        dir_sourceLPM_temp = os.path.join(dir_temp, "source")
        dir_pyLPM_temp = os.path.join(dir_temp, "lpm.py")

        if (not os.path.isdir(dir_sourceLPM_temp)):
            raise RuntimeError("Repo inválido: falta source/")

        if (not os.path.isfile(dir_pyLPM_temp)):
            raise RuntimeError("Repo inválido: falta lpm.py")
        
        if (os.path.isfile(os.path.join(dir_temp, "install.sh"))):
            os.remove(os.path.join(dir_temp, "install.sh"))

        
        print(f"{' '*4}[!] Autoinstalado archivos...")

        os.makedirs(dir_carLPM, exist_ok=True)

        if os.path.isdir(dir_sourceLPM):
            shutil.rmtree(dir_sourceLPM)
        if os.path.isdir(dir_LPMvenv):
            shutil.rmtree(dir_LPMvenv)
        if os.path.isfile(dir_pyLPM):
            os.remove(dir_pyLPM)


        shutil.copytree(dir_sourceLPM_temp, os.path.join(dir_carLPM, "source"))
        shutil.copy2(dir_pyLPM_temp, os.path.join(dir_carLPM, "lpm.py"))

        subprocess.run(["python3", "-m", "venv", dir_LPMvenv], check=True)

        venv_python = os.path.join(dir_carLPM, "lpm_venv", "bin", "python")
        subprocess.run([venv_python, "-m", "pip", "install", "--upgrade", "requests", "brotli"], check=True)

        print(f"{' '*4}[ OK ] Actualizado correctamente")

    finally:
        os.chdir(cwd)
        shutil.rmtree(dir_temp, ignore_errors=True)