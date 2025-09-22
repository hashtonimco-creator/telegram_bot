#!/bin/bash

# Hashtonim Bot Server Setup Script
echo "🚀 Setting up Hashtonim Telegram Bot..."

# Update system
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install required packages
echo "🔧 Installing required packages..."
sudo apt install git python3-pip python3-venv screen -y

# Create user if not exists
if ! id "hashtonim" &>/dev/null; then
    echo "👤 Creating hashtonim user..."
    sudo useradd -m -s /bin/bash hashtonim
fi

# Switch to hashtonim user directory
echo "📁 Setting up project directory..."
sudo -u hashtonim bash << 'EOF'
cd /home/hashtonim

# Clone or update repository
if [ -d "telegram_bot" ]; then
    echo "📥 Updating existing repository..."
    cd telegram_bot
    git pull origin main
else
    echo "📥 Cloning repository..."
    git clone https://github.com/hashtonimco-creator/telegram_bot.git
    cd telegram_bot
fi

# Create virtual environment
echo "🐍 Creating virtual environment..."
python3 -m venv .venv

# Activate virtual environment and install dependencies
echo "📚 Installing dependencies..."
source .venv/bin/activate
pip install -r requirements.txt

echo "✅ Setup completed for user hashtonim"
EOF

# Setup systemd service
echo "⚙️ Setting up systemd service..."
sudo cp /home/hashtonim/telegram_bot/hashtonim_bot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable hashtonim_bot.service

echo "🎉 Setup completed!"
echo ""
echo "📝 Next steps:"
echo "1. Edit bot.py and set your BOT_TOKEN and SUPER_ADMIN_ID"
echo "2. Start the service: sudo systemctl start hashtonim_bot.service"
echo "3. Check status: sudo systemctl status hashtonim_bot.service"
echo "4. View logs: sudo journalctl -u hashtonim_bot.service -f"
