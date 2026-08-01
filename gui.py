import tkinter as tk
import threading
import os

def start():
    os.system("python main.py")

def stop():
    print("Stop manually (press Q in window)")

root = tk.Tk()
root.title("Surveillance Control")

start_btn = tk.Button(root, text="Start System", command=lambda: threading.Thread(target=start).start())
start_btn.pack(pady=10)

stop_btn = tk.Button(root, text="Stop System", command=stop)
stop_btn.pack(pady=10)

root.mainloop()