export interface ClientAddress {
  street_name: string;
  city: string;
  state: string;
  zip_code: string;
}

export interface Session {
  client_id: string;
  client_name: string;
  start_time: string;
  end_time: string;
  client_address: ClientAddress;
  travel_time_to_next: number | null;
}

export interface DaySchedule {
  day: number;
  sessions: Session[];
}

export interface Metrics {
  total_scheduled_hours: number;
  total_drive_time_hours: number;
  scheduled_clients: string[];
}

export interface Schedule {
  schedule: DaySchedule[];
  metrics: Metrics;
}

export interface ScheduleOption extends Schedule {
  id: number;
}

export interface AppointmentProps {
  session: Session;
  isLast: boolean;
}

export interface ScheduleOptionCardProps {
  option: ScheduleOption;
  selectedOption: number;
  onSelect: (id: number) => void;
}

export interface DayScheduleProps {
  daySchedule: DaySchedule;
}
