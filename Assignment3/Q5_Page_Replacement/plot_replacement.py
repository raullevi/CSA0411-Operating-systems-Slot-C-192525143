#!/usr/bin/env python3
import csv

def generate_svg(csv_path, output_svg):
    frames = []
    fifo_loc = []
    lru_loc = []
    clock_loc = []
    opt_loc = []

    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            frames.append(int(row['frames']))
            fifo_loc.append(int(row['fifo_loc']))
            lru_loc.append(int(row['lru_loc']))
            clock_loc.append(int(row['clock_loc']))
            opt_loc.append(int(row['opt_loc']))

    width, height = 750, 460
    pad_left, pad_right, pad_top, pad_bot = 80, 50, 60, 60
    plot_w = width - pad_left - pad_right
    plot_h = height - pad_top - pad_bot

    max_x, min_x = max(frames), min(frames)
    max_y, min_y = 700, 0

    def to_coords(data):
        pts = []
        for x, y in zip(frames, data):
            px = pad_left + (x - min_x) / (max_x - min_x) * plot_w
            py = pad_top + (max_y - y) / (max_y - min_y) * plot_h
            pts.append((px, py, x, y))
        return pts

    pts_fifo = to_coords(fifo_loc)
    pts_lru = to_coords(lru_loc)
    pts_clock = to_coords(clock_loc)
    pts_opt = to_coords(opt_loc)

    def to_path(pts):
        return "M " + " L ".join(f"{px:.1f},{py:.1f}" for px, py, _, _ in pts)

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" style="background:#ffffff; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;">
  <rect width="{width}" height="{height}" fill="#f8fafc" rx="8" />
  <text x="{width/2}" y="32" text-anchor="middle" font-size="16" font-weight="bold" fill="#0f172a">Web Server Page Replacement: Faults vs Frame Count (1,000 References)</text>
  
  <!-- Legend -->
  <g transform="translate(180, 45)">
    <circle cx="0" cy="0" r="5" fill="#ef4444" />
    <text x="10" y="4" font-size="12" fill="#334155" font-weight="600">FIFO</text>
    <circle cx="90" cy="0" r="5" fill="#3b82f6" />
    <text x="100" y="4" font-size="12" fill="#334155" font-weight="600">LRU</text>
    <circle cx="180" cy="0" r="5" fill="#10b981" />
    <text x="190" y="4" font-size="12" fill="#334155" font-weight="600">Clock</text>
    <circle cx="280" cy="0" r="5" fill="#8b5cf6" />
    <text x="290" y="4" font-size="12" fill="#334155" font-weight="600">Optimal (MIN)</text>
  </g>

  <!-- Y Grid -->
'''
    for y in range(0, 750, 100):
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
  
  <text x="{width/2}" y="{height - 15}" text-anchor="middle" font-size="13" font-weight="600" fill="#334155">Allocated Frames</text>
  <text x="25" y="{height/2}" text-anchor="middle" font-size="13" font-weight="600" fill="#334155" transform="rotate(-90 25 {height/2})">Page Faults</text>

  <!-- Paths -->
  <path d="{to_path(pts_fifo)}" fill="none" stroke="#ef4444" stroke-width="2.5" />
  <path d="{to_path(pts_lru)}" fill="none" stroke="#3b82f6" stroke-width="2.5" />
  <path d="{to_path(pts_clock)}" fill="none" stroke="#10b981" stroke-width="2.5" stroke-dasharray="4" />
  <path d="{to_path(pts_opt)}" fill="none" stroke="#8b5cf6" stroke-width="2.5" />
'''
    for pts, col in [(pts_fifo, "#ef4444"), (pts_lru, "#3b82f6"), (pts_clock, "#10b981"), (pts_opt, "#8b5cf6")]:
        for px, py, _, _ in pts:
            svg += f'  <circle cx="{px:.1f}" cy="{py:.1f}" r="4" fill="{col}" stroke="#ffffff" stroke-width="1.5" />\n'

    svg += '</svg>'

    with open(output_svg, 'w') as f:
        f.write(svg)
    print(f"Generated page replacement SVG at {output_svg}")

if __name__ == '__main__':
    generate_svg("page_replacement_workload.csv", "page_replacement_workload.svg")
