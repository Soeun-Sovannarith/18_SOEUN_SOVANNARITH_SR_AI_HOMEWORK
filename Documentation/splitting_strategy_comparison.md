# Text Splitting Strategy Comparison

Comparison of two different text splitting strategies implemented and evaluated on the same 7 school policy documents (`.txt`, `.md`, `.pdf`) in the `data/` directory.

---

## 1. Strategies Overview

### **Strategy 1: Paragraph-Aware Chunking (Active in Pipeline)**
- **How it works:** 
  1. Splits text on natural double-newline paragraph boundaries (`\n\n`).
  2. For paragraphs exceeding `800` characters, it slides a window forward breaking at the nearest whitespace (`" "`) with a `120`-character overlap.
- **Parameters:** `chunk_size = 800`, `overlap = 120`.
- **Goal:** Preserve semantic completeness of paragraphs, lists, and policy rules.

### **Strategy 2: Fixed-Size Window Chunking (Baseline Comparison)**
- **How it works:**
  1. Sweeps across the entire document text in fixed character windows.
  2. Breaks at the nearest whitespace before the 500-character limit, applying a `100`-character sliding overlap between consecutive chunks.
- **Parameters:** `chunk_size = 500`, `overlap = 100`.
- **Goal:** Produce consistent, predictable chunk lengths across all documents.

---

## 2. Quantitative Metrics Comparison

Run script: `poetry run python compare_chunking.py`

| Metric | Strategy 1: Paragraph-Aware | Strategy 2: Fixed-Window |
| :--- | :--- | :--- |
| **Total Chunks Created** | **126** | **68** |
| **Average Chunk Length** | **210.2 characters** | **460.2 characters** |
| **Minimum Chunk Length** | **12 characters** (short headings) | **134 characters** (tail end of docs) |
| **Maximum Chunk Length** | **799 characters** | **499 characters** |

---

## 3. Qualitative Sample Comparison (`data/school_regulations.md`)

### **Strategy 1 Output (Paragraph-Aware):**
```text
[Chunk 1] (33 chars):
# Greenfield International School

[Chunk 2] (42 chars):
## Student Regulations and Code of Conduct
```
* **Observation:** Natural paragraph boundaries are strictly respected. However, standalone Markdown headings produce very short chunks if not merged with the body text.

### **Strategy 2 Output (Fixed-Window):**
```text
[Chunk 1] (499 chars):
# Greenfield International School

## Student Regulations and Code of Conduct

**Document type:** Fictional school policy for RAG testing  
**Effective date:** 1 September 2026  
**Review cycle:** Annually  
**Applies to:** Students, visitors, and school-sponsored activities

> This is sample content created for a school RAG application. It is not an official regulation of a real school.

## 1. Purpose

These regulations create a safe, respectful, inclusive, and productive learning environment.

[Chunk 2] (497 chars):
urpose

These regulations create a safe, respectful, inclusive, and productive learning environment. Students are expected to follow the rules on campus, during online learning, on school transportation, and at school-sponsored events.

## 2. Attendance and punctuality

- Students should arrive at school by 7:45 a.m. and report to homeroom by 7:55 a.m.
- The school day runs from 8:00 a.m. to 3:15 p.m., Monday through Friday.
- Parents or guardians must notify the attendance office before 9:00
```
* **Observation:** Chunks are fuller and uniform in size, but sentences and words can be sliced awkwardly at window borders (e.g., `"urpose"` in Chunk 2).

---

## 4. Key Trade-Offs & Conclusion

| Aspect | Paragraph-Aware Chunking | Fixed-Window Chunking |
| :--- | :--- | :--- |
| **Context Integrity** | **High** — Rules and bullet points stay intact. | **Low / Moderate** — Ideas can be cut mid-sentence across chunks. |
| **Chunk Size Uniformity**| **Low** — Varies from short headings to 800-char paragraphs. | **High** — Nearly all chunks are ~450–500 chars. |
| **Overlap Utility** | Only used for unusually long paragraphs. | Consistently applied across all window transitions. |
| **Pipeline Decision** | **Selected for main RAG pipeline** because policy documents are heavily paragraph- and bullet-structured. | Kept as comparison baseline. |
