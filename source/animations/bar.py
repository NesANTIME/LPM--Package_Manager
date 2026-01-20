import sys
import time


# funciones internas de bar
def type_style(style):
    if style == "clasic":
        return "■", "□"
    elif style == "modern":
        return "▰", "▱"
    else:
        raise ValueError("[!] [ERROR] Error interno de LPM.")


# Clases internas de animations
class BarAnimation:
    def __init__(self, text, style):
        self.type = style
        self.style = type_style(style)
        self.text = text
        self.margen = 4
        self.carga = 0
        self.visible = False

    def enable(self):
        self.visible = True
        self.render(self.text)

    def disable(self):
        self.visible = False
        self.clear_line()

    def clear_line(self):
        sys.stdout.write(f"\r{' '*4}\033[K")
        sys.stdout.flush()

    def log(self, message: str):
        if self.visible:
            self.clear_line()
            sys.stdout.write(message)
            sys.stdout.write("\n")
            sys.stdout.flush()
            self.render(self.text)
        else:
            print(message)

    def new_valor(self, valor: int, textSend=None):
        self.carga = valor
        if textSend:
            self.text = textSend
        self.render(self.text)

    def barra(self):
        completo, incompleto = self.style
        total = 20
        llenos = min(self.carga // 5, total)
        return completo * llenos + incompleto * (total - llenos)

    def render(self, textSend):
        if not self.visible:
            return

        if self.type == "clasic":
            text = f"\r{' ' * self.margen}[{self.barra()}] {self.carga}% • {textSend}"
        else:
            text = f"\r{' ' * self.margen}{textSend} {self.barra()} {self.carga}%"

        self.clear_line()
        sys.stdout.write(text)
        sys.stdout.flush()
