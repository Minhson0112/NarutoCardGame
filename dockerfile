# Dockerfile - Naruto Card Game Bot

# Sử dụng Python 3.11-slim để tối ưu kích thước image
FROM python:3.11-slim

# Thiết lập thư mục làm việc
WORKDIR /app

# Cài đặt các gói phụ thuộc hệ thống cần thiết (nếu có, ví dụ build-essential cho mysqlclient)
# Hiện tại dùng mysql-connector-python nên không cần nhiều build-essential
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libmariadb-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy file requirements trước để tận dụng cache của Docker layer
COPY requirements.txt .

# Nâng cấp pip và cài đặt dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ mã nguồn vào container
COPY . .

# Thiết lập biến môi trường
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Lệnh khởi chạy bot
CMD ["python", "-m", "bot.main"]
