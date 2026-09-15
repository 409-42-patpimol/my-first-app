import streamlit as st
import time

# ตั้งค่าหน้าเพจ
st.set_page_config(page_title="เกม 24 (24 Game)", page_icon="🎮", layout="centered")

# ชุดโจทย์ตามที่กำหนด
QUESTIONS = [
    [1, 7, 4, 5],
    [6, 2, 0, 8],
    [5, 7, 3, 9],
    [2, 6, 6, 3]
]

# เริ่มต้น State ตัวแปรใน Session
if "game_started" not in st.session_state:
    st.session_state.game_started = False
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "expression" not in st.session_state:
    st.session_state.expression = ""
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "feedback_msg" not in st.session_state:
    st.session_state.feedback_msg = ""

# ฟังก์ชันเริ่มต้นเกมใหม่
def start_new_game():
    st.session_state.game_started = True
    st.session_state.current_q = 0
    st.session_state.score = 0
    st.session_state.expression = ""
    st.session_state.start_time = time.time()
    st.session_state.game_over = False
    st.session_state.feedback_msg = ""

# Header
st.title("🎮 เกม 24 (24 Game)")

# ---------------- หน้าจอตอนยังไม่เริ่มเล่น ----------------
if not st.session_state.game_started and not st.session_state.game_over:
    st.write("กติกา: ใช้ตัวเลขตามโจทย์และเครื่องหมายทางคณิตศาสตร์คำนวณให้ได้ผลลัพธ์เท่ากับ **24**")
    st.write("มีทั้งหมด **4 ข้อ** ให้เวลาทำรวม **3 นาที**")
    if st.button("🚀 เริ่มเล่นเกม", type="primary", use_container_width=True):
        start_new_game()
        st.rerun()

# ---------------- หน้าสรุปคะแนน (Game Over) ----------------
elif st.session_state.game_over:
    st.header("🏁 สรุปผลการแข่งขัน")
    score = st.session_state.score
    
    st.subheader(f"คะแนนที่คุณได้: {score} / 4 คะแนน")
    
    # แสดงข้อความประเมินตามคะแนนที่ได้รับ
    if score == 0:
        st.error("😭 คุณแพ้")
    elif score in [1, 2]:
        st.warning("🙂 เกือบได้แล้ว")
    elif score == 3:
        st.info("😮 อีกนิดเดียวเสียดายจัง")
    elif score == 4:
        st.success("🎉 ว้าว เก่งสุดสุดเก่งขั้นเทพ")

    st.write("---")
    if st.button("🔄 เล่นใหม่อีกครั้ง", type="primary", use_container_width=True):
        start_new_game()
        st.rerun()

# ---------------- หน้าเล่นเกม ----------------
else:
    # คำนวณเวลาถอยหลัง (3 นาที = 180 วินาที)
    elapsed_time = time.time() - st.session_state.start_time
    remaining_time = max(0, 180 - int(elapsed_time))
    
    mins, secs = divmod(remaining_time, 60)
    
    # ตรวจสอบว่าหมดเวลาหรือไม่
    if remaining_time <= 0:
        st.session_state.game_over = True
        st.rerun()

    # แสดงแถบเวลาและสถานะข้อ
    col_time, col_q = st.columns(2)
    with col_time:
        st.metric("⏳ เวลาที่เหลือ", f"{mins:02d}:{secs:02d}")
    with col_q:
        st.metric("📌 ข้อที่", f"{st.session_state.current_q + 1} / 4")

    # แสดงโจทย์ตัวเลข
    current_nums = QUESTIONS[st.session_state.current_q]
    st.markdown(f"### ตัวเลขโจทย์: **{' , '.join(map(str, current_nums))}**")

    # ช่องแสดงสมการที่ผู้เล่นสร้าง
    st.text_input("สมการของคุณ:", value=st.session_state.expression, key="expr_input", disabled=True)

    # ปุ่มสำหรับกดเครื่องหมายและลบ
    st.write("เลือกเครื่องหมายเพื่อประกอบสมการ:")
    btn_cols = st.columns(7)
    operators = ['+', '-', '*', '/', '(', ')', 'ล้าง']
    
    for idx, op in enumerate(operators):
        with btn_cols[idx]:
            if op == 'ล้าง':
                if st.button("❌ ล้าง", use_container_width=True):
                    st.session_state.expression = ""
                    st.session_state.feedback_msg = ""
                    st.rerun()
            else:
                if st.button(op, use_container_width=True):
                    st.session_state.expression += op
                    st.session_state.feedback_msg = ""
                    st.rerun()

    # ช่องให้พิมพ์ตัวเลข/แก้ไขเพิ่มเติมด้วยตัวเอง (Optional)
    manual_expr = st.text_input("หรือพิมพ์สมการโดยตรงตรงนี้ (ใช้ตัวเลขจากโจทย์):", value=st.session_state.expression)
    if manual_expr != st.session_state.expression:
        st.session_state.expression = manual_expr

    st.write("---")

    # แสดงข้อความแจ้งเตือนย่อยๆ
    if st.session_state.feedback_msg:
        st.error(st.session_state.feedback_msg)

    # ปุ่มส่งคำตอบและข้ามข้อ
    col_sub, col_skip = st.columns(2)
    
    with col_sub:
        if st.button("✅ ส่งคำตอบ", type="primary", use_container_width=True):
            user_input = st.session_state.expression.strip()
            if not user_input:
                st.session_state.feedback_msg = "กรุณากรอกสมการก่อนส่งคำตอบ!"
                st.rerun()
            else:
                try:
                    # คำนวณผลลัพธ์
                    result = eval(user_input)
                    
                    # ตรวจสอบว่าคำตอบเท่ากับ 24 หรือไม่
                    if abs(result - 24) < 1e-6:
                        st.session_state.score += 1
                        st.session_state.current_q += 1
                        st.session_state.expression = ""
                        st.session_state.feedback_msg = ""
                        
                        # หากทำครบ 4 ข้อ ให้จบเกม
                        if st.session_state.current_q >= len(QUESTIONS):
                            st.session_state.game_over = True
                        st.rerun()
                    else:
                        st.session_state.feedback_msg = f"ยังไม่ถูก! ได้ผลลัพธ์คือ {result} (ยังไม่เท่ากับ 24)"
                        st.rerun()
                except ZeroDivisionError:
                    st.session_state.feedback_msg = "ไม่สามารถหารด้วย 0 ได้!"
                    st.rerun()
                except Exception:
                    st.session_state.feedback_msg = "รูปแบบสมการไม่ถูกต้อง!"
                    st.rerun()

    with col_skip:
        if st.button("⏩ ข้ามข้อนี้", use_container_width=True):
            st.session_state.current_q += 1
            st.session_state.expression = ""
            st.session_state.feedback_msg = ""
            if st.session_state.current_q >= len(QUESTIONS):
                st.session_state.game_over = True
            st.rerun()

    # Auto-refresh หน้าจอเพื่อให้เวลาถอยหลังแบบ Realtime
    time.sleep(1)
    st.rerun()
