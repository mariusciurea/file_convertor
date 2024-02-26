"""File convertor application.

It allows the user to browse for the input file and choose the output file type
--------
The output file type can be:
    .csv
    .txt
    .xlsx
--------
It saves the data from the input file to the output file.
The output file is automatically created at the same path of the input file
by adding the chosen extension.
"""
import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

__auther__ = 'Marius Ciurea'
__email__ = 'marius.ciurea@itschool.ro'
__maintainer__ = __auther__

__all__ = []


class FileConversion:
    def __init__(self, file_path):
        self.file_path = file_path
        self.ext = os.path.splitext(self.file_path)[1]

    def text_to_csv(self):
        pass

    def csv_to_xlsx(self):
        df = pd.read_csv(self.file_path)
        # self.file_path.replace(self.ext, '.xlsx')
        df.to_excel(self.file_path.replace(self.ext, '.xlsx'), index=False)


class ConverterGUI(tk.Frame):
    """GUI that facilitates file conversion. Inherits from tkinter Frame class.

    It has a button widget that allows the user to browse the files and pick up
    the one that wants to be converted

    It has a listbox widget that allows the user to choose one of the following
    file types: .csv, .txt, .xlsx in which the input file must be converted
    """

    def __init__(self, master, color):
        super().__init__()
        self.filename = None
        self.path = None
        self.master = master
        self.configure(bg=color, width=500, height=300)
        self.grid(row=0, column=0)
        self.label_file_explorer = tk.Label(self, text='Choose file',
                                            width=10, height=2, bg=color,
                                            fg='white', font=('Arial', 14))
        self.label_file_explorer.grid(row=0, column=0)

        self.label_file_type = tk.Label(self, text='File Type',
                                            width=10, height=2, bg=color,
                                            fg='white', font=('Arial', 14))
        self.label_file_type.grid(row=0, column=1)

        self.button_explorer = tk.Button(self, text="Button Explorer",
                                         bg='blue', fg='white',
                                         command=self._browse_files)
        self.button_explorer.grid(row=1, column=0)

        self.listbox = tk.Listbox(self)
        self.listbox.grid(row=1, column=1)
        self.listbox.insert(1, '.csv')
        self.listbox.insert(2, '.txt')
        self.listbox.insert(3, '.xlsx')
        self.listbox.selection_set(0)

        self.button_convert = tk.Button(self, text="Convert",
                                        bg='blue', fg='white',
                                        command=self._convert)
        self.button_convert.grid(row=2, column=1, padx=10, pady=10)

        self.grid_propagate(False)

    def _browse_files(self):
        """Opens a file dialog and gives the user the possibility to pick up a file
        Modifies the label text with the name of the chosen file
        """
        self.path = filedialog.askopenfilename(initialdir='/', title='Select a file',
                                               filetypes=(("text files", "*.txt"), ("all files", "*.*")))
        self.filename = self.path[self.path.rfind('/') + 1::]
        self.label_file_explorer.configure(width=len(self.filename), text=self.filename)

    def _get_extension(self):
        selection = {
            0: '.csv',
            1: '.txt',
            2: '.xlsx',
        }

        try:
            return selection[self.listbox.curselection()[0]]
        except IndexError:
            messagebox.showerror(message='Please select an option!')

    def _convert(self):
        """Covert the input file in the chosen file type (.txt, .csv, .xlsx)
           An instance of Conversion class will be created and this will handle
           the conversion
        """
        if not self.path:
            messagebox.showerror(message='Please select a file!')
        else:
            selected_ext = self._get_extension()
            file = FileConversion(self.path)
            try:
                result = _get_method(file, (file.ext, selected_ext))
                result()
                messagebox.showinfo(message='Conversion successfully done!')
            except KeyError:
                messagebox.showinfo(message='Conversion not successfully done!')


def _get_method(obj: FileConversion, ext_pair):

    file_type = {
        ('.csv', '.xlsx'): obj.csv_to_xlsx
    }
    return file_type[ext_pair]


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('500x300')
    cvt = ConverterGUI(root, 'purple')

    root.mainloop()
