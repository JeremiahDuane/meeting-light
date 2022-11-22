#LIBRARIES
import socket
import ipaddress

#LOCAL
from config import Port, Subnet

##
#*    Scan supplied subnet for devices listening to dedicated
#*    meeting light port.
##
def ScanSubnetForHosts(subn = Subnet):
    live_hosts = []
    ports = [Port]
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

    return live_hosts

##
#*  Persist found hosts across GUI instances
##
def SaveHosts(hosts):
    with open("./bin/addresses.txt", "w") as f:
        for host in hosts:
            f.write(f"{str(host)}:{Port}\n")

#MAIN
if __name__ == "__main__":
    scan_subnet_for_hosts()
