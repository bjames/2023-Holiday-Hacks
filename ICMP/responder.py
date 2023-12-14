from scapy.all import *
from subprocess import Popen
import atexit

CONNECTION_TABLE = {}
FLAG = b"flag{f06639ad37f330fc03af6dad7782362b}"
PLAG = b"flagrantfalseflagisfalseandnotaflag{{}"
PAD = b"(-.-)Zzz..........."
OBSFUSCATED_FLAG = bytes([a ^ b for a, b in zip(FLAG, PLAG)])


def reenable_kernel_icmp():
    Popen("echo 0 > /proc/sys/net/ipv4/icmp_echo_ignore_all", shell=True)
    Popen("echo 0 > /proc/sys/net/ipv6/icmp/echo_ignore_all", shell=True)


def disable_kernel_icmp():
    # atexit.register(reenable_kernel_icmp)
    Popen("echo 1 > /proc/sys/net/ipv4/icmp_echo_ignore_all", shell=True)
    Popen("echo 1 > /proc/sys/net/ipv6/icmp/echo_ignore_all", shell=True)


def process_incoming_packets(pkt):
    sender_ip = pkt[IP].src
    seq = pkt[ICMP].seq
    identifier = pkt[ICMP].id

    # handle existing connections
    if sender_ip not in CONNECTION_TABLE:
        CONNECTION_TABLE[sender_ip] = [0, seq]
        CONNECTION_TABLE[sender_ip] = 0
    else:
        CONNECTION_TABLE[sender_ip] += 1

    index = CONNECTION_TABLE[sender_ip] % len(FLAG)

    # logging but lazier
    if index == 0:
        print(CONNECTION_TABLE)

    reply = ICMP(
        type="echo-reply", code=0, id=identifier, seq=OBSFUSCATED_FLAG[index]
    ) / (chr(PLAG[index]).encode() + PAD)

    send(IP(dst=sender_ip) / reply, verbose=False)


def main():
    disable_kernel_icmp()
    sniff(filter="icmp[icmptype] = icmp-echo", prn=process_incoming_packets)


if __name__ == "__main__":
    main()
