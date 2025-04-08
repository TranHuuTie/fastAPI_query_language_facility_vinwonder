# Sử dụng base image Python
FROM python:3.10-slim
# Cài đặt thư viện hệ thống cần thiết
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc \
    && rm -rf /var/lib/apt/lists/*
# Đặt thư mục làm việc trong container
WORKDIR /app
# Sao chép yêu cầu vào container
COPY ./app /app
# Cài đặt các phụ thuộc từ requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
# Chạy FastAPI app với Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]
