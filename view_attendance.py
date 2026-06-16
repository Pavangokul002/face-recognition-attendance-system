"""
Attendance Report Viewer
View and export attendance records from the terminal.

Usage:
    python view_attendance.py              # View today's attendance
    python view_attendance.py 2025-06-15   # View specific date
    python view_attendance.py --all        # List all attendance dates
"""

import sys
import csv
import os
from datetime import datetime
from utils.attendance import get_attendance_summary, list_attendance_files


def print_table(records: list, date_str: str):
    """Print attendance records as a formatted table."""
    print(f"\n{'='*55}")
    print(f"  ATTENDANCE REPORT  |  Date: {date_str}")
    print(f"{'='*55}")

    if not records:
        print("  No attendance records found for this date.")
        print(f"{'='*55}\n")
        return

    print(f"  {'#':<4} {'Name':<25} {'Time':<12} {'Status'}")
    print(f"  {'-'*50}")
    for i, row in enumerate(records, 1):
        print(f"  {i:<4} {row['Name']:<25} {row['Time']:<12} {row['Status']}")

    print(f"{'='*55}")
    print(f"  Total Present: {len(records)}")
    print(f"{'='*55}\n")


def export_to_txt(records: list, date_str: str):
    """Export attendance to a plain text file."""
    filename = f"attendance/report_{date_str}.txt"
    with open(filename, "w") as f:
        f.write(f"ATTENDANCE REPORT - {date_str}\n")
        f.write("="*50 + "\n")
        for i, row in enumerate(records, 1):
            f.write(f"{i}. {row['Name']}  |  {row['Time']}  |  {row['Status']}\n")
        f.write("="*50 + "\n")
        f.write(f"Total Present: {len(records)}\n")
    print(f"[✔] Report exported to: {filename}")


def main():
    args = sys.argv[1:]

    if "--all" in args:
        files = list_attendance_files()
        if not files:
            print("\n[INFO] No attendance records found.")
            return
        print(f"\n[INFO] Attendance records ({len(files)} day(s)):")
        for f in files:
            date = f.replace("_attendance.csv", "")
            summary = get_attendance_summary(date)
            print(f"  {date}  —  {summary['total']} present")
        return

    # Get date from argument or use today
    if args and args[0] != "--all":
        date_str = args[0]
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            print("[ERROR] Invalid date format. Use: YYYY-MM-DD")
            return
    else:
        date_str = datetime.now().strftime("%Y-%m-%d")

    summary = get_attendance_summary(date_str)
    print_table(summary["records"], summary["date"])

    if summary["records"]:
        export = input("Export to TXT? (y/n): ").strip().lower()
        if export == "y":
            export_to_txt(summary["records"], date_str)


if __name__ == "__main__":
    main()
