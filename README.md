# Alpaca Health Software Engineering Take-Home Project

## Approach

### Backend:

The scheduling algorithm described uses a combination of greedy algorithm for sorting clients and backtracking to generate optimized, non-overlapping schedules.

### Steps:

1. **Filter Clients**: Select clients whose availability overlaps with the clinician’s availability.

2. **Calculate Drive Times**: Compute the drive time for each client.

3. **Sort Clients**: Clients are sorted using two different sorting method: one prioritizing earliest availability, then drive time, while the other prioritizes drive time first, then earliest availability, Both method factors the number of client availabilities.

4. **Backtracking**: A backtracking algorithm is used to generate valid schedules. It ensures there are no overlapping sessions and that travel times between clients are respected.

5. **Result**: The final output consists of two schedules, each containing sessions for all five days.

### Frontend:

1. Generates and displays schedule options based on clinician ID.

2. Fetches schedule data from an API and handles errors.

3. Allows the user to select a schedule, view details, and reset the process.

## Design Decisions

- **Backtracking**: Chose backtracking to explore all possible schedules while respecting client availability and drive times, ensuring the generated schedules are valid.
- **Greedy Sorting**: Clients are sorted based on availability and drive time to prioritize the most feasible clients first.

## Setup Instructions

### Backend Setup (Python 3.11+ required)

```bash
# Create and activate virtual environment
python -m venv alpaca_venv
source alpaca_venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dependencies
pip install -r requirements.txt

# Start the server
fastapi dev main.py
```

### Frontend Setup (Node.js 18+ required)

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

The application will be available at:

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Assumptions

1. A client can only have one session in a given day.

## Note:

In the data, the drive time for some cities are missing, so during testing, some sessions might overlap.
