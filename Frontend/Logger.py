from dearpygui.dearpygui import add_text
import q
Tag = q.Tag

t = q.Tag.block.Logger.window()
class pat_Logger:
    def __init__(self):
        pass
    def Log(self, message):
        add_text(message, parent=t)
