import os
from gi.repository import Gtk, AyatanaAppIndicator3

class IconManager:
    def __init__(self, icon_folder="icons", icon_filename="pomodoro.png"):
        """
        Encontra o caminho do ícone e verifica se ele existe.
        """
        # Encontra o caminho absoluto para o ícone
        script_dir = os.path.dirname(os.path.abspath(__file__))
        raiz_do_projeto = os.path.dirname(script_dir)
        self.caminho_completo_icone = os.path.join(raiz_do_projeto, icon_folder, icon_filename)
        
        # Verifica e armazena se o ícone foi encontrado
        self.icon_existe = os.path.exists(self.caminho_completo_icone)
        if not self.icon_existe:
            print(f"AVISO (IconManager): Ícone não encontrado em {self.caminho_completo_icone}")

    def aplicar_a_janela(self, window):
        """
        Aplica o ícone a uma janela Gtk.Window.
        """
        if self.icon_existe:
            window.set_icon_from_file(self.caminho_completo_icone)

    def criar_indicador(self):
        """
        Cria e retorna um objeto de indicador da bandeja de sistema, já com o ícone correto.
        """
        if self.icon_existe:
            print(f"SUCESSO (IconManager): A usar ícone personalizado.")
            indicator = AyatanaAppIndicator3.Indicator.new(
                "pomodoro-app-indicator", "pomodoro-custom",
                AyatanaAppIndicator3.IndicatorCategory.APPLICATION_STATUS)
            indicator.set_icon_full(self.caminho_completo_icone, "Pomodoro Timer")
        else:
            print("INFO (IconManager): A usar ícone de sistema como alternativa.")
            indicator = AyatanaAppIndicator3.Indicator.new(
                "pomodoro-app-indicator", "appointment-new",
                AyatanaAppIndicator3.IndicatorCategory.APPLICATION_STATUS)
        
        return indicator