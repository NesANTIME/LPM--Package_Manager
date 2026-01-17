from source.modules.load_config import load_config, load_configRepo

# funciones internas de icon()
def check_newVersion():
    config_json = load_config()
    config_jsonRepo = load_configRepo()
    

    version_local = config_json["info"]["version"]
    version_lastest = config_jsonRepo["info"]["version"]

    if (version_local != version_lastest):
        return f"[!] Nueva version {version_lastest} disponible!"
    
    return False




# funciones principales
def icon():
    config_json = load_config()
    info_newVersion = check_newVersion()

    icon = config_json["info"]["icon"]

    if (info_newVersion != False):
        icon[1] += info_newVersion

    for i in config_json["info"]["icon"]:
        print(i)