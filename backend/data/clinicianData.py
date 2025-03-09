"""
Sample clinician data for ABA clinic scheduling challenge.
This file contains a list of clinician objects with their availabilities and addresses.
"""

clinicians = [
    {
        "id": "B001",
        "name": "Dr. Emily Rodriguez, BCBA",
        "availabilities": [
            {"day_of_the_week": 1, "start_time": "08:00", "end_time": "18:00"},
            {"day_of_the_week": 2, "start_time": "08:00", "end_time": "18:00"},
            {"day_of_the_week": 3, "start_time": "08:00", "end_time": "18:00"},
            {"day_of_the_week": 4, "start_time": "08:00", "end_time": "18:00"},
            {"day_of_the_week": 5, "start_time": "08:00", "end_time": "18:00"}
        ],
        "address": {
            "street_name": "100 Medical Plaza",
            "city": "San Francisco",
            "state": "CA",
            "zip_code": "94107"
        },
        "max_clients_per_day": 4,
        "session_duration_hours": 2
    },
    {
        "id": "B002",
        "name": "Dr. Michael Taylor, BCBA",
        "availabilities": [
            {"day_of_the_week": 1, "start_time": "09:00", "end_time": "17:00"},
            {"day_of_the_week": 2, "start_time": "09:00", "end_time": "17:00"},
            {"day_of_the_week": 3, "start_time": "09:00", "end_time": "17:00"},
            {"day_of_the_week": 4, "start_time": "09:00", "end_time": "17:00"},
            {"day_of_the_week": 5, "start_time": "09:00", "end_time": "17:00"}
        ],
        "address": {
            "street_name": "250 Health Center Drive",
            "city": "Berkeley",
            "state": "CA",
            "zip_code": "94704"
        },
        "max_clients_per_day": 3,
        "session_duration_hours": 2
    },
    {
        "id": "B003",
        "name": "Dr. Sarah Johnson, BCBA",
        "availabilities": [
            {"day_of_the_week": 1, "start_time": "08:30", "end_time": "16:30"},
            {"day_of_the_week": 2, "start_time": "08:30", "end_time": "16:30"},
            {"day_of_the_week": 4, "start_time": "08:30", "end_time": "16:30"},
            {"day_of_the_week": 5, "start_time": "08:30", "end_time": "16:30"}
        ],
        "address": {
            "street_name": "400 Therapy Way",
            "city": "Oakland",
            "state": "CA",
            "zip_code": "94612"
        },
        "max_clients_per_day": 3,
        "session_duration_hours": 2
    },
    {
        "id": "B004",
        "name": "Dr. David Wilson, BCBA",
        "availabilities": [
            {"day_of_the_week": 2, "start_time": "10:00", "end_time": "18:00"},
            {"day_of_the_week": 3, "start_time": "10:00", "end_time": "18:00"},
            {"day_of_the_week": 4, "start_time": "10:00", "end_time": "18:00"},
            {"day_of_the_week": 5, "start_time": "10:00", "end_time": "18:00"}
        ],
        "address": {
            "street_name": "750 Behavioral Drive",
            "city": "San Jose",
            "state": "CA",
            "zip_code": "95113"
        },
        "max_clients_per_day": 3,
        "session_duration_hours": 2
    },
    {
        "id": "B005",
        "name": "Dr. Jennifer Martinez, BCBA",
        "availabilities": [
            {"day_of_the_week": 1, "start_time": "09:30", "end_time": "17:30"},
            {"day_of_the_week": 3, "start_time": "09:30", "end_time": "17:30"},
            {"day_of_the_week": 5, "start_time": "09:30", "end_time": "17:30"}
        ],
        "address": {
            "street_name": "500 Analysis Avenue",
            "city": "Palo Alto",
            "state": "CA",
            "zip_code": "94301"
        },
        "max_clients_per_day": 3,
        "session_duration_hours": 2
    }
]

if __name__ == "__main__":
    # Print some basic stats about the data
    print(f"Total number of clinicians: {len(clinicians)}")
    
    # Calculate total availability hours per week
    total_hours = 0
    for clinician in clinicians:
        for slot in clinician["availabilities"]:
            start_hour, start_min = map(int, slot["start_time"].split(":"))
            end_hour, end_min = map(int, slot["end_time"].split(":"))
            hours = (end_hour - start_hour) + (end_min - start_min) / 60
            total_hours += hours
    
    print(f"Total availability hours per week: {total_hours:.2f}")
    print(f"Average availability hours per clinician: {total_hours / len(clinicians):.2f}")
