import string

import wx

from raw_gui import RawSpamFrame


class SpamFrame(RawSpamFrame):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.groups = [f'Grupo {g}' for g in string.ascii_uppercase[:5]]

        self.Bind(wx.EVT_BUTTON, self.on_send, self.m_button)

        for i, group in enumerate(self.groups):
            self.m_list.InsertItem(i, group)

    def on_send(self, event):
        selected = [self.m_list.GetFirstSelected()]

        while True:
            next = self.m_list.GetNextSelected(selected[-1])
            if next == -1:
                break
            selected.append(next)

        selected = [self.groups[i] for i in selected]
        typed = self.m_textinput.GetValue()

        dlg = wx.MessageDialog(self,
                               f'Grupos selecionados: {selected}\n'
                               f'Texto digitado: {typed}',
                               'Mensagem',
                               wx.OK
                               )
        dlg.ShowModal()
        dlg.Destroy()


app = wx.App()

frame = SpamFrame(parent=None)
frame.Show()

app.MainLoop()
