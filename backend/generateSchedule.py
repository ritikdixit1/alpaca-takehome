from typing import List, Dict
import datetime
from data.driveTimes import get_drive_time, get_travel_window
import copy

def minutes_to_time(minutes: int) -> str:
    return f"{minutes//60:02d}:{minutes%60:02d}"

def calculate_overlap(clinician_availability: List[Dict], client_availability: List[Dict]) -> int:
    """
    Calculate the total overlap in hours between clinician and client availability.
    """
    overlap_hours = 0
    for clin_avail in clinician_availability:
        for client_avail in client_availability:
            if clin_avail["day_of_the_week"] == client_avail["day_of_the_week"]:
                # Convert times to minutes since midnight
                clin_start = int(clin_avail["start_time"][:2]) * 60 + int(clin_avail["start_time"][3:5])
                clin_end = int(clin_avail["end_time"][:2]) * 60 + int(clin_avail["end_time"][3:5])
                client_start = int(client_avail["start_time"][:2]) * 60 + int(client_avail["start_time"][3:5])
                client_end = int(client_avail["end_time"][:2]) * 60 + int(client_avail["end_time"][3:5])

                # Calculate overlap
                overlap_start = max(clin_start, client_start)
                overlap_end = min(clin_end, client_end)
                if overlap_start < overlap_end:
                    overlap_hours += (overlap_end - overlap_start) / 60
    return overlap_hours

def is_time_slot_available(schedule: List[Dict], start_time: str, end_time: str) -> bool:
    """
    Check if a time slot is available in the clinician's schedule for the day.
    """
    for session in schedule:
        session_start = int(session["start_time"][:2]) * 60 + int(session["start_time"][3:5])
        session_end = int(session["end_time"][:2]) * 60 + int(session["end_time"][3:5])
        new_start = int(start_time[:2]) * 60 + int(start_time[3:5])
        new_end = int(end_time[:2]) * 60 + int(end_time[3:5])

        # Check for overlap
        if not (new_end <= session_start or new_start >= session_end):
            return False 
    return True


