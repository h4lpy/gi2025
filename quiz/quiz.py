import socket
import threading
import random
from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule

HOST = "0.0.0.0"
PORT = 1337

console = Console(color_system="truecolor", force_terminal=True, width=80)

questions = [
    ("What is the capital of France?", "paris"),
    ("What is 5 + 7?", "12"),
    ("What does DNS stand for?", "domain name system"),
    ("What is the binary representation of 5?", "101"),
    ("Who developed the Windows NT kernel?", "microsoft"),
    ("What protocol does HTTPS use for encryption?", "tls"),
    ("What is 0x41 in ASCII?", "a"),
]

FLAG = "CTF{quiz_master_supreme}"
MAX_ATTEMPTS = 3
NUM_QUESTIONS = len(questions)

ASCII_HEADER = r"""
  ____ ____ ______   __  __ _    _ _____ 
 / ___|  _ \___ /  |  \/  | |  | | ____|
| |   | | | ||_ \  | |\/| | |  | |  _|  
| |___| |_| |__) | | |  | | |__| | |___ 
 \____|____/____/  |_|  |_|\_____|_____|
"""

def send(conn, text):
    console.begin_capture()
    console.print(text)
    output = console.end_capture()
    conn.sendall(output.encode())

def handle_client(conn, addr):
    send(conn, Panel.fit(f"[bold green]{ASCII_HEADER}[/bold green]",
                         subtitle="[bright_black]Ultimate CTF Quiz[/bright_black]",
                         border_style="bright_black"))
    send(conn, Rule("[cyan]Answer the questions to earn the flag[/cyan]"))

    chosen_questions = random.sample(questions, NUM_QUESTIONS)
    try:
        for i, (q, answer) in enumerate(chosen_questions, start=1):
            attempts = 0
            send(conn, Panel.fit(f"[bold white]Question {i}/{NUM_QUESTIONS}[/bold white]\n\n[q]{q}[/q]",
                                 border_style="bright_blue"))
            while attempts < MAX_ATTEMPTS:
                conn.sendall(b"> ")
                data = conn.recv(1024)
                if not data:
                    return
                user_answer = data.decode().strip().lower()
                if user_answer == answer:
                    send(conn, Panel.fit("[green]✅ Correct[/green]", border_style="green"))
                    break
                else:
                    attempts += 1
                    if attempts < MAX_ATTEMPTS:
                        send(conn, Panel.fit(f"[red]❌ Incorrect[/red] Attempts left: [yellow]{MAX_ATTEMPTS - attempts}[/yellow]",
                                             border_style="red"))
                    else:
                        send(conn, Panel.fit("[bold red]💀 Too many wrong attempts![/bold red]", border_style="red"))
                        conn.close()
                        return

        send(conn, Rule("[bold green]🏆 Congratulations![/bold green]"))
        send(conn, Panel.fit(f"[bold white on blue]FLAG:[/bold white on blue] {FLAG}",
                             border_style="bright_blue"))
        conn.close()
    except:
        conn.close()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        console.print(f"[*] Listening on {HOST}:{PORT}", style="bright_black")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    main()
