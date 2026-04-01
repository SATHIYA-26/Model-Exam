# Set 1 – Use Case, Feasibility Study, and Test Cases

## 1. Problem statement
Design an **Online Event Booking System for Students**. Students can register and log in, search college events, book seats, cancel bookings, and view their booking history. Admins can create, update, and delete events.

## 2. Major use case description
**Primary actor:** Student

**Goal:** Successfully book a seat in an event.

**Preconditions:**
- Student is registered in the system.
- Student has valid credentials.
- At least one event is available for booking.

**Main success scenario:**
1. Student opens the application.
2. Student logs in using username and password.
3. System validates credentials.
4. System displays list of upcoming events.
5. Student selects an event and number of seats.
6. System checks availability.
7. System confirms booking and generates a booking record.
8. System shows confirmation message and updates booking history.

**Alternative flows:**
- Invalid login – system displays error and asks to retry.
- Event full – system shows "No seats available" and does not confirm booking.
- Network/database error – system shows technical error message.

## 3. Use case diagram (text description)
Main actors and use cases:
- **Student**: Register, Login, View Events, Search Events, Book Event, Cancel Booking, View Booking History.
- **Admin**: Login, Add Event, Update Event, Delete Event, View All Bookings.

Relationships:
- Student must **Login** before accessing **Book Event**, **Cancel Booking**, **View Booking History**.
- Admin must **Login** before **Add/Update/Delete Event** and **View All Bookings**.

## 4. Requirement analysis and feasibility study

### 4.1 Functional requirements
- Student registration and authentication.
- Student login/logout.
- Event CRUD (Create/Read/Update/Delete) for admin.
- Event search and filter (by date, category, location).
- Event booking and cancellation for students.
- Booking history for students; all bookings report for admins.

### 4.2 Non‑functional requirements
- Usability: Simple, mobile‑friendly web UI.
- Reliability: Consistent booking logic, proper validation.
- Performance: Support concurrent logins and bookings for a typical college size.
- Security: Password hashing, role‑based access control (student/admin).
- Maintainability: Layered architecture (presentation, business logic, data layer).

### 4.3 Feasibility study

**Technical feasibility**
- Implemented using widely available open‑source stack (e.g., Python + Flask, HTML/CSS/JS, SQLite/MySQL/PostgreSQL).
- Runs on standard hardware (college lab machines or small cloud VM).
- Integrates with Git and CI tools for version control and deployment.

**Operational feasibility**
- Replaces manual / paper‑based event registration.
- Easy for students and staff to learn (login, select event, click book).
- Reduces queues and manual errors in maintaining event registers.

**Economic feasibility**
- No license cost for open‑source stack.
- Minimal hosting cost on shared server or cloud.
- Development cost mainly student effort (project work) and lab resources.

## 5. Test cases – examples (student login and event registration)

### 5.1 Student login test cases

| TC ID | Scenario                          | Input                          | Expected Result                                  |
|------|-----------------------------------|--------------------------------|--------------------------------------------------|
| TC01 | Valid login                       | Valid username & password     | Login success; redirect to student dashboard    |
| TC02 | Invalid password                  | Valid username, wrong password| Error message: "Invalid credentials"            |
| TC03 | Non‑existing user                 | Unknown username              | Error message: "User not found"                 |
| TC04 | Empty username                    | "" and valid password        | Validation error: "Username required"           |
| TC05 | Empty password                    | Valid username, ""           | Validation error: "Password required"           |
| TC06 | SQL injection attempt             | "admin' OR '1'='1"           | Login fails; input safely handled (no injection) |

### 5.2 Event registration test cases

| TC ID | Scenario                             | Input                                      | Expected Result                                                  |
|------|--------------------------------------|--------------------------------------------|------------------------------------------------------------------|
| TC11 | Book available event                 | Logged‑in student, event with free seats   | Booking success; seats reduced; booking record created          |
| TC12 | Book event with 0 available seats    | Logged‑in student, full event              | Error: "No seats available"; booking not created                |
| TC13 | Book with invalid event ID          | Logged‑in student, invalid event ID        | Error: "Event not found"                                       |
| TC14 | Cancel existing booking             | Logged‑in student, valid booking ID        | Booking cancelled; seats increased; history updated             |
| TC15 | Cancel non‑existing booking         | Logged‑in student, invalid booking ID      | Error: "Booking not found"                                     |
| TC16 | Search events by keyword            | Keyword = "Technical"                     | Events list filtered by keyword; no crash if nothing matches    |

These cover the typical flows like **student login** and **event registration**. More test cases can be added for admin CRUD, performance, and security (session timeout, access control, etc.).
