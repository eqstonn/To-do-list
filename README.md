# Task Management Service

A web application designed for task tracking with persistent data storage and a decoupled backend architecture.

## Tech Stack

* **Backend:** Python, FastAPI
* **Database:** PostgreSQL with SQLAlchemy ORM
* **Frontend:** Vanilla HTML, CSS, and JavaScript

## Status: Functional Base

* [x] Basic CRUD functionality (Add/Delete/Update tasks)
* [x] Database integration using SQLAlchemy
* [x] Server-side search filtering via query parameters
* [x] Backend-calculated task statistics and progress tracking
* [ ] Multi-list support (Work/Personal categorization)



## API Endpoints

| Method | Endpoint | Function |
| :--- | :--- | :--- |
| GET | `/tasks` | Retrieves all task records from the database. |
| POST | `/task` | Creates a new task entry in the PostgreSQL table. |
| GET | `/tasks/search` | Filters tasks based on a title string parameter. |
| GET | `/tasks/stats` | Returns calculated totals and completion percentages. |
| PUT | `/task/{id}` | Modifies the completion status of a specific record. |
| DELETE | `/task/{id}` | Removes a specific record from the database. |

## Implementation Details

### Data Aggregation
The application calculates task statistics on the backend rather than the client. The `/tasks/stats` endpoint queries the database for total and completed counts to return a progress percentage. This approach ensures data consistency and reduces client-side processing requirements.

### Search Logic
Task filtering is handled server-side using SQLAlchemy's `.contains()` method. This allows the database to perform the search operation using SQL `LIKE` logic, which is more efficient for larger datasets than fetching all records and filtering via JavaScript.
