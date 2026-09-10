# Test Log

Run with `poetry run python main.py` after starting Ollama and pulling `llama3.2` and `nomic-embed-text`.

The application printed the retrieved passages before each answer. The entries below record the top retrieved chunk and the generated answer from a local run.

## Questions with answers in the documents

### 1. What time do classes run?

- Expected source: `data/school_information.txt` or `data/school_regulations.md`
- Retrieved chunks: `data/school_information.txt` - "Classes run from 8:00 a.m. to 3:15 p.m., Monday through Friday." The other two results were `data/school_regulations.md` attendance and office-hours passages.
- Generated answer: Classes run from 8:00 a.m. to 3:15 p.m., Monday through Friday.

### 2. How many books may a student borrow?

- Expected source: `data/school_information.txt`
- Retrieved chunks: `data/school_information.txt` - "Students may borrow up to five books for three weeks." The other two results were matching passages from `data/school_handbook.pdf`.
- Generated answer: A student may borrow up to five books for three weeks.

### 3. How should a family appeal a significant disciplinary decision?

- Expected source: `data/school_regulations.md`
- Retrieved chunks: `data/school_regulations.md` - "A family may request a review of a significant disciplinary decision in writing within five school days of receiving the decision."
- Generated answer: A family may request a review of a significant disciplinary decision in writing within five school days of receiving the decision.

### 4. What is required to start a student club?

- Expected source: `data/student_life.md`
- Retrieved chunks: `data/student_life.md` - "Students who want to start a club should submit a short proposal, identify a staff sponsor, and collect interest from at least eight students."
- Generated answer: To start a student club, students must submit a short proposal, identify a staff sponsor, and collect interest from at least eight students.

## Question outside the documents

### 5. Who won the 2026 World Cup?

- Expected behavior: The app should say it could not find the answer in the provided documents.
- Retrieved chunks: `data/school_regulations.md`, `data/school_information.txt`, and `data/school_regulations.md`; none contained the answer.
- Generated answer: I could not find this in the provided documents.