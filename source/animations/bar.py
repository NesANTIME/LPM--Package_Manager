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

    def new_valor(self, valor: int, textSend=None):
        self.carga = valor
        self.render(self.text)

        time.sleep(1)

        if textSend is not None:
            self.text = textSend

        self.render(self.text)

    def barra(self):
        completo, incompleto = self.style
        total = 20
        llenos = min(self.carga // 5, total)
        vacios = total - llenos
        return completo * llenos + incompleto * vacios

    def render(self, textSend):
        if self.type == "clasic":
            text = f"\r{' ' * self.margen}[{self.barra()}] {self.carga}%  • {textSend}"
        else:
            text = f"\r{' ' * self.margen}{textSend} {self.barra()} {self.carga}%"

        sys.stdout.write("\r" + " " * 100)
        sys.stdout.write(text)
        sys.stdout.flush()
