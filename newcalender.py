import tkinter as tk
from tkinter import messagebox
import calendar
import json
import os
from datetime import datetime


# =========================================================
# SETTINGS
# =========================================================

WINDOW_BG = "#F5F0FF"
HEADER_BG = "#6C4AB6"
CARD_BG = "#FFFFFF"
TEXT_COLOR = "#25213B"

TODAY_COLOR = "#6C63FF"
SUNDAY_COLOR = "#FFE0E6"
SATURDAY_COLOR = "#DDEBFF"
REMINDER_COLOR = "#D9F7E5"
BUTTON_COLOR = "#8B5CF6"

DATA_FILE = "reminders.json"


# =========================================================
# LOAD / SAVE REMINDERS
# =========================================================

def load_reminders():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as file:
                return json.load(file)
        except:
            return []

    return []


def save_reminders():
    with open(DATA_FILE, "w") as file:
        json.dump(reminders, file, indent=4)


reminders = load_reminders()


# =========================================================
# MAIN WINDOW
# =========================================================

root = tk.Tk()
root.title(" Calendar")
root.geometry("1050x700")
root.configure(bg=WINDOW_BG)


# =========================================================
# CURRENT MONTH
# =========================================================

now = datetime.now()

current_year = now.year
current_month = now.month

selected_day = now.day


# =========================================================
# HEADER
# =========================================================

header = tk.Frame(
    root,
    bg=HEADER_BG,
    height=100
)

header.pack(fill="x")

title = tk.Label(
    header,
    text=" Calendar",
    font=("Arial", 28, "bold"),
    bg=HEADER_BG,
    fg="white"
)

title.pack(pady=25)


# =========================================================
# MAIN AREA
# =========================================================

main_frame = tk.Frame(
    root,
    bg=WINDOW_BG
)

main_frame.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=20
)


# =========================================================
# CALENDAR CARD
# =========================================================

calendar_card = tk.Frame(
    main_frame,
    bg=CARD_BG,
    bd=0,
    highlightthickness=1,
    highlightbackground="#DDD5F5"
)

calendar_card.pack(
    side="left",
    fill="both",
    expand=True,
    padx=(0, 10)
)


# =========================================================
# CALENDAR HEADER
# =========================================================

calendar_header = tk.Frame(
    calendar_card,
    bg=CARD_BG
)

calendar_header.pack(
    fill="x",
    padx=20,
    pady=15
)


def previous_month():
    global current_month
    global current_year

    current_month -= 1

    if current_month == 0:
        current_month = 12
        current_year -= 1

    display_calendar()


def next_month():
    global current_month
    global current_year

    current_month += 1

    if current_month == 13:
        current_month = 1
        current_year += 1

    display_calendar()


previous_button = tk.Button(
    calendar_header,
    text="◀ Previous",
    command=previous_month,
    bg="#E9DDFF",
    fg="#5B3A9E",
    font=("Arial", 11, "bold"),
    relief="flat",
    padx=12,
    pady=8
)

previous_button.pack(side="left")


month_label = tk.Label(
    calendar_header,
    text="",
    font=("Arial", 22, "bold"),
    bg=CARD_BG,
    fg=TEXT_COLOR
)

month_label.pack(side="left", expand=True)


next_button = tk.Button(
    calendar_header,
    text="Next ▶",
    command=next_month,
    bg="#E9DDFF",
    fg="#5B3A9E",
    font=("Arial", 11, "bold"),
    relief="flat",
    padx=12,
    pady=8
)

next_button.pack(side="right")


# =========================================================
# CALENDAR GRID
# =========================================================

calendar_grid = tk.Frame(
    calendar_card,
    bg=CARD_BG
)

calendar_grid.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=5
)


# =========================================================
# CHECK IF DATE HAS REMINDER
# =========================================================

def has_reminder(day):

    date_string = f"{current_year:04d}-{current_month:02d}-{day:02d}"

    for reminder in reminders:
        if reminder["date"] == date_string:
            return True

    return False


# =========================================================
# SELECT DATE
# =========================================================

def select_date(day):

    global selected_day

    selected_day = day

    date_text = (
        f"{current_year:04d}-"
        f"{current_month:02d}-"
        f"{day:02d}"
    )

    selected_date_label.config(
        text=f"Selected: {date_text}"
    )

    display_reminders()


# =========================================================
# DISPLAY CALENDAR
# =========================================================

