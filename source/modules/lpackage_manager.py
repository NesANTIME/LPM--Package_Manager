import hashlib

from source.modules.lpackage.manager import LPackage
from source.controller.conection_auth import get_firmaForCreador


def calcular_hash(archivo):
    sha1 = hashlib.sha1()
    try:
        with open(archivo, "rb") as f:
            for bloque in iter(lambda: f.read(65536), b""):
                sha1.update(bloque)
        return sha1.hexdigest()
    except Exception:
        return None
    


def descompresor_lpackage(File, huella_for_file, destino_ruta):
    metadata = LPackage.get_metadata(File)

    huella_file = calcular_hash(File)

    if (huella_file != huella_for_file):
        raise ValueError(" [ ❌ ] Huella no semejante")


    name_creador = metadata.get("author")
    version_local = metadata.get("version")
    description_local = metadata.get("description")
    firma_local = metadata.get("firma_autor")
    
    response_server = get_firmaForCreador(name_creador)

    if (response_server.get("existe") != "ERROR") or (not name_creador) or (not version_local) or (not description_local):
        raise ValueError(" [ ❌ ] Error se ha la manipulado la metadata.")
    
    if (firma_local != response_server.get("firma")):
        raise ValueError(" [ ❌ ] Error se ha la manipulado la metadata, [FIRMA INSEGURA]")

    result = LPackage.decompress(File, destino_ruta)

    meta_data = [
        name_creador,
        version_local, 
        description_local, 
        firma_local, 
        f"✅ Extraídos {result['file_count']} archivos en: {result['output_directory']}"
    ]
    return meta_data

