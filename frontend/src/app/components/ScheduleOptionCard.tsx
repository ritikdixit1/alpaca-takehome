import { ScheduleOptionCardProps } from "../interfaces/interface";
import { Calendar, Clock, User } from "lucide-react";

export const ScheduleOptionCard: React.FC<ScheduleOptionCardProps> = ({
  option,
  selectedOption,
  onSelect,
}) => {
  const isSelected = selectedOption === option.id;
  const formatTime = (hours: number) => {
    const totalMinutes = hours * 60;
    const hoursPart = Math.floor(totalMinutes / 60);
    const minutesPart = Math.round(totalMinutes % 60);
    return `${hoursPart}h ${minutesPart}m`;
  };

  return (
    <div
      className={`border rounded-lg p-4 flex flex-col justify-between ${
        isSelected ? "border-black" : "border-gray-200"
      }`}
    >
      <div>
        <div className="flex justify-between items-start mb-4">
          <h3 className="text-lg font-medium">Schedule Option {option.id}</h3>
          <div
            className={`w-6 h-6 rounded-full border ${
              isSelected ? "bg-black border-black" : "border-gray-300"
            } flex items-center justify-center cursor-pointer`}
            onClick={() => onSelect(option.id)}
          >
            {isSelected && (
              <div className="w-2 h-2 rounded-full bg-white"></div>
            )}
          </div>
        </div>

        <div className="flex items-center gap-2 mb-2">
          <Calendar size={16} className="text-gray-500" />
          <span className="text-sm">
            {formatTime(option.metrics.total_scheduled_hours)} hours total
          </span>
        </div>

        <div className="flex items-center gap-2 mb-4">
          <Clock size={16} className="text-gray-500" />
          <span className="text-sm">
            {formatTime(option.metrics.total_drive_time_hours)} drive time
          </span>
        </div>

        <div className="mb-4">
          <div className="flex items-center gap-2 mb-2">
            <User size={16} className="text-gray-500" />
            <span className="text-sm">Clients:</span>
          </div>

          <div className="flex flex-wrap gap-2">
            {option.metrics.scheduled_clients.map((client) => (
              <span
                key={client}
                className="bg-gray-100 text-xs px-3 py-1 rounded-full"
              >
                {client}
              </span>
            ))}
          </div>
        </div>
      </div>

      <div className="mt-4">
        <p className="text-sm font-medium mb-2">Preview:</p>
        <button className="w-full text-center py-2 text-sm border rounded text-gray-600 hover:underline mb-4">
          View Detailed Schedule
        </button>

        <button
          className={`w-full mt-2 py-2 text-sm rounded ${
            isSelected
              ? "bg-black text-white"
              : "bg-white border border-gray-300"
          }`}
          onClick={() => onSelect(option.id)}
        >
          {isSelected ? "Selected" : "Select Schedule"}
        </button>
      </div>
    </div>
  );
};
