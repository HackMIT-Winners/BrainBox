"use client";
import React, { useMemo, useState, useEffect } from "react";
import { createClient } from "@supabase/supabase-js";
import Link from "next/link";
import HomeBar from "@/components/HomeBar";

// Initialize Supabase client
const NEXT_PUBLIC_SUPABASE_URL = "https://rpaqzsgohrzebjdunwya.supabase.co";
const NEXT_PUBLIC_SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJwYXF6c2dvaHJ6ZWJqZHVud3lhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTc4MjU3MTAsImV4cCI6MjA3MzQwMTcxMH0.eR-Gu0TDWCq8jsAqsQzMtLZmhC1Oojc4IpE91blDPnE";
const supabase = createClient(NEXT_PUBLIC_SUPABASE_URL, NEXT_PUBLIC_SUPABASE_ANON_KEY);

type CalendarEvent = {
  id: string;
  title: string;
  color?: string;
  time?: string;
  description?: string;
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

export default function ElegantCalendar() {
  const [currentMonth, setCurrentMonth] = useState<Date>(startOfMonth(new Date()));
  const [selectedDate, setSelectedDate] = useState<Date | null>(null);
  const [events, setEvents] = useState<Record<string, CalendarEvent[]>>({});

  // Fetch events from Supabase
  useEffect(() => {
    async function fetchEvents() {
      const { data, error } = await supabase.from("calendar").select("*");
      if (error) {
        console.error("Error fetching events:", error);
        return;
      }
      const eventsByDate: Record<string, CalendarEvent[]> = {};
      data.forEach((ev: any) => {
        const iso = typeof ev.date === "string"
          ? ev.date.slice(0, 10)
          : new Date(ev.date).toISOString().slice(0, 10);
        if (!eventsByDate[iso]) eventsByDate[iso] = [];
        eventsByDate[iso].push({
          id: ev.id,
          title: ev.title,
          color: ev.color,
          time: ev.time,
          description: ev.description,
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
  }

  const monthLabel = useMemo(() => {
    const opts: Intl.DateTimeFormatOptions = { month: "long", year: "numeric" };
    return currentMonth.toLocaleDateString(undefined, opts);
  }, [currentMonth]);

  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 text-white">
      <HomeBar />
      {/* Header */}

      {/* Calendar Section */}
      <main className="flex-1 flex flex-col items-center justify-center px-4 py-10">
        <div className="w-full max-w-3xl bg-gradient-to-br from-gray-800 via-gray-900 to-gray-800 rounded-3xl shadow-2xl p-6 border border-white/10">
          <div className="bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 rounded-2xl shadow p-4">
            <header className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold text-white">{monthLabel}</h2>
              <div className="flex gap-2">
                <button
                  aria-label="Previous month"
                  onClick={() => go(-1)}
                  className="px-3 py-1 rounded hover:bg-gray-700 focus:ring-2 focus:ring-indigo-300 text-gray-200"
                >
                  ◀
                </button>
                <button
                  aria-label="Today"
                  onClick={() => setCurrentMonth(startOfMonth(new Date()))}
                  className="px-3 py-1 rounded hover:bg-gray-700 focus:ring-2 focus:ring-indigo-300 text-gray-200"
                >
                  Today
                </button>
                <button
                  aria-label="Next month"
                  onClick={() => go(1)}
                  className="px-3 py-1 rounded hover:bg-gray-700 focus:ring-2 focus:ring-indigo-300 text-gray-200"
                >
                  ▶
                </button>
              </div>
            </header>

            <div className="grid grid-cols-7 gap-0 text-center text-sm text-gray-300 border border-gray-700 rounded-lg overflow-hidden">
              {["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"].map((d) => (
                <div key={d} className="py-2 font-medium bg-gray-800 border-b border-gray-700">
                  {d}
                </div>
              ))}
{monthGrid.flat().map((day, idx) => {
  const iso = day ? formatISO(day) : null;
  const dayEvents = iso ? events[iso] ?? [] : [];
  const isToday = iso === todayISO;
  const isSelected = selectedDate && iso === formatISO(selectedDate);
  const isCurrentMonth = day ? day.getMonth() === currentMonth.getMonth() : false;

  return (
    <button
      key={idx}
      onClick={() => handleSelect(day)}
      disabled={!day}
      className={`
        relative h-24 p-2 text-left transition-all duration-150 focus:ring-2 focus:ring-indigo-300
        border border-gray-700
        ${!day ? "bg-gray-900 opacity-40 cursor-default" : ""}
        ${isSelected ? "z-10 scale-110 shadow-2xl ring-4 ring-pink-400 bg-gradient-to-br from-indigo-900 via-indigo-700 to-pink-900 text-white font-bold" : ""}
        ${isToday && !isSelected ? "border-2 border-indigo-400" : ""}
        ${isCurrentMonth && !isSelected ? "bg-gray-800 hover:bg-gray-700" : ""}
        ${!isCurrentMonth && !isSelected ? "bg-gray-900 text-gray-600" : ""}
      `}
      style={{
        boxShadow: isSelected
          ? "0 8px 32px 0 rgba(236, 72, 153, 0.3)"
          : undefined,
        transition: "transform 0.15s, box-shadow 0.15s"
      }}
    >
      <div className={`text-xs font-semibold mb-1 ${isToday ? "text-indigo-400" : ""}`}>
        {day ? day.getDate() : ""}
      </div>
      <div className="flex gap-1 mt-1 absolute bottom-2 left-2 right-2">
        {dayEvents.slice(0, 3).map((ev) => (
          <span
            key={ev.id}
            title={ev.title}
            className="w-2 h-2 rounded-full inline-block"
            style={{
              background: isSelected
                ? "#831843" // Tailwind's pink-900
                : ev.color ?? "#6366F1"
            }}
          />
        ))}
        {dayEvents.length > 3 && (
          <span className="text-xs text-gray-400 ml-auto">+{dayEvents.length - 3}</span>
        )}
      </div>
    </button>
  );
})}
            </div>
              {/* Show event details for selected date */}
              {selectedDate && (
                <div className="mt-4 border-t border-gray-700 pt-3">
                  <h3 className="text-sm font-semibold text-white">{selectedDate.toDateString()}</h3>
                  <div className="mt-2">
                    {(() => {
                      const iso = formatISO(selectedDate);
                      const list = events[iso] ?? [];
                      if (list.length === 0)
                        return <p className="text-sm text-gray-400">No events for this date.</p>;
                      return (
                        <ul className="space-y-2">
                          {list.map((ev) => (
                            <li key={ev.id} className="flex gap-3 bg-gray-800 p-2 rounded shadow-sm">
                              <div className="w-3 h-3 rounded-full mt-1" style={{ background: ev.color ?? "#6366F1" }} />
                              <div>
                                <div className="text-sm font-medium text-white">{ev.title}</div>
                                {ev.time && (
                                  <div className="text-xs text-gray-400">
                                    {(() => {
                                      const match = ev.time.match(/^(\d{2}:\d{2}:\d{2})([+-]\d{2})(?::?\d{2})?$/);
                                      if (match) {
                                        const [, time, offset] = match;
                                        return `${time} (UTC ${offset.replace(/^([+-])0?/, '$1')})`;
                                      }
                                      return ev.time;
                                    })()}
                                  </div>
                                )}
                                {ev.description && (
                                  <div className="text-xs text-gray-300 mt-1 italic">{ev.description}</div>
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
      </main>

      {/* Footer */}
      <footer className="bg-black/30 backdrop-blur-lg border-t border-white/10 text-gray-300 py-4 text-center text-sm">
        <p>&copy; 2025 BrainBox. All rights reserved.</p>
      </footer>
    </div>
  );
}