from time import time
import streamlit as st
import json
import os
import random

    
# Danh sách nguyên liệu bán trong shop
SHOP_INGREDIENTS = [
    {"icon": "💧", "name": "Nước", "price": 5},
    {"icon": "🔥", "name": "Lửa", "price": 5},
    {"icon": "🥬", "name": "Rau sà lách", "price": 8},
    {"icon": "🥚", "name": "Trứng", "price": 10},
    {"icon": "🍚", "name": "Gạo", "price": 10},
    {"icon": "🌶️", "name": "Ớt cay", "price": 15},
    {"icon": "😃", "name": "Niềm vui", "price": 20},
    {"icon": "🥩", "name": "Thịt tươi", "price": 13},
]

# Danh sách bí kíp (Tips)
SHOP_TIPS = [
    {
        "id": "tip_1", 
        "name": "Món Cuốn Tiện Lợi", 
        "price": 30, 
        "desc": "Bí quyết kết hợp rau thịt cho Khủng Long đau răng.", 
        "content": "Kết hợp 🥬 + 💧 để tạo ra 🥗 (Salad). Món này cực mềm cho những khách hàng đang đau răng!"
    },
    {
        "id": "tip_2", 
        "name": "Nghệ Thuật Luộc Nấu", 
        "price": 50, 
        "desc": "Cách tạo ra Nước Sôi để chế biến món ăn thanh đạm.", 
        "content": "Nấu 💧 + 🔥 để ra ♨️ (Nước sôi). Sau đó dùng ♨️ + 🥩 = 🍲 (Thịt luộc) hoặc ♨️ + 🥬 = 🥣 (Canh rau)."
    },
    {
        "id": "tip_3", 
        "name": "Bậc Thầy Cơm Chiên", 
        "price": 50, 
        "desc": "Cách làm món cơm trứng ốp la huyền thoại.", 
        "content": "Rán trứng trước: 🥚 + 🔥 = 🍳. Sau đó lấy 🍳 + 🍚 để tạo ra 🍛 (Cơm trứng) phục vụ các tín đồ mê trứng!"
    },
    {
        "id": "tip_4", 
        "name": "Bữa Ăn Hạnh Phúc", 
        "price": 100, 
        "desc": "Công thức đắt giá nhất dành cho Khủng Long đang buồn!", 
        "content": "Bước 1: Nướng thịt (🥩 + 🔥 = 🍖). Bước 2: Trộn 🍖 + 😃 + 🌶️ để tạo ra 🍛 (Cà ri cay vui vẻ) trị giá 80 đồng!"
    },
    {
        "id": "tip_5", 
        "name": "Gia Vị Bùng Nổ", 
        "price": 40, 
        "desc": "Cách chiều lòng các thực khách thích ăn cay.", 
        "content": "Nếu đã có sẵn 🍛 (Cơm trứng), hãy thêm 🌶️ để biến nó thành món cơm cay nồng cháy ngay lập tức!"
    }
]


# Giả sử hàm load_que này đọc file data que.json
def load_que_data():
    try:
        with open('data_que.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return ["Vạn sự tùy duyên.", "Hãy kiên nhẫn hơn.", "Một cơ hội mới đang đến."]

def render_shop():
    # --- Khởi tạo các trạng thái cần thiết ---
    if 'unlocked_tips' not in st.session_state:
        st.session_state.unlocked_tips = []
    
    if 'current_que' not in st.session_state:
        st.session_state.current_que = None # Lưu nội dung quẻ vừa bốc

    # ================= HIỂN THỊ QUẺ (TRANG ĐỌC QUẺ) =================
    if st.session_state.current_que:
        st.balloons()
        st.markdown("### 🏮 Quẻ Xăm Của Bạn")
        st.info(st.session_state.current_que)
        
        if st.button("Tiếp tục (Continue)"):
            st.session_state.current_que = None
            st.rerun()
        return # Dừng render phần shop bên dưới khi đang đọc quẻ

    # ================= GIAO DIỆN SHOP CHÍNH =================
    tab1, tab2, tab3 = st.tabs(["🍎 Nguyên liệu", "📜 Bí kíp nấu ăn", "🏮 Xin quẻ"])

    # --- TAB 1 & 2 giữ nguyên logic của bạn ---
    with tab1:
        cols = st.columns(2)
        for index, item in enumerate(SHOP_INGREDIENTS):
            col = cols[index % 2]
            with col:
                buy_label = f"Mua {item['icon']} - {item['price']}đ"
                if st.button(buy_label, key=f"buy_ing_{index}", use_container_width=True):
                    if st.session_state.money >= item['price']:
                        st.session_state.money -= item['price']
                        st.session_state.inventory[item['icon']] = st.session_state.inventory.get(item['icon'], 0) + 1
                        st.toast(f"Đã mua 1 {item['name']}!", icon="✅")
                        st.rerun()
                    else:
                        st.toast("Không đủ tiền!", icon="❌")

    with tab2:
        for index, tip in enumerate(SHOP_TIPS):
            st.markdown(f"**{tip['name']}**")
            if tip['id'] in st.session_state.unlocked_tips:
                st.info(f"💡 **Đã mở khóa:** {tip['content']}")
            else:
                st.caption(tip['desc'])
                if st.button(f"📖 Mua bí kíp ({tip['price']} đồng)", key=f"buy_tip_{index}"):
                    if st.session_state.money >= tip['price']:
                        st.session_state.money -= tip['price']
                        st.session_state.unlocked_tips.append(tip['id'])
                        st.rerun()
            st.divider()

    # ================= TAB 3: XIN QUẺ (MỚI) =================
    with tab3:
        st.subheader("🏮 Miếu Khủng Long Tiên Tri")
        st.write("Bạn đang gặp bế tắc? Hãy xin một lời khuyên từ thần linh.")
        
        # Tạo giá tiền ngẫu nhiên cho mỗi lần render hoặc cố định trong session
        if 'que_price' not in st.session_state:
            st.session_state.que_price = random.randint(300, 500)
        
        st.warning(f"Phí xin quẻ: **{st.session_state.que_price}đ**")
        
        if st.button("🏮 Thành tâm xin quẻ", use_container_width=True):
            if st.session_state.money >= st.session_state.que_price:
                # Trừ tiền
                st.session_state.money -= st.session_state.que_price
                
                # Lấy dữ liệu quẻ
                ques = load_que_data()
                st.session_state.current_que = random.choice(ques)
                
                # Reset giá quẻ cho lần sau
                st.session_state.que_price = random.randint(300, 500)
                st.rerun()
            else:
                st.error("Bạn không đủ tiền công đức để xin quẻ!")