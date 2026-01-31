import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


class UI:
    def __init__(self, image, file_name, ocr_result, stop_loop):
        """
        辅助识别图片中的文字，当识别错误手动更改后返回更改后的结果
        :param image: 图片
        :param file_name: 图片名
        :param ocr_result: 识别结果
        :param stop_loop: 是否停止循环识别
        """
        self.file_name = file_name
        self.image = image
        self.ocr_result = ocr_result
        self.final_result = None
        self.stop_loop = stop_loop
        # 初始化 Tkinter 窗口
        self.root = tk.Tk()
        self.root.title("(快捷键)确认: \"enter\";修改:\"space\"")

        # 确保窗口始终在最上层
        self.root.attributes("-topmost", True)
        self.root.focus_force()

        # 设置窗口居中
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = 370
        window_height = 300
        position_x = (screen_width - window_width) // 2
        position_y = (screen_height - window_height) // 3
        self.root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

        # 缩放图片以便显示
        self.image_resized = ImageTk.PhotoImage(self.image.resize((170, 170)))

        # 创建标签显示图片和 OCR 结果
        label1 = tk.Label(self.root, text="真实图片", font=("Arial", 10, "bold"))
        label1.grid(row=0, column=0, padx=10, pady=2, sticky="ew")

        label2 = tk.Label(self.root, text="识别结果", font=("Arial", 10, "bold"))
        label2.grid(row=0, column=1, padx=10, pady=2, sticky="ew")

        # 显示图片
        img_label = tk.Label(self.root, image=self.image_resized)
        img_label.grid(row=1, column=0, padx=10, pady=10)

        # 显示 OCR 结果文本
        text_label = tk.Label(self.root, text=self.ocr_result, font=("Arial", 80, "bold"))
        text_label.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        # 输入框
        self.input_entry = ttk.Entry(self.root, width=45)
        self.input_entry.grid(row=2, columnspan=2, padx=10, pady=5, sticky="ew")

        # 确认和更改按钮
        self.confirm_button = ttk.Button(self.root, text="确认", command=self.confirm)
        self.confirm_button.grid(row=3, column=0, padx=10, pady=10)

        modify_button = ttk.Button(self.root, text="更改", command=self.modify)
        modify_button.grid(row=3, column=1, padx=10, pady=10)

        # 绑定键盘事件
        self.root.bind("<KeyPress>", self.on_keypress)

        # 启动 Tkinter 主循环
        self.root.mainloop()

    def on_keypress(self, event):
        if event.keysym == "Return":  # 回车键
            self.confirm()
        elif event.keysym == "space":  # 空格键
            self.modify()
        elif event.keysym == "Escape":  # ESC 键
            self.cancel()

    def confirm(self):
        if self.input_entry.get() == "":
            self.final_result = self.ocr_result
        else:
            self.final_result = self.input_entry.get()
        # 确认后关闭窗口
        self.root.destroy()

    def modify(self):
        # 聚焦输入框，允许修改
        self.input_entry.focus_set()

    def cancel(self):
        # 取消后直接关闭窗口并且传出信号停止循环
        self.stop_loop = True
        self.root.destroy()
