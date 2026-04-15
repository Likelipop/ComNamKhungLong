import streamlit as st

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

def render_shop():
    # Khởi tạo kho lưu trữ bí kíp đã mua
    if 'unlocked_tips' not in st.session_state:
        st.session_state.unlocked_tips = []

    # Chia Shop thành 2 Tab cho gọn gàng
    tab1, tab2 = st.tabs(["🍎 Nguyên liệu", "📜 Bí kíp nấu ăn"])

    # ================= TAB 1: MUA NGUYÊN LIỆU =================
    with tab1:
        # Tạo lưới 2 cột để hiển thị nút mua
        cols = st.columns(2)
        for index, item in enumerate(SHOP_INGREDIENTS):
            col = cols[index % 2] # Chia đều item vào 2 cột
            with col:
                buy_label = f"Mua {item['icon']} - {item['price']}đ"
                # Nút bấm mua hàng
                if st.button(buy_label, key=f"buy_ing_{index}", use_container_width=True):
                    if st.session_state.money >= item['price']:
                        # Trừ tiền
                        st.session_state.money -= item['price']
                        # Thêm vào kho (Nếu chưa có thì tạo mới với giá trị 1)
                        st.session_state.inventory[item['icon']] = st.session_state.inventory.get(item['icon'], 0) + 1
                        st.toast(f"Đã mua 1 {item['name']} ({item['icon']})!", icon="✅")
                        st.rerun() # Tải lại trang để cập nhật tiền và bảng kho
                    else:
                        st.toast("Không đủ tiền!", icon="❌")

    # ================= TAB 2: MUA BÍ KÍP =================
    with tab2:
        for index, tip in enumerate(SHOP_TIPS):
            st.markdown(f"**{tip['name']}**")
            
            # Kiểm tra xem đã mua bí kíp này chưa
            if tip['id'] in st.session_state.unlocked_tips:
                st.info(f"💡 **Đã mở khóa:** {tip['content']}")
            else:
                st.caption(tip['desc'])
                buy_tip_label = f"📖 Mua bí kíp ({tip['price']} đồng)"
                if st.button(buy_tip_label, key=f"buy_tip_{index}"):
                    if st.session_state.money >= tip['price']:
                        st.session_state.money -= tip['price']
                        st.session_state.unlocked_tips.append(tip['id'])
                        st.toast("Đã học được bí kíp mới!", icon="🎓")
                        st.rerun()
                    else:
                        st.toast("Chưa đủ tiền mua bí kíp này!", icon="❌")
            st.divider()