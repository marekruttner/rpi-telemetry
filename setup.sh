#!/bin/bash

# Update package lists
echo "Updating package lists..."
sudo apt-get update

# Install system dependencies
echo "Installing system dependencies..."
sudo apt-get install -y python3 python3-pip python3-venv

# Optional: Create a virtual environment
echo "Setting up Python virtual environment..."
python3 -m venv ~/rpi_telemetry_env
source ~/rpi_telemetry_env/bin/activate

# Install Python packages
echo "Installing Python packages..."
pip install --upgrade pip
pip install psutil flask plotly pandas

# Install Hailo SDK dependencies (Assuming manual installation)
echo "Please ensure that the Hailo SDK is installed as per the official instructions."
echo "Visit https://hailo.ai/developer-zone/ for installation steps."

# Application directory (Assuming current directory)
APP_DIR=$(pwd)
echo "Application directory is $APP_DIR"

# Ensure that utils/__init__.py exists
touch utils/__init__.py

# Create systemd service file
echo "Creating systemd service file..."

sudo bash -c 'cat > /etc/systemd/system/rpi_telemetry.service << EOF
[Unit]
Description=Raspberry Pi Telemetry Application
After=network.target

[Service]
User='$USER'
Environment=VIRTUAL_ENV='"$HOME"'/rpi_telemetry_env
Environment=PATH='"$HOME"'/rpi_telemetry_env/bin:/usr/bin
WorkingDirectory='"$APP_DIR"'
ExecStart='"$HOME"'/rpi_telemetry_env/bin/python main.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF'

# Reload systemd daemon to recognize new service
echo "Reloading systemd daemon..."
sudo systemctl daemon-reload

# Enable and start the service
echo "Enabling and starting service..."
sudo systemctl enable rpi_telemetry.service
sudo systemctl start rpi_telemetry.service

echo "Setup complete!"
echo "Access the telemetry dashboard at http://<raspberry_pi_ip>:8080"
