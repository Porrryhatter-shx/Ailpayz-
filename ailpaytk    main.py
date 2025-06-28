import tkinter as tk
from tkinter import messagebox, simpledialog
import sys
import time
from datetime import datetime
from ANTForest3_5 import ANTForest
#2O25_3.4

# 定义全局变量
zh = ['shx', 'A', 'b', 'c', 'd', 'zzy']  # A：Administrator
mm = {'shx': '121314', 'A': '00000A', 'b': '137908', 'c': '000012', 'd': '132567', 'zzy': '464646'}
zfmm = {'shx': '0955', 'A': 'zf1', 'b': 'zf2', 'c': 'zf3', 'd': 'zf4', 'zzy': 'zf5'}
money = {'shx': 2012, 'A': 100, 'b': 200, 'c': 300, 'd': 50, 'zzy': 2013}
dk = (1, 5, 10, 12, 15, 20, 30, 40, 60, 100, 200, 10000)

class AlipayApp:
    def __init__(self, root):
        self.root = root
        self.root.title("支付宝")
        self.root.geometry("600x400")

        self.logged_in = False
        self.username = ""

        self.create_widgets()

    def create_widgets(self):
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(pady=20)

        tk.Label(self.login_frame, text="支付宝", font=("Arial", 20)).pack()
        tk.Label(self.login_frame, text="账户:").pack()
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.pack()
        tk.Label(self.login_frame, text="密码:").pack()
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.pack()
        tk.Button(self.login_frame, text="登录", command=self.login).pack()
        tk.Button(self.login_frame, text="测试", command=self.loguser).pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username in zh and mm[username] == password:
            self.logged_in = True
            self.username = username
            self.login_frame.destroy()
            self.create_main_menu()
        else:
            messagebox.showerror("错误", "账户或密码错误！")

    def loguser(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username not in zh:
            self.logged_in = True
            self.username = username
            self.login_frame.destroy()
            self.create_main_menu()
            mm[username]=password
            money[username]=0
            zfmm[username]=0
        else:
            messagebox.showerror("错误", "你已注册")

    def create_main_menu(self):
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(pady=20)

        tk.Label(self.main_frame, text=f"欢迎 {self.username}", font=("Arial", 16)).pack()

        self.menu_frame = tk.Frame(self.main_frame)
        self.menu_frame.pack(pady=10)

        tk.Button(self.menu_frame, text="转账", command=self.transfer_money).grid(row=0, column=0, padx=10)
        tk.Button(self.menu_frame, text="我的钱包", command=self.show_wallet).grid(row=0, column=1, padx=10)
        tk.Button(self.menu_frame, text="蚂蚁森林", command=self.ant_forest).grid(row=0, column=2, padx=10)
        tk.Button(self.menu_frame, text="时钟", command=self.show_time).grid(row=1, column=0, padx=10)
        tk.Button(self.menu_frame, text="贷款", command=self.loan_money).grid(row=1, column=1, padx=10)
        tk.Button(self.menu_frame, text="设置", command=self.settings).grid(row=1, column=2, padx=10)
        tk.Button(self.menu_frame, text="退出", command=self.logout).grid(row=2, column=1, padx=10)

    def transfer_money(self):
        recipient = simpledialog.askstring("转账", "请输入收款人账户:")
        if recipient not in zh or recipient == self.username:
            messagebox.showerror("错误", "无效的收款人账户！")
            return

        amount = int(simpledialog.askinteger("转账", "请输入转账金额:"))
        if amount > money[self.username]:
            messagebox.showerror("错误", "余额不足！")
            return

        payment_password = simpledialog.askstring("转账", "请输入支付密码:", show="*")
        if payment_password == zfmm[self.username]:
            try:
                money[recipient] += amount
                money[self.username] -= amount
            except KeyError:
                 messagebox.showerror("错误", f"账户不存在")
            
            messagebox.showinfo("成功", f"已转账 {amount} 元！")
            
        else:
            messagebox.showerror("错误", "支付密码错误！")

    def show_wallet(self):
        password = simpledialog.askstring("钱包", "请输入支付密码:", show="*")
        if password == zfmm[self.username]:
            messagebox.showinfo("我的钱包", f"余额: {money[self.username]} 元")
        else:
            messagebox.showerror("错误", "支付密码错误！")

    def show_time(self):
        now = datetime.now()
        messagebox.showinfo("当前时间", now.strftime("%Y/%m/%d %H:%M"))

    def loan_money(self):
        amount = simpledialog.askinteger("贷款", "请输入贷款金额:")
        if amount > 200:
            messagebox.showerror("贷款金额不能超过100元！")
            return

        payment_password = simpledialog.askstring("贷款", "请输入支付密码:", show="*")
        if payment_password == zfmm[self.username]:
            money[self.username] += amount
            messagebox.showinfo("成功", f"贷款成功！余额: {money[self.username]} 元")
        else:
            messagebox.showerror("错误", "支付密码错误！")

    def ant_forest(self):
        from ANTForest3_5 import ANTForest
        ANTForest(root)

    def settings(self):
        messagebox.showinfo("设置", "关于程序\n版本: 5_z\n开发: 沈 and 朱")

    def logout(self):
        if messagebox.askyesno("退出", "确定要退出支付宝吗？"):
            self.logged_in = False
            self.username = ""
            self.main_frame.destroy()
            self.create_widgets()

if __name__ == "__main__":
    root = tk.Tk()
    app = AlipayApp(root)
    root.mainloop()
