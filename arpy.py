import socket
import ipaddress

def scan_subnet_for_hosts(subn = '192.168.1.0/24'):
    live_hosts = []
    ports = [8787]
    network = ipaddress.IPv4Network(subn)
    for ipaddr in list(network.hosts()):
        for port in ports:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(.1)
                result = s.connect_ex((str(ipaddr), port))
                
                if result == 0:
                    live_hosts.append(ipaddr)
                
                s.close()
            except socket.error:
                continue

    with open("./bin/addresses.txt", "w") as f:
        for host in live_hosts:
            f.write(str(host)+"\n")

if __name__ == "__main__":
    scan_subnet_for_hosts()