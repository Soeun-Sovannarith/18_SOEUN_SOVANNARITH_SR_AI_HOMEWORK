# Test Log

Test execution log using `poetry run python main.py` with local models `llama3.2` and `nomic-embed-text`.

---

## Questions with Answers Inside the Documents

### 1. What time do classes run?
- **Question:** What time do classes run?
- **Expected Source:** `data/school_information.txt` / `data/academic_calendar.md`
- **Retrieved Chunks:**
  1. `data/academic_calendar.md` (distance=0.205) — *"The campus is open from 7:30 a.m. to 4:30 p.m. on regular school days. Classes run from 8:00 a.m. to 3:15 p.m., Monday through Friday."*
  2. `data/school_information.txt` (distance=0.298) — *"SCHOOL HOURS: Classes run from 8:00 a.m. to 3:15 p.m., Monday through Friday."*
  3. `data/school_regulations.md` (distance=0.325) — *"Students must arrive in their assigned classroom before 8:00 a.m."*
- **Generated Answer:** Classes run from 8:00 a.m. to 3:15 p.m., Monday through Friday.

---

### 2. How many books may a student borrow?
- **Question:** How many books may a student borrow?
- **Expected Source:** `data/school_information.txt` / `data/campus_services.md`
- **Retrieved Chunks:**
  1. `data/campus_services.md` (distance=0.237) — *"The library is open Monday through Friday from 7:45 a.m. to 4:00 p.m. Students may borrow up to five books for three weeks."*
  2. `data/school_information.txt` (distance=0.250) — *"LIBRARY AND LEARNING CENTER: Students may borrow up to five books for three weeks."*
  3. `data/school_handbook.pdf` (distance=0.262) — *"Students may borrow up to five books for three weeks. A renewal is allowed when another student has not reserved the item."*
- **Generated Answer:** A student may borrow up to five books for three weeks.

---

### 3. How should a family appeal a significant disciplinary decision?
- **Question:** How should a family appeal a significant disciplinary decision?
- **Expected Source:** `data/school_regulations.md`
- **Retrieved Chunks:**
  1. `data/school_regulations.md` (distance=0.211) — *"A family may request a review of a significant disciplinary decision in writing within five school days of receiving the decision."*
  2. `data/school_regulations.md` (distance=0.344) — *"Disciplinary review requests are submitted to the Head of School's office."*
  3. `data/school_information.txt` (distance=0.385) — *"General School Regulations and Family Communication Procedures."*
- **Generated Answer:** A family may request a review of a significant disciplinary decision in writing within five school days of receiving the decision.

---

### 4. What is required to start a student club?
- **Question:** What is required to start a student club?
- **Expected Source:** `data/student_life.md` / `data/campus_services.md`
- **Retrieved Chunks:**
  1. `data/student_life.md` (distance=0.224) — *"Students who want to start a club should submit a short proposal, identify a staff sponsor, and collect interest from at least eight students."*
  2. `data/campus_services.md` (distance=0.258) — *"Approved clubs may use classrooms after school until 4:15 p.m. on weekdays, subject to room availability."*
  3. `data/school_information.txt` (distance=0.352) — *"The school offers student clubs, community projects, creative arts, and athletics."*
- **Generated Answer:** To start a student club, students must submit a short proposal, identify a staff sponsor, and collect interest from at least eight students.

---

### 5. How much is the annual tuition for Grade 10?
- **Question:** How much is the annual tuition for Grade 10?
- **Expected Source:** `data/tuition_and_fees.md`
- **Retrieved Chunks:**
  1. `data/tuition_and_fees.md` (distance=0.269) — *"Junior High (Grades 9–10): $16,800 per academic year ($8,400 per semester)."*
  2. `data/tuition_and_fees.md` (distance=0.305) — *"Tuition invoices are issued by the Finance Office 30 days before each payment deadline."*
  3. `data/tuition_and_fees.md` (distance=0.316) — *"Annual Tuition by Grade Level: Middle School $14,500, Junior High $16,800, Senior High $18,500."*
- **Generated Answer:** The annual tuition for Grade 10 is $16,800 (or $8,400 per semester).

---

## Question Outside the Documents

### 6. Who won the 2026 World Cup?
- **Question:** Who won the 2026 World Cup?
- **Expected Behavior:** Model should state that it cannot find the answer in the provided documents and suppress references.
- **Retrieved Chunks:**
  1. `data/school_regulations.md` (distance=0.485) — *"Code of conduct on campus and during extracurricular events."*
  2. `data/student_life.md` (distance=0.492) — *"Athletic schedules and inter-school competitions."*
  3. `data/academic_calendar.md` (distance=0.510) — *"School athletic sports day and holiday schedules."*
- **Generated Answer:** I could not find this in the provided documents.
- **References:** Suppressed (no references displayed for ungrounded/fallback queries).