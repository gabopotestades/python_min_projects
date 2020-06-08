import decimal as dc
import tkinter as tk
from tkinter import ttk

# Initialize constants for Decimal-32
coeff32 = 7
e_max32 = 90
e_val_max32 = 9999999
e_min32 = -101
e_val_min32 = 1000000
bias32 = 101
val32 = 7
exp_rep32 = 8

# Initialize constants for Decimal-64
coeff64 = 16
e_max64 = 369
e_val_max64 = 9999999999999999
e_min64 = -398
e_val_min64 = 1000000000000000
bias64 = 398
val64 = 16
exp_rep64 = 10

class BinaryConversion:

#   Insert integer to be converted to exponent representation
    def get_exp_rep(self, exp, mode):

        exp_rep_val = ''
        exp_rep = 0
        exponent = 0
        bias = 0

        if mode == 32:
            bias = bias32
            exp_rep = exp_rep32

        else:
            bias = bias64
            exp_rep = exp_rep64

        exponent = exp + bias
        exp_rep_val = bin(exponent)[2:]
        exp_rep_val = str('0' * (exp_rep - len(exp_rep_val))) + exp_rep_val

        return exponent, exp_rep_val

#   Insert string to split exponent representation and continuation
    def get_exp_cont(self, exp_rep_val):
        exp_rep_val_2msb = exp_rep_val[:2]
        exp_cont = exp_rep_val[2:]

        return exp_rep_val_2msb, exp_cont

#   Insert 3 digit integer to be converted to DPD
    def get_dpd(self, val):

        aei_val = str(val)

        a = int(aei_val[0])
        e = int(aei_val[1])
        i = int(aei_val[2])

        a_bin = format(a, '#06b')[2:]
        e_bin = format(e, '#06b')[2:]
        i_bin = format(i, '#06b')[2:]

#       First DPD
        p = ''
        q = ''
        r = a_bin[3]

#       Second DPD
        s = ''
        t = ''
        u = e_bin[3]

        v = ''

#       Third DPD
        w = ''
        x = ''
        y = i_bin[3]

        if a > 7 or e > 7 or i > 7:
            v = '1'

            if a > 7 and e > 7 and i > 7:
                p = '0'
                q = '0'

                s = '1'
                t = '1'

                w = '1'
                x = '1'

            elif a > 7 and e > 7 and i < 8:

                p = i_bin[1]
                q = i_bin[2]

                s = '0'
                t = '0'

                w = '1'
                x = '1'

            elif a > 7 and e < 8 and i > 7:

                p = e_bin[1]
                q = e_bin[2]

                s = '0'
                t = '1'

                w = '1'
                x = '1'

            elif a < 8 and e > 7 and i > 7:

                p = a_bin[1]
                q = a_bin[2]

                s = '1'
                t = '0'

                w = '1'
                x = '1'

            elif a > 7 and e < 8 and i < 8:

                p = i_bin[1]
                q = i_bin[2]

                s = e_bin[1]
                t = e_bin[2]

                w = '1'
                x = '0'

            elif a < 8 and e > 7 and i < 8:

                p = a_bin[1]
                q = a_bin[2]

                s = i_bin[1]
                t = i_bin[2]

                w = '0'
                x = '1'

            elif a < 8 and e < 8 and i > 7:

                p = a_bin[1]
                q = a_bin[2]

                s = e_bin[1]
                t = e_bin[2]

                w = '0'
                x = '0'

        else:

            p = a_bin[1]
            q = a_bin[2]

            s = e_bin[1]
            t = e_bin[2]

            v = '0'

            w = i_bin[1]
            x = i_bin[2]

#       For testing
#        return p + q + r + ' ' + s + t + u + ' ' + v + ' ' + w + x + y
        return p + q + r + s + t + u + v + w + x + y

#   Insert string of exponent representation and integer MSD of coefficient
    def get_comb_field(self, exp_rep_val_2msb, coeff_msd):

        combi_field = ''

        coeff_msd = int(coeff_msd)
        if coeff_msd > 7:
            combi_field = '11' + exp_rep_val_2msb + bin(coeff_msd)[5:6]
        else:
            combi_field = exp_rep_val_2msb + format(coeff_msd, '#05b')[2:]

        return combi_field

