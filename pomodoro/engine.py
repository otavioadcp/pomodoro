# engine.py
import gi
import os
import pygame

gi.require_version('Gtk', '3.0')
from gi.repository import GObject, GLib

# A nossa classe de lógica herda de GObject.Object para poder emitir sinais
class PomodoroEngine(GObject.Object):
    # Definimos os sinais que a nossa classe pode emitir.
    # Isto permite que a interface gráfica "ouça" as mudanças na lógica.
    __gsignals__ = {
        'tempo-alterado': (GObject.SignalFlags.RUN_FIRST, None, (str,)),
        'estado-alterado': (GObject.SignalFlags.RUN_FIRST, None, (str,)),
        'som-disparado': (GObject.SignalFlags.RUN_FIRST, None, ())
    }

    def __init__(self):
        super().__init__()
        
        # Variáveis de estado internas
        self.tempo_restante_em_segundos = 0
        self.tempo_foco_configurado = 25 * 60
        self.tempo_descanso_configurado = 5 * 60
        
        self.esta_rodando = False
        self.em_sessao_foco = True
        self.timer_id = None
        
        pygame.mixer.init()

    def configurar_tempos(self, minutos_foco, minutos_descanso):
        self.tempo_foco_configurado = minutos_foco * 60
        self.tempo_descanso_configurado = minutos_descanso * 60
        print(f"Tempos configurados: Foco={minutos_foco}min, Descanso={minutos_descanso}min")

    def iniciar(self):
        if not self.esta_rodando:
            self.esta_rodando = True
            if self.em_sessao_foco:
                self.emit('estado-alterado', "A focar...")
            else:
                self.emit('estado-alterado', "A descansar...")
            self.timer_id = GLib.timeout_add_seconds(1, self.on_timer_tick)

    def pausar(self):
        if self.esta_rodando:
            self.esta_rodando = False
            GLib.source_remove(self.timer_id)
            self.timer_id = None
            self.emit('estado-alterado', "Pausado.")

    def reiniciar(self):
        if self.esta_rodando:
            self.pausar()
        
        self.em_sessao_foco = True
        self.tempo_restante_em_segundos = self.tempo_foco_configurado
        self._atualizar_e_emitir_tempo()
        self.emit('estado-alterado', "Pronto para focar?")

    def on_timer_tick(self):
        self.tempo_restante_em_segundos -= 1
        self._atualizar_e_emitir_tempo()

        if self.tempo_restante_em_segundos >= 0:
            return True # Continua o timer
        else:
            self.emit('som-disparado')
            self.esta_rodando = False
            self.em_sessao_foco = not self.em_sessao_foco
            
            if self.em_sessao_foco:
                self.tempo_restante_em_segundos = self.tempo_foco_configurado
                self.emit('estado-alterado', "Descanso concluído! Clique em Iniciar para focar.")
            else:
                self.tempo_restante_em_segundos = self.tempo_descanso_configurado
                self.emit('estado-alterado', "Foco concluído! Clique em Iniciar para descansar.")
            
            self._atualizar_e_emitir_tempo()
            return False # Para o timer

    def _atualizar_e_emitir_tempo(self):
        minutos, segundos = divmod(self.tempo_restante_em_segundos, 60)
        texto_formatado = f"{minutos:02d}:{segundos:02d}"
        # Emite um sinal com o novo tempo para a interface ouvir
        self.emit('tempo-alterado', texto_formatado)