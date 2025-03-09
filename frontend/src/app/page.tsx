"use client";

import { useState } from "react";

import { ScheduleOption, Schedule } from "./interfaces/interface";
import { ScheduleOptionCard } from "./components/ScheduleOptionCard";
import { DayScheduleComponent } from "./components/DayScheduleComponent";

const SchedulePage: React.FC = () => {
  const [selectedOption, setSelectedOption] = useState<number>(0);
  const [schedules, setSchedules] = useState<ScheduleOption[]>([]);
  const [clinicianId, setClinicianId] = useState<string>("");
  const [error, setError] = useState<string>("");
  const [isScheduleGenerated, setIsScheduleGenerated] = useState(false);

  const handleGenerateSchedules = async () => {
    if (!clinicianId) {
      setError("Please enter a Clinician ID.");
      return;
    }

    try {
      const response = await fetch("http://127.0.0.1:8000/generate-schedules", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ clinician_id: clinicianId }),
      });

      if (!response.ok) {
        throw new Error("Failed to fetch schedules");
      }

      const data = await response.json();
      const options: ScheduleOption[] = data.schedules.map(
        (schedule: Schedule, index: number) => ({
          ...schedule,
          id: index + 1,
        })
      );

      setSchedules(options);
      setError("");
      setIsScheduleGenerated(true);
    } catch (err) {
      setError("Failed to fetch schedules. Please try again.");
      setSchedules([]);
    }
  };

  const selectedSchedule = schedules.find((s) => s.id === selectedOption);

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      {!isScheduleGenerated ? (
        <div className="p-8 max-w-3xl mx-auto min-h-screen">
          <h1 className="text-4xl font-semibold text-gray-800 text-center pb-4 border-b-2 border-gray-200">
            Alpaca Health
          </h1>

          <div className="bg-white p-8 rounded-xl shadow-lg bg-gray-50">
            <div className="mb-6">
              <label
                htmlFor="clinician-id"
                className="block text-base text-gray-700 mb-2 font-medium"
              >
                Clinician ID:
              </label>
              <input
                type="text"
                id="clinician-id"
                value={clinicianId}
                onChange={(e) => setClinicianId(e.target.value)}
                placeholder="Enter Clinician ID"
                className="w-full max-w-md p-3 rounded-lg border border-gray-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-500 transition-colors outline-none"
              />
            </div>

            <button
              onClick={handleGenerateSchedules}
              className="bg-blue-500 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-600 active:bg-blue-700 transition-colors uppercase tracking-wide"
            >
              Generate Schedules
            </button>

            {error && (
              <div className="bg-red-100 text-red-700 p-4 rounded-lg mt-6">
                {error}
              </div>
            )}
          </div>
        </div>
      ) : (
        <div>
          <div className="flex">
            <h1 className="text-2xl font-bold mb-4">
              Compatible Client Schedules
            </h1>
            <button
              className="border rounded mx-5 h-[35px] px-4"
              onClick={() => {
                setClinicianId("");
                setIsScheduleGenerated(false);
              }}
            >
              Reset
            </button>
          </div>

          <p className="text-gray-600 mb-6">
            Select a schedule option that works for you. Each option shows
            available timeslots, drive times, and the clients who share this
            schedule.
          </p>

          {schedules.length > 0 && (
            <>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {schedules.map((schedule) => (
                  <ScheduleOptionCard
                    key={schedule.id}
                    option={schedule}
                    selectedOption={selectedOption}
                    onSelect={setSelectedOption}
                  />
                ))}
              </div>

              {selectedSchedule && (
                <div className="mt-12">
                  <div className="mb-6">
                    <h2 className="text-xl font-bold">
                      Schedule Option {selectedSchedule.id} Details
                    </h2>
                    <p className="text-gray-600">
                      {selectedSchedule.metrics.total_scheduled_hours.toFixed(
                        1
                      )}{" "}
                      hours •{" "}
                      {selectedSchedule.metrics.total_drive_time_hours.toFixed(
                        1
                      )}{" "}
                      hours drive time
                    </p>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-5 gap-3">
                    {selectedSchedule.schedule.map((daySchedule) => (
                      <DayScheduleComponent
                        key={daySchedule.day}
                        daySchedule={daySchedule}
                      />
                    ))}
                  </div>
                </div>
              )}
            </>
          )}
        </div>
      )}
    </div>
  );
};

export default SchedulePage;
