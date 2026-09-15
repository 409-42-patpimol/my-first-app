import tkinter as tk
from tkinter import messagebox

class Game24:
    def __init__(self, root):
        self.root = root
        self.root.title("เกม 24 (24 Game)")
        self.root.geometry("450 x 550")
        self.root.resizable(False, False)

        # ชุดโจทย์ตามที่กำหนด
        self.questions = [
            [1, 7, 4, 5],
            [6, 2, 0, 8],
            [5, 7, 3, 9],
            [2, 6, 6, 3]
        ]
        self.current_q_idx = 0
        self.time_left = 180  # เวลา 3 นาที (180 วินาที)
        self.timer_running = False

        self.setup_ui()

    def setup_ui(self):
        # ส่วนหัวและเวลา
        self.lbl_title = tk.Label(self.root, text="เกม 24", font=("Helvetica", 20, "bold"))
        self.lbl_title.pack(pady=10)

        self.lbl_timer = tk.Label(self.root, text="เวลาเหลือ: 03:00", font=("Helvetica", 14), fg="red")
        self.lbl_timer.pack(pady=5)

        self.lbl_question_num = tk.Label(self.root, text="ข้อที่ 1 / 4", font=("Helvetica", 12))
        self.lbl_question_num.pack(pady=5)

        # แสดงตัวเลขโจทย์
        self.lbl_numbers = tk.Label(self.root, text="กด 'เริ่มเล่น' เพื่อเริ่มเกม", font=("Helvetica", 18, "bold"), bg="#e0e0e0", width=25, height=2)
        self.lbl_numbers.pack(pady=15)

        # ช่องกรอก/แสดงสมการที่ผู้เล่นเลือก
        self.entry_expr = tk.Entry(self.root, font=("Helvetica", 16), justify="center", state="disabled")
        self.entry_expr.pack(pady=10, fill="x", padx=40)

        # ปุ่มเครื่องหมาย + - * / () และปุ่มลบ
        frame_operators = tk.Frame(self.root)
        frame_operators.pack(pady=10)

        ops = ['+', '-', '*', '/', '(', ')', 'Clear']
        for op in ops:
            if op == 'Clear':
                btn = tk.Button(frame_operators, text=op, font=("Helvetica", 12, "bold"), width=6, bg="#ff6666", fg="white", command=self.clear_entry)
            else:
                btn = tk.Button(frame_operators, text=op, font=("Helvetica", 14, "bold"), width=3, command=lambda o=op: self.add_to_entry(o))
            btn.pack(side="left", padx=3)

        # ปุ่มเริ่มเล่น และ ปุ่มส่งคำตอบ
        frame_actions = tk.Frame(self.root)
        frame_actions.pack(pady=20)

        self.btn_start = tk.Button(frame_actions, text="เริ่มเล่น", font=("Helvetica", 12, "bold"), bg="#4CAF50", fg="white", width=10, command=self.start_game)
        self.btn_start.pack(side="left", padx=10)

        self.btn_submit = tk.Button(frame_actions, text="ส่งคำตอบ", font=("Helvetica", 12, "bold"), bg="#2196F3", fg="white", width=10, state="disabled", command=self.check_answer)
        self.btn_submit.pack(side="left", padx=10)

    def start_game(self):
        self.current_q_idx = 0
        self.time_left = 180
        self.timer_running = True
        self.btn_start.config(state="disabled")
        self.btn_submit.config(state="normal")
        self.entry_expr.config(state="normal")
        
        self.load_question()
        self.update_timer()

    def load_question(self):
        if self.current_q_idx < len(self.questions):
            nums = self.questions[self.current_q_idx]
            self.lbl_question_num.config(text=f"ข้อที่ {self.current_q_idx + 1} / {len(self.questions)}")
            self.lbl_numbers.config(text=f"ตัวเลข:  {nums[0]}   {nums[1]}   {nums[2]}   {nums[3]}")
            self.clear_entry()
        else:
            self.timer_running = False
            messagebox.showinfo("ยินดีด้วย!", "คุณตอบถูกครบทุกข้อแล้ว! เก่งมากครับ 🎉")
            self.reset_game()

    def update_timer(self):
        if self.timer_running and self.time_left > 0:
            mins, secs = divmod(self.time_left, 60)
            self.lbl_timer.config(text=f"เวลาเหลือ: {mins:02d}:{secs:02d}")
            self.time_left -= 1
            self.root.after(1000, self.update_timer)
        elif self.time_left == 0 and self.timer_running:
            self.timer_running = False
            messagebox.showwarning("หมดเวลา!", "หมดเวลา 3 นาทีแล้วครับ ลองใหม่อีกครั้งนะ!")
            self.reset_game()

    def add_to_entry(self, char):
        if self.btn_submit['state'] == 'normal':
            self.entry_expr.insert(tk.END, char)

    def clear_entry(self):
        self.entry_expr.delete(0, tk.END)

    def check_answer(self):
        user_input = self.entry_expr.get().strip()
        if not user_input:
            return

        try:
            # คำนวณผลลัพธ์จากสมการที่ผู้เล่นพิมพ์/กดเลือก
            result = eval(user_input)
            
            # ตรวจสอบว่าผลลัพธ์เท่ากับ 24 หรือไม่ (ใช้ abs ป้องกันปัญหาทศนิยม)
            if abs(result - 24) < 1e-6:
                messagebox.showinfo("ถูกต้อง!", "ถูกต้องแล้วครับ! ไปข้อถัดไป")
                self.current_q_idx += 1
                self.load_question()
            else:
                messagebox.showerror("ยังไม่ถูก", f"ผลลัพธ์ที่คุณได้คือ {result} (ยังไม่เท่ากับ 24) ลองใหม่อีกครั้ง!")
        except ZeroDivisionError:
            messagebox.showerror("ข้อผิดพลาด", "ไม่สามารถหารด้วย 0 ได้ครับ")
        except Exception:
            messagebox.showerror("ข้อผิดพลาด", "รูปแบบสมการไม่ถูกต้อง กรุณาตรวจสอบตัวเลขและเครื่องหมาย")

    def reset_game(self):
        self.timer_running = False
        self.btn_start.config(state="normal")
        self.btn_submit.config(state="disabled")
        self.clear_entry()
        self.entry_expr.config(state="disabled")
        self.lbl_numbers.config(text="กด 'เริ่มเล่น' เพื่อเริ่มเกม")
        self.lbl_timer.config(text="เวลาเหลือ: 03:00")
        self.lbl_question_num.config(text="ข้อที่ 1 / 4")

if __name__ == "__main__":
    root = tk.Tk()
    app = Game24(root)
    root.mainloop()
