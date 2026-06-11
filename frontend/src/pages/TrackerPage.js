import React, { useState, useEffect, useMemo, useCallback } from 'react';
import axios from 'axios';
import { toast } from 'sonner';
import { deduplicateMedications } from '@/lib/utils';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const TrackerPage = () => {
  const [medications, setMedications] = useState([]);
  const [prescriptions, setPrescriptions] = useState([]);
  const [logs, setLogs] = useState([]);
  const [stats, setStats] = useState({ taken: 0, skipped: 0, total: 0, adherence_rate: 100 });
  const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split('T')[0]);
  const [loading, setLoading] = useState(true);
  const [showAllSlots, setShowAllSlots] = useState(false);

  const isToday = selectedDate === new Date().toISOString().split('T')[0];

  const currentSlot = useMemo(() => {
    const hour = new Date().getHours();
    if (hour >= 5 && hour < 12) return 'morning';
    if (hour >= 12 && hour < 17) return 'afternoon';
    if (hour >= 17 && hour < 21) return 'evening';
    return 'night';
  }, []);

  const shouldShowSlot = (slotName) => {
    if (!isToday || showAllSlots) return true;
    return slotName === currentSlot || slotName === 'general' || slotName === 'with meals';
  };

  const isPastDate = useMemo(() => {
    const today = new Date().toISOString().split('T')[0];
    return selectedDate < today;
  }, [selectedDate]);

  const isFutureSlot = (slotName) => {
    if (!isToday) return false;
    const slotOrder = ['morning', 'afternoon', 'evening', 'night'];
    const currentIdx = slotOrder.indexOf(currentSlot);
    const targetIdx = slotOrder.indexOf(slotName);
    
    if (currentIdx === -1 || targetIdx === -1) return false;
    return targetIdx > currentIdx;
  };

  // Generate last 7 days memoized
  const timelineDays = useMemo(() => {
    const days = [];
    for (let i = 6; i >= 0; i--) {
      const d = new Date();
      d.setDate(d.getDate() - i);
      days.push({
        dateStr: d.toISOString().split('T')[0],
        dayName: d.toLocaleDateString('en-US', { weekday: 'short' }),
        dayNum: d.getDate(),
      });
    }
    return days;
  }, []);

  const fetchData = useCallback(async () => {
    setLoading(true);
    try {
      // Fetch medications & prescriptions
      const medRes = await axios.get(`${API}/medications`);
      const presRes = await axios.get(`${API}/prescriptions`);
      setMedications(medRes.data);
      setPrescriptions(presRes.data);

      // Fetch logs for the 7-day range
      const startDate = timelineDays[0].dateStr;
      const endDate = timelineDays[6].dateStr;
      const logsRes = await axios.get(`${API}/adherence`, {
        params: { start_date: startDate, end_date: endDate }
      });
      setLogs(logsRes.data);

      // Fetch stats for the 7-day range
      const statsRes = await axios.get(`${API}/adherence/stats`, {
        params: { start_date: startDate, end_date: endDate }
      });
      setStats(statsRes.data);
    } catch (error) {
      console.error('Error fetching tracker data:', error);
      toast.error('Failed to load tracker data');
    } finally {
      setLoading(false);
    }
  }, [timelineDays]);

  useEffect(() => {
    fetchData();
  }, [selectedDate, fetchData]);

  const allMedications = deduplicateMedications([
    ...medications,
    ...prescriptions.flatMap(p => p.medications)
  ]);

  // Map of medication ID/name -> list of logs for the selected date
  const getLogStatus = (medId, timeSlot) => {
    const log = logs.find(
      l => l.medication_id === medId && l.date === selectedDate && l.time_slot === timeSlot
    );
    return log ? log.status : null; // 'taken', 'skipped', or null
  };

  const handleLogAdherence = async (med, timeSlot, status) => {
    const medId = med.id || med.name;
    const medName = med.name;
    
    try {
      await axios.post(`${API}/adherence`, {
        medication_id: medId,
        medication_name: medName,
        date: selectedDate,
        time_slot: timeSlot,
        status: status
      });
      
      toast.success(`Logged ${medName} (${timeSlot}) as ${status}!`);
      
      // Refresh logs & stats
      const startDate = timelineDays[0].dateStr;
      const endDate = timelineDays[6].dateStr;
      const logsRes = await axios.get(`${API}/adherence`, {
        params: { start_date: startDate, end_date: endDate }
      });
      setLogs(logsRes.data);

      const statsRes = await axios.get(`${API}/adherence/stats`, {
        params: { start_date: startDate, end_date: endDate }
      });
      setStats(statsRes.data);
    } catch (error) {
      console.error('Error logging adherence:', error);
      toast.error('Failed to log adherence status');
    }
  };

  // Group medications by time slots for the daily checklist
  const getScheduledSlotsForDay = () => {
    const slots = {
      morning: [],
      afternoon: [],
      evening: [],
      night: [],
      'with meals': [],
      general: []
    };

    allMedications.forEach(med => {
      const timings = med.timing && med.timing.length > 0 ? med.timing : ['general'];
      timings.forEach(time => {
        const slotKey = slots[time] ? time : 'general';
        slots[slotKey].push(med);
      });
    });

    return slots;
  };

  const scheduledSlots = getScheduledSlotsForDay();
  const hasAnyScheduled = Object.values(scheduledSlots).some(arr => arr.length > 0);

  // Motivational nudge based on adherence rate
  const getNudgeMessage = () => {
    const rate = stats.adherence_rate;
    if (rate >= 90) return "Exceptional consistency! Keeping steady medication levels helps your body recover and stay strong.";
    if (rate >= 75) return "Great job! A few missed doses happen, but staying close to 100% keeps your health on track.";
    if (rate > 0) return "Every dose is a step toward feeling better. Link your schedule to daily habits to help you remember!";
    return "No compliance logged for this week yet. Start logging today to take control of your wellness journey!";
  };

  return (
    <div className="min-h-screen bg-paper py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Header */}
        <div className="mb-12">
          <h1 className="font-fraunces text-5xl md:text-7xl font-light leading-[0.95] text-stone-900 mb-4">
            Daily Tracker
          </h1>
          <p className="text-lg md:text-xl leading-relaxed text-stone-600 font-jakarta">
            Log your daily medication intake and review consistency
          </p>
        </div>

        {/* Weekly Stats Card */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-12">
          <div className="lg:col-span-2 bg-white rounded-3xl border border-stone-100 shadow-[0_8px_30px_rgb(0,0,0,0.04)] p-8 flex flex-col md:flex-row items-center justify-between gap-6">
            <div className="space-y-3 flex-1">
              <span className="inline-block bg-sage/10 text-sage px-3 py-1 rounded-full text-xs font-jakarta font-medium">
                Behavioral Nudge
              </span>
              <h3 className="font-fraunces text-2xl font-semibold text-stone-900">
                Why Compliance Matters
              </h3>
              <p className="text-stone-600 font-jakarta leading-relaxed text-sm">
                {getNudgeMessage()}
              </p>
            </div>
            
            <div className="flex flex-col items-center justify-center p-6 bg-sage/5 rounded-2xl min-w-[180px]">
              <span className="text-sm font-bold uppercase tracking-widest text-sage font-jakarta mb-1">
                Weekly Adherence
              </span>
              <span className="font-fraunces text-5xl font-light text-stone-900">
                {stats.adherence_rate}%
              </span>
              <span className="text-xs text-stone-500 font-jakarta mt-2">
                {stats.taken} of {stats.total} doses taken
              </span>
            </div>
          </div>

          <div className="bg-white rounded-3xl border border-stone-100 shadow-[0_8px_30px_rgb(0,0,0,0.04)] p-8 flex flex-col justify-between">
            <h3 className="font-fraunces text-xl font-semibold text-stone-900 mb-4">
              Week Summary
            </h3>
            <div className="space-y-4">
              <div className="flex justify-between items-center text-sm font-jakarta">
                <span className="text-stone-600">Total Doses Taken</span>
                <span className="font-bold text-sage">{stats.taken}</span>
              </div>
              <div className="flex justify-between items-center text-sm font-jakarta">
                <span className="text-stone-600">Total Doses Skipped</span>
                <span className="font-bold text-clay">{stats.skipped}</span>
              </div>
              <div className="w-full bg-stone-100 h-2.5 rounded-full overflow-hidden">
                <div 
                  className="bg-sage h-full transition-all duration-500" 
                  style={{ width: `${stats.adherence_rate}%` }}
                />
              </div>
            </div>
          </div>
        </div>

        {/* Date Timeline Switcher */}
        <div className="bg-white rounded-3xl border border-stone-100 shadow-[0_8px_30px_rgb(0,0,0,0.04)] p-6 mb-8">
          <div className="flex justify-between items-center overflow-x-auto gap-4 py-2">
            {timelineDays.map((day) => {
              const isSelected = day.dateStr === selectedDate;
              return (
                <button
                  key={day.dateStr}
                  onClick={() => setSelectedDate(day.dateStr)}
                  className={`flex flex-col items-center justify-center p-4 rounded-2xl min-w-[70px] transition-all duration-300 ${
                    isSelected 
                      ? 'bg-sage text-white shadow-lg -translate-y-1' 
                      : 'hover:bg-stone-50 text-stone-700'
                  }`}
                >
                  <span className="text-xs font-bold uppercase tracking-widest opacity-80 mb-1">
                    {day.dayName}
                  </span>
                  <span className="font-fraunces text-2xl font-normal">
                    {day.dayNum}
                  </span>
                </button>
              );
            })}
          </div>
        </div>

        {/* Daily Checklist */}
        {isToday && (
          <div className="flex items-center justify-between mb-6 bg-white rounded-2xl border border-stone-100 p-4 shadow-[0_4px_20px_rgb(0,0,0,0.02)]">
            <div className="flex items-center gap-2">
              <span className="text-xl">⏰</span>
              <p className="text-stone-700 font-jakarta text-sm">
                It's currently <strong className="capitalize">{currentSlot}</strong>. Showing active schedules.
              </p>
            </div>
            <button
              onClick={() => setShowAllSlots(!showAllSlots)}
              className="text-xs font-bold uppercase tracking-widest text-sage hover:text-sage/80 font-jakarta"
            >
              {showAllSlots ? 'Show Active Only' : 'Show All Slots'}
            </button>
          </div>
        )}

        {loading ? (
          <div className="text-center py-12">
            <p className="text-stone-600 font-jakarta">Loading checklist...</p>
          </div>
        ) : !hasAnyScheduled ? (
          <div className="bg-white rounded-3xl border border-stone-100 shadow-[0_8px_30px_rgb(0,0,0,0.04)] p-12 text-center">
            <div className="w-20 h-20 bg-sage/10 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-4xl">🗓️</span>
            </div>
            <h3 className="font-fraunces text-2xl font-semibold text-stone-900 mb-2">
              No medications scheduled
            </h3>
            <p className="text-stone-600 font-jakarta">
              Add some medications on the Medications page first to populate your timeline!
            </p>
          </div>
        ) : (
          <div className="space-y-8">
            {Object.keys(scheduledSlots).filter(shouldShowSlot).map((slotName) => {
              const meds = scheduledSlots[slotName];
              if (meds.length === 0) return null;

              return (
                <div key={slotName} className="space-y-4">
                  <h3 className="font-fraunces text-2xl font-normal text-stone-900 capitalize flex items-center gap-2">
                    <span className="w-2.5 h-2.5 rounded-full bg-sage" />
                    {slotName} Schedule
                  </h3>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {meds.map((med, idx) => {
                      const medId = med.id || med.name;
                      const status = getLogStatus(medId, slotName);

                      return (
                        <div 
                          key={medId + idx}
                          className="bg-white rounded-2xl border border-stone-100 shadow-[0_4px_20px_rgb(0,0,0,0.02)] p-6 flex items-center justify-between gap-4"
                        >
                          <div>
                            <h4 className="font-fraunces text-xl font-semibold text-stone-900">
                              {med.name}
                            </h4>
                            <p className="text-stone-500 font-jakarta text-sm mt-1">
                              {med.dosage} • {med.frequency}
                            </p>
                          </div>

                          {(() => {
                            const isFuture = isFutureSlot(slotName);
                            const isDisabled = (isPastDate && !status) || isFuture;
                            return (
                              <div className="flex flex-col items-end gap-1.5">
                                <div className="flex gap-2">
                                  <button
                                    onClick={() => handleLogAdherence(med, slotName, 'taken')}
                                    disabled={isDisabled}
                                    className={`px-4 py-2 rounded-full font-jakarta text-xs font-semibold shadow-sm transition-all duration-200 ${
                                      status === 'taken'
                                        ? 'bg-sage text-white shadow-md'
                                        : isDisabled
                                          ? 'bg-stone-100 text-stone-400 cursor-not-allowed'
                                          : 'bg-stone-50 hover:bg-stone-100 text-stone-700'
                                    }`}
                                  >
                                    ✓ Taken
                                  </button>
                                  <button
                                    onClick={() => handleLogAdherence(med, slotName, 'skipped')}
                                    disabled={isDisabled}
                                    className={`px-4 py-2 rounded-full font-jakarta text-xs font-semibold shadow-sm transition-all duration-200 ${
                                      status === 'skipped'
                                        ? 'bg-clay text-white shadow-md'
                                        : isDisabled
                                          ? 'bg-stone-100 text-stone-400 cursor-not-allowed'
                                          : 'bg-stone-50 hover:bg-stone-100 text-stone-700'
                                    }`}
                                  >
                                    ✗ Skipped
                                  </button>
                                </div>
                                {isDisabled && (
                                  <span className="text-[10px] font-bold uppercase tracking-widest text-clay font-jakarta mr-1">
                                    {isFuture ? 'Locked (Future Slot)' : 'Locked (Day Passed)'}
                                  </span>
                                )}
                              </div>
                            );
                          })()}
                        </div>
                      );
                    })}
                  </div>
                </div>
              );
            })}
          </div>
        )}

      </div>
    </div>
  );
};

export default TrackerPage;
