from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import AsyncImage
from kivy.properties import StringProperty, ListProperty, ObjectProperty
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.list import TwoLineListItem, ThreeLineListItem, OneLineListItem
from kivy.metrics import dp
from kivy.factory import Factory
from kivy.uix.textinput import TextInput
import datetime
import time, socket

Window.size = (350, 480)

kv = Builder.load_file("Begin_Work.kv")

number = 0  # Нужен
password = ""  # Нужен

command_for_server = ""  # Нужен
info = ""  # Нужен

value_kurs = []
kurs_valut_command = []

text = ""

number_card_for_transfer=""

class MainWindow(Screen):
    card = ObjectProperty()
    check_number_card = ObjectProperty()

    s = socket.socket()

    def message_to_number_card(self):
        global command_for_server, info
        command_for_server = "check_number_card"
        info = self.card.text
        Important = MyMainApp()
        Important.send_message()

    def Not_Perexod(self):
        pass

    def Perexod_Second(self):
        g = MyMainApp()
        gh = g.Check_Server_Answer()
        if gh == "Zapis_1":
            self.manager.current = "SecondWindow"
            self.manager.transition.direction = "left"
        else:
            pass

    def Perexod_To_SecondWindows(self):
        self.message_to_number_card()
        g = MyMainApp()
        t = g.Check_Server_Answer()
        print(t)
        if t == "OK":
            self.manager.current = "SecondWindow"
            self.manager.transition.direction = "left"
        else:
            pass

    def Number_Card(self):
        k = 0
        text_card = ""
        legit = 0
        for i in self.card.text.split(' '):
            for char in i:
                if char.isdigit():
                    text_card = char + text_card

            if len(text_card) == 4:
                legit = len(text_card) + legit
                k = k + 1
                text_card = ""
            elif (len(text_card) > 4 or len(text_card) < 4) and text_card.isdigit() == False:
                pass

        if k == 4:
            self.check_number_card = "Yes"
            k = 0
            time.sleep(0.5)
        else:
            time.sleep(0.5)
            k = 0
            self.check_number_card = "No"
        return self.check_number_card


class SecondWindow(Screen):
    one_Num_text = ObjectProperty()
    two_Num_text = ObjectProperty()
    third_Num_text = ObjectProperty()
    four_Num_text = ObjectProperty()
    five_Num_text = ObjectProperty()
    check_pass = ObjectProperty()

    Name = ""
    Surname = ""
    Number_Card = ""
    Money = ""

    password = ""

    def Perexod_To_Wait(self):
        global command_for_server, info
        command_for_server = "add_password"
        info = password
        Important = MyMainApp()
        Important.send_message()
        t = Important.Check_Server_Answer()
        print(t)
        if t == "OK":
            print(self)
            self.manager.current = "WindowsWait"
            self.manager.transition.direction = "left"
        else:
            pass

    def Password_add(self, instance):
        global number
        global password
        if number < 5:
            if number == 0:
                self.one_Num_text.text = instance.text
                password = password + instance.text
                number = number + 1
            elif number == 1:
                self.two_Num_text.text = instance.text
                password = password + instance.text
                number = number + 1
            elif number == 2:
                self.third_Num_text.text = instance.text
                password = password + instance.text
                number = number + 1
            elif number == 3:
                self.four_Num_text.text = instance.text
                password = password + instance.text
                number = number + 1
            elif number == 4:
                self.five_Num_text.text = instance.text
                password = password + instance.text
                number = number + 1

    def Password_clear(self, instance):
        global number
        global password
        if number != 0:
            if number == 1:
                #self.one_Num_text.text = "0"
                self.one_Num_text.clear()
                password = password[0:-1]
                number = number - 1
            elif number == 2:
                #self.two_Num_text.text = ""
                self.two_Num_text.clear()
                password = password[0:-1]
                number = number - 1
            elif number == 3:
                self.third_Num_text.text = ""
                password = password[0:-1]
                number = number - 1
            elif number == 4:
                #self.four_Num_text.text = ""
                self.four_Num_text.clear()
                password = password[0:-1]
                number = number - 1
            elif number == 5:
                self.five_Num_text.text = ""
                password = password[0:-1]
                number = number - 1

    def Check_Password(self):
        global password
        if len(password) == 5:
            if password.isdigit() == True:
                self.check_pass = "Yes"
        else:
            self.check_pass = "No"

        return self.check_pass

    def Info_Client(self):
        g = MyMainApp()
        data = g.Check_Server_Answer()
        k = 0
        num = 0
        for i in data.split(' '):
            if k == 0:
                SecondWindow.Name = i
                k = k + 1
            elif k == 1:
                SecondWindow.Surname = i
                k = k + 1
            elif k == 2 and num < 4:
                SecondWindow.Number_Card = SecondWindow.Number_Card + i
                SecondWindow.Number_Card = SecondWindow.Number_Card + " "
                num = num + 1
            else:
                SecondWindow.Money = i


