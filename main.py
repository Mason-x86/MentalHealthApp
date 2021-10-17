from kivy.app import App
from kivy.uix.dropdown import DropDown
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.base import runTouchApp
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty
from kivy.properties import StringProperty
from kivy.lang import Builder
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from datetime import date


file_name = "diary.txt"
preference_file = "preferences.txt"

page_number = 0

def get_last_date_index(datestamp):
    file = open("diary.txt")
    string = str(file.read())
    current_largest_index = 1
    read_time_stamps = False
    lines = string.split('\n')
    for line in lines:
        # print(line)
        if line[1:11] == datestamp:
            read_time_stamps = True
            print(line)
        else:
            read_time_stamps = False
        i = 0
        if len(line) > 0:
            if line[i] == "*" and read_time_stamps:
                if (int(line[12]) + 1) < 10:
                    current_largest_index = int(line[12]) + 1
                else:
                    current_largest_index = 0

    return current_largest_index


class Home(Screen, Widget):

    def on_button_click(self, value):
        if value != "|||":
            kv.current = value


class Diary(Screen, Widget):

    def write_order_to_text(self, text):
        output_file = open(file_name, "a")
        number = get_last_date_index(str(date.today()).split()[0])
        if number != 0:
            text = "*" + str(date.today()).split()[0] + "#" + str(number) + "<" + text + ">"
            output_file.write(text)
            output_file.write("\n")
            output_file.close()

    def on_button_click(self, value):
        if value != "|||":
            kv.current = value


class Log(Screen, Widget):

    def on_button_click(self, value):
        if value != "|||":
            kv.current = value

    def open_diary(self, widget, given_date):
        file = open("diary.txt")
        string = str(file.read())
        prepare_read = False
        append_line = False
        global page_number
        page_number = 0
        page = ""
        lines = string.split('\n')
        #                     0    1    2    3    4    5    6    7    8    9   10
        date_reader_queue = ["*", "Y", "Y", "Y", "Y", "-", "M", "M", "-", "D", "D"]

        for char in string:
            date_detect = ""
            for i in range(0, 10):
                date_detect += date_reader_queue[i]

            if date_detect == given_date and date_reader_queue[10] == "#":
                prepare_read = True
                page_number = int(char)

            if append_line and char == ">":
                break

            if append_line:
                page += char

            if prepare_read and char == "<":
                append_line = True

            for i in range(0, 10):
                date_reader_queue[i] = date_reader_queue[i + 1]  # shift L
            date_reader_queue[10] = str(char)

        widget.text = page

    def change_page(self, widget, given_date, id):
        global page_number
        if id == "Next":
            print("Next")
            file = open("diary.txt")
            string = str(file.read())
            prepare_read = False
            append_line = False
            page = ""
            lines = string.split('\n')
            #                     0    1    2    3    4    5    6    7    8    9   10
            date_reader_queue = ["*", "Y", "Y", "Y", "Y", "-", "M", "M", "-", "D", "D"]

            for char in string:
                date_detect = ""
                for i in range(0, 10):
                    date_detect += date_reader_queue[i]

                if date_detect == given_date and date_reader_queue[10] == "#":
                    if int(char) == (page_number + 1):
                        prepare_read = True
                        print(page_number)
                        page_number = int(char)


                if append_line and char == ">":
                    break

                if append_line:
                    page += char

                if prepare_read and char == "<":
                    append_line = True

                for i in range(0, 10):
                    date_reader_queue[i] = date_reader_queue[i + 1]  # shift L
                date_reader_queue[10] = str(char)

            widget.text = page
        elif id == "Back":
            file = open("diary.txt")
            string = str(file.read())
            prepare_read = False
            append_line = False
            page = ""
            lines = string.split('\n')
            #                     0    1    2    3    4    5    6    7    8    9   10
            date_reader_queue = ["*", "Y", "Y", "Y", "Y", "-", "M", "M", "-", "D", "D"]

            for char in string:
                date_detect = ""
                for i in range(0, 10):
                    date_detect += date_reader_queue[i]

                if date_detect == given_date and date_reader_queue[10] == "#":

                    if int(char) == (page_number - 1):
                        prepare_read = True
                        page_number = int(char)

                if append_line and char == ">":
                    break

                if append_line:
                    page += char

                if prepare_read and char == "<":
                    append_line = True

                for i in range(0, 10):
                    date_reader_queue[i] = date_reader_queue[i + 1]  # shift L
                date_reader_queue[10] = str(char)

            widget.text = page
        else:
            pass



class Feeling(Screen, Widget):
    def on_button_click(self, value):
        if value != "|||":
            kv.current = value


    def save_emotional_state(self, value):
        print(str(value))
        output_file = open(file_name, "a")
        output_file.write(value)
        output_file.write("\n")
        output_file.close()


class Help(Screen, Widget):
    def on_button_click(self, value):
        if value != "|||":
            kv.current = value



class Setting(Screen, Widget):
    def on_button_click(self, value):
        if value != "|||":
            kv.current = value



class MyMain(App):
    def build(self):
        return kv


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("interface.kv")
if __name__ == '__main__':
    MyMain().run()
