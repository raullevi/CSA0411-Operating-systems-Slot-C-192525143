#!/usr/bin/env python3
import csv

def generate_svg(csv_path, output_svg):
    frames = []
    faults = []
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            frames.append(int(row['frames']))
            faults.append(int(row['faults']))

    width, height = 700, 420
    pad_left, pad_right, pad_top, pad_bot = 80, 40, 50, 60
    plot_w = width - pad_left - pad_right
    plot_h = height - pad_top - pad_bot

    max_x, min_x = max(frames), min(frames)
    max_y, min_y = 40, 0

    points = []
    for x, y in zip(frames, faults):
        px = pad_left + (x - min_x) / (max_x - min_x) * plot_w
        py = pad_top + (max_y - y) / (max_y - min_y) * plot_h
        points.append((px, py, x, y))

    path_d = "M " + " L ".join(f"{px:.1f},{py:.1f}" for px, py, _, _ in points)

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" style="background:#ffffff; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;">
  <rect width="{width}" height="{height}" fill="#f8fafc" rx="8" />
  <text x="{width/2}" y="30" text-anchor="middle" font-size="16" font-weight="bold" fill="#0f172a">Medical Imaging: Page Faults vs. Allocated Frames (Working Set Curve)</text>
  
  <!-- Grid Lines -->
'''
    for y in range(0, 45, 10):
        py = pad_top + (max_y - y) / (max_y - min_y) * plot_h
        svg += f'  <line x1="{pad_left}" y1="{py}" x2="{width - pad_right}" y2="{py}" stroke="#e2e8f0" stroke-width="1" />\n'
        svg += f'  <text x="{pad_left - 10}" y="{py + 4}" text-anchor="end" font-size="12" fill="#64748b">{y}</text>\n'

    for x in range(min_x, max_x + 1):
        px = pad_left + (x - min_x) / (max_x - min_x) * plot_w
        svg += f'  <line x1="{px}" y1="{pad_top}" x2="{px}" y2="{height - pad_bot}" stroke="#e2e8f0" stroke-width="1" />\n'
        svg += f'  <text x="{px}" y="{height - pad_bot + 18}" text-anchor="middle" font-size="12" fill="#64748b">{x}</text>\n'

    svg += f'''
  <!-- Axes -->
  <line x1="{pad_left}" y1="{height - pad_bot}" x2="{width - pad_right}" y2="{height - pad_bot}" stroke="#334155" stroke-width="2" />
  <line x1="{pad_left}" y1="{pad_top}" x2="{pad_left}" y2="{height - pad_bot}" stroke="#334155" stroke-width="2" />
  
  <text x="{width/2}" y="{height - 15}" text-anchor="middle" font-size="13" font-weight="600" fill="#334155">Allocated Physical Frames (RAM Capacity)</text>
  <text x="25" y="{height/2}" text-anchor="middle" font-size="13" font-weight="600" fill="#334155" transform="rotate(-90 25 {height/2})">Page Fault Count</text>

  <!-- Curve -->
  <path d="{path_d}" fill="none" stroke="#2563eb" stroke-width="3" />
'''
    for px, py, x, y in points:
        svg += f'  <circle cx="{px:.1f}" cy="{py:.1f}" r="5" fill="#2563eb" stroke="#ffffff" stroke-width="2" />\n'
        svg += f'  <text x="{px:.1f}" y="{py - 10:.1f}" text-anchor="middle" font-size="11" font-weight="bold" fill="#1e40af">{y}</text>\n'

    svg += '''  <!-- Working set callout -->
  <rect x="420" y="80" width="220" height="60" rx="6" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.5" />
  <text x="430" y="102" font-size="12" font-weight="bold" fill="#1e3a8a">Working Set Knee (Frames = 10)</text>
  <text x="430" y="122" font-size="11" fill="#1e40af">Faults drop drastically to 10</text>
</svg>'''

    with open(output_svg, 'w') as f:
        f.write(svg)
    print(f"Generated SVG plot at {output_svg}")

if __name__ == '__main__':
    generate_svg("page_fault_curve.csv", "page_fault_curve.svg")
