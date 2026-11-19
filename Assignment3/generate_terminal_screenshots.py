#!/usr/bin/env python3
"""
Generates crisp, high-resolution dark terminal screenshots for all tasks.
"""
import os
from PIL import Image, ImageDraw, ImageFont

def render_terminal(title, text_lines, output_png, width=950):
    line_height = 20
    top_bar_height = 36
    padding = 20
    content_height = len(text_lines) * line_height
    height = top_bar_height + padding * 2 + content_height

    img = Image.new('RGB', (width, height), color=(15, 23, 42)) # Slate 900
    draw = ImageDraw.Draw(img)

    # Top title bar
    draw.rectangle([(0, 0), (width, top_bar_height)], fill=(30, 41, 59))
    # Window controls (macOS traffic lights)
    draw.ellipse([(14, 12), (24, 22)], fill=(239, 68, 68)) # Red
    draw.ellipse([(32, 12), (42, 22)], fill=(245, 158, 11)) # Yellow
    draw.ellipse([(50, 12), (60, 22)], fill=(16, 185, 129)) # Green

    # Title
    draw.text((width // 2 - len(title) * 4, 10), title, fill=(203, 213, 225))

    # Try loading a monospace font or default
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 13)
    except Exception:
        font = ImageFont.load_default()

    y = top_bar_height + padding
    for line in text_lines:
        line_str = line.rstrip()
        # Syntax highlighting logic for terminal lines
        if line_str.startswith("===") or line_str.startswith("---") or line_str.startswith("[STEP"):
            color = (56, 189, 248) # Cyan header
        elif "SUCCESS" in line_str or "ACCEPTED" in line_str or "SECURE" in line_str or "0 page faults" in line_str:
            color = (74, 222, 128) # Green success
        elif "ERROR" in line_str or "REJECTED" in line_str or "TRAP" in line_str or "FAILED" in line_str or "ANOMALY" in line_str:
            color = (248, 113, 113) # Red highlight
        elif line_str.startswith("$") or line_str.startswith(">>>"):
            color = (250, 204, 21) # Yellow prompt
        elif ":" in line_str and not line_str.startswith("http"):
            color = (226, 232, 240) # Slate 200
        else:
            color = (148, 163, 184) # Muted slate 400

        draw.text((padding, y), line_str, fill=color, font=font)
        y += line_height

    img.save(output_png)
    print(f"Generated screenshot: {output_png} ({width}x{height})")

def main():
    repo_dir = os.path.dirname(os.path.abspath(__file__))
    tasks = [
        ("Q1_Linking_Loading", "experiment_q1_results.log", "task01_output_screenshot.png", "Terminal - Task 01: Linking & Dynamic Hot Patching"),
        ("Q2_Paging", "experiment_q2_results.log", "task02_output_screenshot.png", "Terminal - Task 02: Paging & Address Translation"),
        ("Q3_Segmentation", "experiment_q3_results.log", "task03_output_screenshot.png", "Terminal - Task 03: Segmentation & MMU Exception Handling"),
        ("Q4_Virtual_Memory", "experiment_q4_results.log", "task04_output_screenshot.png", "Terminal - Task 04: Virtual Memory, Demand Paging & COW"),
        ("Q5_Page_Replacement", "experiment_q5_results.log", "task05_output_screenshot.png", "Terminal - Task 05: Page Replacement & Belady Anomaly"),
        ("Q6_Disk_Management", "experiment_q6_results.log", "task06_output_screenshot.png", "Terminal - Task 06: Disk Management & RAID Reliability"),
        ("Q7_Memory_Management_Plan", "experiment_q7_results.log", "task07_output_screenshot.png", "Terminal - Task 07: Real-Time Memory Locking & Edge Design")
    ]

    for folder, log_file, out_name, title in tasks:
        log_path = os.path.join(repo_dir, folder, log_file)
        if os.path.exists(log_path):
            with open(log_path, 'r', errors='ignore') as f:
                lines = f.readlines()
            # Take representative sample (first 45 lines)
            sample_lines = lines[:45]
            out_path = os.path.join(repo_dir, folder, out_name)
            render_terminal(title, sample_lines, out_path)

if __name__ == '__main__':
    main()
