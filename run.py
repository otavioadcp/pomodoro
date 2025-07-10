import gi
import sys

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from src.main_window import JanelaPrincipal

class App:
    def __init__(self):
        # Cria e mostra a janela principal
        win = JanelaPrincipal()
        win.show_all()

if __name__ == '__main__':
    app = App()
    # Inicia o loop principal do GTK
    Gtk.main()