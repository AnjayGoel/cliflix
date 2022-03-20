sudo apt install -y vlc vlc-plugin-bittorrent
python3 setup.py install --user
echo "alias cliflix='python3 -m cliflix'" >>/home/"$USER"/.bashrc