#   Insert string to convert to 4 digit hex
    def get_hex(self, val, mode):

        if mode == 32:
            return '0x{0:0{1}X}'.format(int(val, 2), 8)[2:]
        else:
            return '0x{0:0{1}X}'.format(int(val, 2), 16)[2:]


class Main(tk.Tk):

    def __init__(self, *args, **kwargs):

#Process the inserted values in the text box.
        def button_func():

            mode = 32
            message = ''

            # Initialize variables
            signed_bit = '0'
            coefficient = 0
            combination_field = ''
            exponent_continuation = ''
            coefficient_continuation = ''
            ans = ''
            hex_ans = ''

            sb_string.set('')
            combi_string.set('')
            exp_cont_string.set('')
            coeff_cont_string.set('')
            hex_string.set('')

            if combo_box.get() == 'Decimal-64':
                mode = 64

            #if val_entry.get() == '':
                #val_string.set('0')

            #if exp_entry.get() == '':
                #exp_string.set('0')

            if not self.check_valid(val_entry.get()):

                sb_string.set('-')

                combi_string.set('11111')

                if mode == 32:
                    exp_cont_string.set('0' + ('-' * 5))
                    coeff_cont_string.set('-' * 20)
                else:
                    exp_cont_string.set('0' + ('-' * 7))
                    coeff_cont_string.set('-' * 50)

                message_label.config(text='Entry not valid, considered as NaN!')
                return

            elif not self.check_valid(exp_entry.get()):

                message_label.config(text='Exponent entry not a valid number!')
                return

            else:
                message_label.config(text='')

            exponent = round(float(exp_entry.get()))
            coeff = dc.Decimal(val_entry.get())
            exponent_from_coeff = 0

            if self.check_negative(coeff):
                signed_bit = '1'
            elif coeff == 0 and val_entry.get()[:2] == '-0':
                signed_bit = '1'

            coeff, exponent_normalized = self.shift_decimal(exponent, coeff, mode)

            message = self.check_range(exponent_normalized, coeff, mode)

            if message == 'infinity':

                sb_string.set(signed_bit)

                if signed_bit == '0':
                    signed_bit = '+'
                else:
                    signed_bit = '-'

                combi_string.set('11110')

                if mode == 32:
                    exp_cont_string.set('-' * 6)
                    coeff_cont_string.set('-' * 20)
                else:
                    exp_cont_string.set('-' * 8)
                    coeff_cont_string.set('-' * 50)

                message = 'Too large to be represented, considered as ' + signed_bit + 'Infinity'
                message_label.config(text=message)
                return

            elif message != '':
                message_label.config(text=message)
                return

            else:
                message_label.config(text='')

            combination_field, exponent_continuation, coefficient_continuation, ans = \
                self.get_decimal_rep(signed_bit, str(coeff), exponent_normalized, mode)

            hex_ans = BinaryConversion.get_hex(BinaryConversion, ans.replace(' ', ''), mode)

            sb_string.set(signed_bit)
            combi_string.set(combination_field)
            exp_cont_string.set(exponent_continuation)
            coeff_cont_string.set(coefficient_continuation)
            hex_string.set(hex_ans)

            #message_label.config(text='0b ' + ans + ' or ' + '0x' + hex_ans)

        tk.Tk.__init__(self, *args, **kwargs)
        self.title('IEEE-754 Decimal-32 and 64 Floating Point Converter')

        self.minsize(width=480, height=480)
        self.resizable(width=False, height=False)

