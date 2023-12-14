from scapy.all import *
from subprocess import Popen

CONNECTION_TABLE = {}
PAD = b"(-.-)Zzz..........."
OFFSET_KEY = -len(PAD) - 1
OFFSET_SEQ = -len(PAD) - 2


def process_incoming_packets(pkt):
    sender_ip = pkt[IP].src
    seq = pkt[ICMP].seq
    identifier = pkt[ICMP].id
    payload = pkt[ICMP].load
    print(sender_ip)
    print(str(payload))

    print(chr(payload[0]))
    msg_byte = bytes([a ^ b for a, b in zip([payload[0]], [seq])])
    print(msg_byte)

    # handle existing connections
    if sender_ip not in CONNECTION_TABLE:
        CONNECTION_TABLE[sender_ip] = msg_byte
    else:
        CONNECTION_TABLE[sender_ip] += msg_byte
    print(CONNECTION_TABLE)


def main():
    sniff(filter="icmp[icmptype] = icmp-echoreply", prn=process_incoming_packets)


if __name__ == "__main__":
    main()
