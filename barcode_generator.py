import tkinter 
import tkinter.messagebox as tkmsg
from tkinter import *

# Kelas utama membuat window interface
class Main_Window:
    def __init__(self):
        self.__root = Tk()
        self.__root.geometry("400x420")
        self.__root.title("EAN-13 [by Aimee Ernanto]")

        # Main Frame
        self.__main_frame = Frame(self.__root)
        self.__main_frame.pack()

        # Postscript Frame
        self.__ps_frame = Frame(self.__main_frame)
        self.__ps_frame.pack()
        Label(self.__ps_frame, text="Save barcode to PS file [eg: EAN13.eps]:").pack()
        self.__input_ps = StringVar()
        self.__field_ps = Entry(self.__ps_frame, textvariable=self.__input_ps, width=20) 
        self.__field_ps.pack()

        # Code Frame
        self.__code_frame = Frame(self.__main_frame)
        self.__code_frame.pack()
        Label(self.__code_frame, text="Enter code (first 12 decimal digits):").pack()
        self.__input_code = StringVar()
        self.__field_code = Entry(self.__code_frame, textvariable=self.__input_code, width=20)
        self.__field_code.pack()

        # Buttons Frame
        self.__tombol_frame = Frame(self.__main_frame)
        self.__tombol_frame.pack()

        # Button 'Generate Code'
        self.__generate_button = Button(self.__tombol_frame, text="Generate Code", command=self.evaluasi_kode, bg='green')
        self.__generate_button.pack(side=LEFT, padx=5)

        # Button 'Cancel'
        self.__cancel_button = Button(self.__tombol_frame, text="Cancel", command=self.clear_text, bg='red')
        self.__cancel_button.pack(side=LEFT, padx=5)

        self.__field_code.bind("<Return>", self.evaluasi_kode)

        # Canvas
        self.__display = Canvas(self.__main_frame, bg='#ECECEC', height=300, width=400)
        self.__display.pack()

    def run(self):
        self.__root.mainloop()  

    def get_kode(self):
        return self.__input_code.get()
    
    def get_nama_file(self):
        return self.__input_ps.get()
    
    def error_muncul(self, title, message):
        tkmsg.showerror(title, message)

    def clear_text(self):
        self.__input_ps.set("")
        self.__input_code.set("")

    # Fungsi untuk menghandle input code dan menjalankan evaluate code
    def evaluasi_kode(self, *args):
        # Memastikan entry code telah terisi
        if self.get_kode():
            try:
                if int(self.get_kode()):
                    pass
                else:
                    raise ValueError
                
                if len(self.get_kode()) != 12:
                    raise IndexError
                
                self.nama_file()

            except ValueError:
                self.error_muncul("Wrong Input!", "Please enter correct input code.")

            except IndexError:
                self.error_muncul("Wrong Input!", "Length of code is not 12.")

    # Fungsi untuk menghandle input nama file dan menyimpan barcode ke dalam file postscript   
    def nama_file(self, *args):
        try:
            if self.get_nama_file()[-4:] == ".eps" or self.get_nama_file()[-3:] == ".ps":
                pass
            else:
                raise TypeError

            try:
                if open(self.get_nama_file(), "r"):
                    raise FileExistsError

            except FileNotFoundError:
                barcode = Barcode(self.get_kode())
                self.display_barcode(barcode.get_bits(), barcode.get_kode())

                self.__display.update()
                self.__display.postscript(file=self.get_nama_file(), colormode="color")

                # Save barcode information to text file
                self.save_barcode_info()

        except TypeError:
            self.error_muncul("Wrong Input!", "Please enter correct postscript input file!")
            self.clear_text()

        except FileExistsError:
            self.error_muncul("File Exists Error!", "File Exists. Program will not continue to save file!")
            barcode = Barcode(self.get_kode())
            self.display_barcode(barcode.get_bits(), barcode.get_kode())

    def display_barcode(self, bits, code):
        self.__display.delete("all")
        self.__display.create_text(200, 50, fill='purple', font='* 20 bold', text='EAN-13 Barcode:')

        # Mencetak barcode
        for a in range(95):
            if bits[a] == '1':
                if a <= 2:
                    self.__display.create_rectangle((57 + a * 3, 70, 60 + a * 3, 235), fill='blue', outline='blue', width=0)
                elif a >= 45 and a <= 49:
                    self.__display.create_rectangle((57 + a * 3, 70, 60 + a * 3, 235), fill='blue', outline='blue', width=0)
                elif a >= 92 and a <= 94:
                    self.__display.create_rectangle((57 + a * 3, 70, 60 + a * 3, 235), fill='blue', outline='blue', width=0)
                else:
                    self.__display.create_rectangle((57 + a * 3, 70, 60 + a * 3, 220), fill='black', width=0)

        # Mencetak digit code dan checksum
        self.__display.create_text(46, 245, font='* 16 bold', text=code[0], fill='#AA336A')
        for b in range(13):
            if b >= 1 and b <= 6:
                self.__display.create_text(58 + b * 21, 245, font='* 16 bold', text=f'{code[b]}', fill='#AA336A')
            elif b >= 7 and b <= 12:
                self.__display.create_text(70 + b * 21, 245, font='* 16 bold', text=f'{code[b]}', fill='#AA336A')
 
        self.__display.create_text(200, 275, fill='#338A94', font='* 16 bold', text=f'Check Digit: {code[-1]}')

    def save_barcode_info(self):
        filename = "barcode_info.txt"
        with open(filename, "w") as file:
            file.write("EAN-13 Barcode Information:\n")
            file.write(f"Code: {self.get_kode()}\n")
            file.write(f"PS File: {self.get_nama_file()}\n")

