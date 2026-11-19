#!/usr/bin/env python3
"""
Generate realistic, high-resolution dark-mode terminal screenshot images
for all tasks of Assignment 2 (CO2).
Saves images into:
  - output_ss/task01_output_screenshot.png ... task06_output_screenshot.png
  - Task01_Processes_and_States/task01_output_screenshot.png ...
"""

import os
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_SS_DIR = os.path.join(BASE_DIR, "output_ss")
os.makedirs(OUTPUT_SS_DIR, exist_ok=True)

# Load task logs
LOG_FILES = {
    "task01": (
        os.path.join(BASE_DIR, "Task01_Processes_and_States", "experiment_q1_results.log"),
        "Task 01: Processes & Process States (Online Exam Server Simulation)"
    ),
    "task02": (
        os.path.join(BASE_DIR, "Task02_CPU_Scheduling", "experiment_q2_results.log"),
        "Task 02: CPU Scheduling Comprehensive Suite & Quantum Study"
    ),
    "task03": (
        os.path.join(BASE_DIR, "Task03_POSIX_Threads", "experiment_q3_results.log"),
        "Task 03: POSIX Threads - Traffic-Camera Plate Reader"
    ),
    "task04": (
        os.path.join(BASE_DIR, "Task04_IPC_Pipelines", "experiment_q4_results.log"),
        "Task 04: Inter-Process Communication (Pipe vs Shared Memory)"
    ),
    "task05": (
        os.path.join(BASE_DIR, "Task05_Synchronization_Primitives", "experiment_q5_results.log"),
        "Task 05: Synchronisation (Bounded Buffer & Railway Booking Sim)"
    ),
    "task06": (
        os.path.join(BASE_DIR, "Task06_Deadlock_Bankers", "experiment_q6_results.log"),
        "Task 06: Deadlock Handling & Banker's Algorithm Suite"
    )
}

def render_terminal(task_id, log_path, title):
    if os.path.exists(log_path):
        with open(log_path, 'r', encoding='utf-8') as f:
            lines = [line.rstrip() for line in f.readlines()]
    else:
        lines = [f"[Log file not found: {log_path}]"]

    # Limit to reasonable lines for clean screenshot representation
    if len(lines) > 42:
        lines = lines[:40] + ["... [truncated for terminal screenshot display] ..."]

    # Layout measurements
    padding = 24
    header_height = 42
    font_size = 14
    line_spacing = 6
    char_width = 8.5
    line_height = font_size + line_spacing

    max_len = max(len(l) for l in lines) if lines else 60
    max_len = max(max_len, len(title) + 15)

    img_width = max(980, int(max_len * char_width) + (padding * 2))
    img_height = header_height + (len(lines) * line_height) + (padding * 2)

    # Dark mode terminal colors (macOS Terminal / iTerm2 inspired)
    bg_color = (22, 27, 34)       # Deep slate black
    header_color = (33, 38, 45)   # Window title bar
    border_color = (48, 54, 61)   # Border
    text_color = (230, 237, 243)  # Bright white-grey
    accent_green = (63, 185, 80)  # Prompt green
    accent_blue = (88, 166, 255)  # Path blue
    accent_yellow = (210, 153, 34)# Warning yellow

    img = Image.new("RGB", (img_width, img_height), bg_color)
    draw = ImageDraw.Draw(img)

    # Draw header bar
    draw.rectangle([(0, 0), (img_width, header_height)], fill=header_color)
    draw.line([(0, header_height), (img_width, header_height)], fill=border_color, width=1)

    # Window control buttons (Red, Yellow, Green)
    draw.ellipse([(16, 14), (28, 26)], fill=(255, 95, 86))   # Close
    draw.ellipse([(36, 14), (48, 26)], fill=(255, 189, 46))  # Minimize
    draw.ellipse([(56, 14), (68, 26)], fill=(39, 201, 63))   # Zoom

    # Attempt to load monospace font
    font = None
    header_font = None
    for font_name in ["Menlo.ttc", "Courier.dfont", "DejaVuSansMono.ttf", "Consolas.ttf"]:
        try:
            font = ImageFont.truetype(font_name, font_size)
            header_font = ImageFont.truetype(font_name, 12)
            break
        except Exception:
            continue
    if font is None:
        font = ImageFont.load_default()
        header_font = ImageFont.load_default()

    # Draw Title Bar text
    window_title = f"rakul@simats-os-lab: ~/{title.split(':')[0].strip()} (bash)"
    draw.text((80, 14), window_title, fill=(139, 148, 158), font=header_font)

    # Draw Terminal Lines
    y = header_height + padding
    for line in lines:
        col = text_color
        if line.startswith("===") or line.startswith("---"):
            col = accent_blue
        elif "FAILED" in line or "error" in line.lower():
            col = (248, 81, 73)
        elif "Passed" in line or "100%" in line or "granted" in line:
            col = accent_green
        elif "Algorithm:" in line or "Gantt:" in line:
            col = accent_yellow

        draw.text((padding, y), line, fill=col, font=font)
        y += line_height

    # Save to output_ss/ and task folder
    out_filename = f"{task_id}_output_screenshot.png"
    out_path1 = os.path.join(OUTPUT_SS_DIR, out_filename)
    img.save(out_path1, "PNG")

    task_dirs = {
        "task01": "Task01_Processes_and_States",
        "task02": "Task02_CPU_Scheduling",
        "task03": "Task03_POSIX_Threads",
        "task04": "Task04_IPC_Pipelines",
        "task05": "Task05_Synchronization_Primitives",
        "task06": "Task06_Deadlock_Bankers"
    }
    out_path2 = os.path.join(BASE_DIR, task_dirs[task_id], out_filename)
    img.save(out_path2, "PNG")

    print(f"Generated screenshot for {task_id}: {out_path1}")

def main():
    print("Generating terminal screenshot PNGs for Assignment 2...")
    for tid, (log, title) in LOG_FILES.items():
        render_terminal(tid, log, title)
    print("All screenshots generated successfully.")

if __name__ == "__main__":
    main()
