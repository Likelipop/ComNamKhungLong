import streamlit as st
import json
import random

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