#Insert objects to the UI
        message_label = tk.Label(self, text='', fg='red')
        message_label.config(font=("Calibri", 13))
        message_label.grid(row=0, columnspan=4, pady=(20, 0))

        label = tk.Label(self, text='Enter a decimal number to be represented:')
        label.config(font=("Calibri", 16))
        label.grid(row=1, columnspan=4, ipadx=50, ipady=20)

        val_label = tk.Label(self, text='Decimal:')
        val_label.grid(row=2, column=0, padx=(0, 0))

        val_string = tk.StringVar()
        val_entry = tk.Entry(self, textvariable=val_string)
        val_entry.grid(row=2, column=1)

        exp_label = tk.Label(self, text='x 10^')
        exp_label.grid(row=2, column=2, padx=(0, 0))

        exp_string = tk.StringVar()
        exp_entry = tk.Entry(self, textvariable=exp_string)
        exp_entry.grid(row=2, column=3)

        modes = ['Decimal-32', 'Decimal-64']
        combo_box = ttk.Combobox(self, state='readonly', values=modes, width=12)
        combo_box.grid(row=3, column=0, columnspan=4, pady=(20, 0))
        combo_box.current(0)

        button = tk.Button(self, text='Convert', width=15, command=button_func)
        button.grid(row=4, column=0, columnspan=4, pady=(20, 0))

        sb_label = tk.Label(self, text='Signed bit:')
        sb_label.grid(row=5, column=0, padx=(10, 0), pady=(20, 0))

        sb_string = tk.StringVar()
        sb_entry = tk.Entry(self, state='readonly', textvariable=sb_string)
        sb_entry.grid(row=5, column=1, pady=(20, 0))

        combi_field_label = tk.Label(self, text='Combination field:')
        combi_field_label.grid(row=6, column=0, padx=(10, 0), pady=(20, 0))

        combi_string = tk.StringVar()
        combi_field_entry = tk.Entry(self, state='readonly', textvariable=combi_string)
        combi_field_entry.grid(row=6, column=1, pady=(20, 0))

        exponent_cont_label = tk.Label(self, text='Exponent Cont:')
        exponent_cont_label.grid(row=7, column=0, padx=(10, 0), pady=(20, 0))

        exp_cont_string = tk.StringVar()
        exponent_cont_entry = tk.Entry(self, state='readonly', textvariable=exp_cont_string)
        exponent_cont_entry.grid(row=7, column=1, pady=(20, 0))

        coeff_cont_label = tk.Label(self, text='Coefficient Cont:')
        coeff_cont_label.grid(row=8, column=0, padx=(10, 0), pady=(20, 0))

        coeff_cont_string = tk.StringVar()
        coeff_cont_entry = tk.Entry(self, state='readonly', textvariable=coeff_cont_string, width=53)
        coeff_cont_entry.grid(row=8, column=1, columnspan=3, pady=(20, 0))

        hex_label = tk.Label(self, text='Hex value:')
        hex_label.grid(row=9, column=0, padx=(10, 0), pady=(20, 0))

        hex_string = tk.StringVar()
        hex_entry = tk.Entry(self, state='readonly', textvariable=hex_string)
        hex_entry.grid(row=9, column=1, pady=(20, 0))

# Boolean that returns true if integer is negative
    def check_negative(self, n):
        if n < dc.Decimal(0.0) and n != dc.Decimal(0.0):
            return True
        else:
            return False

# Check if the number is valid
    def check_valid(self, n):
        try:
            dc.Decimal(n)
            return True
        except dc.InvalidOperation:
            return False

# Check if the range is valid
    def check_range(self, exp, val, mode=32):

        message = ''

        val_int = int(val)

        if mode == 32 and exp > e_max32:
            message = 'infinity'
            return message
        elif mode == 32 and exp < e_min32:
            message = 'This value is too small to be represented in 32 bits!'
            return message
        elif mode == 64 and exp > e_max64:
            message = 'infinity'
            return message
        elif mode == 64 and exp < e_min64:
            message = 'This value is too small to be represented in 64 bits!'
            return message

        return message

# Converts a integer to string to get length
    def get_int_len(self, n):

        val = len(str(int(n)))

        if val == 1 and n == 0:
            val = 0

        return val

