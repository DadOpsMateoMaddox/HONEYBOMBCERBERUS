#!/bin/bash

echo "[*] Cleaning up and reinitializing HONEYBOMBV2 workspace..."

# 1. Detect current WSL username
USER_NAME=$(whoami)
WSL_HOME="/home/$USER_NAME"

# 2. Fix .bashrc prompt
echo "[*] Fixing PS1 in .bashrc..."
sed -i '/^PS1=/d' "$WSL_HOME/.bashrc"
printf '%s\n' 'PS1="\[\e[0;32m\]\u@\h:\w\$ \[\e[m\]"' >>"$WSL_HOME/.bashrc"

# 3. Create clean structure
WORKDIR="$WSL_HOME/HONEYBOMBV2"
echo "[*] Creating clean structure at $WORKDIR..."
mkdir -p "$WORKDIR"/{keys,config,cerberus,deployment/archive/pcap_dumps}

# 4. Locate misplaced keys & move
echo "[*] Searching for SSH keys to migrate..."
find /mnt/c/Users/under/OneDrive/Desktop/ -type f -name "honeybombv2_droplet_key*" -exec mv {} "$WORKDIR/keys/" \;

# 5. Set permissions
chmod 600 "$WORKDIR/keys/honeybombv2_droplet_key" 2>/dev/null

echo "[+] Environment cleaned and rebuilt under: $WORKDIR"
echo "[+] You can now SSH using:"
echo "    ssh -i $WORKDIR/keys/honeybombv2_droplet_key root@137.184.126.9"
