# quiz_server_hacker_fixed.py
import socket
import secrets
import time
import os
from typing import Optional

HOST = "0.0.0.0"
PORT = 1337

# Toggle typing effect (set env var FAST=1 to disable)
FAST = os.getenv("FAST", "0") == "1"

G = "\x1b[32m"   # green
W = "\x1b[37m"   # white
D = "\x1b[2m"    # dim
B = "\x1b[1m"    # bold
R = "\x1b[31m"   # red
RESET = "\x1b[0m"

QUESTIONS = [
    {"q": "Subject of the email?", "a": "URGENT: Payment Missed"},
    {"q": "Suspicious sender (email)?", "a": "rob.banks1337@payyourpal.com"},
    {"q": "Suspicious filename?", "a": "invoice.pdf.svg"},
    {"q": "Destination path (site)?", "a": "admin"},
]


def make_flag() -> str:
    return "flag{svg_im4ges_c4n_c0nta1n_c0de_56de733928f2}"

def send_all(conn: socket.socket, s: str) -> None:
    try:
        conn.sendall(s.encode("utf-8"))
    except Exception:
        pass

def send_slow(conn: socket.socket, s: str, delay: float = 0.008) -> None:
    if FAST:
        send_all(conn, s)
        return
    for ch in s:
        send_all(conn, ch)
        time.sleep(delay)

def recv_line(conn: socket.socket, max_bytes: int = 4096) -> Optional[str]:
    try:
        data = conn.recv(max_bytes)
        if not data:
            return None
        return data.decode("utf-8", errors="ignore").strip()
    except Exception:
        return None

def hex_prompt() -> str:
    return f"0x{secrets.token_hex(2)}>"


def handle_client(conn: socket.socket, addr):
    flag = "flag{svg_im4ges_c4n_c0nta1n_c0de}"
    print(f"[+] connection from {addr} -> flag {flag}")

    with conn:
        # header (fixed: single triple-quoted string for ASCII art)
        ascii_art = """   _____      _     _   _____                  __      _______ _____ _____ 
  / ____|    (_)   | | |_   _|                 \ \    / /_   _|_   _|_   _|
 | |  __ _ __ _  __| |   | |  _ __ ___  _ __    \ \  / /  | |   | |   | |  
 | | |_ | '__| |/ _` |   | | | '__/ _ \| '_ \    \ \/ /   | |   | |   | |  
 | |__| | |  | | (_| |  _| |_| | | (_) | | | |    \  /   _| |_ _| |_ _| |_ 
  \_____|_|  |_|\__,_| |_____|_|  \___/|_| |_|     \/   |_____|_____|_____|                                                                                                                                                                                                                                                             
"""
        banner = B + G + ascii_art + RESET + D + " "*18 + "Stealthy Vector Graphics — [forensics]\n" + RESET + "\n"
        send_all(conn, banner)

        noise_lines = [
            "[init] kernel modules check...",
            "[probe] smtp parser loaded",
            "[trace] challenge active",
            "[watch] network stack: listening",
        ]
        for ln in noise_lines:
            send_slow(conn, D + ln + RESET + "\n", delay=0.01)
        send_all(conn, "\n")

        for i, item in enumerate(QUESTIONS, start=1):
            attempts = 0
            qline = f"{B}{G}[{i}/{len(QUESTIONS)}]{RESET} {W}{item['q']}{RESET}\n"
            while True:
                prompt = D + hex_prompt() + " " + RESET
                send_all(conn, qline)
                send_all(conn, prompt)
                reply = recv_line(conn)
                if reply is None:
                    send_all(conn, "\n" + R + "[-] disconnected\n" + RESET)
                    print(f"[-] {addr} disconnected")
                    return

                attempts += 1
                if reply.strip().lower() == item["a"].lower():
                    send_all(conn, G + "=> ok\n\n" + RESET)
                    break
                else:
                    send_all(conn, R + "=> no\n" + RESET)

        send_slow(conn, B + "\n+++ AUTHORIZED +++\n" + RESET, delay=0.01)
        send_slow(conn, D + "[proc] generating token...\n" + RESET, delay=0.01)
        time.sleep(0.12 if not FAST else 0)
        send_slow(conn, G + f"FLAG: {flag}\n" + RESET, delay=0.01)

        # graceful close
        send_slow(conn, D + "\n[proc] session complete. wiping ephemeral traces...\n" + RESET, delay=0.01)
        send_all(conn, "\n" + D + "bye.\n" + RESET)
        try:
            conn.shutdown(socket.SHUT_RDWR)
        except Exception:
            pass

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(5)
        print(f"[*] listening on {HOST}:{PORT} (FAST={FAST})")
        while True:
            conn, addr = s.accept()
            try:
                handle_client(conn, addr)
            except Exception as e:
                print(f"[!] error: {e}")
            finally:
                try:
                    conn.close()
                except Exception:
                    pass

if __name__ == "__main__":
    main()
