import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox

# إعداد المظهر
ctk.set_appearance_mode("dark")  # أو "light" أو "system"
ctk.set_default_color_theme("blue")  # أو "green" أو "dark-blue"

class ModernCalculator:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("آلة حاسبة ")
        self.window.geometry("350x500")
        self.window.resizable(False, False)
        
        # المتغيرات
        self.current_input = ""
        self.result_var = tk.StringVar(value="0")
        
        # إنشاء الواجهة
        self.create_widgets()
    
    def create_widgets(self):
        # شاشة العرض
        display_frame = ctk.CTkFrame(self.window)
        display_frame.pack(pady=20, padx=20, fill="x")
        
        display_label = ctk.CTkLabel(
            display_frame,
            textvariable=self.result_var,
            font=("Arial", 24),
            anchor="e",
            height=60
        )
        display_label.pack(pady=10, padx=10, fill="x")
        
        # لوحة الأزرار
        buttons_frame = ctk.CTkFrame(self.window)
        buttons_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        # تخطيط الأزرار
        buttons = [
            ['C', '±', '%', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '', '.', '=']
        ]
        
        for i, row in enumerate(buttons):
            for j, text in enumerate(row):
                if text:  # إذا لم يكن النص فارغاً
                    # تحديد لون الزر
                    if text in ['÷', '×', '-', '+', '=']:
                        button_color = "#1f6aa5"  # أزرق للعمليات
                    elif text in ['C', '±', '%']:
                        button_color = "#a51f1f"  # أحمر للأزرار الخاصة
                    else:
                        button_color = "#2b2b2b"  # رمادي للأرقام
                    
                    # زر الصفر يأخذ مساحة أكبر
                    if text == '0':
                        btn = ctk.CTkButton(
                            buttons_frame,
                            text=text,
                            font=("Arial", 18),
                            fg_color=button_color,
                            hover_color=self.darken_color(button_color),
                            command=lambda t=text: self.button_click(t),
                            height=60
                        )
                        btn.grid(row=i, column=j, columnspan=2, sticky="ew", padx=2, pady=2)
                    else:
                        btn = ctk.CTkButton(
                            buttons_frame,
                            text=text,
                            font=("Arial", 18),
                            fg_color=button_color,
                            hover_color=self.darken_color(button_color),
                            command=lambda t=text: self.button_click(t),
                            height=60
                        )
                        btn.grid(row=i, column=j, sticky="ew", padx=2, pady=2)
        
        # تكبير الأعمدة
        for i in range(4):
            buttons_frame.columnconfigure(i, weight=1)
        for i in range(5):
            buttons_frame.rowconfigure(i, weight=1)
    
    def darken_color(self, color):
        """تغميق اللون عند التحويم"""
        if color.startswith("#"):
            rgb = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
            darkened = tuple(max(0, c - 30) for c in rgb)
            return f"#{darkened[0]:02x}{darkened[1]:02x}{darkened[2]:02x}"
        return color
    
    def button_click(self, value):
        """معالجة النقر على الأزرار"""
        try:
            if value == 'C':
                self.current_input = ""
                self.result_var.set("0")
            
            elif value == '=':
                # استبدال الرموز الرياضية
                expression = self.current_input.replace('×', '*').replace('÷', '/')
                result = eval(expression)
                self.result_var.set(str(result))
                self.current_input = str(result)
            
            elif value == '±':
                if self.current_input and self.current_input[0] == '-':
                    self.current_input = self.current_input[1:]
                else:
                    self.current_input = '-' + self.current_input
                self.result_var.set(self.current_input or "0")
            
            elif value == '%':
                if self.current_input:
                    result = eval(self.current_input) / 100
                    self.result_var.set(str(result))
                    self.current_input = str(result)
            
            else:
                # استبدال الرموز للعرض
                display_value = value
                if value == '*':
                    display_value = '×'
                elif value == '/':
                    display_value = '÷'
                
                self.current_input += value
                display_input = self.current_input.replace('*', '×').replace('/', '÷')
                self.result_var.set(display_input or "0")
                
        except Exception as e:
            messagebox.showerror("خطأ", "عملية غير صحيحة")
            self.current_input = ""
            self.result_var.set("0")
    
    def run(self):
        """تشغيل التطبيق"""
        self.window.mainloop()

# تشغيل البرنامج
if __name__ == "__main__":
    calculator = ModernCalculator()
    calculator.run()