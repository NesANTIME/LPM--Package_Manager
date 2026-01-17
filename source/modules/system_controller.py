import os
import stat

from source.controller.credentials.credential import func_userConfig, return_userConfig
from source.modules.chargate_config import returnLocal_RutaPATH, returnLocal_RutaPackagesLPM

def add_package_at_funcConfig(name_package, version_package, main):
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



def add_path_package(package_name, version, entrypoint):
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
    path_programs = returnLocal_RutaPackagesLPM()

    if (os.path.isfile(file_path)):
        os.remove(file_path)

    if (os.path.isdir(path_programs)):
        os.chdir(path_programs)