class Windows3(Screen):
    items_text = ""

    def Perexod_Kurs(self):
        self.manager.current = "WindowsKurs"
        self.manager.transition.direction = "left"

    def Perexod_Credit_Card(self):
        self.manager.current = "WindowsCreditMenu"
        self.manager.transition.direction = "left"

    def Perexod_Istoria_Pay(self):
        self.manager.current = "WindowsIstoriaPay"
        self.manager.transition.direction = "left"

    def Perexod_Map(self):
        self.manager.current = "WindowsMap"
        self.manager.transition.direction = "left"

    def Perexod_Pay(self):
        self.manager.current = "WindowsPay"
        self.manager.transition.direction = "left"

    def Kurs_Valut(self, s):
        global kurs_valut_command, value_kurs
        data = s.recv(1024).decode()
        for i in data.replace(',', '.').split(' '):
            if is_number(i):
                value_kurs.append(i)
            else:
                kurs_valut_command.append(i)

    def Credit_Card(self):
        money_text = str("%.2f" % float(SecondWindow.Money))
        Windows3.items_text = TwoLineListItem(text=f"Номер карты: {SecondWindow.Number_Card}",
                                              secondary_text=f"Баланc карты: {money_text} ₽")
        self.ids.osnova_credit_card.add_widget(Windows3.items_text)

    def Clear_Credit_Card(self):
        self.ids.osnova_credit_card.remove_widget(Windows3.items_text)
        Windows3.items_text = ""


class WindowsKurs(Screen):
    text_value_USD = StringProperty()
    text_value_EUR = StringProperty()
    text_value_GBP = StringProperty()
    text_value_TRY = StringProperty()

    text_value_sell_USD = StringProperty()
    text_value_sell_EUR = StringProperty()
    text_value_sell_GBP = StringProperty()
    text_value_sell_TRY = StringProperty()

    def Back_Perexod(self):
        self.manager.current = "Windows3"
        self.manager.transition.direction = "right"

    def Check_Value_Kurs(self):
        global kurs_valut_command, value_kurs
        for i in range(len(value_kurs)):
            if kurs_valut_command[i] == "USD":
                self.text_value_USD = value_kurs[i]
                self.text_value_sell_USD = str(float(value_kurs[i]) - 0.75)
            elif kurs_valut_command[i] == "EUR":
                self.text_value_EUR = value_kurs[i]
                self.text_value_sell_EUR = str(float(value_kurs[i]) - 1.25)
            elif kurs_valut_command[i] == "GBP":
                self.text_value_GBP = value_kurs[i]
                self.text_value_sell_GBP = str(float(value_kurs[i]) - 2.5)
            elif kurs_valut_command[i] == "TRY":
                self.text_value_TRY = value_kurs[i]
                self.text_value_sell_TRY = str(float(value_kurs[i]) - 1.75)


def is_number(str):
    try:
        float(str)
        return True
    except ValueError:
        return False


def is_date(str):
    try:
        datetime.datetime.strptime(str, '%d.%m.%Y')
        return True
    except:
        return False


class WindowsWait(Screen):
    surname_text = ObjectProperty()
    text_name = ObjectProperty()

    def Wait(self):
        time.sleep(6)
        self.op = 10

    def Zastavka(self):
        g = SecondWindow()
        self.text_surname.text = g.Surname
        self.text_name.text = g.Name


