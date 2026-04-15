import streamlit as st
import time
import pandas as pd
import random
import os # Thêm os để kiểm tra đường dẫn file
from game_logic import init_inventory, compose, calculate_price
from events import get_customer, serve_food, load_random_quote, get_mafia_riddle
import streamlit as st
import time
import pandas as pd
import os
from game_logic import init_inventory, compose, calculate_price
from events import get_customer, serve_food, load_random_quote, get_mafia_riddle
from shop import render_shop # THÊM DÒNG NÀY VÀO ĐÂY


st.set_page_config(layout="wide", page_title="Nấu ăn cho Khủng Long 🦖", page_icon="🍳")


def reset_inputs():
    st.session_state["compose_in"] = ""
    st.session_state["serve_in"] = ""
    st.session_state["answer_in"] = ""



if 'money' not in st.session_state:
    print("try")
    st.session_state.money = 100
    st.session_state.inventory = init_inventory()
    st.session_state.current_customer = get_customer()
    
    # NEW: quản lý ngày
    st.session_state.total_customers = random.randint(3, 6)
    st.session_state.customers_served = 0
    
    st.session_state.mafia_event = False
    st.session_state.msg_right_col = ""
    st.session_state.img_right_col = None
    st.session_state.waiting_next = False  # NEW: chờ bấm khách tiếp theo

# --- KIỂM TRA THẮNG THUA & THỜI GIAN ---
if st.session_state.money >= 1000:
    st.balloons()
    st.success("🎉 CHÚC MỪNG BẠN ĐÃ ĐƯỢC TỰ DO! 🎉")
    st.stop()

# --- KIỂM TRA HẾT NGÀY ---
if st.session_state.customers_served >= st.session_state.total_customers:
    st.success("🌙 Hết ngày rồi! Sang ngày mới...")
    time.sleep(3)
    
    # reset ngày mới
    st.session_state.total_customers = random.randint(3, 6)
    st.session_state.customers_served = 0
    
    # 20% gặp bảo kê đầu ngày
    if random.random() <= 0.2:

        st.session_state.mafia_event = True
        st.session_state.riddle = get_mafia_riddle()
    
    st.rerun()
# --- GIAO DIỆN ---
col_left, col_right = st.columns([6, 4])

