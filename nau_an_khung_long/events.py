import random
import json
impor os
def load_random_quote():
    with open(os.path.join("data", "quotes.json"), "r", encoding="utf-8") as f:
        quotes = json.load(f)
    return random.choice(list(quotes.values()))

def get_customer():
    customers = [
        {"desc": "Tôi đang đau răng, cần món gì mềm mềm... 🦖", "wants": "🥗"},
        {"desc": "Tôi đang rất buồn bã, cần một cú sốc vị giác! 🦕", "wants": "🍛"},
        {"desc": "Đói quá đói quá, cho xin miếng thịt! 🦖", "wants": "🍖"}
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