class WindowsCreditMenu(Screen):
    number = []
    money = []
    text_item = ""
    text_item_text = ""
    items = []
    text_data = ""

    def Back_Menu(self):
        self.manager.current = "Windows3"
        self.manager.transition.direction = "right"

    def Credit_Card_Other(self):
        number_balans = []
        money = []
        text_1 = ""
        k = 0
        WindowsCreditMenu.text_data = MyMainApp().Check_Server_Answer()
        if WindowsCreditMenu.text_data != "Nothing":
            for i in WindowsCreditMenu.text_data.split(' '):
                if i != "/" and k < 4:
                    text_1 = text_1 + i
                    text_1 = text_1 + " "
                    k += 1
                elif i != "/" and not k < 4:
                    money.append(str("%.2f" % float(i)))
                elif i == "/":
                    number_balans.append(text_1)

            for i in range(len(number_balans)):
                items_text = TwoLineListItem(text=f"Номер карты: {number_balans[i]}",
                                             secondary_text=f"Баланc карты: {money[i]} ₽")
                self.ids.container.add_widget(items_text)
                WindowsCreditMenu.items.append(items_text)

        else:
            WindowsCreditMenu.items_text = OneLineListItem(text="Дополнительных карт нет")
            self.ids.container.add_widget(WindowsCreditMenu.items_text)

    def Credit_Card_Osnova(self):
        money_text = str("%.2f" % float(SecondWindow.Money))
        WindowsCreditMenu.text_item_text = TwoLineListItem(text=f"Номер карты: {SecondWindow.Number_Card}",
                                                           secondary_text=f"Баланc карты: {money_text} ₽")
        self.ids.container_1.add_widget(WindowsCreditMenu.text_item_text)

    def Clear(self):
        if WindowsCreditMenu.text_data != "Nothing":
            for i in range(len(WindowsCreditMenu.items)):
                self.ids.container.remove_widget(WindowsCreditMenu.items[i])
            WindowsCreditMenu.items.clear()
            self.ids.container_1.remove_widget(WindowsCreditMenu.text_item_text)
        else:
            self.ids.container.remove_widget(WindowsCreditMenu.items_text)
            self.ids.container_1.remove_widget(WindowsCreditMenu.text_item_text)
            WindowsCreditMenu.text_item_text = ""
            WindowsCreditMenu.items_text = ""
            WindowsCreditMenu.text_data = ""


class WindowsIstoriaPay(Screen):
    operation_card = []
    number_card_send = []
    number_card_prinimal = []
    money_send = []
    date_send = []
    items = []
    text = ""

    def Back_Menu(self):
        self.manager.current = "Windows3"
        self.manager.transition.direction = "right"

    def Create_Table(self):
        WindowsIstoriaPay.text = MyMainApp().Check_Server_Answer()
        text_number = ""
        k = 0
        kol = 0
        if WindowsIstoriaPay.text != "Nothing":
            for i in WindowsIstoriaPay.text.split(' '):
                if not i.isdigit() and not (i == "//" or i == '/') and is_number(i) == False and is_date(i) == False:
                    WindowsIstoriaPay.operation_card.append(i)
                elif i.isdigit() and k < 4 and kol == 0:
                    text_number = text_number + i
                    text_number = text_number + " "
                    k += 1
                elif i == "//" and kol == 0:
                    k = 0
                    WindowsIstoriaPay.number_card_send.append(text_number)
                    text_number = ""
                    kol += 1
                elif i.isdigit() and k < 4 and kol >= 1:
                    text_number = text_number + i
                    text_number = text_number + " "
                    k += 1
                elif i == "//" and kol >= 1:
                    k = 0
                    WindowsIstoriaPay.number_card_prinimal.append(text_number)
                    text_number = ""
                    kol += 1
                elif kol >= 1 and is_number(i):
                    WindowsIstoriaPay.money_send.append(str("%.2f" % float(i)))
                elif i == "/":
                    k = 0
                    text_number = ""
                    kol = 0
                elif is_date(i) == True:
                    WindowsIstoriaPay.date_send.append(i)

    def Open_Table(self):
        if WindowsIstoriaPay.text != "Nothing":
            for i in range(len(WindowsIstoriaPay.date_send)):
                items = ThreeLineListItem(text=f"Дата: {WindowsIstoriaPay.date_send[i]}",
                                          secondary_text=f"Карта получателя: {WindowsIstoriaPay.number_card_prinimal[i]}",
                                          tertiary_text=f"{WindowsIstoriaPay.money_send[i]} ₽")
                WindowsIstoriaPay.items.append(items)
                self.ids.histori_pay.add_widget(items)
        else:
            items = OneLineListItem(text="Истории переводов нет")
            self.ids.histori_pay.add_widget(items)
            WindowsIstoriaPay.items.append(items)

    def Clear_Table(self):
        if WindowsIstoriaPay.text != "Nothing":
            for i in range(len(WindowsIstoriaPay.items)):
                self.ids.histori_pay.remove_widget(WindowsIstoriaPay.items[i])
            WindowsIstoriaPay.items.clear()
            WindowsIstoriaPay.operation_card.clear()
            WindowsIstoriaPay.number_card_send.clear()
            WindowsIstoriaPay.number_card_prinimal.clear()
            WindowsIstoriaPay.money_send.clear()
            WindowsIstoriaPay.date_send.clear()
        else:
            self.ids.histori_pay.remove_widget(WindowsIstoriaPay.items[0])
            WindowsIstoriaPay.text = ""
            WindowsIstoriaPay.items.clear()
            WindowsIstoriaPay.operation_card.clear()
            WindowsIstoriaPay.number_card_send.clear()
            WindowsIstoriaPay.number_card_prinimal.clear()
            WindowsIstoriaPay.money_send.clear()
            WindowsIstoriaPay.date_send.clear()


