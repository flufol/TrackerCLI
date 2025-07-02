import json
import os
import sys
import argparse
import pyfiglet
from pathlib import Path
from datetime import date
from rich.console import Console
from rich.table import Table
from rich.text import Text


DIR = Path(__file__).resolve().parent
SAVE = DIR / 'save.json'



def get_save():
    with open(SAVE, "r") as file:
        data = json.load(file)
    return data


def mark_day(week, day, value):
    status_map = {
        "complete": True,
        "fail": False,
        "empty": None
    }

    data = get_save()

    week = str(week)
    day = str(day)

    if value not in status_map:
        print("Not a correct value")
        return

    if week not in data:
        data[week] = {}

    if int(day) not in range(1, 8):
        print("Not a valid day")
        return

    if day not in data[week]:
        data[week][day] = {"completed": None}

    data[week][day]['completed'] = status_map[value]

    with open(SAVE, "w") as file:
        json.dump(data, file, indent=2)


def get_current_day():
    return date.today().isocalendar().weekday


def get_current_week():
    return date.today().isocalendar().week


def get_week_status(week: int = None):
    if week is None:
        week = get_current_week()

    data = get_save()
    return data.get(str(week), {})


def get_streak(week: int = None):
    if week is None:
        week = get_current_week() if get_current_day() == 7 else get_current_week() - 1

    if week < 1:
        return 0

    status = get_week_status(week)
    for i in range(1, 8):
        day_data = status.get(str(i), {"completed": None})
        if day_data.get("completed") is not True:
            return 0
    
    return 1 + get_streak(week - 1)


def get_streak_color(streak: int):
    streak_colors = {
        range(0, 1): "gray",
        range(1, 3): "white",
        range(3, 5): "green",
        range(5, 8): "cyan",
        range(8, 11): "blue",
        range(11, 14): "magenta",
        range(14, 17): "orange1",
        range(17, 20): "yellow1",
        range(20, 24): "bright_red",
        range(30, 40): "deep_pink1",
        range(40, 51): "gold1"
    }

    default_color = "bold gold3"

    for streak_range, color in streak_colors.items():
        if streak in streak_range:
            return color
    return default_color


def display_streak():
    streak = get_streak()

    ascii = pyfiglet.figlet_format(str(streak))
    console = Console()
    console.print(Text(ascii, style=get_streak_color(streak)))


def display_week(week: int):
    status_map = {
        True:  "[green on green] WW [/]",
        False: "[red on red] WW [/]",
        None:  "[black on black] WW [/]"
    }

    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    status_list = []

    for i in range(1, 8):
        day_data = get_week_status(week).get(str(i), {"completed": None})
        status_list.append(status_map[day_data.get("completed")])

    console = Console()
    table = Table(show_header=True, box=None, padding=(0, 1))

    for i in days:
        table.add_column(justify="center")

    table.add_row(*status_list)
    table.add_row(*[f"[dim]{day}[/]" for day in days])
    console.print(f"[underline]Week {week}[/], streak of [{get_streak_color(get_streak())}]{get_streak()}[/]")
    console.print(table)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tracker of what you want")

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    subparsers = parser.add_subparsers(dest='command')

    parser_mark_today = subparsers.add_parser('mark-day', help='Marks today as the specified status')
    parser_mark_today.add_argument('--day', help='choose a specific day to set the status off', type=int, default=get_current_day(), choices=[1, 2, 3, 4, 5, 6, 7])
    parser_mark_today.add_argument('status', help='the status the day will be set to', type=str, choices=['complete', 'fail', 'empty'], nargs='?', default="empty")

    parser_display = subparsers.add_parser('display-week', help="Displays the current week status")
    parser_display.add_argument('week', help='the specific week to display', type=int, nargs='?', default=get_current_week())

    parser_streak = subparsers.add_parser('streak', help='Shows the current streak of fully completed weeks')

    args = parser.parse_args()

    if args.command == 'display-week':
        display_week(args.week)
    elif args.command == 'mark-day':
        mark_day(get_current_week(), args.day, args.status)
        display_week(get_current_week())
    elif args.command == 'streak':
        display_streak()


#TODO Make seperate things to mark off, make a differernt json for each? or seperate json dicts
#TODO Make displaying streaks pretty