# Converts the coefficient and returns the normalized exponent
    def shift_decimal(self, exp, n, mode=32):

        nval = abs(n)
        limit_check = 0
        exponent_add = 0
        bias = 0
        max_val = 0

        if mode == 32:
            limit_check = val32
            bias = e_min32
        else:
            limit_check = val64
            bias = e_min64

        if nval == 0:
            nval = str(int(nval))

            nval = str('0' * (limit_check - len(nval))) + nval
            return nval, 0

        if len(str(int(nval))) > limit_check:

            exponent_add = self.get_int_len(nval) - limit_check

            nval = nval * dc.Decimal(10**-exponent_add)

        elif len(str(int(nval))) == limit_check:
            exponent_add = 0
        else:

            snval = str(nval)
            snval = snval.rstrip('0').rstrip('.') if '.' in snval else snval

            whole_places = self.get_int_len(nval)

            d = dc.Decimal(snval)
            decimal_places = d.as_tuple().exponent

            total_exp = exp

            if exp == bias:
                exponent_add = 0
                if int(nval) == 0:
                    exponent_add = bias - 1
            elif exp < bias:
                exponent_add = bias - 1
            elif decimal_places == 0:
                exponent_add = 0
            else:

                exponent_add -= 1
                nval_temp = nval

                while whole_places < limit_check or int(nval_temp) == 0:

                    nval_temp = nval * dc.Decimal(10 ** -exponent_add)

                    #print('nval_temp')
                    #print(nval_temp)

                    snval_temp = str(nval_temp)
                    snval_temp = snval_temp.rstrip('0').rstrip('.') if '.' in snval_temp else snval_temp
                    snval_dec_temp = dc.Decimal(snval_temp)
                    nval_temp_places = snval_dec_temp.as_tuple().exponent

                    total_exp -= 1

                    #print('nval_temp_places')
                    #print(nval_temp_places)

                    if nval_temp_places == 0:
                        break
                    elif total_exp <= bias:
                        break

                    exponent_add -= 1
                    whole_places += 1

                if int(nval_temp) == 0:
                    exponent_add = bias - 1
                else:
                    nval = nval * dc.Decimal(10 ** -exponent_add)
                    #print('test')
                    #print(nval)


#       Adding exponent to normalized exponent from coefficient
        exponent_add = exp + exponent_add

#       Converting coefficient to string and add zeros in front for processing

        if len(str(round(nval))) > limit_check:
            nval = str(int(nval))
        else:
            nval = str(round(nval))

        nval = str('0' * (limit_check - len(nval))) + nval

        #print('------------------------')
        #print('Final answer:')
        #print(nval)
        #print(exponent_add)

        return nval, exponent_add

# Converts the inserted values to the final answer
    def get_decimal_rep(self, sb, coeff_val, exponent, mode):

        bc = BinaryConversion
        ans = sb + ' '

        exp_with_bias, exp_rep = bc.get_exp_rep(bc, exponent, mode)

        exp_rep_2msb, exp_cont = bc.get_exp_cont(bc, exp_rep)

        combi_field = bc.get_comb_field(bc, exp_rep_2msb, coeff_val[0]) + ' '

        ans = ans + combi_field + exp_cont + ' '

        coeff_without_msd = coeff_val[1:]

        coeff_cont = ''

        if mode == 32:

            #ans = ans + bc.get_dpd(coeff_without_msd[0:3]) + ' '
            #ans = ans + bc.get_dpd(coeff_without_msd[3:6])

            coeff_cont = bc.get_dpd(bc, coeff_without_msd[0:3]) + ' ' + bc.get_dpd(bc, coeff_without_msd[3:6])

        else:

            #ans = ans + bc.get_dpd(coeff_without_msd[0:3]) + ' '
            #ans = ans + bc.get_dpd(coeff_without_msd[3:6]) + ' '
            #ans = ans + bc.get_dpd(coeff_without_msd[6:9]) + ' '
            #ans = ans + bc.get_dpd(coeff_without_msd[9:12]) + ' '
            #ans = ans + bc.get_dpd(coeff_without_msd[12:15]) + ' '

            coeff_cont = bc.get_dpd(bc, coeff_without_msd[0:3]) + ' ' \
                         + bc.get_dpd(bc, coeff_without_msd[3:6]) + ' ' \
                         + bc.get_dpd(bc, coeff_without_msd[6:9]) + ' ' \
                         + bc.get_dpd(bc, coeff_without_msd[9:12]) + ' ' \
                         + bc.get_dpd(bc, coeff_without_msd[12:15])

        ans = ans + coeff_cont

        return combi_field, exp_cont, coeff_cont, ans


app = Main()
app.mainloop()
