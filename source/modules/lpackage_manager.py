import os
import json
import brotli
import struct
from pathlib import Path


# Compresor lpackages ~~~
def compresor_lpackage(carpeta_, nombre_salida):
    entradas = []
    carpeta_ = Path(carpeta_).resolve()

    for root, _, files in os.walk(carpeta_):
        for name in files:
            full = Path(root) / name
            rel = full.relative_to(carpeta_).as_posix()
            entradas.append((rel, full.read_bytes()))

    file_count = len(entradas)
    blob = struct.pack(">I", file_count)

    for path, data in entradas:
        p = path.encode("utf-8")
        blob += struct.pack(">I", len(p))
        blob += p
        blob += struct.pack(">Q", len(data))
        blob += data

    compressed = brotli.compress(blob, quality=11)

    metadata = {
        "package": carpeta_.name,
        "file": file_count,
        "compression": "lpackage"
    }

    meta_bytes = json.dumps(metadata).encode("utf-8")

    with open(nombre_salida, "wb") as f:
        f.write(b"LPKG")
        f.write(b"\x01")
        f.write(struct.pack(">I", len(meta_bytes)))
        f.write(meta_bytes)
        f.write(compressed)

    print("PACKETE CREADO")

compresor_lpackage("aña", "load.lpackage")




def descompresor_lpackage(pkg_path, salida):
    pkg_path = Path(pkg_path)
    salida = Path(salida)

    with pkg_path.open("rb") as f:
        if (f.read(4) != b"LPKG"):
            raise ValueError("Archivo invalido")
        
        if (f.read(1) != b"\x01"):
            raise ValueError("Version no soportada")
        
        meta_len = struct.unpack(">I", f.read(4))[0]
        metadata = json.loads(f.read(meta_len))

        compressed = f.read()

    data = brotli.decompress(compressed)

    offset = 0
    file_count = struct.unpack(">I". data[offset:offset+4])[0]
    offset += 4

    if (file_count == 0):
        raise RuntimeError("Paquete vacio o formato incorrecto")
    
    print("Estrayendo paquete")

    for i in range(file_count):
        p_len = struct.unpack(">I", data[offset:offset+4])[0]
        offset += 4

        path = data[offset:offset+p_len].decode("utf-8")
        offset += p_len

        size = struct.unpack(">Q", data[offset:offset+8])[0]
        offset += 8

        content = data[offset:offset+size]
        offset += size

        out = salida / path
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(content)

        print(f"[ OK ] [{i+1}/{file_count}] {path}")

    print("COMPLETADO")