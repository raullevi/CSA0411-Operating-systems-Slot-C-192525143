#!/usr/bin/env python3
"""
Generate realistic, high-resolution dark-mode terminal screenshot images
for all executed tasks of Assignment 5 (CO5).
Saves images into:
  - output_ss/taskb1_output_screenshot.png
  - output_ss/taskb2_output_screenshot.png
  - output_ss/taskb3_output_screenshot.png
  - output_ss/taskb4_output_screenshot.png
"""

import os
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_SS_DIR = os.path.join(BASE_DIR, "output_ss")
os.makedirs(OUTPUT_SS_DIR, exist_ok=True)

LOG_FILES = {
    "taskb1": (
        os.path.join(BASE_DIR, "TaskB1_Linux_Server_Admin", "experiment_b1_results.log"),
        "Task B1: Linux Server Admin (Log Summary awk & Automated Disk Alert)"
    ),
    "taskb2": (
        os.path.join(BASE_DIR, "TaskB2_Containerise_Portal", "experiment_b2_results.log"),
        "Task B2: Containerise the Portal (Multi-Stage Dockerfile & Gunicorn Execution)"
    ),
    "taskb3": (
        os.path.join(BASE_DIR, "TaskB3_Deployment_Comparison", "experiment_b3_results.log"),
        "Task B3: Deployment Comparison (Bare Metal vs VM vs Container & K8s Healing)"
    ),
    "taskb4": (
        os.path.join(BASE_DIR, "TaskB4_Final_Engineering_Decision", "experiment_b4_results.log"),
        "Task B4: Final Engineering Decision (Multi-Service Limits & Capacity Sizing)"
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
    img_width = max(860, int(max_len * char_width) + padding * 2)
    img_height = header_height + (len(lines) * line_height) + padding * 2

    img = Image.new("RGB", (img_width, img_height), "#0d1117")
    draw = ImageDraw.Draw(img)

    # Window title bar
    draw.rectangle([(0, 0), (img_width, header_height)], fill="#161b22")
    draw.line([(0, header_height), (img_width, header_height)], fill="#30363d", width=1)

    # Mac style window buttons
    draw.ellipse([(14, 15), (26, 27)], fill="#ff5f56")
    draw.ellipse([(34, 15), (46, 27)], fill="#ffbd2e")
    draw.ellipse([(54, 15), (66, 27)], fill="#27c93f")

    # Font
    try:
        font = ImageFont.truetype("/System/Library/Fonts/SFNSMono.ttf", font_size)
        title_font = ImageFont.truetype("/System/Library/Fonts/SFNSMono.ttf", 12)
    except Exception:
        try:
            font = ImageFont.truetype("/Library/Fonts/Courier New.ttf", font_size)
            title_font = font
        except Exception:
            font = ImageFont.load_default()
            title_font = font

    # Draw Title Bar text
    title_text = f"bash - {title}"
    draw.text((80, 14), title_text, fill="#8b949e", font=title_font)

    # Draw Terminal Lines
    y = header_height + padding
    for line in lines:
        if line.startswith("===") or line.startswith("---"):
            color = "#58a6ff"  # Soft Blue
        elif "[OK]" in line or "Auto-Healed" in line:
            color = "#3fb950"  # GitHub Green
        elif "Error" in line or "FAIL" in line or "denied" in line:
            color = "#f85149"  # Red
        elif line.startswith("$ "):
            color = "#d29922"  # Golden command prompt
        elif line.startswith("#"):
            color = "#8b949e"  # Gray comments
        elif any(k in line for k in ["Total Workload", "Capacity", "Container Pods Needed", "Decision :"]):
            color = "#e3b341"  # Bold yellow
        elif "Deployment" in line or "Bare Metal" in line or "Requests per status code" in line:
            color = "#79c0ff"  # Light blue
        else:
            color = "#c9d1d9"  # Default clean terminal foreground

        draw.text((padding, y), line, fill=color, font=font)
        y += line_height

    out_file = os.path.join(OUTPUT_SS_DIR, f"{task_id}_output_screenshot.png")
    img.save(out_file, "PNG", dpi=(300, 300))
    print(f"Generated screenshot: {out_file} ({img_width}x{img_height})")

def main():
    print("Generating terminal screenshot images for Assignment 5...")
    for task_id, (log_path, title) in LOG_FILES.items():
        render_terminal(task_id, log_path, title)
    print("All Assignment 5 terminal screenshots generated successfully.")

if __name__ == "__main__":
    main()
