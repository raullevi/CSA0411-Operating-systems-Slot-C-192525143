# Task 12: Day-4 Design Challenge - Re-evaluate and Adapt the Design

**Course:** CSA0411 / CSA04 - Operating Systems (Slot C)  
**Student Name:** Rakul K  
**Register Number:** 192525143  
**Institution:** SIMATS Engineering, Saveetha University  
**Bloom's Taxonomy Level:** K5 – Evaluate  

---

## 1. Changed Requirements
The hospital expands its operational scope:
1. **Remote Patient Monitoring at Home:** Thousands of discharged cardiac and post-operative patients use cellular/Wi-Fi connected wearable devices at home, transmitting real-time biometrics over the public internet.
2. **Cloud-Based Patient Records:** Moving central electronic health records from an on-premise server room to a multi-region public cloud provider (AWS / Google Cloud) shared across 3 healthcare hospital groups.

---

## 2. Part A: Impact Analysis (2 Marks)
- **Operating System Types Affected:**
  - *Home Devices:* Home internet lacks deterministic latency guarantees; consumer broadband experiences packet jitter and disconnects. Requires an **Embedded Real-Time OS with Store-and-Forward Local Flash Buffering** (e.g., FreeRTOS or Zephyr RTOS on ARM Cortex-M).
  - *Cloud Records:* Shifts from physical cluster OS to **Cloud-Native Containerized Orchestration (Kubernetes / EKS)** running distributed cloud database instances (Amazon Aurora PostgreSQL / Google Cloud Spanner).
- **Protection & Security Affected:**
  - Transmission over the public internet introduces severe vulnerabilities (Man-in-the-Middle, eavesdropping, DDoS).
  - Mandatory deployment of **Hardware Cryptographic Secure Elements (TPM 2.0 / ARM TrustZone)** on home monitors with mutual TLS 1.3 (mTLS) certificate pinning.

---

## 3. Part B: Evaluation of the Original Design (2 Marks)
- **Response Time:** Home patient alarms cannot guarantee $< 10\,\text{ms}$ cloud round-trip times due to internet transit latencies ($30-80\,\text{ms}$).  
  *Evaluation:* Local home monitors must execute onboard edge anomaly detection to trigger local audible sirens within $\le 10\,\text{ms}$, while simultaneously transmitting telemetry alerts to the cloud hospital dashboard.
- **Reliability:** An on-premise physical database server fails to support elastic scaling when 150,000 patients and clinics query records simultaneously. Cloud multi-region replication eliminates single data center vulnerability.
- **Security:** Moving to the cloud requires strict compliance with HIPAA and ISO 27001 data residency regulations, demanding envelope encryption with customer-managed KMS keys.

---

## 4. Part C: Adaptation & Redesigned Architecture (2 Marks)
The architecture is **MODIFIED into a Hybrid Edge-Cloud Distributed Infrastructure**:
1. **Edge Tier (Patient Homes):** Wearable devices running Zephyr RTOS with localized machine-learning arrhythmia detection. Local alarms sound instantly ($< 5\,\text{ms}$).
2. **Gateway Tier (Zero Trust Ingestion):** Scalable AWS API Gateway / Cloudflare Edge ingesting encrypted MQTT/HTTPS biometric packets.
3. **Cloud Core Tier (Multi-Region Cloud):** Managed Kubernetes (EKS) hosting microservices with multi-region Aurora PostgreSQL delivering $99.999\%$ global availability and sub-second cross-hospital record sharing.

---

## 5. Part D: Evidence-Based Defense (2 Marks)
> **Final Defense:** The hybrid edge-cloud adaptation preserves life-safety deterministic response at the patient bedside while unlocking infinite elastic scale and cross-hospital federation in the cloud.
- Edge intelligence guarantees zero patient harm during residential internet blackouts.
- Cloud distribution achieves automated disaster recovery failover across geographically separated data centers in $< 5 \text{ seconds}$.
