import wx
from raw_gui import RawSpamFrame
import string
from client import SteveBannonClient
import telegram, config


class SpamFrame(RawSpamFrame):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.Bind(wx.EVT_BUTTON, self.on_send, self.m_button)

        self.post_init()


    def post_init(self):

        config.client.connect()
        if config.client.is_user_authorized():
            self.init_telegram_data()
        else:
            dlg = wx.TextEntryDialog(None, 'Digite seu número de telefone', 'Autenticação')
            if dlg.ShowModal() == wx.ID_OK:
                config.client.send_code_request(dlg.GetValue())
                dlg = wx.TextEntryDialog(None, 'Digite o código recebido', 'Autenticação')
                if dlg.ShowModal() == wx.ID_OK:
                    config.client.sign_in(code=dlg.GetValue())
                    self.post_init()


    def init_telegram_data(self):
        self.groups = telegram.get_all_dialogs()
        print(self.groups)
            
        for i, group in enumerate(self.groups):
            self.m_list.InsertItem(i, group.name)


    def on_send(self, event):
        selected = [self.m_list.GetFirstSelected()]

        while True:
            next = self.m_list.GetNextSelected(selected[-1])
            if next == -1:
                break
            selected.append(next)

        selected = [self.groups[i] for i in selected]

        typed = self.m_textinput.GetValue()
        times = self.m_spinCtrl1.GetValue()

        for chat in selected:
            telegram.send_message(chat, typed, loop=times)

        self.m_textinput.SetValue('')

        dlg = wx.MessageDialog(self,
                               f'Texto digitado: {typed}',
                               'Mensagem enviada',
                               wx.OK
                               )
        dlg.ShowModal()
        dlg.Destroy()



app = wx.App()

frame = SpamFrame(parent=None)
frame.Show()

app.MainLoop()
