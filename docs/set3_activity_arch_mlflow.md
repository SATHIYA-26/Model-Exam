# Set 3 – Activity Diagram, 3‑Layer Architecture, and MLflow

## 1. Activity diagram – Event booking workflow (text description)

Main activities for **student event booking**:
1. Start.
2. Open application.
3. Login with username/password.
4. System validates credentials.
5. If invalid → show error → back to login.
6. If valid → show student dashboard.
7. Student searches or browses events.
8. Student selects event and seats.
9. System checks seat availability.
10. If no seats → show "No seats available" → back to event list.
11. If seats available → create booking and update seats.
12. Show confirmation and update booking history.
13. End.

This can be drawn in UML as an activity diagram with decisions on login success and seat availability.

---

## 2. Suitable system architecture – Presentation, Business Logic, Data layers

We use a classic **3‑layer architecture**:

1. **Presentation Layer (Web UI/API)**
   - Technologies: HTML/CSS/JavaScript + Flask templates or REST API endpoints.
   - Responsibilities:
     - Display login page, event list, booking forms.
     - Collect user input and send to backend.
     - Show success/error messages.

2. **Business Logic Layer (Services)**
   - Technologies: Python service classes/modules.
   - Responsibilities:
     - Implement use cases (login, search, booking, cancellation).
     - Validate inputs and enforce rules.
     - Coordinate calls between UI and Data Layer.

3. **Data Layer (Repositories/Database)**
   - Technologies: SQLite/MySQL/PostgreSQL; repository classes.
   - Responsibilities:
     - CRUD operations for User, Event, Booking tables.
     - Hide database details from business logic.

**Booking flow across layers:**
- UI posts booking request → BookingService (Business layer) validates and checks availability via repositories → updates Booking and Event tables (Data layer) → returns result to UI.

---

## 3. Booking scenario – step‑by‑step demonstration

1. Student logs in and reaches dashboard.
2. Student clicks "View Events" → system shows available events.
3. Student filters by date/category or keyword.
4. Student selects one event and number of seats.
5. System checks if seats are available.
6. If available, system creates booking record and decreases seats.
7. System shows confirmation with booking ID.
8. Student can later view or cancel booking from history page.

---

## 4. Using MLflow to manage development of the scenario

Even though this is primarily a transaction system, we can use **MLflow** to manage and track experiments related to the system, for example:
- Building a model to **recommend events** to students.
- Analysing **booking conversion rate** for different UI designs.

### 4.1 What MLflow provides
- **Experiment tracking**: log parameters, metrics, artifacts, and models.
- **Model registry**: register versions of models.
- **UI**: visualize experiment runs and compare them.

### 4.2 Example of tracking module logs and metrics

In code (Python), we can:
- Log which module or feature is under test.
- Log metrics like number of successful bookings, failed bookings, or model accuracy.

A simple example (we will include a `mlflow_demo.py` script in the project):
- Start MLflow run.
- Log parameter: `scenario = "event_booking"`.
- Log metrics: `successful_bookings`, `failed_bookings`, `conversion_rate`.
- Optionally log artifacts like CSV logs or charts.

### 4.3 Benefits
- Clear history of how the system and any ML components evolved.
- Ability to compare different versions (e.g., algorithm A vs B for event recommendations).
- Traceability: which code version and configuration produced which results.

MLflow complements Git: Git tracks **code versions**, while MLflow tracks **experiment runs and metrics**.
