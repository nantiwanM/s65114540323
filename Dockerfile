FROM python:3.12

# ติดตั้ง Node.js, npm 
RUN apt-get update && \
    apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    npm install -g npm@latest && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# ตั้ง working directory
WORKDIR /app

# ติดตั้ง Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# คัดลอก package.json
COPY theme/static_src/package*.json /app/theme/static_src/

# ติดตั้ง npm dependencies
WORKDIR /app/theme/static_src
RUN npm install

# คัดลอก source code ที่เหลือ
WORKDIR /app
COPY . .