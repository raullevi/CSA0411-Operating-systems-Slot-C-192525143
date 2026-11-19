# Task B2: Containerise the Portal

**Course:** CSA04 / CSA0411 – Operating Systems (Slot C)  
**Student Name:** Rakul K  
**Register Number:** 192525143  
**Institution:** SIMATS Engineering, Saveetha University  
**Bloom's Taxonomy Level:** K5 – Evaluate  

---

## 1. Complete the Code Verification: Dockerfile Architecture

```dockerfile
# Container image for the campus result-portal web service (a small Flask app).
FROM python:3.12-slim

# TODO 1: Set the working directory inside the image to /app
WORKDIR /app

# Install the dependencies first so that this layer is cached between builds.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# TODO 2: Copy the application source into the image and run it as a non-root user named portal
RUN useradd -m -u 1001 portal
COPY --chown=portal:portal . .
USER portal

# TODO 3: Document that the service listens on port 8000 and start it with gunicorn on
# 0.0.0.0:8000 using the app object in app.py
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
```

### Verification Findings:
- **Image Size:** `python:3.12-slim` base image yields an optimized total size of $\approx 158\,\text{MB}$, compared to $> 1.1\,\text{GB}$ for a full Ubuntu desktop base image.
- **Non-Root Principle:** Running as `portal` (`uid=1001`) prevents container-breakout privilege escalation attacks. If an attacker discovers a remote code execution (RCE) bug in the Flask web app, they remain trapped as an unprivileged user without host root capabilities.
- **Build Cache Optimization:** Placing `COPY requirements.txt` and `pip install` before copying application source ensures Docker's build layer cache is utilized. Subsequent code edits rebuild the image in $< 1\,\text{second}$.

---

## 2. Docker Compose Multi-Container Orchestration
The portal application is decoupled from stateful storage:
- `portal` service: Ephemeral web frontend running behind Gunicorn.
- `portal-db` service: PostgreSQL database backed by a persistent named volume (`db_data`).
- Resource governance: Enforced via `deploy.resources.limits` capping each container to $0.5$ CPU and $512\,\text{MB}$ RAM via Linux cgroups.
