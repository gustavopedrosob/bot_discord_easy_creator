import tkinter as tk
from interfaces.tkclasses.SearchBox import SearchBox as Sb
from interfaces.commands.newmessage import Commands
from interfaces.colors import *
from interfaces.fonts import *
from interpreter.conditions import conditions_keys
import emoji

class FrameEntrada:
    def main(self):
        frame_preenchimento = tk.Frame(
            master = self.camada_1,
            bg = azul_frame,
            borderwidth = 10,
        )
        self.name_text = tk.Label(
            master = frame_preenchimento,
            text = f"Nome: {self.load}" if self.load else "Nome:",
            font = arial,
            bg = azul_frame,
        )
        self.name = tk.Entry(
            master = frame_preenchimento,
            font = arial,
            bg = azul_entrada,
            relief = tk.FLAT,
            borderwidth = 1,
            selectbackground = azul_selecionado
        )
        expected_message_text = tk.Label(
            master = frame_preenchimento,
            text = "Mensagem esperada",
            font = arial,
            bg = azul_frame,
        )
        expected_message = tk.Entry(
            master = frame_preenchimento,
            font = arial,
            bg = azul_entrada,
            relief = tk.FLAT,
            borderwidth = 1,
            selectbackground = azul_selecionado
        )
        reply_text = tk.Label(
            master = frame_preenchimento,
            text = 'Resposta',
            font = arial,
            bg = azul_frame,
        )
        reply = tk.Entry(
            master = frame_preenchimento,
            font = arial,
            bg = azul_entrada,
            relief = tk.FLAT,
            borderwidth = 1,
            selectbackground = azul_selecionado
        )
        reactions_text = tk.Label(
            master = frame_preenchimento,
            text = 'Reações',
            font = arial,
            bg= azul_frame,
        )
        reactions = Sb(
            master = frame_preenchimento,
            font = arial,
            lista = [v["en"] for v in emoji.EMOJI_DATA.values()],
            master_overlap = self.camada_2,
            bg = azul_entrada,
            relief = tk.FLAT,
            borderwidth = 1,
            selectbackground = azul_selecionado
        )
        conditions_text = tk.Label(
            master = frame_preenchimento,
            text = 'Condições',
            font = arial,
            bg = azul_frame,
        )
        conditions = Sb(
            master = frame_preenchimento,
            font = arial,
            lista = conditions_keys,
            master_overlap = self.camada_2,
            bg = azul_entrada,
            relief = tk.FLAT,
            borderwidth = 1,
            selectbackground = azul_selecionado
        )
        adicionar = tk.Button(
            master = frame_preenchimento,
            text = 'Adicionar',
            command = lambda : Commands.insert_any_on_listbox(self),
            bg = azul_entrada,
            relief = tk.FLAT,
            borderwidth = 1,
        )
        self.name_text.pack(
            fill = tk.X,
            expand = True
        )
        self.name.pack(
            fill = tk.X,
            expand = True
        )
        conditions_text.pack(
            fill = tk.X,
            expand = True
        )
        conditions.pack(
            fill = tk.X,
            expand = True
        )
        expected_message_text.pack(
            fill = tk.X,
            expand = True
        )
        expected_message.pack(
            fill = tk.X,
            expand = True
        )
        reply_text.pack(
            fill = tk.X,
            expand = True
        )
        reply.pack(
            fill = tk.X,
            expand = True
        )
        reactions_text.pack(
            fill = tk.X,
            expand = True
        )
        reactions.pack(
            fill = tk.X,
            expand = True
        )
        adicionar.pack(
            fill = tk.X,
            expand = True,
            pady = 10
        )
        frame_preenchimento.pack(
            side = tk.LEFT,
            fill = tk.BOTH,
            expand = True
        )

        expected_message.bind('<Return>', lambda event: Commands.insert_on_listbox(self, self.listbox_messages, expected_message))
        reply.bind('<Return>', lambda event: Commands.insert_on_listbox(self, self.listbox_replys, reply))
        reactions.bind('<Return>', lambda event: Commands.insert_on_listbox(self, self.listbox_reactions, reactions, limit = 19))
        conditions.bind('<Return>', lambda event: Commands.insert_on_listbox(self, self.listbox_conditions, conditions))
        self.name.bind('<Return>', lambda event: Commands.update_name(self))

        self.lista_de_entradas = [expected_message, reply, reactions, conditions]