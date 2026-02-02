#!/bin/bash

echo "[*] Setting up Shennina for Termux..."

echo "[*] Updating packages..."
pkg update -y && pkg upgrade -y

echo "[*] Installing dependencies..."
pkg install -y python nmap git clang libffi openssl unstable-repo

echo "[*] Installing Metasploit..."
pkg install -y metasploit

echo "[*] Upgrading pip..."
pip install --upgrade pip

echo "[*] Installing Python dependencies..."
# Set flags for building on Android if necessary
export CFLAGS="-Wno-deprecated-declarations -Wno-unreachable-code"
pip install -r requirements.txt

echo "[*] Setup complete!"
echo "[*] Note: You may need to run 'msfconsole' and set up the database separately."
