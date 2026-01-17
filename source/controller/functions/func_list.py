# ~~~ funciones internas de lpm ~~~
from source.modules.system_controller import func_userConfig


def main_list():
    data = func_userConfig("r", None)

    print(f"{' '*4}[!] Listando todos los paquetes\n")

    print(f"{' '*6}[Name Package]{' '*9}[Version]  \n{' '*6}{'-'*22} {'-'*12}")

    for name, info in data["package_install"].items():
        for clave, valor in info.items():
            if (clave == "version_use"):
                print(f"{' '*7}{name}{' '*(22 - len(name))}{valor}")