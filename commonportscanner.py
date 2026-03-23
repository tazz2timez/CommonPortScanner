Python 3.14.3 (v3.14.3:323c59a5e34, Feb  3 2026, 11:41:37) [Clang 16.0.0 (clang-1600.0.26.6)] on darwin
Enter "help" below or click "Help" above for more information.
import socket
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

# Common ports list
COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 139, 143, 443, 445, 3389]

open_ports = []

def get_service(port):
    try:
        return socket.getservbyport(port)
    except:
        return "Unknown"

def scan_port(target, port, timeout):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        result = s.connect_ex((target, port))

        if result == 0:
            service = get_service(port)
            banner = ""

            try:
                s.send(b"HEAD / HTTP/1.0\r\n\r\n")
                banner = s.recv(1024).decode(errors="ignore").strip()
            except:
                banner = "No banner"

            output = f"[+] Port {port} OPEN ({service})"
            if banner:
                output += f" | Banner: {banner[:50]}"

            print(output)
            open_ports.append(port)
        else:
            print(f"[-] Port {port} CLOSED")

        s.close()

    except Exception as e:
        print(f"[!] Error scanning port {port}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Python Port Scanner")
    parser.add_argument("-t", "--target", help="Target IP or hostname")
    parser.add_argument("-p", "--ports", help="Port range (e.g., 1-1000)")
    parser.add_argument("-c", "--common", action="store_true", help="Scan common ports")
    parser.add_argument("-o", "--output", help="Save results to file")
    parser.add_argument("-th", "--threads", type=int, default=50, help="Number of threads")
    parser.add_argument("-to", "--timeout", type=float, default=1, help="Timeout per port")

    args = parser.parse_args()

    # 🔥 Interactive fallback
    if not args.target:
        args.target = input("Enter target (IP or domain): ")

    if not args.ports and not args.common:
        choice = input("Scan common ports? (y/n): ").lower()
        if choice == "y":
            args.common = True
        else:
            args.ports = input("Enter port range (e.g., 1-1000): ")

    # Resolve hostname
...     try:
...         target_ip = socket.gethostbyname(args.target)
...     except socket.gaierror:
...         print("[-] Invalid hostname")
...         return
... 
...     print(f"\nScanning Target: {args.target} ({target_ip})")
...     print(f"Start Time: {datetime.now()}\n")
... 
...     # Determine ports
...     if args.common:
...         ports_to_scan = COMMON_PORTS
...     else:
...         start, end = map(int, args.ports.split("-"))
...         ports_to_scan = list(range(start, end + 1))
... 
...     start_time = datetime.now()
... 
...     # Multithreading
...     with ThreadPoolExecutor(max_workers=args.threads) as executor:
...         for port in ports_to_scan:
...             executor.submit(scan_port, target_ip, port, args.timeout)
... 
...     end_time = datetime.now()
...     duration = end_time - start_time
... 
...     print("\nScan Complete")
...     print(f"Open Ports: {open_ports}")
...     print(f"Time Taken: {duration}")
... 
...     # Save results
...     if args.output:
...         with open(args.output, "w") as f:
...             f.write(f"Scan Results for {args.target} ({target_ip})\n")
...             f.write(f"Open Ports: {open_ports}\n")
...             f.write(f"Time Taken: {duration}\n")
...         print(f"[+] Results saved to {args.output}")
... 
... if __name__ == "__main__":
