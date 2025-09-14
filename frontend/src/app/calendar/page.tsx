"use client";
import React, { useMemo, useState, useEffect } from "react";
import { createClient } from "@supabase/supabase-js";

// Initialize Supabase client

const NEXT_PUBLIC_SUPABASE_URL="https://rpaqzsgohrzebjdunwya.supabase.co"
const NEXT_PUBLIC_SUPABASE_ANON_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJwYXF6c2dvaHJ6ZWJqZHVud3lhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTc4MjU3MTAsImV4cCI6MjA3MzQwMTcxMH0.eR-Gu0TDWCq8jsAqsQzMtLZmhC1Oojc4IpE91blDPnE"


const supabaseUrl = NEXT_PUBLIC_SUPABASE_URL;
const supabaseKey = NEXT_PUBLIC_SUPABASE_ANON_KEY;
const supabase = createClient(supabaseUrl, supabaseKey);
type CalendarEvent = {
  id: string;
  title: string;
  color?: string;
  time?: string;
};

type Props = {
  initialDate?: Date;
  events?: Record<string, CalendarEvent[]>;
  onSelectDate?: (date: Date) => void;
  className?: string; // allow custom class for embedding
};

function startOfMonth(date: Date) {
  return new Date(date.getFullYear(), date.getMonth(), 1);
}
function endOfMonth(date: Date) {
  return new Date(date.getFullYear(), date.getMonth() + 1, 0);
}
function addMonths(date: Date, delta: number) {
  return new Date(date.getFullYear(), date.getMonth() + delta, 1);
}
function formatISO(d: Date) {
  return d.toISOString().slice(0, 10);
}

