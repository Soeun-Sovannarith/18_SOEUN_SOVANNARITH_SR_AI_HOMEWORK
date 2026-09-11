# Test Execution Log

Interactive CLI testing log with local models (`llama3.2` and `nomic-embed-text`).

---

### Startup & Indexing

```bash
(18-soeun-sovannarith-sr-ai-homework-py3.12) sovannarith@Sovannariths-Mac-mini 18_SOEUN_SOVANNARITH_SR_AI_HOMEWORK_ % python3 main.py 
Indexed 7 documents into 126 chunks.
Ask a question about the documents. Type 'exit' to quit.
```

---

### Question 1: Student Life & Activities (Relevant)

```bash
You: what's life like of student there ?

--- Retrieved Chunks ---
[1] Source: data/student_life.md (distance=0.411)
Greenfield International School offers student clubs, community projects, creative arts, and athletics alongside the academic program. Club schedules are published by the student services office at the beginning of each semester.

[2] Source: data/school_handbook.pdf (distance=0.446)
hool is closed on weekends and public holidays unless a scheduled event is
 announced.                                                                     
                                                                                
ACADEMIC PROGRAM                                                                
All students take English, mathematics, science, social studies, physical educat
ion, digital literacy, and a second language. Students in Grades 10-12 choose el
ectives such as computer science, visual arts, economics, environmental studies,
 music, and design technology.                                                  
                                                                                
The academic year has two semesters:

[3] Source: data/school_information.txt (distance=0.454)
SCHOOL HOURS
The campus is open from 7:30 a.m. to 4:30 p.m. on regular school days.
Classes run from 8:00 a.m. to 3:15 p.m., Monday through Friday.
The reception office is open from 7:45 a.m. to 4:00 p.m.
The school is closed on weekends and public holidays unless a scheduled event is announced.

----------------------------------------

Assistant: Students at Greenfield International School participate in various activities such as clubs, community projects, creative arts, and athletics alongside their academic program. They have access to a range of subjects including English, mathematics, science, social studies, physical education, digital literacy, and a second language. Students in Grades 10-12 can also choose electives like computer science, visual arts, economics, environmental studies, music, and design technology.

References:
1. data/student_life.md (distance=0.411)
2. data/school_handbook.pdf (distance=0.446)
3. data/school_information.txt (distance=0.454)
```

---

### Question 2: Sibling Discount Policy (Relevant)

```bash
You: if I have 2 child, do i still pay full price ?

--- Retrieved Chunks ---
[1] Source: data/tuition_and_fees.md (distance=0.436)
- **Sibling Discount:**
  - Second enrolled child: 10% discount on annual tuition.
  - Third and subsequent enrolled children: 15% discount on annual tuition.
  - Sibling discounts apply to the younger child's tuition rate.

[2] Source: data/tuition_and_fees.md (distance=0.441)
Families can choose one of three payment plans:

[3] Source: data/tuition_and_fees.md (distance=0.472)
2. **Semester Plan (Two Installments):**
   - Semester 1 Payment: Due 15 August 2026 (50% of annual tuition)
   - Semester 2 Payment: Due 15 January 2027 (50% of annual tuition)

----------------------------------------

Assistant: No, you would be eligible for a 10% discount on your annual tuition due to the sibling discount.

References:
1. data/tuition_and_fees.md (distance=0.436)
2. data/tuition_and_fees.md (distance=0.441)
3. data/tuition_and_fees.md (distance=0.472)
```

---

### Question 3: Tuition Fees (Relevant)

```bash
You: how much for the tuition fee ?

--- Retrieved Chunks ---
[1] Source: data/tuition_and_fees.md (distance=0.336)
- **Technology and Lab Fee:** $450 per academic year (covers high-speed campus Wi-Fi, software licenses, IT helpdesk, and science laboratory supplies).
- **School Uniform Set:** Approximately $220 for the standard starter kit (2 formal uniforms, 2 daily shirts, and 1 physical education kit).
- **School Bus Transportation (Optional):**
  - Zone 1 (within 5 km): $850 per semester ($1,700 per academic year)
  - Zone 2 (5 km to 15 km): $1,200 per semester ($2,400 per academic year)
  - Zone 3 (over 15 km): $1,500 per semester ($3,000 per academic year)
- **Cafeteria Meal Plan (Optional):**
  - Full Lunch Plan: $650 per semester
  - Breakfast and Lunch Combo Plan: $900 per semester
  - Individual meals may also be purchased daily via the student campus card.
- **Advanced Examination and AP/IB

[2] Source: data/tuition_and_fees.md (distance=0.362)
- **Application Fee:** $150 (one-time, non-refundable, due upon submission of admission application)
- **New Student Registration and Enrollment Fee:** $1,000 (one-time fee for newly admitted students to secure enrollment placement)
- **Re-enrollment Deposit for Returning Students:** $500 (annual deposit due by 15 April, credited toward Semester 1 tuition)

[3] Source: data/tuition_and_fees.md (distance=0.377)
- **Middle School (Grades 7–8):** $14,500 per academic year ($7,250 per semester)
- **Junior High (Grades 9–10):** $16,800 per academic year ($8,400 per semester)
- **Senior High (Grades 11–12):** $18,500 per academic year ($9,250 per semester)

----------------------------------------

Assistant: Here are the tuition fees:

* Middle School (Grades 7–8): $14,500 per academic year ($7,250 per semester)
* Junior High (Grades 9–10): $16,800 per academic year ($8,400 per semester)
* Senior High (Grades 11–12): $18,500 per academic year ($9,250 per semester)

References:
1. data/tuition_and_fees.md (distance=0.336)
2. data/tuition_and_fees.md (distance=0.362)
3. data/tuition_and_fees.md (distance=0.377)
```

---

### Question 4: Richest man (Irrelevant / Out-of-Domain Fallback)

```bash
You: who is the richest man ? 

--- Retrieved Chunks ---
[1] Source: data/school_information.txt (distance=0.523)
GREENFIELD INTERNATIONAL SCHOOL
General School Information

[2] Source: data/school_regulations.md (distance=0.527)
## 1. Purpose

[3] Source: data/school_regulations.md (distance=0.532)
# Greenfield International School

----------------------------------------

Assistant: I could not find this in the provided documents.
```

---

### Question 5: OpenAI Founder (Irrelevant / Out-of-Domain Fallback)

```bash
You: who is the founder of OpenAI

--- Retrieved Chunks ---
[1] Source: data/school_regulations.md (distance=0.324)
## 1. Purpose

[2] Source: data/campus_services.md (distance=0.325)
## Cafeteria

[3] Source: data/school_regulations.md (distance=0.359)
# Greenfield International School

----------------------------------------

Assistant: I could not find this in the provided documents.
```

---

### Question 6: Hacking NASA (Irrelevant / Out-of-Domain Fallback)

```bash
You:  how to hack NASA with html

--- Retrieved Chunks ---
[1] Source: data/campus_services.md (distance=0.360)
## Cafeteria

[2] Source: data/school_regulations.md (distance=0.395)
# Greenfield International School

[3] Source: data/school_regulations.md (distance=0.409)
## 1. Purpose

----------------------------------------

Assistant: I could not find this in the provided documents.
```

---