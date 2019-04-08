set -x

wg-quick up jf
sudo sysctl -w net.inet.ip.forwarding=1
sudo pfctl -d
sudo pfctl -e -f /etc/pf.conf
