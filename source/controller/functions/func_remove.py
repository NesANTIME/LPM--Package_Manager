import os
import sys
import time


from source.animations.bar import BarAnimation
from source.modules.system_controller import func_userConfig
from source.modules.system_controller import add_path_package
from source.modules.chargate_config import returnLocal_RutaPackagesLPM, returnLocal_RutaPATH




def main_remove(name_package):
    data = func_userConfig("r", None)

    name = name_package[0]
    version_pkg = name_package[1]

    if (name in data.get("package_install", {})):
        package_name = data["package_install"][name]

        if (version_pkg != None):
            version = version_pkg
        else:
            version = package_name.get("version_use")

        validate = input(f"{' '*4}[!] Esta seguro de desintalar el paquete? (y/n): ").strip().lower()
        if (validate not in ("y", "s")):
            print(f"{' '*6}[!] Operacion cancelada por el usuario!")
            sys.exit(0)


        bar = BarAnimation(f"[!] Desintalando {name} - {version}", "modern")
        rut = os.path.join(os.path.expanduser(returnLocal_RutaPackagesLPM()), name, version)

        if (os.path.isdir(rut)):
            os.chdir(rut)

            bin_dir = os.path.expanduser(returnLocal_RutaPATH())
            launcher = os.path.join(bin_dir, name)

            if (os.path.isfile(launcher)):
                os.remove(launcher)

            time.sleep(2)
            bar.new_valor(40, "[!] Limpiando path!")

            if (version in data["package_install"][name]["version_instaladas"]):
                data["package_install"][name]["version_instaladas"].remove(version)

                use_version = data["package_install"][name]["version_instaladas"][-1]
                data["package_install"][name]["version_use"] = use_version

                main_pkg = data["package_install"][name]["__main-use__"]

                bar.new_valor(100, "Completado...")

                validate = input(f"{' '*4}[!] Le gustaria usar como predeterminado el paquete {use_version} de {name}? (y/n): ").strip().lower()
                if (validate not in ("y", "s")):
                    add_path_package(name, use_version, main_pkg)
                    print(f"{' '*4}Añadido al path correctamente!")

            else:
                data["package_install"][name_package].remove()
            
            func_userConfig("w", data)
            
        else:
            print(f"{' '*4}[ ERROR ] No se puede eliminar un paquete que no existe!")

    else:
        print(f"{' '*4}[ ERROR ] El paquete no se encuentra instalado o no existe!")