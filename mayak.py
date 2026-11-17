import tkinter as tk
from datetime import datetime
from zoneinfo import ZoneInfo
import time

# =========================
# MAIN WINDOW
# =========================

root = tk.Tk()
root.title("Advanced Digital Clock")
root.geometry("1000x850")
root.configure(bg="#101015")
root.minsize(650, 650)

bg = "#101015"
white = "#F5F5F5"
blue = "#4AAFFF"
green = "#50DC96"
gray = "#999999"
orange = "#FFB347"

fullscreen = False

# =========================
# TITLE
# =========================

title = tk.Label(
    root,
    text="ADVANCED DIGITAL CLOCK",
    font=("Arial", 28, "bold"),
    bg=bg,
    fg=blue
)
title.pack(pady=15)

# =========================
# DIGITAL CLOCK
# =========================

time_label = tk.Label(
    root,
    font=("Consolas", 75, "bold"),
    bg=bg,
    fg=white
)
time_label.pack()

ampm_label = tk.Label(
    root,
    font=("Arial", 25, "bold"),
    bg=bg,
    fg=green
)
ampm_label.pack()

date_label = tk.Label(
    root,
    font=("Arial", 22),
    bg=bg,
    fg=gray
)
date_label.pack(pady=5)

day_label = tk.Label(
    root,
    font=("Arial", 28, "bold"),
    bg=bg,
    fg=blue
)
day_label.pack()

status_label = tk.Label(
    root,
    text="● CLOCK RUNNING",
    font=("Arial", 15, "bold"),
    bg=bg,
    fg=green
)
status_label.pack(pady=10)


def update_clock():
    now = datetime.now()

    time_label.config(
        text=now.strftime("%I:%M:%S")
    )

    ampm_label.config(
        text=now.strftime("%p")
    )

    date_label.config(
        text=now.strftime("%d %B %Y")
    )

    day_label.config(
        text=now.strftime("%A")
    )

    root.after(1000, update_clock)


# =========================
# STOPWATCH
# =========================

tk.Label(
    root,
    text="STOPWATCH",
    font=("Arial", 22, "bold"),
    bg=bg,
    fg=orange
).pack(pady=(15, 5))

stopwatch_label = tk.Label(
    root,
    text="00:00:00.00",
    font=("Consolas", 35, "bold"),
    bg=bg,
    fg=white
)
stopwatch_label.pack()

running = False
start_time = 0
elapsed = 0


def update_stopwatch():
    if running:
        total = elapsed + time.perf_counter() - start_time

        hours = int(total // 3600)
        minutes = int((total % 3600) // 60)
        seconds = int(total % 60)
        centiseconds = int((total % 1) * 100)

        stopwatch_label.config(
            text=f"{hours:02}:{minutes:02}:"
                 f"{seconds:02}.{centiseconds:02}"
        )

    root.after(30, update_stopwatch)


def start_stopwatch():
    global running, start_time

    if not running:
        start_time = time.perf_counter()
        running = True


def pause_stopwatch():
    global running, elapsed

    if running:
        elapsed += time.perf_counter() - start_time
        running = False


def reset_stopwatch():
    global running, elapsed, start_time

    running = False
    elapsed = 0
    start_time = 0

    stopwatch_label.config(
        text="00:00:00.00"
    )


button_frame = tk.Frame(root, bg=bg)
button_frame.pack(pady=10)

tk.Button(
    button_frame,
    text="START",
    command=start_stopwatch,
    bg=green,
    fg="black",
    width=10,
    font=("Arial", 11, "bold")
).pack(side="left", padx=5)

tk.Button(
    button_frame,
    text="PAUSE",
    command=pause_stopwatch,
    bg=orange,
    fg="black",
    width=10,
    font=("Arial", 11, "bold")
).pack(side="left", padx=5)

tk.Button(
    button_frame,
    text="RESET",
    command=reset_stopwatch,
    bg="#FF5555",
    fg="white",
    width=10,
    font=("Arial", 11, "bold")
).pack(side="left", padx=5)


# =========================
# WORLD CLOCK
# =========================

tk.Label(
    root,
    text="WORLD CLOCK",
    font=("Arial", 22, "bold"),
    bg=bg,
    fg=blue
).pack(pady=(15, 8))

world_frame = tk.Frame(root, bg=bg)
world_frame.pack()

cities = {
    "India": "Asia/Kolkata",
    "London": "Europe/London",
    "New York": "America/New_York",
    "Dubai": "Asia/Dubai",
    "Tokyo": "Asia/Tokyo",
    "Sydney": "Australia/Sydney"
}

world_labels = {}

for city in cities:

    row = tk.Frame(world_frame, bg=bg)
    row.pack(fill="x", pady=3)

    tk.Label(
        row,
        text=city,
        font=("Arial", 15, "bold"),
        bg=bg,
        fg=gray,
        width=15,
        anchor="w"
    ).pack(side="left")

    label = tk.Label(
        row,
        text="",
        font=("Consolas", 16, "bold"),
        bg=bg,
        fg=green
    )
    label.pack(side="left")

    world_labels[city] = label


def update_world_clock():

    now = datetime.now()

    for city, timezone in cities.items():

        city_time = now.astimezone(
            ZoneInfo(timezone)
        )

        world_labels[city].config(
            text=city_time.strftime(
                "%I:%M:%S %p  |  %d-%m-%Y"
            )
        )

    root.after(1000, update_world_clock)


# =========================
# FULLSCREEN
# =========================

def fullscreen_mode(event=None):
    global fullscreen

    fullscreen = not fullscreen

    root.attributes(
        "-fullscreen",
        fullscreen
    )


def exit_clock(event=None):
    root.destroy()


root.bind("<F11>", fullscreen_mode)
root.bind("<Escape>", exit_clock)


# =========================
# START ALL FEATURES
# =========================

update_clock()
update_stopwatch()
update_world_clock()

root.mainloop()
