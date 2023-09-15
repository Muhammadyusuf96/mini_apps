import itertools
from tkinter import StringVar
from tkinter.ttk import Frame, Separator, Entry, Label


class Main(Frame):
    def __init__(self):
        super().__init__()

        self.master.geometry("292x104+537+300")
        self.master.resizable(0, 0)
        self.master.title("Proportsiya kalkulyatori")

        self.TLabel1 = Label(self.master, text="Asosiy bog'liqlik")
        self.TLabel1.place(x=101, y=6, height=19, width=90)

        self.TSeparator1 = Separator(None)
        self.TSeparator1.place(x=0, y=60, width=320)

        self.entries = {}
        self.str_var = {}
        self.calced = ''

        self.pack(fill="both", expand=True)
        self.basic()
        self.master.mainloop()

    def calc(self, key):
        if key not in ['00', '10']:
            obj = self.str_var[key]
            a = self.str_var['00'].get()
            b = self.str_var['10'].get()
            if b and a and obj.get():
                val = float(obj.get())
                if key.startswith('0'):
                    temp = val * float(b) / float(a)
                    name = f'1{key[1:]}'
                else:
                    temp = val * float(a) / float(b)
                    name = f'0{key[1:]}'
                self.calced = self.str_var[name]._name
                self.str_var[name].set(temp)
        else:
            if len(self.entries) >= 4:
                self.reset()
            self.center_window()

    def reset(self):
        if len(self.entries) > 4:
            keys = ['00', '01', '10', '11']
            for key in self.str_var.copy():
                if key not in keys:
                    self.str_var.pop(key, None)
                    self.entries[key].destroy()
                    self.entries.pop(key, None)
                elif key not in ['00', '10']:
                    self.str_var[key].set('')
        self.calced = ''

    def on_change(self, *args):
        name = args[0]
        for key in self.str_var.copy():
            if obj := self.str_var.get(key, None):
                if obj._name == name:
                    temp = self.clear(obj.get())
                    if obj.get() != temp:
                        obj.set(temp)
                    if self.calced != name:
                        self.calc(key)
                    else:
                        self.calced = ''
        self.check_for_new_entries()

    def clear(self, value):
        value.replace(',', '.')
        if value.startswith('.'):
            value = f'0{value}'
        temp = ''
        for val in value:
            if val.isdigit():
                temp += val
            elif val == '.':
                if '.' not in temp:
                    temp += val

        if temp.startswith('0'):
            if '.' in temp:
                if len(temp[:temp.index('.')]) > 1:
                    temp = str(int(temp[:temp.index('.')])) + temp[temp.index('.'):]
            elif len(temp) > 1:
                temp = temp[1:]

        return temp

    def check_for_new_entries(self):
        t = sum(
            self.str_var[
                key
            ].get() != '' for key in list(self.entries.keys())[-2:])

        if t >= 2:
            self.add_new_entries()

    def basic(self):
        for row, col in itertools.product(range(2), range(2)):
            cel = str(col) + str(row)
            self.str_var[cel] = StringVar()
            self.entries[cel] = Entry(self, textvariable=self.str_var[cel])
            self.str_var[cel].trace("w", self.on_change)
            self.entries[cel].grid(row=row, column=col, padx=(10, 10), pady=(26, 5))

    def add_new_entries(self):
        start = len(self.entries) // 2
        if start <= 20:
            for row, col in itertools.product(range(start, start + 1), range(2)):
                cel = str(col) + str(row)
                self.str_var[cel] = StringVar()
                self.entries[cel] = Entry(self, textvariable=self.str_var[cel])
                self.str_var[cel].trace("w", self.on_change)
                self.entries[cel].grid(
                    row=row, column=col,
                    padx=(10, 10), pady=(5, 5))
            self.center_window()

    def center_window(self):
        self.master.geometry("")
        x = (self.master.winfo_screenwidth() - self.master.winfo_width()) / 2
        y = (
            self.master.winfo_screenheight() - self.master.winfo_height()) / 2 - 32
        self.master.geometry('+%d+%d' % (x, y))


if __name__ == '__main__':
    app = Main()
