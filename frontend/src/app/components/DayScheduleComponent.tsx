import { DayScheduleProps } from "../interfaces/interface";
import { AppointmentComponent } from "./AppointmentComponent";

export const DayScheduleComponent: React.FC<DayScheduleProps> = ({
  daySchedule,
}) => {
  const getDayName = (dayNumber: number) => {
    const days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"];
    return days[dayNumber - 1];
  };

  return (
    <div className="flex-1 border rounded">
      <div className="bg-gray-100 p-3 font-medium mb-4 ">
        {getDayName(daySchedule.day)}
      </div>
      <div className="px-3">
        {daySchedule.sessions.map((session, index) => (
          <AppointmentComponent
            key={session.client_id}
            session={session}
            isLast={index === daySchedule.sessions.length - 1}
          />
        ))}
      </div>
    </div>
  );
};