# Kelas untuk mendefinisikan spesifikasi EAN13
class EAN13_Specs:
    SIDE_GUARD = '101'
    MIDDLE_GUARD = '01010'
    

    __ENCODING = {
        '0': 'llllllrrrrrr',
        '1': 'llglggrrrrrr',
        '2': 'llgglgrrrrrr',
        '3': 'llggglrrrrrr',
        '4': 'lgllggrrrrrr',
        '5': 'lggllgrrrrrr',
        '6': 'lgggllrrrrrr',
        '7': 'lglglgrrrrrr',
        '8': 'lglgglrrrrrr',
        '9': 'lgglglrrrrrr'
    }

    __LCODE = {
        '0': '0001101',
        '1': '0011001',
        '2': '0010011',
        '3': '0111101',
        '4': '0100011',
        '5': '0110001',
        '6': '0101111',
        '7': '0111011',
        '8': '0110111',
        '9': '0001011'
    }

    __GCODE = {
        '0': '0100111',
        '1': '0110011',
        '2': '0011011',
        '3': '0100001',
        '4': '0011101',
        '5': '0111001',
        '6': '0000101',
        '7': '0010001',
        '8': '0001001',
        '9': '0010111'
    }

    _RCODE = {
        '0': '1110010',
        '1': '1100110',
        '2': '1101100',
        '3': '1000010',
        '4': '1011100',
        '5': '1001110',
        '6': '1010000',
        '7': '1000100',
        '8': '1001000',
        '9': '1110100'
    }

    def get_bits(self, code, number):
        if code == 'l':
            return self.__LCODE[number]
        elif code == 'g':
            return self.__GCODE[number]
        elif code == 'r':
            return self.__GCODE[number][::-1]
        else:
            raise SyntaxError

    def get_cek_total(self, code):
        checksum = 0
        for c in code[0::2]:
            checksum += int(c)
        for c in code[1::2]:
            checksum += int(c) * 3

        return str((10 - checksum%10)%10)
    
    def get_encoding(self, number):
        return self.__ENCODING[number]

# Kelas untuk menggabungkan  95 bits yang telah terencode 
class Barcode(EAN13_Specs):
    def __init__(self, code):
        bagian_pertama = code[0]
        bagian_lainnya = code[1:]
        bagian_lainnya += super().get_cek_total(code)

        encoding = super().get_encoding(bagian_pertama)
        bits = ''
        bits += super().SIDE_GUARD
        for d in range(12):
            if d == 6:
                bits += super().MIDDLE_GUARD
            bits += super().get_bits(encoding[d], bagian_lainnya[d])
        bits += super(). SIDE_GUARD
        code += super().get_cek_total(code)

        self.__bits = bits
        self.__code = code

    def get_kode(self):
        return self.__code
    
    def get_bits(self):
        return self.__bits

def main():
    e = Main_Window()
    e.run() 

# Menjalankan program
if __name__ == '__main__':
    main()