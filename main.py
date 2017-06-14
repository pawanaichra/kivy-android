from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
import socket
import thread

host = "192.168.0.101"
port = 9009
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

class MainGridLayout(GridLayout):
    message_to_send = ""
    
    def __init__(self, **kwargs):
        super(MainGridLayout, self).__init__(**kwargs)
        Window.bind(on_key_down=self.key_action)
        self.ids.label1.text = str("Welcome")
        thread.start_new_thread(self.handleClientMessages, ())

    def key_action(self, *args):
        if args[1] == 13:
        	self.send_message()


    def Display_Message(self, message_to_send):
        self.ids.label1.text = str(message_to_send)
        
    def send_message(self):
        thread.start_new_thread(self.handleSentMessages, (self.ids.entry.text,))

    def handleSentMessages(self, message):
        self.message_to_send = self.message_to_send + "Pawan: " + message + "\n"
        self.Display_Message(self.message_to_send)
        self.ids.entry.text = ""
        s.send(message + "\n")

    def handleClientMessages(self):
        while 1:
            try:
                data = s.recv(1024)
                print data
                if not data:
                    break
                self.message_to_send = self.message_to_send + str(data)
                self.Display_Message(self.message_to_send)
            except:
                break
        s.close()


class MainApp(App):
    def build(self):
        return MainGridLayout()

if __name__ == '__main__':
    MainApp().run()
