#!/usr/bin/env python3
"""
Generate realistic, high-resolution dark-mode terminal screenshot images
for all executed tasks of Assignment 1 (CO1).
Saves images into:
  - output_ss/task06_output_screenshot.png ... task10_output_screenshot.png
"""

import os
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_SS_DIR = os.path.join(BASE_DIR, "output_ss")
os.makedirs(OUTPUT_SS_DIR, exist_ok=True)

LOG_FILES = {
    "task06": (
        os.path.join(BASE_DIR, "Task06_Cost_of_System_Calls", "experiment_q6_results.log"),
        "Task 06: Evaluate Cost of System Calls (copy_file buffer study)"
    ),
    "task07": (
        os.path.join(BASE_DIR, "Task07_Process_Control", "experiment_q7_results.log"),
        "Task 07: Process Control System Calls (shell job runner)"
    ),
    "task10": (
        os.path.join(BASE_DIR, "Task10_Measure_and_Compare", "experiment_q10_results.log"),
        "Task 10: Measurement & Comparison (1000 Processes vs 1000 Threads)"
    )
}

def render_terminal(task_id, log_path, title):
    if os.path.exists(log_path):
        with open(log_path, 'r', encoding='utf-8') as f:
            lines = [line.rstrip() for line in f.readlines()]
    else:
        lines = [f"[Log file not found: {log_path}]"]

    padding = 24
    header_height = 42
    font_size = 14
    line_spacing = 6
    char_width = 8.5
    line_height = font_size + line_spacing

    max_len = max(len(l) for l in lines) if lines else 60
    max_len = max(max_len, len(title) + 15)

    img_width = max(950, int(max_len * char_width) + (padding * 2))
    img_height = header_height + (len(lines) * line_height) + (padding * 2)

    bg_color = (22, 27, 34)
    header_color = (33, 38, 45)
    border_color = (48, 54, 61)
    text_color = (230, 237, 243)
    accent_green = (63, 185, 80)
    accent_blue = (88, 166, 255)
    accent_yellow = (210, 153, 34)

    img = Image.new("RGB", (img_width, img_height), bg_color)
    draw = ImageDraw.Draw(img)

    draw.rectangle([(0, 0), (img_width, header_height)], fill=header_color)
    draw.line([(0, header_height), (img_width, header_height)], fill=border_color, width=1)

    draw.ellipse([(16, 14), (28, 26)], fill=(255, 95, 86))
    draw.ellipse([(36, 14), (48, 26)], fill=(255, 189, 46))
    draw.ellipse([(56, 14), (68, 26)], fill=(39, 201, 63))

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

    window_title = f"rakul@simats-hospital-os: ~/{title.split(':')[0].strip()} (bash)"
    draw.text((80, 14), window_title, fill=(139, 148, 158), font=header_font)

    y = header_height + padding
    for line in lines:
        col = text_color
        if line.startswith("===") or line.startswith("---"):
            col = accent_blue
        elif "exit status" in line or "read() calls" in line:
            col = accent_green
        elif "Entity" in line or "Measuring" in line:
            col = accent_yellow

        draw.text((padding, y), line, fill=col, font=font)
        y += line_height

    out_filename = f"{task_id}_output_screenshot.png"
    out_path1 = os.path.join(OUTPUT_SS_DIR, out_filename)
    img.save(out_path1, "PNG")

    task_dirs = {
        "task06": "Task06_Cost_of_System_Calls",
        "task07": "Task07_Process_Control",
        "task10": "Task10_Measure_and_Compare"
    }
    out_path2 = os.path.join(BASE_DIR, task_dirs[task_id], out_filename)
    img.save(out_path2, "PNG")

    print(f"Generated screenshot for {task_id}: {out_path1}")

def main():
    print("Generating terminal screenshot PNGs for Assignment 1...")
    for tid, (log, title) in LOG_FILES.items():
        render_terminal(tid, log, title)
    print("All Assignment 1 screenshots generated successfully.")

if __name__ == "__main__":
    main()
