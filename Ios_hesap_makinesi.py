import tkinter as tk

class RoundButton(tk.Canvas):
    def __init__(self, parent, text, command=None, width=70, height=70, bg="#333333", fg="white", font=("Helvetica", 22, "bold")):
        super().__init__(parent, width=width, height=height, bg=parent['bg'], highlightthickness=0)
        self.command = command
        self.width = width
        self.height = height
        self.bg = bg

        if width > height:  # Oval görünüm için (özellikle "0" butonu)
            self.rect = self.create_round_rect(2, 2, width - 2, height - 2, radius=35, fill=bg, outline=bg)
        else:  # Normal yuvarlak buton
            self.rect = self.create_oval(2, 2, width - 2, height - 2, fill=bg, outline=bg)

        self.text = self.create_text(width / 2, height / 2, text=text, fill=fg, font=font)

        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)
        self.bind("<Enter>", lambda e: self.itemconfig(self.rect, fill=self._darker(bg)))
        self.bind("<Leave>", lambda e: self.itemconfig(self.rect, fill=bg))

    def create_round_rect(self, x1, y1, x2, y2, radius=25, **kwargs):
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1
        ]
        return self.create_polygon(points, smooth=True, **kwargs)

    def _on_press(self, event):
        self.itemconfig(self.rect, fill=self._darker(self.bg, factor=0.7))

    def _on_release(self, event):
        self.itemconfig(self.rect, fill=self.bg)
        if self.command:
            self.command()

    def _darker(self, color, factor=0.85):
        color = color.lstrip('#')
        lv = len(color)
        rgb = tuple(int(color[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
        rgb = tuple(max(0, int(c * factor)) for c in rgb)
        return '#%02x%02x%02x' % rgb



class IOSCalculator:
    
    def __init__(self, root):
        self.root = root
        self.root.title("iOS Stil Hesap Makinesi")
        self.root.geometry("360x580")  # Yüksekliği biraz artırdım
        self.root.resizable(False, False)
        self.root.configure(bg='black')

        self.expression = ""

        self.display = tk.Entry(root, font=("Helvetica", 32), bd=0, bg="black", fg="white", justify='right')
        self.display.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=12, pady=15)
        self.display.insert(0, "0")

        # Renkler
        self.color_num = "#333333"
        self.color_op = "#FF9500"
        self.color_func = "#A5A5A5"

        # Buton listesi
        buttons = [
            ('C', 1, 0, self.clear, self.color_func),
            ('±', 1, 1, self.plus_minus, self.color_func),
            ('%', 1, 2, self.percent, self.color_func),
            ('÷', 1, 3, lambda: self.add_operator('÷'), self.color_op),

            ('7', 2, 0, lambda: self.add_digit('7'), self.color_num),
            ('8', 2, 1, lambda: self.add_digit('8'), self.color_num),
            ('9', 2, 2, lambda: self.add_digit('9'), self.color_num),
            ('×', 2, 3, lambda: self.add_operator('×'), self.color_op),

            ('4', 3, 0, lambda: self.add_digit('4'), self.color_num),
            ('5', 3, 1, lambda: self.add_digit('5'), self.color_num),
            ('6', 3, 2, lambda: self.add_digit('6'), self.color_num),
            ('-', 3, 3, lambda: self.add_operator('-'), self.color_op),

            ('1', 4, 0, lambda: self.add_digit('1'), self.color_num),
            ('2', 4, 1, lambda: self.add_digit('2'), self.color_num),
            ('3', 4, 2, lambda: self.add_digit('3'), self.color_num),
            ('+', 4, 3, lambda: self.add_operator('+'), self.color_op),

            ('0', 5, 0, lambda: self.add_digit('0'), self.color_num),  # 0 butonu ilk sütunda başlar
            ('.', 5, 2, lambda: self.add_dot(), self.color_num),
            ('=', 5, 3, self.calculate, self.color_op)
        ]

        for (text, row, col, cmd, color) in buttons:
            if text == '0':
                # 0 butonu yatayda 2 sütun kaplayacak, yüksekliği diğer butonlarla aynı (70)
                btn = RoundButton(root, text=text, width=150, height=70, bg=color, command=cmd)
                btn.grid(row=row, column=col, columnspan=2, padx=6, pady=6, sticky="we")
            else:
                btn = RoundButton(root, text=text, width=70, height=70, bg=color, command=cmd)
                btn.grid(row=row, column=col, padx=6, pady=6)

        # Grid ayarları
        for i in range(6):
            root.grid_rowconfigure(i, weight=1)
        for i in range(4):
            root.grid_columnconfigure(i, weight=1)

    def add_digit(self, digit):
        if self.expression == "0":
            self.expression = digit
        else:
            self.expression += digit
        self.update_display()

    def add_operator(self, op):
        if self.expression and self.expression[-1] not in '+-×÷':
            self.expression += op
        elif self.expression and self.expression[-1] in '+-×÷':
            self.expression = self.expression[:-1] + op
        self.update_display()

    def add_dot(self):
        if not self.expression or self.expression[-1] in '+-×÷':
            self.expression += '0.'
        else:
            last_num = ''
            for c in reversed(self.expression):
                if c in '+-×÷':
                    break
                last_num = c + last_num
            if '.' not in last_num:
                self.expression += '.'
        self.update_display()

    def clear(self):
        self.expression = ""
        self.update_display()

    def plus_minus(self):
        try:
            tokens = self.tokenize(self.expression)
            if not tokens:
                return
            last = tokens[-1]
            if last.startswith('-'):
                tokens[-1] = last[1:]
            else:
                tokens[-1] = '-' + last
            self.expression = ''.join(tokens)
            self.update_display()
        except:
            pass

    def percent(self):
        try:
            val = self.eval_expression(self.expression)
            val = val / 100
            self.expression = str(val)
            self.update_display()
        except:
            pass

    def calculate(self):
        try:
            val = self.eval_expression(self.expression)
            self.expression = str(val)
            self.update_display()
        except:
            self.expression = ""
            self.update_display()

    def update_display(self):
        self.display.delete(0, tk.END)
        self.display.insert(0, self.expression if self.expression else "0")

    def tokenize(self, expr):
        tokens = []
        num = ''
        for c in expr:
            if c in '+-×÷':
                if num:
                    tokens.append(num)
                    num = ''
                tokens.append(c)
            else:
                num += c
        if num:
            tokens.append(num)
        return tokens

    def eval_expression(self, expr):
        expr = expr.replace('×', '*').replace('÷', '/')
        return eval(expr)

if __name__ == "__main__":
    root = tk.Tk()
    app = IOSCalculator(root)
    root.mainloop()