# ================= CỘT TRÁI: BẾP & QUẢN LÝ =================
with col_left:
    st.header("🍳 Khu Vực Nấu Ăn")
    
    # 1. Thanh trạng thái & Cửa hàng
    c1, c2 = st.columns(2)
    c1.metric(label="💰 Tiền hiện tại", value=f"{st.session_state.money} đồng")
    
    with c2.expander("🛒 Cửa hàng"):
        render_shop()

    st.markdown("---")
    
    # 2. Bảng nguyên liệu (ĐÃ SỬA ĐỂ DỄ COPY)
    st.subheader("🎒 Kho nguyên liệu")
    st.caption("💡 Mẹo: Bôi đen các icon bên dưới và nhấn Ctrl+C để copy!")
    df_inv = pd.DataFrame([st.session_state.inventory])
    
    # Sử dụng st.table thay vì st.dataframe để dễ dàng bôi đen text/emoji
    st.table(df_inv)
    
    # 3. Khu vực Compose (Nấu)
    st.subheader("🔥 Bếp lò (Compose)")
    st.caption("Gợi ý: Thử dán 🥩+🔥 hoặc 🥬+💧 vào đây (Có thể trộn tự do với 60% cơ hội thành công)")
    
    compose_input = st.text_input("Nhập các emoji nguyên liệu:", key="compose_in")
    if st.button("Nấu ngay! (Compose)"):
        if compose_input:
            # Truyền trực tiếp session_state.inventory để hàm compose thay đổi nó
            success, result = compose(compose_input, st.session_state.inventory)
            print(st.session_state.inventory)
            if success:
                st.success(f"Tạo thành công: **{result}**")
                time.sleep(1) # Nghỉ 1 giây để người dùng kịp nhìn thấy thông báo thành công
                st.rerun()    # Cập nhật lại toàn bộ giao diện và kho
            else:
                st.error(f"Thất bại: **{result}**")
                
    st.markdown("---")
    
    # 4. Khu vực Serve (Phục vụ) & Trả lời bảo kê
    if st.session_state.mafia_event:
        st.warning("⚠️ BẢO KÊ ĐẾN THU TIỀN!")
        answer = st.text_input("Nhập câu trả lời của bạn:",key="answer_in")
        if st.button("Trả lời"):
            if answer.lower().strip() == st.session_state.riddle['a']:
                st.success("Hắn lườm bạn rồi bỏ đi. Bạn an toàn!")
                st.session_state.mafia_event = False
            else:
                st.error("Sai rồi! Bị trừ 50 đồng.")
                st.session_state.money -= 50
                st.session_state.mafia_event = False
                time.sleep(4)
            st.rerun()
    else:
        st.subheader("🍽️ Phục vụ (Serve)")
        serve_input = st.text_input("Nhập món ăn hoàn chỉnh để dọn lên (VD: 🍖 (Thịt nướng)):", key="serve_in")
        if st.button("Phục vụ Khách!"):
                    # Truyền thêm st.session_state.inventory vào hàm
                    status = serve_food(food_name=serve_input,
                                        customer_wants= st.session_state.current_customer['wants'],
                                        inventory= st.session_state.inventory)
                    print(status)
                    if status == "not_found":
                        st.error("⚠️ Bạn không có món này trong kho! Hãy copy đúng tên món ăn từ kho nguyên liệu nhé.")
                        st.rerun()
                    else:
                        # Nếu có món, bắt đầu xét phản ứng của khách
                        if status == "success":
                            earned = calculate_price(serve_input)
                            st.session_state.money += earned
                            st.session_state.msg_right_col = f"Khủng Long rất hài lòng! Bạn nhận được {earned} đồng.\n\n📖 '{load_random_quote()}'"
                            st.session_state.img_right_col =  os.path.join("nau_an_khung_long","assets", "a.png")
                        elif status == "scam":
                            st.session_state.msg_right_col = "Khủng Long ăn xong khen ngon rồi chạy mất dép! Không thu được đồng nào."
                            st.session_state.img_right_col =  os.path.join("nau_an_khung_long","assets", "a.png")
                        elif status == "leave":
                            st.session_state.msg_right_col = "Khủng Long nhảy lên làm nũng hong chịu đou!"
                            st.session_state.img_right_col = os.path.join("nau_an_khung_long","assets", "b.png")

                        st.session_state.waiting_next = True
                        st.session_state.customers_served += 1
                        st.rerun()

        if st.session_state.waiting_next:
            if st.button("➡️ Khách tiếp theo"):
                st.session_state.current_customer = get_customer()
                st.session_state.waiting_next = False
                st.session_state.msg_right_col = ""
                st.session_state.img_right_col = None
                st.rerun()

# ================= CỘT PHẢI: HIỂN THỊ & CỐT TRUYỆN =================
with col_right:
    st.header("🦖 Khách Hàng")
    
    st.markdown("---")
    
    if st.session_state.mafia_event:
        st.subheader("Bảo Kê Đòi Tiền!")
        # ĐÃ SỬA HIỂN THỊ ẢNH BẢO KÊ
        if os.path.exists(os.path.join("nau_an_khung_long","assets", "c.png")):
            st.image(os.path.join("nau_an_khung_long","assets", "c.png"), use_container_width=True)
        else:
            st.error("Không tìm thấy ảnh: assets/c.png")
            
        st.error(f"**Hắn hỏi:** {st.session_state.riddle['q']}")
    else:
        st.info(f"💬 **Khách nói:** {st.session_state.current_customer['desc']}")
        
        if st.session_state.msg_right_col:
            st.markdown(f"**Kết quả:** {st.session_state.msg_right_col}")
            
            # ĐÃ SỬA HIỂN THỊ ẢNH KHÁCH HÀNG
            if st.session_state.img_right_col:
                if os.path.exists(st.session_state.img_right_col):
                    st.image(st.session_state.img_right_col, use_container_width=True)
                else:
                    st.error(f"Không tìm thấy ảnh: {st.session_state.img_right_col}")