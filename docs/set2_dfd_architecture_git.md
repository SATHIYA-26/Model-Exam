# Set 2 – DFDs, Architecture Design, and Git/GitLab Workflow

## 1. Scenario recap
System: **Online Event Booking System for Students**.

Main scenario: Student logs in, searches events, books/cancels bookings. Admin manages event data.

---

## 2. Level 0 DFD (Context Diagram)

**External entities:**
- Student
- Admin

**Single process:**
- Process 0: Event Booking System

**Data stores:**
- D1: User Database
- D2: Event & Booking Database

**Data flows:**
- Student ↔ Event Booking System: Login details, event search, booking/cancellation requests, booking confirmations.
- Admin ↔ Event Booking System: Event details (create/update/delete), view booking reports.
- Event Booking System ↔ D1: Read/write user records.
- Event Booking System ↔ D2: Read/write event and booking records.

---

## 3. Level 1 DFD (Major processes)

Processes under Event Booking System:
1. **P1 – User Management** (Register, Login, Logout)
2. **P2 – Event Management** (Add/Update/Delete Events – admin)
3. **P3 – Booking Management** (Book/Cancel/View Bookings – student)
4. **P4 – Search & Reporting** (search events, generate reports)

Data stores:
- D1: User DB (student/admin credentials, profiles)
- D2: Event DB (event details)
- D3: Booking DB (student bookings)

Examples of flows:
- Student → P1: Login details → P1 validates against D1 → Student: Login success/failure.
- Admin → P2: Event details → P2 writes to D2 → Admin: Confirmation.
- Student → P3: Booking request → P3 checks D2 for availability, writes booking into D3 → Student: Confirmation.
- Student/Admin → P4: Search/report request → P4 reads from D2/D3 → Result back to actor.

---

## 4. Level 2 DFD (Drilling into Booking Management – P3)

Decompose **P3 – Booking Management** into:
- **P3.1 – Validate Session** (ensure user logged in as student)
- **P3.2 – Check Availability** (read event seats from D2)
- **P3.3 – Create Booking** (write booking entry into D3)
- **P3.4 – Update Seats** (decrement/increment available seats in D2)
- **P3.5 – Manage Booking History** (fetch booking records from D3)

Flows (example: Book Event):
1. Student → P3.1: Booking request.
2. P3.1 → D1: Read session/user data; if invalid, error to Student.
3. P3.1 → P3.2: Validated booking request.
4. P3.2 → D2: Read event seats.
5. P3.2 → P3.3: Availability OK / not OK.
6. P3.3 → D3: Insert booking.
7. P3.3 → P3.4: Trigger seat update.
8. P3.4 → D2: Update event seats.
9. P3.3 → Student: Booking confirmation.

Flows (example: Cancel Booking) similarly involve P3.1, P3.5, P3.4 and D3/D2.

---

## 5. Converting DFD to Architecture Design

We adopt a **3‑layer architecture**:
1. **Presentation layer (UI/Web layer)**
   - Login page, student dashboard, admin dashboard.
   - Pages: Login, Register, Event List, Event Details, Booking History, Admin Event Management.

2. **Business Logic layer (Service layer)**
   - Implements use cases: authenticate user, search events, book/cancel, manage events.
   - Validates inputs, enforces rules (e.g., cannot book more seats than available).

3. **Data Access layer (Repository/DAO layer)**
   - Interacts with the database (User, Event, Booking tables).
   - Exposes methods like `get_user_by_username`, `get_events`, `add_event`, `save_booking`, `update_seats`, `delete_event`.

### Mapping from DFD to layers
- **P1 User Management** → Auth service in Business Logic Layer + User repository in Data Layer.
- **P2 Event Management** → Event service + Event repository.
- **P3 Booking Management** → Booking service + Booking repository + Event repository.
- **P4 Search & Reporting** → Search/report service + appropriate repositories.

---

## 6. Example: Login page and customer login + service selection

**Login Page (presentation layer):**
- Fields: Username, Password, Role (Student/Admin – optional).
- Actions: Login button, Register link.

Flow:
1. User enters username/password and clicks Login.
2. UI sends POST `/login` to backend.
3. Business logic validates credentials via User repository.
4. On success, session created; user redirected to appropriate dashboard.

**Service selection:**
- After login, student dashboard lets user select services:
  - View/Search Events.
  - Book Event.
  - Cancel Booking.
  - View Booking History.

Each action calls appropriate business services which interact with the Data Layer, ensuring **smooth transactions and accurate updates**.

---

## 7. Git / GitLab (or GitHub) workflow and CI/CD

### 7.1 Git version control during system development and deployment

- Initialize repository: `git init`.
- Create main branches:
  - `main` (production‑ready code)
  - `develop` (integration branch for features)
- Feature branches:
  - Create a branch for each task, e.g., `feature/login`, `feature/booking`.
  - Workflow:
    1. `git checkout -b feature/login`
    2. Implement code, run local tests.
    3. `git add .` and `git commit -m "Implement login feature"`.
    4. `git push` and open Merge Request (GitLab) or Pull Request (GitHub) into `develop` or `main`.

This ensures: traceability, easy rollback, and isolation of features.

### 7.2 Handling merge conflicts

- When two branches modify the same lines, merging may fail.
- Developer resolves conflicts locally using an editor, tests the result, and commits the merged version.
- CI pipeline then runs on the merged code to ensure nothing is broken.

### 7.3 Sample GitLab CI pipeline (.gitlab-ci.yml)

```yaml
stages:
  - test

python-tests:
  image: python:3.11
  stage: test
  before_script:
    - pip install -r requirements.txt
  script:
    - python -m compileall app
```

- This pipeline installs dependencies and checks that the Python code in `app/` compiles.
- If a developer pushes code with syntax errors, the **pipeline fails**, signalling a problem before deployment.

### 7.4 Smooth transaction and accurate updates

- Atomic operations at the database layer (transactions) ensure that seat counts and bookings update together.
- Version control + CI/CD ensures that only tested, reviewed code reaches production.
- Branching and merging strategies prevent accidental overwrites of working code.

---

## 8. CRUD operations: Search, Add, Delete

- **Search**: UI sends query to Search service → service calls Event repository → returns filtered list.
- **Add** (Admin): Admin form → Event service validates input → Event repository inserts row into Event table.
- **Delete** (Admin): Admin chooses event → Event service checks constraints (e.g., existing bookings) → Event repository deletes or marks inactive.

These operations are implemented in the **Business Logic layer** using the **Data Access layer** for actual database calls, keeping responsibilities cleanly separated.
