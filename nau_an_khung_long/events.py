import random
import json
import os


def load_random_quote():
    with open(os.path.join("nau_an_khung_long", "data", "quotes.json"), "r", encoding="utf-8") as f:
        quotes = json.load(f)
    return random.choice(list(quotes.values()))

def get_customer():
    customers = [
        # Các món cơ bản
        {"desc": "Khủng Long đang đau răng, cần món gì mềm mềm... 🦖", "wants": "🥗"},
        {"desc": "Đói quá đói quá, cho xin miếng thịt! 🦖", "wants": "🍖"},
        
        # Các món nấu 2 giai đoạn (Sử dụng nước sôi ♨️)
        {"desc": "Bé Khủng Long muốn ăn thịt nhưng phải là thịt luộc cho thanh đạm cơ! 🦕", "wants": "🍲"},
        {"desc": "Khủng Long bị cảm rồi, muốn húp một bát canh rau nóng hổi... 🦖", "wants": "🥣"},
        {"desc": "Trời lạnh quá, cho xin một ít nước sôi để sưởi ấm cái bụng nào! ♨️", "wants": "♨️"},

        # Các món từ Trứng (🥚)
        {"desc": "Chỉ cần một quả trứng chiên vàng ươm là đủ hạnh phúc rồi! 🍳", "wants": "🍳"},
        {"desc": "Khủng Long thích ăn cơm chiến ốp la huhu 🦖", "wants": "🍛"},

        # Các món phức tạp / Cay
        {"desc": "Khủng Long đang bùn, mún có gì cay cay vui vẻ vui vẻ! 🦕", "wants": "🍛"},
        {"desc": "Cần một đĩa cơm thật thịnh soạn với thịt nướng và gia vị cay nồng! 🦖", "wants": "🍛"}
    ]
    return random.choice(customers)

def serve_food(food_name, customer_wants, inventory):
    # Kiểm tra xem món ăn có trong kho không

    print("bên trong serve", inventory)
    print(food_name)
    if (food_name not in inventory) or (inventory[food_name] <= 0):
        return "not_found"
    
    # Nếu có, trừ 1 món ăn khỏi kho
    inventory[food_name] -= 1
    if inventory[food_name] <= 0:
        del inventory[food_name]
    
    # Kiểm tra xem khách có thích món này không
    if food_name == customer_wants:
        import random
        if random.random() < 0.1: # 10% bị quỵt tiền
            return "scam"
        return "success"
    else:
        return "leave"

def get_mafia_riddle():
    riddles = [
        {"q": "Tôi có 3 quả táo, tôi lấy đi 2 quả. Tôi có bao nhiêu quả táo?", "a": "2"},
        {"q": "Tháng nào ngắn nhất trong năm?", "a": "tháng 2"}
    ]
    return random.choice(riddles)