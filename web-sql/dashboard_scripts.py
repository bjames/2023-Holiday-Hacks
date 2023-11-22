import os

def ping(host: str):
    # ping the host four times
    output = os.popen(f'ping -c 4 {host}').read()
    return output

def traceroute(host: str):
    output = os.popen(f"traceroute {host}").read()
    return output

def curl(host: str):
    output = os.popen(f"curl {host}").read()
    return output