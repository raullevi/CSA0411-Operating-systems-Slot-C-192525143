# Task A5: Design the Cloud Deployment and Orchestration

**Course:** CSA04 / CSA0411 – Operating Systems (Slot C)  
**Student Name:** Rakul K  
**Register Number:** 192525143  
**Institution:** SIMATS Engineering, Saveetha University  
**Bloom's Taxonomy Level:** K5 – Evaluate  

---

## 1. Task A5.1: Cloud Service Models & Architecture for Result Day

| Cloud Service Model | Responsibilities Managed by University | Responsibilities Managed by Cloud Provider | Suitability for University Result Portal |
| :--- | :--- | :--- | :--- |
| **IaaS (Infrastructure as a Service)** | OS, Patches, Web Runtime, Database, Autoscaling. | Physical Servers, Hypervisors, Data Center, Network. | High management effort; risky for sudden traffic surges. |
| **PaaS (Platform as a Service)** | Application Code and Database Schema. | OS, Runtime, Automatic Patching, Scaling Infrastructure. | Good for developers, but higher cost at extreme scale. |
| **Cloud-Native Managed Kubernetes (CaaS)** | Container Image, Kubernetes Manifests, HPA rules. | Kubernetes Control Plane, Worker Node Autoscale, Storage. | **RECOMMENDED & DEFENDED** |

### Cloud Architecture for 150,000 Students on Result Day:
```
[150,000 Concurrent Students]
             |
             v
+-----------------------------+
| Cloud Load Balancer (ALB)   | -> Elastic multi-AZ distribution, WAF rate limiting
+-----------------------------+
             |
             v
+-----------------------------+
| Managed Kubernetes Cluster  | -> Horizontal Pod Autoscaler (HPA) scales from 3
| (Amazon EKS / Google GKE)   |    to 30 replicas based on 70% CPU threshold
+-----------------------------+
             |
             v
+-----------------------------+
| Managed Cloud Database      | -> Amazon Aurora PostgreSQL / Cloud SQL with 
| (Multi-AZ with Read Replica)|    Read Replicas dedicated to student result queries
+-----------------------------+
```

---

## 2. Task A5.2: Kubernetes Primitives for Scalability and Resilience
1. **Pods:** Smallest deployable unit; encapsulates the result-portal container sharing local loopback networking and volumes.
2. **Deployments & Replicas:** Declarative controller managing pod lifecycles. If a pod crashes or a worker node loses power, the deployment controller automatically provisions a replacement pod on an alternate healthy node.
3. **Services (`LoadBalancer` / `ClusterIP`):** Exposes an immutable internal DNS name and stable virtual IP, load-balancing traffic across ephemeral pod IP addresses.
4. **Resource Requests and Limits:**
   - `requests.cpu = 250m, requests.memory = 256Mi`: Guaranteed hardware reservations used by the Kubernetes scheduler.
   - `limits.cpu = 500m, limits.memory = 512Mi`: Hard boundaries enforced via cgroups, preventing a memory leak in one container from exhausting node RAM.
5. **Horizontal Pod Autoscaler (HPA):** Continuously samples metrics via `metrics-server`. When average CPU exceeds $70\%$, HPA automatically scales deployment from 3 pods to 30 pods within seconds.

---

## 3. Alternative Concept & Complexity Analysis: Fixed VMs vs. Elastic Kubernetes

If the university purchased fixed cloud VMs sized for result day traffic:
- **Financial Waste on the Other 364 Days:** Sustaining 30 large cloud VMs year-round costs $> \$45,000/\text{year}$, while the servers sit at $< 2\%$ CPU utilization outside result days.
- **Elastic Kubernetes Economics:** Kubernetes scales down to 2 small pods during normal days and dynamically scales up to 30 pods for only 4 hours on result day, reducing annual cloud compute bills by over **$85\%$**.
