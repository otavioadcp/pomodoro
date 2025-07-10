# main_window.py
import gi
import os
import pygame
import logging

gi.require_version('Gtk', '3.0')
gi.require_version('AyatanaAppIndicator3', '0.1')
from gi.repository import Gtk, AyatanaAppIndicator3

# Importamos a nossa classe de lógica
from src.engine import PomodoroEngine
from src.sound_manager import SoundManager
from src.icon_manager import IconManager

class JanelaPrincipal(Gtk.Window):
    def __init__(self):
        super().__init__(title="Pomodoro Timer")
        self.set_icon_name("pomodoro")
        self.set_default_size(350, 400)
        self.connect("delete-event", self.on_janela_fechar)

        
        self.motor = PomodoroEngine() # Instância do motor de lógica
        self.sound_manager = SoundManager() # Instância do SoundManager
        self.icon_manager = IconManager() # Instância para carregar o icone da aplicação

        # Conectar os sinais do motor aos métodos desta classe
        self.motor.connect('tempo-alterado', self.on_motor_tempo_alterado)
        self.motor.connect('estado-alterado', self.on_motor_estado_alterado)
        self.motor.connect('som-disparado', self.on_motor_som_disparado)
        
        # --- Construção da UI ---
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox.set_margin_top(15); vbox.set_margin_bottom(15); vbox.set_margin_start(15); vbox.set_margin_end(15)
        self.add(vbox)
        
        self.label_status = Gtk.Label()
        vbox.pack_start(self.label_status, False, False, 0)

        self.label_tempo = Gtk.Label()
        vbox.pack_start(self.label_tempo, True, True, 0)

        hbox_botoes = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox_botoes.set_halign(Gtk.Align.CENTER)
        vbox.pack_start(hbox_botoes, False, False, 10)
        
        self.botao_iniciar = Gtk.Button(label="Iniciar")
        self.botao_pausar = Gtk.Button(label="Pausar")
        self.botao_reiniciar = Gtk.Button(label="Reiniciar")
        
        hbox_botoes.pack_start(self.botao_iniciar, True, True, 0)
        hbox_botoes.pack_start(self.botao_pausar, True, True, 0)
        hbox_botoes.pack_start(self.botao_reiniciar, True, True, 0)

        self.botao_iniciar.connect("clicked", self.on_iniciar_clicado)
        self.botao_pausar.connect("clicked", self.on_pausar_clicado)
        self.botao_reiniciar.connect("clicked", self.on_reiniciar_clicado)

        grid_config = Gtk.Grid(column_spacing=10, row_spacing=5, halign=Gtk.Align.CENTER)
        vbox.pack_start(grid_config, False, False, 10)

        ajuste_foco = Gtk.Adjustment(value=25, lower=1, upper=120, step_increment=1, page_increment=5)
        self.spin_foco = Gtk.SpinButton(adjustment=ajuste_foco, climb_rate=1, digits=0)
        grid_config.attach(Gtk.Label(label="Tempo de Foco (min):", xalign=1), 0, 0, 1, 1)
        grid_config.attach(self.spin_foco, 1, 0, 1, 1)

        ajuste_descanso = Gtk.Adjustment(value=5, lower=1, upper=60, step_increment=1, page_increment=5)
        self.spin_descanso = Gtk.SpinButton(adjustment=ajuste_descanso, climb_rate=1, digits=0)
        grid_config.attach(Gtk.Label(label="Tempo de Descanso (min):", xalign=1), 0, 1, 1, 1)
        grid_config.attach(self.spin_descanso, 1, 1, 1, 1)

        self.pasta_sons = "sounds"
        self.lista_sons = [f for f in os.listdir(self.pasta_sons) if f.endswith(('.wav', '.mp3'))]
        self.lista_sons.sort()
        self.combo_som = Gtk.ComboBoxText()
        for som in self.lista_sons: self.combo_som.append_text(som)
        self.combo_som.set_active(0)
        grid_config.attach(Gtk.Label(label="Alerta Sonoro:", xalign=1), 0, 2, 1, 1)
        grid_config.attach(self.combo_som, 1, 2, 1, 1)
        
        
        # --------- Configurar Icone da aplicação -----------
        self.icon_manager.aplicar_a_janela(self) # "self" é a própria janela
        self.indicator = self.icon_manager.criar_indicador() # Pega no indicador já pronto

        self.indicator.set_status(AyatanaAppIndicator3.IndicatorStatus.ACTIVE)
        self.menu = Gtk.Menu()
        item_mostrar = Gtk.MenuItem(label="Mostrar Janela"); item_mostrar.connect("activate", self.on_mostrar); self.menu.append(item_mostrar)
        item_sair = Gtk.MenuItem(label="Sair"); item_sair.connect("activate", self.on_sair); self.menu.append(item_sair)
        self.menu.show_all()
        self.indicator.set_menu(self.menu)
        # ---------------------------------------------------
        
        
        # Inicia o estado da aplicação
        self.on_reiniciar_clicado(None)

    # --- Métodos que reagem aos cliques ---
    def on_iniciar_clicado(self, widget):
        self.motor.iniciar()

    def on_pausar_clicado(self, widget):
        self.motor.pausar()

    def on_reiniciar_clicado(self, widget):
        foco = self.spin_foco.get_value_as_int()
        descanso = self.spin_descanso.get_value_as_int()
        self.motor.configurar_tempos(foco, descanso)
        self.motor.reiniciar()

    # --- Métodos que reagem aos sinais do motor ---
    def on_motor_tempo_alterado(self, motor, texto_tempo):
        self.label_tempo.set_markup(f"<span size='xx-large' weight='bold'>{texto_tempo}</span>")
    
    def on_motor_estado_alterado(self, motor, texto_status):
        self.label_status.set_text(texto_status)
    
    def on_motor_som_disparado(self, motor):
        """
        Este método é chamado quando o motor diz que é hora de tocar um som.
        Ele pega a seleção da UI e manda para o SoundManager.
        """
        som_selecionado = self.combo_som.get_active_text()
        self.sound_manager.play_sound(som_selecionado) # Delega a tarefa!

    # --- Métodos de controle da janela em si ---
    def on_mostrar(self, widget): self.show_all()
    def on_janela_fechar(self, widget, event): self.hide(); return True
    def on_sair(self, widget): Gtk.main_quit()