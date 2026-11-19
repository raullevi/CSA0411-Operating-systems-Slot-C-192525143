# Task A2: Design the System Administration

**Course:** CSA04 / CSA0411 – Operating Systems (Slot C)  
**Student Name:** Rakul K  
**Register Number:** 192525143  
**Institution:** SIMATS Engineering, Saveetha University  
**Bloom's Taxonomy Level:** K5 – Evaluate  

---

## 1. Task A2.1: Users, Services, and Log Architecture

### Dedicated User Accounts & Groups:
- **`portal` user (System Account):** Dedicated unprivileged user (`uid=1001, gid=1001`) with no shell login (`/usr/sbin/nologin`). Runs the Python Gunicorn web application with read-only access to `/var/www/result-portal`.
- **`postgres` user:** Dedicated database service account isolated from application code.
- **Administrative Group (`devops`):** Sudoer group with multi-factor authentication (MFA) and SSH key-only access.

### Systemd Service Configuration (`result-portal.service`):
```ini
[Unit]
Description=University Result Portal Gunicorn Service
After=network.target postgresql.service

[Service]
Type=notify
User=portal
Group=portal
WorkingDirectory=/var/www/result-portal
ExecStart=/usr/local/bin/gunicorn -w 8 -b 127.0.0.1:8000 app:app
Restart=always
RestartSec=3s
LimitNOFILE=65536
ProtectSystem=full
ProtectHome=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

---

## 2. Task A2.2: Networking, Reverse Proxy, and Security Firewall

```
[Internet: 150,000 Students]
             |
             v (HTTPS Port 443 / HTTP Port 80)
   +--------------------+
   |  UFW / Iptables    | -> Allows ONLY Ports 80, 443, and 22 (SSH VPN)
   +--------------------+
             |
             v
   +--------------------+
   |   Nginx Reverse    | -> SSL Termination, Gzip, Rate Limiting (50 r/s),
   |   Proxy (Frontend) |    Static Assets (/static/)
   +--------------------+
             | (Unix Domain Socket / Localhost HTTP)
             v
   +--------------------+
   |  Gunicorn Python   | -> 8 Worker Processes handling dynamic result queries
   |  (Backend Portal)  |
   +--------------------+
             | (TCP Port 5432)
             v
   +--------------------+
   | PostgreSQL Engine  | -> Connection pool (pgbouncer)
   +--------------------+
```

---

## 3. Task A2.3: System Automation with Cron
Scheduled recurring maintenance cron entries:
```bash
# Automated database backup every midnight
0 0 * * * /usr/local/bin/backup_db.sh >> /var/log/backup.log 2>&1

# Hourly log rotation and web traffic summary
0 * * * * /usr/local/bin/access_log_summary.sh >> /var/log/portal_traffic.log 2>&1

# Disk space alert check every 15 minutes (alert if > 85%)
*/15 * * * * /usr/local/bin/disk_alert.sh
```

---

## 4. Alternative Concept & Complexity Analysis: Ansible vs. Hand-Written Shell Scripts

If the university configured its servers using an automated Infrastructure-as-Code tool (Ansible) rather than custom shell scripts:
- **Configuration Drift Elimination:** Shell scripts are rarely idempotent; re-running them may create duplicate configuration blocks or fail halfway through. Ansible playbooks are declaratively idempotent, ensuring that all 20 result-portal servers maintain identical software versions.
- **Time to Provision 20 Servers:**
  - Hand-written scripts across 20 servers: $20 \times 45\,\text{minutes} = 15\,\text{hours}$.
  - Ansible Playbook execution: $1 \times 5\,\text{minutes} = \mathbf{5\,\text{minutes}}$ across all 20 nodes concurrently via parallel SSH forks.
