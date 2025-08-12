import argparse
import socket
import threading
import json
import csv
from datetime import datetime, UTC

def scan_port(host, port, timeout, banner):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        if result == 0:
            if banner:
                try:
                    sock.send(b"HEAD / HTTP/1.1\r\n\r\n")
                    data = sock.recv(1024)
                    print(f"[+] {port}/tcp open - Banner: {data.decode().strip()}")
                except:
                    print(f"[+] {port}/tcp open - No banner")
            else:
                print(f"[+] {port}/tcp open")
        sock.close()
    except:
        pass

def main():
    parser = argparse.ArgumentParser(description="Simple Python Port Scanner")
    parser.add_argument("target", nargs="?", default="127.0.0.1", help="Target IP address or hostname")
    parser.add_argument("-p", "--ports", help="Comma-separated list of ports to scan")
    parser.add_argument("--top-ports", type=int, help="Scan top N ports")
    parser.add_argument("--all-ports", action="store_true", help="Scan all 65535 ports")
    parser.add_argument("-t", "--threads", type=int, default=10, help="Number of threads")
    parser.add_argument("--timeout", type=float, default=1.0, help="Connection timeout")
    parser.add_argument("--banner", action="store_true", help="Grab banner of services")
    parser.add_argument("-oJ", "--out-json", help="Output results to JSON file")
    parser.add_argument("-oC", "--out-csv", help="Output results to CSV file")
    parser.add_argument("-q", "--quiet", action="store_true", help="Suppress console output")
    args = parser.parse_args()

    if args.ports:
        ports = [int(p.strip()) for p in args.ports.split(",")]
    elif args.top_ports:
        ports = list(range(1, args.top_ports + 1))
    elif args.all_ports:
        ports = list(range(1, 65536))
    else:
        ports = list(range(1, 1025))  # Default: first 1024 ports

    start = datetime.now(UTC)

    threads = []
    for port in ports:
        t = threading.Thread(target=scan_port, args=(args.target, port, args.timeout, args.banner))
        threads.append(t)
        t.start()
        if len(threads) >= args.threads:
            for thread in threads:
                thread.join()
            threads = []

    for thread in threads:
        thread.join()

    end = datetime.now(UTC)
    print(f"\nScan completed in: {end - start}")

if __name__ == "__main__":
    main()