def generate_schedules(clinician: Dict, clients: List[Dict], max_schedules: int = 2) -> List[Dict]:
    """
    Generate multiple valid schedules for the clinician for the entire week.
    Each schedule contains appointments for all 5 days.
    """
    clinician_availability = clinician["availabilities"]
    max_clients_per_day = clinician["max_clients_per_day"]
    session_duration_hours = clinician["session_duration_hours"]
    session_duration_minutes = session_duration_hours * 60  

    # Step 1: Filter clients with overlapping schedules
    filtered_clients = [
        client for client in clients
        if calculate_overlap(clinician_availability, client["availabilities"]) > 0
    ]

    # Step 2: Calculate drive time and travel window for each client
    clinician_address = clinician["address"]
    for client in filtered_clients:
        drive_time = get_drive_time(clinician_address, client["address"])
        client["drive_time_including_travel_window"] = get_travel_window(drive_time)

    # Step 3: Precompute sorted clients for each day
    day_to_sorted_clients = [{} for _ in range(max_schedules)]
    for day in range(1, 6): 
        clients_for_day = [
            client for client in filtered_clients
            if any(avail["day_of_the_week"] == day for avail in client["availabilities"])
        ]

        
        sorting_methods = [
            lambda x: (
                min(avail["start_time"] for avail in x["availabilities"] if avail["day_of_the_week"] == day),
                x["drive_time_including_travel_window"],
                len(x["availabilities"])
            ),
            lambda x: (
                x["drive_time_including_travel_window"],
                min(avail["start_time"] for avail in x["availabilities"] if avail["day_of_the_week"] == day),
                len(x["availabilities"])
            ),
        ]

        for i in range(max_schedules):
            sorted_clients = sorted(clients_for_day, key=sorting_methods[i % len(sorting_methods)])
            day_to_sorted_clients[i][day] = sorted_clients


    schedules = []

    def backtrack(day: int, week_schedule: List[Dict], used_clients: set, schedule_count: int, schedule_idx: int):
        if schedule_count >= max_schedules:
            return

        if day > 5:  
            if len(week_schedule) == 5: 
                schedules.append(copy.deepcopy(week_schedule)) 
            return

        sorted_clients = day_to_sorted_clients[schedule_idx].get(day, [])
        day_schedule = []
        last_session_end_time = None
        used_clients_for_day = set()

        for client in sorted_clients:
            if client["id"] in used_clients_for_day or client["id"] in used_clients:
                continue

            for avail in client["availabilities"]:
                if avail["day_of_the_week"] != day:
                    continue

                start_min = int(avail["start_time"][:2])*60 + int(avail["start_time"][3:])
                end_min = int(avail["end_time"][:2])*60 + int(avail["end_time"][3:])
                
                session_end_min = start_min + session_duration_minutes
                
                if session_end_min > end_min:
                    continue 

                if not is_time_slot_available(day_schedule, 
                                            minutes_to_time(start_min),
                                            minutes_to_time(session_end_min)):
                    continue

     
                if last_session_end_time is not None:
                    required_start = last_session_end_time + client["drive_time_including_travel_window"]
                    if start_min < required_start:
                        continue 

                day_schedule.append({
                    "client_id": client["id"],
                    "client_name": client["name"],
                    "start_time": minutes_to_time(start_min),
                    "end_time": minutes_to_time(session_end_min) 
                })
                
                used_clients_for_day.add(client["id"])
                last_session_end_time = session_end_min  

                if len(day_schedule) >= max_clients_per_day:
                    break

        week_schedule.append({
            "day": day,
           "sessions": copy.deepcopy(day_schedule)
        })

        # Recur for the next day
        backtrack(day + 1, week_schedule, used_clients | used_clients_for_day, schedule_count, schedule_idx)

        # Backtrack
        week_schedule.pop()

    # Step 5: Generate distinct schedules with added variability (sorting methods)
    for i in range(max_schedules):
        if len(schedules) >= max_schedules:
            break
        backtrack(1, [], set(), len(schedules), i)

    # Step 6: Generate schedules with additional metrics
    final_schedules = []
    clinician_address = clinician["address"]

    for schedule in schedules:
        total_hours = 0
        total_drive_time_minutes = 0
        scheduled_clients = set()
        week_schedule = []

        for day_schedule in schedule:
            day = day_schedule["day"]
            sessions = []
            previous_location = clinician_address

            day_sessions = day_schedule["sessions"]
            total_sessions = len(day_sessions)

            for i, session in enumerate(day_sessions):
                current_client = next(c for c in filtered_clients if c["id"] == session["client_id"])
                
                scheduled_clients.add(current_client["name"])

                start = datetime.datetime.strptime(session["start_time"], "%H:%M")
                end = datetime.datetime.strptime(session["end_time"], "%H:%M")
                duration = (end - start).total_seconds() / 3600
                total_hours += duration

                travel_time = 0
                if i > 0:
                    travel_time = get_drive_time(previous_location, current_client["address"])
                    total_drive_time_minutes = get_travel_window(travel_time)
                    sessions[-1]["travel_time_to_next"] = total_drive_time_minutes

                session_entry = {
                    **session,
                    "client_address": current_client["address"],
                    "travel_time_to_next": None  
                }

                if i < total_sessions - 1:
                    session_entry["travel_time_to_next"] = travel_time

                sessions.append(session_entry)
                previous_location = current_client["address"]

            week_schedule.append({
                "day": day,
                "sessions": sessions
            })

        final_schedules.append({
            "schedule": week_schedule,
            "metrics": {
                "total_scheduled_hours": round(total_hours, 2),
                "total_drive_time_hours": round(total_drive_time_minutes / 60, 2),
                "scheduled_clients": list(scheduled_clients)
            }
        })
    return final_schedules[:max_schedules]