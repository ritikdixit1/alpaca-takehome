import { AppointmentProps } from "../interfaces/interface";
import { Clock, MapPin } from "lucide-react";

export const AppointmentComponent: React.FC<AppointmentProps> = ({
  session,
  isLast,
}) => {
  const formatTimeRange = (start: string, end: string) => {
    const format = (time: string) => {
      const [hours, minutes] = time.split(":");
      const date = new Date();
      date.setHours(parseInt(hours), parseInt(minutes));
      return date.toLocaleTimeString([], {
        hour: "numeric",
        minute: "2-digit",
      });
    };
    return `${format(start)} - ${format(end)}`;
  };

  return (
    <div className="mb-6">
      <div
        className="border rounded p-2 d-flex flex-column h-full"
        style={{ minHeight: 150 }}
      >
        <div className="flex justify-between items-start mb-2">
          <div className="font-medium">
            {formatTimeRange(session.start_time, session.end_time)}
          </div>
          <div className="bg-black text-white text-xs px-4 py-1 rounded-full">
            {session.client_name}
          </div>
        </div>

        <div className="flex items-center gap-2 text-sm text-gray-600 min-h-[2rem]">
          <MapPin size={14} />
          <span className="whitespace-normal">
            {Object.values(session.client_address).join(", ")}
          </span>
        </div>
      </div>

      {!isLast && session.travel_time_to_next && (
        <div className="mt-2 flex items-center gap-2 text-sm text-amber-700 border-l-4 border-amber-500 pl-2 py-1">
          <Clock size={14} />
          <span>{session.travel_time_to_next}m drive time</span>
        </div>
      )}
    </div>
  );
};
