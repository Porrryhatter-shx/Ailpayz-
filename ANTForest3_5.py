import tkinter as tk
from tkinter import messagebox, simpledialog
from pathlib import Path
import time
#2O25.3.4
class ANTForest:
    def __init__(self, root):
        self.root = root
        self.root.title("蚂蚁森林")
        self.root.geometry("500x600")

        # 初始化变量
        self.water = 0
        self.tdtime = int(time.time()) // 86400
        self.read()

        # 创建界面
        self.create_widgets()

    def read(self):
        # 读取分数
        self.path = Path('score.txt')
        try:
            self.score = int(self.path.read_text())
        except (FileNotFoundError, ValueError):
            self.score = 0
            self.path.write_text(str(self.score))

        # 读取签到日期
        self.pathd = Path('day.txt')
        try:
            self.day = int(self.pathd.read_text())
        except (FileNotFoundError, ValueError):
            self.day = self.tdtime
            self.pathd.write_text(str(self.tdtime))

        # 读取连续签到天数
        self.pathjc = Path('jc.txt')
        try:
            self.jc = int(self.pathjc.read_text())
        except (FileNotFoundError, ValueError):
            self.jc = 1
            self.pathjc.write_text(str(self.jc))

        # 检查签到状态
        if self.day > self.tdtime:
            self.day = self.tdtime
            self.jc = 1
            self.pathd.write_text(str(self.tdtime))
            self.pathjc.write_text(str(self.jc))

    def create_widgets(self):
        self.tree_status_label = tk.Label(self.root, text="加载中...", font=("Arial", 14))
        self.tree_status_label.pack(pady=20)

        self.score_label = tk.Label(self.root, text=f"生长值: {self.score}", font=("Arial", 12))
        self.score_label.pack()

        self.water_label = tk.Label(self.root, text=f"水: {self.water} mL", font=("Arial", 12))
        self.water_label.pack()

        self.sign_in_button = tk.Button(self.root, text="签到", command=self.sign_in)
        self.sign_in_button.pack(pady=10)

        self.water_frame = tk.Frame(self.root)
        self.water_frame.pack(pady=10)

        tk.Button(self.water_frame, text="浇水 1mL", command=lambda: self.water_plant(1)).grid(row=0, column=0, padx=5)
        tk.Button(self.water_frame, text="浇水 2mL", command=lambda: self.water_plant(2)).grid(row=0, column=1, padx=5)
        tk.Button(self.water_frame, text="浇水 3mL", command=lambda: self.water_plant(3)).grid(row=0, column=2, padx=5)
        tk.Button(self.water_frame, text="浇水 5mL", command=lambda: self.water_plant(5)).grid(row=0, column=3, padx=5)

        self.quit_button = tk.Button(self.root, text="退出", command=self.root.destroy)
        self.quit_button.pack(pady=20)

        # 字符画显示区域
        self.ascii_art_label = tk.Label(self.root, text="", font=("Courier", 10), justify="left")
        self.ascii_art_label.pack(pady=20)

        # 更新树的状态和字符画
        self.update_tree_status()

    def update_tree_status(self):
        if self.score < 10:
            status = "1级: 种子"
            ascii_art = "_____.____\n1级: 种子"
        elif 10 <= self.score < 50:
            status = "2级: 发芽"
            ascii_art = "      _ _\n_____|____\n2级: 发芽"
        elif 50 <= self.score < 100:
            status = "3级: 树苗"
            ascii_art = "      0\n     0/0\n    o/0\n_____|____\n3级: 树苗"
        elif 100 <= self.score < 200:
            status = "4级: 小树前期"
            ascii_art = "     0|\n    0-|°\n    0/0\n     |\n_____|____\n4级: 小树前期"
        elif 200 <= self.score < 500:
            status = "5级: 小树"
            ascii_art = "     o\n   0||0\n  00\\00\n 0000||000\n   00||\n_____||____\n5级: 小树"
        elif 500 <= self.score < 1000:
            status = "6级: 开花的小树"
            ascii_art = "     o\n    0||*\n  00*||00\n 00*0||000\n   00//*\n_____||____\n6级: 开花的小树"
        elif 1000 <= self.score < 2000:
            status = "7级: 结果的小树"
            ascii_art = "     o\n   0||0\n  00\\.0\n 00.0||0*0\n   00||\n___._||____\n7级: 结果的小树"
        elif 2000 <= self.score < 5000:
            status = "8级: 大树"
            ascii_art = "     。\n    0||0\n   00|\\0*\n  .00| |00*\n 0000| |*0*0\n   00| |.0:\n    0| |0\n_____| |______\n8级: 大树"
        elif 5000 <= self.score < 10000:
            status = "9级: 参天大树"
            ascii_art = "     。\n    0| |0\n   00| \\0*\n  .00|  |00*\n 0*00|  |*0*0\n   00|  |.0:\n    0/  /0\n    .|  |\n___._|  |__*___\n9级: 参天大树"
        else:
            status = "已完成目标！🎉"
            ascii_art = "      o\n     0|\\0\n    00| \\0*\n   .00|  |00*\n  0*00|  |*0*0\n    00|  |.0:\n     0|  |0\n     .|  |\n____._|  |__*___\n     ^_^    \n&.恭喜!你已达成目标.&\n        ANT*"

        self.tree_status_label.config(text=status)
        self.ascii_art_label.config(text=ascii_art)

    def sign_in(self):
        if self.tdtime - self.day == 1:
            if self.jc <= 9:
                self.scorep = 2 ** self.jc
            else:
                self.scorep = 512
            self.jc += 1
        elif self.tdtime == self.day:
            messagebox.showinfo("签到", "今日已签到！")
            return
        else:
            self.scorep = 2
            self.jc = 1

        self.score += self.scorep
        self.path.write_text(str(self.score))
        self.pathd.write_text(str(self.tdtime))
        self.pathjc.write_text(str(self.jc))

        self.score_label.config(text=f"生长值: {self.score}")
        self.update_tree_status()
        messagebox.showinfo("签到成功", f"获得 {self.scorep} 滴生长值！")

    def water_plant(self, amount):
        self.water += amount
        self.water_label.config(text=f"水: {self.water} mL")
        messagebox.showinfo("浇水", f"已浇水 {amount} mL！")

if __name__ == "__main__":
    root = tk.Tk()
    app = ANTForest(root)
    root.mainloop()