def display_calendar():

    for widget in calendar_grid.winfo_children():
        widget.destroy()

    month_label.config(
        text=f"{calendar.month_name[current_month]} {current_year}"
    )

    # Days of week
    days = [
        ("Sun", "#FF4D6D"),
        ("Mon", "#4A4E69"),
        ("Tue", "#4A4E69"),
        ("Wed", "#4A4E69"),
        ("Thu", "#4A4E69"),
        ("Fri", "#4A4E69"),
        ("Sat", "#1976D2")
    ]

    for column, (day_name, color) in enumerate(days):

        label = tk.Label(
            calendar_grid,
            text=day_name,
            font=("Arial", 11, "bold"),
            bg="#EFE8FF",
            fg=color,
            pady=10
        )

        label.grid(
            row=0,
            column=column,
            sticky="nsew",
            padx=2,
            pady=2
        )

    # Calendar weeks
    month_calendar = calendar.monthcalendar(
        current_year,
        current_month
    )

    for row, week in enumerate(month_calendar, start=1):

        for column, day in enumerate(week):

            if day == 0:
                label = tk.Label(
                    calendar_grid,
                    text="",
                    bg=CARD_BG
                )

                label.grid(
                    row=row,
                    column=column,
                    sticky="nsew",
                    padx=2,
                    pady=2
                )

                continue

            # Normal colour
            bg = "#FFFFFF"
            fg = TEXT_COLOR

            # Sunday
            if column == 0:
                bg = SUNDAY_COLOR
                fg = "#C62828"

            # Saturday
            elif column == 6:
                bg = SATURDAY_COLOR
                fg = "#1565C0"

            # Today
            if (
                day == now.day
                and current_month == now.month
                and current_year == now.year
            ):
                bg = TODAY_COLOR
                fg = "white"

            # Reminder
            elif has_reminder(day):
                bg = REMINDER_COLOR
                fg = "#18864B"

            button = tk.Button(
                calendar_grid,
                text=str(day),
                command=lambda d=day: select_date(d),
                font=("Arial", 12, "bold"),
                bg=bg,
                fg=fg,
                relief="flat",
                bd=0,
                activebackground="#C9B6FF"
            )

            button.grid(
                row=row,
                column=column,
                sticky="nsew",
                padx=2,
                pady=2
            )

    # Make calendar expand
    for column in range(7):
        calendar_grid.columnconfigure(
            column,
            weight=1
        )

    for row in range(len(month_calendar) + 1):
        calendar_grid.rowconfigure(
            row,
            weight=1
        )


# =========================================================
# REMINDER SIDE PANEL
# =========================================================

side_panel = tk.Frame(
    main_frame,
    bg=CARD_BG,
    width=330,
    highlightthickness=1,
    highlightbackground="#DDD5F5"
)

side_panel.pack(
    side="right",
    fill="y"
)

side_panel.pack_propagate(False)


# =========================================================
# ADD REMINDER TITLE
# =========================================================

reminder_title = tk.Label(
    side_panel,
    text="➕ Add Reminder",
    font=("Arial", 20, "bold"),
    bg="#EDE2FF",
    fg="#57349B",
    pady=15
)

reminder_title.pack(
    fill="x"
)


# =========================================================
# SELECTED DATE
# =========================================================

selected_date_label = tk.Label(
    side_panel,
    text="",
    font=("Arial", 11, "bold"),
    bg=CARD_BG,
    fg="#55516A"
)

selected_date_label.pack(
    pady=(15, 5)
)


# =========================================================
# REMINDER TEXT
# =========================================================

tk.Label(
    side_panel,
    text="Reminder:",
    font=("Arial", 11, "bold"),
    bg=CARD_BG,
    fg=TEXT_COLOR
).pack(
    anchor="w",
    padx=20
)

reminder_entry = tk.Entry(
    side_panel,
    font=("Arial", 12),
    relief="solid",
    bd=1
)

reminder_entry.pack(
    fill="x",
    padx=20,
    pady=8,
    ipady=8
)


# =========================================================
# TIME
# =========================================================

tk.Label(
    side_panel,
    text="Time (24-hour format):",
    font=("Arial", 11, "bold"),
    bg=CARD_BG,
    fg=TEXT_COLOR
).pack(
    anchor="w",
    padx=20,
    pady=(10, 0)
)

time_entry = tk.Entry(
    side_panel,
    font=("Arial", 12),
    relief="solid",
    bd=1
)

time_entry.insert(0, "18:30")

