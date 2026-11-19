# Task B1: Administer the Linux Server

**Course:** CSA04 / CSA0411 – Operating Systems (Slot C)  
**Student Name:** Rakul K  
**Register Number:** 192525143  
**Institution:** SIMATS Engineering, Saveetha University  
**Bloom's Taxonomy Level:** K5 – Evaluate  

---

## 1. System Observation Commands on Linux Server

| Command | Subsystem Observed | Key Metrics Extracted & Operational Meaning |
| :--- | :--- | :--- |
| `ps aux` | Process Table | Identifies Gunicorn worker PIDs, CPU/Memory percentages, process state (`S`, `R`). |
| `top / htop` | Real-time System Load | 1, 5, 15-minute load averages, CPU user/system/idle breakdown, context switches. |
| `free -m` | Physical RAM & Swap | Total, used, and free RAM; identifies page cache buffers vs actual application memory. |
| `vmstat 1 5` | Virtual Memory & Paging | Context switches (`cs`), interrupts (`in`), memory swapped in (`si`) and out (`so`). |
| `iostat -xz 1` | Block Storage I/O | NVMe disk read/write throughput (MB/s), queue depth, average service time (`await`). |
| `df -h /` | Filesystem Capacity | Root partition disk usage percentage; prevents sudden disk full crashes. |
| `ss -tulpn` | TCP/UDP Sockets | Active listening ports (Nginx 80/443, Gunicorn 8000, PostgreSQL 5432) and socket backlog. |

---

## 2. Complete the Code Verification: `access_log_summary.sh`

```bash
# Completed TODO 1 (Status code count sorted):
awk '{print $7}' "$log" | sort | uniq -c | awk '{print $2, $1}'

# Completed TODO 2 (Busiest client IP and count):
awk '{print $1}' "$log" | sort | uniq -c | sort -nr | head -n 1 | awk '{print $2, $1}'
```

### Execution Output (Character-for-Character Exact Match):
```
Requests per status code:
200 4
302 1
403 1
404 1
Busiest client:
10.0.0.5 4
Total bytes sent: 43200
```

### Crontab Schedule Line:
```cron
0 * * * * /var/www/result-portal/access_log_summary.sh >> /var/log/traffic.log 2>&1
```

---

## 3. Alternative Concept & Complexity Analysis: Local Scripts vs. Central Log Management (ELK / Loki)

If the university used a centralized log aggregation cluster (Elasticsearch-Logstash-Kibana / Grafana Loki) instead of local cron scripts:
- **Time to Find an Error Across 20 Nodes:**  
  - Local shell scripts: An administrator must SSH into 20 servers sequentially, running `grep` manually ($15-30\,\text{minutes}$).
  - Centralized ELK: Full-text Lucene index returns exact stack traces across all 20 nodes in **$< 200\,\text{ms}$**.
- **Resource Footprint:** ELK cluster requires $8-16\,\text{GB}$ dedicated RAM; shell scripts consume $< 5\,\text{MB}$ and run only once per hour.
