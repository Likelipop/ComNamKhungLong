#!/bin/bash

# Tên thư mục dự án
PROJECT_NAME="nau_an_khung_long"

echo "🚀 Bắt đầu khởi tạo dự án: $PROJECT_NAME"

# Tạo thư mục gốc và di chuyển vào đó
mkdir -p "$PROJECT_NAME"
cd "$PROJECT_NAME" || exit


# 2. Tạo các thư mục con
echo "📂 Đang tạo các thư mục con (data, assets)..."
mkdir -p data assets

# 3. Tạo các file Python và requirements
echo "📄 Đang tạo các file mã nguồn..."
touch app.py game_logic.py events.py shop.py

echo "streamlit" > requirements.txt
echo "pandas" >> requirements.txt

# 4. Tạo file dữ liệu JSON với nội dung mặc định
echo "📝 Đang tạo file dữ liệu quotes.json..."
cat <<EOF > data/quotes.json
{
  "1": "Cuộc đời cũng giống như món 🥩🔥, đôi khi hơi khét nhưng vẫn phải nhai.",
  "2": "Tự do chỉ cách bạn 1000 đồng, hoặc một con khủng long bùng tiền.",
  "3": "Hãy thêm một chút 😃 vào món ăn, biết đâu đời sẽ bớt 💧."
}
EOF

# 5. Tạo các file ảnh trống (placeholder) để test
echo "🖼️ Đang tạo các file ảnh placeholder..."
touch assets/a.png assets/b.png assets/c.png

echo "---------------------------------------------------"
echo "✅ KHỞI TẠO THÀNH CÔNG! Dự án đã sẵn sàng."
echo "👉 Để bắt đầu code và chạy game, hãy thực hiện lần lượt các lệnh sau:"
echo ""
echo "   cd $PROJECT_NAME"
echo "   source venv/bin/activate  # (Nếu dùng Windows Git Bash, dùng: source venv/Scripts/activate)"
echo "   pip install -r requirements.txt"
echo "   streamlit run app.py"
echo "---------------------------------------------------"