time_entry.pack(
    fill="x",
    padx=20,
    pady=8,
    ipady=8
)


# =========================================================
# SAVE REMINDER
# =========================================================

def add_reminder():

    text = reminder_entry.get().strip()
    reminder_time = time_entry.get().strip()

    if text == "":
        messagebox.showwarning(
            "Missing Reminder",
            "Please enter a reminder."
        )
        return

    try:
        datetime.strptime(
            reminder_time,
            "%H:%M"
        )
    except ValueError:
        messagebox.showerror(
            "Invalid Time",
            "Please use HH:MM format.\nExample: 18:30"
        )
        return

    date_string = (
        f"{current_year:04d}-"
        f"{current_month:02d}-"
        f"{selected_day:02d}"
    )

    reminder = {
        "date": date_string,
        "time": reminder_time,
        "text": text,
        "alerted": False
    }

    reminders.append(reminder)

    save_reminders()

    reminder_entry.delete(0, tk.END)

    display_calendar()
    display_reminders()

    messagebox.showinfo(
        "Reminder Saved",
        f"Reminder saved for {date_string}"
    )


save_button = tk.Button(
    side_panel,
    text="💾 Save Reminder",
    command=add_reminder,
    bg=BUTTON_COLOR,
    fg="white",
    font=("Arial", 12, "bold"),
    relief="flat",
    pady=10
)

save_button.pack(
    fill="x",
    padx=20,
    pady=10
)


# =========================================================
# REMINDER LIST
# =========================================================

list_title = tk.Label(
    side_panel,
    text="🔔 My Reminders",
    font=("Arial", 16, "bold"),
    bg="#E8F8EE",
    fg="#237A45",
    pady=10
)

list_title.pack(
    fill="x",
    pady=(15, 5)
)


reminder_list = tk.Frame(
    side_panel,
    bg=CARD_BG
)

reminder_list.pack(
    fill="both",
    expand=True,
    padx=15,
    pady=5
)


# =========================================================
# DELETE REMINDER
# =========================================================

def delete_reminder(index):

    if 0 <= index < len(reminders):

        reminders.pop(index)

        save_reminders()

        display_calendar()
        display_reminders()


# =========================================================
# DISPLAY REMINDERS
# =========================================================

def display_reminders():

    for widget in reminder_list.winfo_children():
        widget.destroy()

    date_string = (
        f"{current_year:04d}-"
        f"{current_month:02d}-"
        f"{selected_day:02d}"
    )

    found = False

    for index, reminder in enumerate(reminders):

        if reminder["date"] != date_string:
            continue

        found = True

        card = tk.Frame(
            reminder_list,
            bg="#F0FAF3",
            bd=1,
            relief="solid"
        )

        card.pack(
            fill="x",
            pady=5
        )

        text = tk.Label(
            card,
            text=f"🔔 {reminder['text']}\n⏰ {reminder['time']}",
            font=("Arial", 10, "bold"),
            bg="#F0FAF3",
            fg="#245A38",
            justify="left"
        )

        text.pack(
            side="left",
            padx=8,
            pady=8
        )

        delete_button = tk.Button(
            card,
            text="🗑",
            command=lambda i=index: delete_reminder(i),
            bg="#FFE1E6",
            fg="#D62839",
            relief="flat",
            font=("Arial", 10)
        )

        delete_button.pack(
            side="right",
            padx=8
        )

    if not found:

        label = tk.Label(
            reminder_list,
            text="No reminders for this date.",
            font=("Arial", 10),
            bg=CARD_BG,
            fg="#777777"
        )

        label.pack(
            pady=20
        )


# =========================================================
# CHECK REMINDERS
# =========================================================

def check_reminders():

    current_time = datetime.now()

    current_date = current_time.strftime("%Y-%m-%d")
    current_clock = current_time.strftime("%H:%M")

    for reminder in reminders:

        if (
            reminder["date"] == current_date
            and reminder["time"] == current_clock
            and not reminder["alerted"]
        ):

            messagebox.showinfo(
                "🔔 Reminder",
                reminder["text"]
            )

            reminder["alerted"] = True

            save_reminders()

    root.after(
        10000,
        check_reminders
    )


# =========================================================
# START
# =========================================================

selected_date_label.config(
    text=(
        f"Selected: "
        f"{current_year:04d}-"
        f"{current_month:02d}-"
        f"{selected_day:02d}"
    )
)

display_calendar()
display_reminders()

check_reminders()

root.mainloop()