export default function ElegantCalendar({
  initialDate = new Date(),
  onSelectDate,
  className = "",
}: Props) {
  const [currentMonth, setCurrentMonth] = useState<Date>(startOfMonth(initialDate));
  const [selectedDate, setSelectedDate] = useState<Date | null>(null);
  const [events, setEvents] = useState<Record<string, CalendarEvent[]>>({});

  // 2. Fetch events from Supabase
  useEffect(() => {
    async function fetchEvents() {
      const { data, error } = await supabase
        .from("calendar")
        .select("*");
      if (error) {
        console.error("Error fetching events:", error);
        return;
      }
      console.log("Fetched events:", data);
      // 3. Map events by date (assuming you have a 'date' column in YYYY-MM-DD format)
      const eventsByDate: Record<string, CalendarEvent[]> = {};
      data.forEach((ev: any) => {
        const iso = ev.date; // adjust if your column is named differently
        if (!eventsByDate[iso]) eventsByDate[iso] = [];
        eventsByDate[iso].push({
          id: ev.id,
          title: ev.title,
          color: ev.color,
          time: ev.time,
        });
      });
      setEvents(eventsByDate);
    }
    fetchEvents();
  }, []);
  const todayISO = useMemo(() => formatISO(new Date()), []);

  const monthGrid = useMemo(() => {
    const start = startOfMonth(currentMonth);
    const end = endOfMonth(currentMonth);

    const startWeekday = start.getDay();
    const daysInMonth = end.getDate();

    const cells: (Date | null)[] = [];
    for (let i = 0; i < startWeekday; i++) cells.push(null);
    for (let d = 1; d <= daysInMonth; d++)
      cells.push(new Date(currentMonth.getFullYear(), currentMonth.getMonth(), d));
    while (cells.length % 7 !== 0) cells.push(null);

    const weeks: (Date | null)[][] = [];
    for (let i = 0; i < cells.length; i += 7) weeks.push(cells.slice(i, i + 7));
    return weeks;
  }, [currentMonth]);

  function go(delta: number) {
    setCurrentMonth((m) => addMonths(m, delta));
  }

  function handleSelect(d: Date | null) {
    if (!d) return;
    setSelectedDate(d);
    onSelectDate?.(d);
  }

  const monthLabel = useMemo(() => {
    const opts: Intl.DateTimeFormatOptions = { month: "long", year: "numeric" };
    return currentMonth.toLocaleDateString(undefined, opts);
  }, [currentMonth]);

  return (
    <div className={`w-full ${className}`}>
      <div className="bg-white rounded-2xl shadow p-4">
        <header className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold">{monthLabel}</h2>
          <div className="flex gap-2">
            <button
              aria-label="Previous month"
              onClick={() => go(-1)}
              className="px-3 py-1 rounded hover:bg-gray-50 focus:ring-2 focus:ring-indigo-300"
            >
              ◀
            </button>
            <button
              aria-label="Today"
              onClick={() => setCurrentMonth(startOfMonth(new Date()))}
              className="px-3 py-1 rounded hover:bg-gray-50 focus:ring-2 focus:ring-indigo-300"
            >
              Today
            </button>
            <button
              aria-label="Next month"
              onClick={() => go(1)}
              className="px-3 py-1 rounded hover:bg-gray-50 focus:ring-2 focus:ring-indigo-300"
            >
              ▶
            </button>
          </div>
        </header>

        <div className="grid grid-cols-7 gap-1 text-center text-sm text-gray-600">
          {["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"].map((d) => (
            <div key={d} className="py-1 font-medium">
              {d}
            </div>
          ))}
        </div>

        <div className="grid grid-cols-7 gap-2 mt-2">
          {monthGrid.map((week, wi) => (
            <React.Fragment key={wi}>
              {week.map((day, di) => {
                const iso = day ? formatISO(day) : null;
                const dayEvents = iso ? events[iso] ?? [] : [];
                const isToday = iso === todayISO;
                const isSelected = selectedDate && iso === formatISO(selectedDate);
                const isCurrentMonth = day ? day.getMonth() === currentMonth.getMonth() : false;

                return (
                  <button
                    key={di}
                    onClick={() => handleSelect(day)}
                    disabled={!day}
                    className={`relative h-20 p-2 text-left rounded transition-colors focus:ring-2 focus:ring-indigo-300 ${
                      !day ? "opacity-40 cursor-default" : ""
                    } ${isSelected ? "ring-2 ring-indigo-400 bg-indigo-50" : ""} ${
                      isToday ? "border border-indigo-200" : ""
                    } ${isCurrentMonth ? "" : "text-gray-400"}`}
                  >
                    <div className="text-sm font-medium">{day ? day.getDate() : ""}</div>
                    <div className="flex gap-1 mt-2 absolute bottom-2 left-2 right-2">
                      {dayEvents.slice(0, 3).map((ev) => (
                        <span
                          key={ev.id}
                          title={ev.title}
                          className={`w-2 h-2 rounded-full inline-block ${ev.color ? "" : "bg-indigo-500"}`}
                          style={ev.color ? { background: ev.color } : undefined}
                        />
                      ))}
                      {dayEvents.length > 3 && (
                        <span className="text-xs text-gray-500 ml-auto">+{dayEvents.length - 3}</span>
                      )}
                    </div>
                  </button>
                );
              })}
            </React.Fragment>
          ))}
        </div>

        {selectedDate && (
          <div className="mt-4 border-t pt-3">
            <h3 className="text-sm font-semibold">{selectedDate.toDateString()}</h3>
            <div className="mt-2">
              {(() => {
                const iso = formatISO(selectedDate);
                const list = events[iso] ?? [];
                if (list.length === 0)
                  return <p className="text-sm text-gray-500">No events for this date.</p>;
                return (
                  <ul className="space-y-2">
                    {list.map((ev) => (
                      <li key={ev.id} className="flex gap-3 bg-gray-50 p-2 rounded shadow-sm">
                        <div className="w-3 h-3 rounded-full mt-1" style={{ background: ev.color ?? "#6366F1" }} />
                        <div>
                          <div className="text-sm font-medium">{ev.title}</div>
                          {ev.time && (
  <div className="text-xs text-gray-500">
    {(() => {
      // Extract time and offset
      const match = ev.time.match(/^(\d{2}:\d{2}:\d{2})([+-]\d{2})(?::?\d{2})?$/);
      if (match) {
        const [, time, offset] = match;
        return `${time} (UTC ${offset.replace(/^([+-])0?/, '$1')})`;
      }
      return ev.time;
    })()}
  </div>
)}
                        </div>
                      </li>
                    ))}
                  </ul>
                );
              })()}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
