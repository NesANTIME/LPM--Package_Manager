def main_remove(name_package):
    data = lpm_Userpackage()
    if (name_package in data.get("package_install", {})):
        package = data["package_install"][name_package]
        version = package.get("version_use")

        rut = os.path.join(LOCAL_SOURCES, name_package, version)
        if os.path.isfile(rut):
            os.remove(rut)
            
            if (name_package in data.get("package_install", {})):
                if (version in data["package_install"][name_package]["version_instaladas"]):
                    data["package_install"][name_package]["version_instaladas"].remove(version)
                    data["package_install"][name_package]["version_use"] = data["package_install"][name_package]["version_instaladas"][-1]
                
                else:
                    data["package_install"][name_package].remove()

                save_lpm(data)
            
        else:
            print(f"{' '*4}[ ERROR ] No se puede eliminar un paquete que no existe!")

    else:
        print(f"{' '*4}[ ERROR ] El paquete no se encuentra instalado o no existe!")