class WindowsPass(Screen):
    one_Num_text = ObjectProperty()
    two_Num_text = ObjectProperty()
    third_Num_text = ObjectProperty()
    four_Num_text = ObjectProperty()
    five_Num_text = ObjectProperty()
    check_pass = ObjectProperty()

    SecondWindow.Name = ""
    SecondWindow.Surname = ""
    SecondWindow.Number_Card = ""
    SecondWindow.Money = ""

    password = ""

    def Password_add(self, instance):
        global number
        global password
        if number < 5:
            if number == 0:
                self.one_Num_text.text = "*"
                password = password + instance.text
                number = number + 1
            elif number == 1:
                self.two_Num_text.text = "*"
                password = password + instance.text
                number = number + 1
            elif number == 2:
                self.third_Num_text.text = "*"
                password = password + instance.text
                number = number + 1
            elif number == 3:
                self.four_Num_text.text = "*"
                password = password + instance.text
                number = number + 1
            elif number == 4:
                self.five_Num_text.text = "*"
                password = password + instance.text
                number = number + 1

    def Password_clear(self, instance):
        global number
        global password
        if number != 0:
            if number == 1:
                self.one_Num_text.text = ""
                password = password[0:-1]
                number = number - 1
            elif number == 2:
                self.two_Num_text.text = ""
                password = password[0:-1]
                number = number - 1
            elif number == 3:
                self.third_Num_text.text = ""
                password = password[0:-1]
                number = number - 1
            elif number == 4:
                self.four_Num_text.text = ""
                password = password[0:-1]
                number = number - 1
            elif number == 5:
                self.five_Num_text.text = ""
                password = password[0:-1]
                number = number - 1

    def Check_Password(self):
        global password
        if len(password) == 5:
            if password.isdigit() == True:
                self.check_pass = "Yes"
        else:
            self.check_pass = "No"

        return self.check_pass

    def Info_Client_ID(self):
        k = 0
        kol = 0
        text_number_card = ""
        g = MyMainApp()
        text = g.Check_Server_Answer()
        for i in text.split(' '):
            if kol == 0:
                SecondWindow.Surname = i
                kol += 1
            elif kol == 1:
                SecondWindow.Name = i
                kol += 1
            elif kol == 2 and k < 4:
                text_number_card = text_number_card + i + " "
                k += 1
            elif kol == 2 and not k < 4:
                SecondWindow.Number_Card = text_number_card
                SecondWindow.Money = i
                kol += 1
                k = 0

    def Perexod_To_Wait(self):
        global password
        g = MyMainApp()
        g.Send_Password()
        text = g.Check_Server_Answer()
        print(self)
        if text == password:
            self.manager.current = "WindowsWait"
            self.manager.transition.direction = "left"
        else:
            pass


class WindowsMap(Screen):

    def Back_Menu(self):
        self.manager.current = "Windows3"
        self.manager.transition.direction = "right"
    pass


class WindowsPay(Screen):
    number = []
    money = []
    text_item = ""
    text_item_text = ""
    items = []
    text_data = ""
    number_Card_For_Transfer=ObjectProperty()
    money_For_Transfer=ObjectProperty()
    balance=""


    def Back_Menu(self):
        self.manager.current = "Windows3"
        self.manager.transition.direction = "right"
    pass

    def Credit_Card(self):
        money_text = str("%.2f" % float(SecondWindow.Money))
        WindowsPay.items_text = TwoLineListItem(text=f" {SecondWindow.Number_Card}",
                                              secondary_text=f" {money_text} ₽")
        self.ids.osnova_credit_card.add_widget(WindowsPay.items_text)

    def Transfer(self):
        global command_for_server, info
        #if self.money_For_Transfer.text<int(TwoLineListItem.secondary_text):
        command_for_server = "Transfer_To_Card"
        info=self.number_Card_For_Transfer.text+" // "+self.money_For_Transfer.text+" // "+SecondWindow.Number_Card
        Important = MyMainApp()
        Important.send_message()
        t = Important.Check_Server_Answer()
        print(t)
        if t == "OK":
            print(self)
            self.manager.current = "WindowsWait"
            self.manager.transition.direction = "left"
        else:
            pass
        # command_for_server = "add_transfer"
        # info = self.number_Card_For_Transfer.text + " // " + self.money_For_Transfer.text + " // " + SecondWindow.Number_Card
        # Important = MyMainApp()
        # Important.send_message()
        # g = MyMainApp()
        # data = g.Check_Server_Answer()
            #balance=data
            #t = Important.Check_Server_Answer()
            #print(t)
        #else: "Недостаточно средст для перевода"
            # if t == "OK":
            #     print(self)
            #     self.manager.current = "WindowsPaySuccess"
            #     self.manager.transition.direction = "left"
             #else:
                #pass


