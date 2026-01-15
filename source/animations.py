import sys
import time
import random
import itertools

# ~~ modulos internos lpm ~~
from source.modules.load_config import load_config, check_newVersion


# Clases de animaciones
class BarAnimation:
    def __init__(self, text, style, espacio: int):
        if style == "clasic":
            self.estilo = "■", "□"
        elif style == "modern":
            self.estilo = "▰", "▱"
        else:
            raise ValueError("Estilo no válido")

        self.espacio = espacio
        self.style = style
        self.text = text
        self.carga = 0

    def new_valor(self, valor: int, textSend=None):
        self.carga = valor
        self.render(self.text)

        time.sleep(1)

        if textSend is not None:
            self.text = textSend
        self.render(self.text)

    def barra(self):
        completo, incompleto = self.estilo
        total = 20
        llenos = min(self.carga // 5, total)
        vacios = total - llenos
        return completo * llenos + incompleto * vacios

    def render(self, textSend):
        if self.style == "clasic":
            text = f"\r{' ' * self.espacio}[{self.barra()}] {self.carga}%  • {textSend}"
        else:
            text = f"\r{' ' * self.espacio}{textSend} {self.barra()} {self.carga}%"

        sys.stdout.write("\r" + " " * 80)
        sys.stdout.write(text)
        sys.stdout.flush()

    


# ~~~ funciones principales de animacion ~~~

def icon():
    config_json = load_config()
    info_newVersion = check_newVersion()

    icon = config_json["info"]["icon"]

    if (info_newVersion != False):
        icon[1] += info_newVersion

    for i in config_json["info"]["icon"]:
        print(i)


def message_animation(msg, msg_completed, duration = 0.8, num = 1):
    spinner = itertools.cycle("⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏")
    end_time = time.time() + duration
    indent = " " * num

    while time.time() < end_time:
        sys.stdout.write(f"\r\033[K{indent}{msg} {next(spinner)}")
        sys.stdout.flush()
        time.sleep(0.1)

    sys.stdout.write(f"\r\033[K{indent}{msg_completed}\n")
    sys.stdout.flush()
