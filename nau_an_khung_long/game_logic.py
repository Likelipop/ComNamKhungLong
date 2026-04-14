from collections import Counter
import random

# 1. BẢNG GIÁ (Bao gồm nguyên liệu cơ bản, trung gian và món hoàn chỉnh)
PRICES = {
    "💧": 8, "🔥": 8, "🥬": 13, "🥚": 13, "🍚": 13, "🥩": 25, "😃": 30, "🌶️": 8,
    "♨️ (Nước sôi)": 10,         # Nguyên liệu trung gian 
    "🍳 (Trứng ốp la)": 15,     # Nguyên liệu trung gian / Món ăn cơ bản
    "🍖 (Thịt nướng)": 40,
    "🥗 (Salad)": 25,
    "🍲 (Thịt luộc)": 50,
    "🥣 (Canh rau)": 30,
    "🍛 (Cơm trứng)": 35,
    "🍛 (Cà ri vui vẻ)": 80,
    "🌮 (Thịt cuốn rau)": 60
}

# 2. CÔNG THỨC NẤU ĂN PHONG PHÚ (Hỗ trợ nấu nhiều giai đoạn)
# Hàm này giúp sắp xếp thứ tự emoji, nhập "🔥+🥩" hay "🥩+🔥" đều hiểu là một món.
def make_recipe_key(items):
    return "+".join(sorted(items))

RECIPES = {
    make_recipe_key(["🥩", "🔥"]): "🍖",
    make_recipe_key(["🥬", "💧"]): "🥗",
    
    # --- Nấu nhiều giai đoạn (Multi-stage) ---
    make_recipe_key(["💧", "🔥"]): "♨️",                 # Giai đoạn 1: Tạo nước sôi
    make_recipe_key(["♨️", "🥩"]): "🍲",      # Giai đoạn 2: Dùng nước sôi luộc thịt
    make_recipe_key(["♨️", "🥬"]): "🥣",       # Giai đoạn 2: Dùng nước sôi nấu rau
    
    make_recipe_key(["🥚", "🔥"]): "🍳",               # Giai đoạn 1: Rán trứng
    make_recipe_key(["🍳", "🍚"]): "🍛",   # Giai đoạn 2: Làm cơm trứng
    
    # --- Nấu phức tạp (3 nguyên liệu) ---
    make_recipe_key(["🍖", "😃", "🌶️"]): "🍛",
}

def init_inventory():
    return {
        "🥩": 5, "🥬": 5, "💧": 10, "🔥": 10, "😃": 2, "🌶️": 2, 
        "🥚": 5, "🍚": 5 # Cấp thêm nguyên liệu mới đầu game
    }

def compose(ingredients_str, inventory):
    
    # --- BỘ NHẬN DIỆN THÔNG MINH ---
    # Lấy tất cả tên nguyên liệu từ Kho và Bảng giá (PRICES)
    valid_items = list(set(list(inventory.keys()) + list(PRICES.keys())))
    # Sắp xếp theo độ dài giảm dần (để ưu tiên nhận diện chữ dài như "♨️ (Nước sôi)" trước)
    valid_items.sort(key=len, reverse=True)
    
    raw_items = []
    # Xóa dấu cộng (nếu người chơi có lỡ nhập) để dễ phân tích
    remaining_str = ingredients_str.replace("+", "")
    
    # Quét chuỗi nhập vào để bóc tách từng nguyên liệu
    while remaining_str:
        found = False
        for item in valid_items:
            # Nếu đoạn đầu của chuỗi khớp với tên nguyên liệu
            if remaining_str.startswith(item):
                raw_items.append(item)
                # Cắt phần nguyên liệu đã nhận diện ra khỏi chuỗi
                remaining_str = remaining_str[len(item):]
                found = True
                break
        
        if not found:
            # Nếu là khoảng trắng hoặc ký tự lạ không nhận ra, bỏ qua 1 ký tự và quét tiếp
            remaining_str = remaining_str[1:]
            
    if not raw_items:
        return False, "Vui lòng nhập đúng nguyên liệu có trong kho!"

    # 1. KIỂM TRA XEM CÓ ĐỦ NGUYÊN LIỆU TRONG KHO KHÔNG
    needed_items = Counter(raw_items)
    
    for item, count in needed_items.items():
        if inventory.get(item, 0) < count:
            return False, f"Không đủ: {item} (Cần {count}, đang có {inventory.get(item, 0)})"

    # 2. TRỪ NGUYÊN LIỆU KHỎI KHO
    for item, count in needed_items.items():
        inventory[item] -= count
        # Xóa hẳn key nếu số lượng về 0 cho gọn bảng
        if inventory[item] == 0:
            del inventory[item]

    # 3. TIẾN HÀNH NẤU (So khớp công thức)
    recipe_key = make_recipe_key(raw_items)
    
    # Nếu đúng công thức
    if recipe_key in RECIPES and random.random() <= 0.65:
        result_dish = RECIPES[recipe_key]
        # THÊM MÓN VỪA NẤU VÀO KHO
        inventory[result_dish] = inventory.get(result_dish, 0) + 1
        print(inventory[result_dish])
        print(result_dish)
        print(len(result_dish))
        return True, result_dish
    else:
        return False, "💩 (Thất bại, món ăn cháy đen!)"

def calculate_price(dish_name):
    # Trả về giá tiền có sẵn trong bảng PRICES, nếu là món "sáng tạo" lạ thì tính theo độ dài tên
    if dish_name in PRICES:
        return PRICES[dish_name]
    return 15 + (len(dish_name) * 3)