class WindowsPaySuccess(Screen):

    def Back_Menu(self):
        self.manager.current = "Windows3"
        self.manager.transition.direction = "right"

    # def Credit_Card(self):
    #     #money_text = str("%.2f" % float(SecondWindow.Money))
    #     WindowsPaySuccess.items_text = OneLineListItem(text=f" {SecondWindow.Number_Card}")
    #                                           #secondary_text=f" {money_text} ₽")
    #     self.ids.osnova_credit_card.add_widget(WindowsPaySuccess.items_text)
    #
    # def Balance(self):
    #     WindowsPaySuccess.items_text = OneLineListItem(text=f" {WindowsPay.balance}")
    #     self.ids.balance.add_widget(WindowsPaySuccess.items_text)

    pass


class MyMainApp(MDApp):
    check_number_card = ""
    check_pass = ""

    host = '127.0.0.1'
    port = 7000

    s = socket.socket()

    def build(self):
        MyMainApp().connect_to_server()
        MyMainApp().Send_Server_Check_Zapis()
        text = MyMainApp().Check_Server_Answer()
        screen_manager = ScreenManager()
        if text != "Zapis_1":
            screen_manager.add_widget(MainWindow(name='MainWindow'))
            screen_manager.add_widget(SecondWindow(name='SecondWindow'))
            screen_manager.add_widget(Windows3(name='Windows3'))
            screen_manager.add_widget(WindowsWait(name='WindowsWait'))
            screen_manager.add_widget(WindowsKurs(name='WindowsKurs'))
            screen_manager.add_widget(WindowsCreditMenu(name='WindowsCreditMenu'))
            screen_manager.add_widget(WindowsIstoriaPay(name='WindowsIstoriaPay'))
            screen_manager.add_widget(WindowsMap(name='WindowsMap'))
            screen_manager.add_widget(WindowsPay(name='WindowsPay'))
            screen_manager.add_widget(WindowsPaySuccess(name='WindowsPaySuccess'))

        else:
            screen_manager.add_widget(WindowsPass(name='WindowsPass'))
            screen_manager.add_widget(WindowsWait(name='WindowsWait'))
            screen_manager.add_widget(Windows3(name='Windows3'))
            screen_manager.add_widget(WindowsKurs(name='WindowsKurs'))
            screen_manager.add_widget(WindowsCreditMenu(name='WindowsCreditMenu'))
            screen_manager.add_widget(WindowsIstoriaPay(name='WindowsIstoriaPay'))
            screen_manager.add_widget(WindowsMap(name='WindowsMap'))
            screen_manager.add_widget(WindowsPay(name='WindowsPay'))
            screen_manager.add_widget(WindowsPaySuccess(name='WindowsPaySuccess'))


        return screen_manager


    def connect_to_server(self):
        self.s.connect((self.host, self.port))

    def send_message(self):
        global info, command_for_server
        self.message = info
        self.command = command_for_server
        self.s.send(self.command.encode())
        self.s.send(self.message.encode())


    def Send_Server_Live_Check(self):
        self.command = "check_server"
        self.s.send(self.command.encode())

    def Send_Server_Check_Zapis(self):
        self.command = "check"
        self.s.send(self.command.encode())

    def Send_Server_Command_Kurs_Valut(self):
        self.command = "kurs_valut"
        self.s.send(self.command.encode())
        g = Windows3()
        g.Kurs_Valut(self.s)

    def Info_User(self):
        self.command = "Info_User"
        self.s.send(self.command.encode())

    def Info_User_Card_Other(self):
        self.command = "Info_User_Other_Card"
        self.s.send(self.command.encode())

    def Histori_Operation(self):
        self.command = "Operation_Histori"
        self.s.send(self.command.encode())

    def Find_SurnameName_Password(self):
        self.command = "zapis_password_for_id"
        self.s.send(self.command.encode())

    def Check_Server_Answer(self):
        data = str(self.s.recv(1024).decode())
        return data

    def Send_Password(self):
        self.command = "Send_Password"
        self.s.send(self.command.encode())


if __name__ == "__main__":
    MyMainApp().run()
