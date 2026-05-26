import tkinter as tk
from tkinter import ttk, messagebox
import time
import threading
import winsound

class PomodoroApp:
 
            fg="#3498db"
        )
        self.mode_label.pack(pady=10)

        # 时间显示
        self.time_label = tk.Label(
            self.root,
            text="25:00",
            font=("Courier New", 48, "bold"),
            bg="#2c3e50",
            fg="#e74c3c"
        )
        self.time_label.pack(pady=20)

        # 进度条
        self.progress = ttk.Progressbar(
            self.root,
            length=280,
            mode='determinate',
            maximum=100
        )
        self.progress.pack(pady=10)

        # 统计信息
        self.stats_label = tk.Label(
            self.root,
            text="完成番茄: 0",
            font=("Microsoft YaHei", 11),
            bg="#2c3e50",
            fg="#95a5a6"
        )
        self.stats_label.pack(pady=5)

        # 按钮区域
        btn_frame = tk.Frame(self.root, bg="#2c3e50")
        btn_frame.pack(pady=20)

        self.start_btn = tk.Button(
            btn_frame,
            text="开始",
            font=("Microsoft YaHei", 12),
            width=8,
            bg="#27ae60",
            fg="white",
            activebackground="#2ecc71",
            relief=tk.FLAT,
            command=self.start_timer
        )
        self.start_btn.pack(side=tk.LEFT, padx=5)

        self.pause_btn = tk.Button(
            btn_frame,
            text="暂停",
            font=("Microsoft YaHei", 12),
            width=8,
            bg="#f39c12",
            fg="white",
            activebackground="#f1c40f",
            relief=tk.FLAT,
            command=self.pause_timer,
            state=tk.DISABLED
        )
        self.pause_btn.pack(side=tk.LEFT, padx=5)

        self.reset_btn = tk.Button(
            btn_frame,
            text="重置",
            font=("Microsoft YaHei", 12),
            width=8,
            bg="#e74c3c",
            fg="white",
            activebackground="#c0392b",
            relief=tk.FLAT,
            command=self.reset_timer
        )
        self.reset_btn.pack(side=tk.LEFT, padx=5)

        # 模式切换区域
        mode_frame = tk.Frame(self.root, bg="#2c3e50")
        mode_frame.pack(pady=10)

        self.work_btn = tk.Button(
            mode_frame,
            text="专注",
            font=("Microsoft YaHei", 10),
            width=8,
            bg="#3498db",
            fg="white",
            relief=tk.FLAT,
            command=lambda: self.switch_mode("work")
        )
        self.work_btn.pack(side=tk.LEFT, padx=3)

        self.short_btn = tk.Button(
            mode_frame,
            text="短休息",
            font=("Microsoft YaHei", 10),
            width=8,
            bg="#1abc9c",
            fg="white",
            relief=tk.FLAT,
            command=lambda: self.switch_mode("short_break")
        )
        self.short_btn.pack(side=tk.LEFT, padx=3)

        self.long_btn = tk.Button(
            mode_frame,
            text="长休息",
            font=("Microsoft YaHei", 10),
            width=8,
            bg="#9b59b6",
            fg="white",
            relief=tk.FLAT,
            command=lambda: self.switch_mode("long_break")
        )
        self.long_btn.pack(side=tk.LEFT, padx=3)

    def switch_mode(self, mode):
        if self.running:
            self.pause_timer()
        self.current_mode = mode
        if mode == "work":
            self.time_left = self.work_time * 60
            self.mode_label.config(text="专注时间", fg="#3498db")
            self.time_label.config(fg="#e74c3c")
        elif mode == "short_break":
            self.time_left = self.short_break * 60
            self.mode_label.config(text="短休息", fg="#1abc9c")
            self.time_label.config(fg="#1abc9c")
        elif mode == "long_break":
            self.time_left = self.long_break * 60
            self.mode_label.config(text="长休息", fg="#9b59b6")
            self.time_label.config(fg="#9b59b6")
        self.update_display()

    def start_timer(self):
        if not self.running:
            self.running = True
            self.start_btn.config(state=tk.DISABLED)
            self.pause_btn.config(state=tk.NORMAL)
            self.timer_thread = threading.Thread(target=self.countdown)
            self.timer_thread.daemon = True
            self.timer_thread.start()

    def pause_timer(self):
        self.running = False
        self.start_btn.config(state=tk.NORMAL)
        self.pause_btn.config(state=tk.DISABLED)

    def reset_timer(self):
        self.running = False
        self.start_btn.config(state=tk.NORMAL)
        self.pause_btn.config(state=tk.DISABLED)
        if self.current_mode == "work":
            self.time_left = self.work_time * 60
        elif self.current_mode == "short_break":
            self.time_left = self.short_break * 60
        else:
            self.time_left = self.long_break * 60
        self.update_display()

    def countdown(self):
        while self.running and self.time_left > 0:
            time.sleep(1)
            if self.running:
                self.time_left -= 1
                self.root.after(0, self.update_display)

        if self.running and self.time_left <= 0:
            self.root.after(0, self.timer_complete)

    def update_display(self):
        minutes = self.time_left // 60
        seconds = self.time_left % 60
        self.time_label.config(text=f"{minutes:02d}:{seconds:02d}")

        # 更新进度条
        if self.current_mode == "work":
            total = self.work_time * 60
        elif self.current_mode == "short_break":
            total = self.short_break * 60
        else:
            total = self.long_break * 60

        progress = ((total - self.time_left) / total) * 100
        self.progress['value'] = progress

        # 更新窗口标题显示剩余时间
        self.root.title(f"{'专注' if self.current_mode == 'work' else '休息'} - {minutes:02d}:{seconds:02d}")

    def timer_complete(self):
        self.running = False
        self.start_btn.config(state=tk.NORMAL)
        self.pause_btn.config(state=tk.DISABLED)

        # 播放提示音
        try:
            winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
        except:
            pass

        if self.current_mode == "work":
            self.cycle_count += 1
            self.stats_label.config(text=f"完成番茄: {self.cycle_count}")

            if self.cycle_count % self.cycles_before_long_break == 0:
                messagebox.showinfo("番茄钟", "恭喜！完成一个番茄，该长休息了！")
                self.switch_mode("long_break")
            else:
                messagebox.showinfo("番茄钟", "专注时间结束！休息一下吧。")
                self.switch_mode("short_break")
        else:
            messagebox.showinfo("番茄钟", "休息结束！准备开始新的专注时间。")
            self.switch_mode("work")

if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroApp(root)
    root.mainloop()
