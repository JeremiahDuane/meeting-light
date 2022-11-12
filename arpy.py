import socket
import ipaddress

live_hosts = []

# google popular tcp/udp ports and add more port numbers to your liking
ports = [8787]

def scan_subnet_for_hosts(subn = '192.168.1.0/24'):
    network = ipaddress.IPv4Network(subn)
    for ipaddr in list(network.hosts()):
        for port in ports:
             try:
                print(str(ipaddr))
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(.1)
                result = s.connect_ex((str(ipaddr), port))

                if result == 0:
                    live_hosts.append(ipaddr)
                
                s.close()
             except socket.error:
                pass

scan_subnet_for_hosts()
with open("./bin/addresses.txt", "w") as f:
    for host in live_hosts:
        f.write(str(host))
