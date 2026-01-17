import sys
import argparse

# ~~ modulos internos lpm ~~
from source.animations.icon import icon
from source.core import init_, lpm_version, lpm_restart
from source.controller.update_lpm import System_upgradeLPM


# ~~~ funciones ~~~

def install(args):
    icon()
    name_package = [None, args.package]

    if (args.v):
        name_package = ["mode_v", name_package, args.v]
    if (args.force):
        name_package = ["mode_force", name_package]

    init_("install", name_package)


def search(args):
    icon()
    init_("search", args.package)

def list(args):
    icon()
    init_("list", None)

def update(args):
    icon()
    init_("update", None)

def use(args):
    init_("use", [args.package, args.args_script])

def remove(args):
    print(f"Desinstalando el paquete {args.name}...")

#def delivery_config():
#    print("En Desarrollo")





parser = argparse.ArgumentParser( prog="lpm", description="Administrador de paquetes by NesAnTime.")

parser.add_argument('--upgrade-now', action='store_true', help='[!] Actualizar lpm desde el repositorio!')
parser.add_argument('--upgrade-now-force', action='store_true', help='[!] Forzar actualizar lpm desde el repositorio')
parser.add_argument('--restart', action='store_true', help='[!] Reiniciar archivos e instalaciones de lpm')
parser.add_argument('--version', action='store_true', help='[!] Mostrar version LPM!')

subparsers = parser.add_subparsers(dest="command")


install_parser = subparsers.add_parser("install", help="[!] Instala un paquete.")
install_parser.add_argument("package")
install_parser.add_argument("--force", help="Forzar la instalacion del paquete", default=None)
install_parser.add_argument("--v", help="Versión específica del paquete", default=None)
install_parser.set_defaults(func=install)


search_parser = subparsers.add_parser("search", help="[!] Busca un paquete.")
search_parser.add_argument("package")
search_parser.set_defaults(func=search)


use_parser = subparsers.add_parser("use", help="[!] Ejecuta un paquete.")
use_parser.add_argument("package")
use_parser.add_argument('args_script', nargs=argparse.REMAINDER, help='Argumentos del ejecutable')
use_parser.set_defaults(func=use)


remove_parser = subparsers.add_parser("remove", help="[!] Desinstalar un paquete.")
remove_parser.add_argument("name")
remove_parser.set_defaults(func=remove)

 
list_parser = subparsers.add_parser("list", help="[!] Listar los paquetes instalados.")
list_parser.set_defaults(func=list)


update_parser = subparsers.add_parser("update", help="[!] Actualizar todos los paquetes instalados.")
update_parser.set_defaults(func=update)


args = parser.parse_args()

if (args.version):
    icon()
    lpm_version()
    sys.exit(0)

if (args.upgrade_now) or (args.upgrade_now_force):
    icon()
    if (args.upgrade_now):
        System_upgradeLPM("normal")
    else:
        System_upgradeLPM("force")

    sys.exit(0)

if (args.restart):
    icon()
    lpm_restart()
    sys.exit(0)


if (hasattr(args, "func")):
    args.func(args)
else:
    icon()
    parser.print_help()