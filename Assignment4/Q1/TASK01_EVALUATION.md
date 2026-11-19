# Task 1: File-System Design Review

**Course:** CSA04 / CSA0411 – Operating Systems (Slot C)  
**Student Name:** Rakul K  
**Register Number:** 192525143  
**Institution:** SIMATS Engineering, Saveetha University  
**Bloom's Taxonomy Level:** K5 – Evaluate  

---

## 1. Task 1.1: Evaluation of the Proposed File Organisation (Weaknesses Analysis)

A college proposes storing files for 12,000 students on a single shared server using:
- One single flat directory
- Files named only by the student's choice
- Contiguous allocation for every file
- No access control ("students will not look at each other's files")

### Five Critical Weaknesses Identified:
1. **Catastrophic Namespace Collisions:** In a flat directory, filename uniqueness is mandatory. When hundreds of students submit files named `assignment1.c`, `project.pdf`, or `lab.docx`, successive writes overwrite existing students' submissions without warning.
2. **Pathological Linear Directory Search Latency ($O(N)$):** With 12,000 students holding an average of 50 files each ($600,000$ files total), opening a file requires linearly scanning through over 600,000 directory entry records on disk, causing directory lookup times to exceed several seconds per operation.
3. **Severe External Fragmentation & Inability to Grow Files:** Contiguous allocation requires that the entire file occupy consecutive physical disk blocks. As students continuously append code or dataset records, the file cannot expand if adjacent blocks are occupied, requiring massive disk defragmentation and reallocation.
4. **Complete Absence of Security & Privacy (FERPA / Regulatory Violation):** Relying on an "honor system" violates confidentiality regulations. Any student can inspect, plagiarize, alter, or maliciously `unlink()` peer examination submissions and faculty answer keys.
5. **Impractical Backup & Granular Disaster Recovery:** A single flat namespace prevents incremental per-department or per-student backups. An accidental file corruption risks directory table invalidation for the entire university.

---

## 2. Task 1.2: Improved File-System Organisation Design

```
/ (Root)
└── home/
    └── students/
        └── cse/
            ├── 2025/
            └── 2026/
                ├── 192525143/ (Rakul K) [rwxr-x--- : 750]
                │   ├── assignments/
                │   ├── labs/
                │   └── group_project -> /shared/groups/os_project_slot_c/
                └── 192525144/
```

### Key Architectural Enhancements:
- **Hierarchical Tree Directory Structure:** Partitioned by Department $\to$ Academic Year $\to$ Student Register Number. Directory lookup complexity drops from $O(N)$ to $O(\log N)$ using B-tree indexed directory entries (e.g., ext4 `dir_index` / XFS).
- **Access Control Lists (ACLs) & POSIX Permissions:**
  - Student home directories: `chmod 750` (`rwxr-x---`) owned by `student:student_group`.
  - Faculty grading accounts belong to an administrative group with read access via POSIX ACLs (`setfacl -m g:faculty:rx`).
- **Acyclic Graph Directory Links for Group Work:**
  - Shared directories created in `/shared/groups/<project_id>` with SGID bit set (`chmod 2770`) so newly created files automatically inherit project group permissions.
  - Symbolic links (`ln -s`) allow students to access project repositories directly from their private home directories.

---

## 3. Task 1.3: Design Defence (Within 100 Words)

> **Design Defence:**  
> The hierarchical tree directory isolates student namespaces, preventing collisions and reducing search latency to $O(\log N)$. Strict POSIX permissions (`750`) and discretionary ACLs enforce mandatory confidentiality, ensuring students cannot inspect or modify peer files. Collaboration is enabled cleanly via SGID group project repositories linked into individual home directories using symbolic links. This dual structure guarantees privacy, supports dynamic file growth through indexed extent allocation, and enables automated, granular per-department backup snapshots without compromising multi-user collaborative workflows.

---

## 4. Alternative Concept & Complexity Analysis: Cloud Storage (Google Drive / OneDrive)

If the college adopted cloud storage (e.g., Google Workspace / Microsoft OneDrive) instead of an on-premise shared server:
- **Search & Retrieval Complexity:** Cloud object search relies on serverless inverted metadata indexes ($O(1)$ lookup time), and file opening involves HTTPS REST APIs rather than local VFS POSIX inodes.
- **Storage Redundancy & Cost:** Cloud services introduce file duplication when students copy shared assets locally, whereas on-premise symbolic links consume zero additional data blocks ($O(1)$ space).
- **Data Sovereignty & Governance:** Cloud providers hold encryption keys unless customer-managed keys (CMEK) are provisioned. On-premise storage retains full institutional data governance, audit logging, and compliance control.
