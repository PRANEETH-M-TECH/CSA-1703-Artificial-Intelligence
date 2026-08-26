"""
Module 1 — Intelligent Scheduling Engine
Syllabus mapping: Unit I (problem formulation, intelligent agents),
                   Unit II (informed search, A*, greedy best-first, CSP)

Formulation
-----------
Constraint Satisfaction Problem:
  - Variables  : each pending Task
  - Domain     : discrete candidate start-time slots (15-minute granularity)
                 inside the user's daily work-hour window, over a fixed
                 planning horizon (default 21 days from now)
  - Constraints:
        1. no-overlap   -> a slot cannot intersect another task already
                            placed in this schedule
        2. deadline      -> soft constraint: violating it costs "lateness"
        3. work-hours    -> slot + duration must fit inside
                             [work_start_hour, work_end_hour) on that day
        4. no-past       -> a slot cannot start before "now"

Search
------
Tasks (CSP variables) are ordered most-constrained-first: earliest
deadline, then highest priority (a classic scheduling MRV-style ordering).

For each task, the best slot is found with an **A\\* search** over the
candidate slots:
    g(slot) = lateness_minutes(slot)      -- actual incurred cost
    h(slot) = minutes_from_now(slot) * EPS -- tiny admissible tie-break
              that nudges the frontier towards earlier slots (i.e.
              maximises slack) whenever two slots tie on lateness
    f(slot) = g(slot) + h(slot)
A min-heap priority queue expands candidates in increasing f, so the
first feasible slot popped is the A*-optimal choice for that task.
"""
import heapq
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Optional, Tuple

SLOT_GRANULARITY_MIN = 15
PLANNING_HORIZON_DAYS = 21
TIE_BREAK_EPS = 1e-6


@dataclass
class SchedulableTask:
    id: int
    title: str
    category: str
    priority: int
    duration_minutes: int
    deadline: datetime


@dataclass
class PlacedEntry:
    task_id: int
    task_title: str
    category: str
    priority: int
    start_time: datetime
    end_time: datetime
    slack_minutes: float


def _overlaps(start_a, end_a, start_b, end_b) -> bool:
    return start_a < end_b and start_b < end_a


def _candidate_slots(now: datetime, duration: timedelta, work_start_hour: int, work_end_hour: int):
    """Generate the CSP domain: valid (start, end) pairs inside work hours."""
    day_cursor = now.replace(minute=(now.minute // SLOT_GRANULARITY_MIN) * SLOT_GRANULARITY_MIN,
                              second=0, microsecond=0)
    for day_offset in range(PLANNING_HORIZON_DAYS):
        day = (now + timedelta(days=day_offset)).date()
        window_start = datetime(day.year, day.month, day.day, work_start_hour)
        window_end = datetime(day.year, day.month, day.day, work_end_hour)
        slot = max(window_start, day_cursor if day_offset == 0 else window_start)
        while slot + duration <= window_end:
            if slot >= now:
                yield slot, slot + duration
            slot += timedelta(minutes=SLOT_GRANULARITY_MIN)


def _a_star_best_slot(
    now: datetime,
    task: SchedulableTask,
    occupied: List[Tuple[datetime, datetime]],
    work_start_hour: int,
    work_end_hour: int,
) -> Optional[PlacedEntry]:
    duration = timedelta(minutes=task.duration_minutes)
    frontier: List[Tuple[float, int, datetime, datetime]] = []
    counter = 0

    for start, end in _candidate_slots(now, duration, work_start_hour, work_end_hour):
        if any(_overlaps(start, end, os_, oe_) for os_, oe_ in occupied):
            continue
        lateness = max(0.0, (end - task.deadline).total_seconds() / 60.0)
        minutes_from_now = (start - now).total_seconds() / 60.0
        g = lateness
        h = minutes_from_now * TIE_BREAK_EPS
        f = g + h
        counter += 1
        heapq.heappush(frontier, (f, counter, start, end))
        if counter >= 4000:  # bound the search space for responsiveness
            break

    if not frontier:
        return None

    f_best, _, start, end = heapq.heappop(frontier)
    lateness = max(0.0, (end - task.deadline).total_seconds() / 60.0)
    slack = (task.deadline - end).total_seconds() / 60.0
    return PlacedEntry(
        task_id=task.id,
        task_title=task.title,
        category=task.category,
        priority=task.priority,
        start_time=start,
        end_time=end,
        slack_minutes=slack,
    )


def generate_schedule(
    tasks: List[SchedulableTask],
    now: Optional[datetime] = None,
    work_start_hour: int = 9,
    work_end_hour: int = 18,
    fixed_occupied: Optional[List[Tuple[datetime, datetime]]] = None,
) -> Tuple[List[PlacedEntry], List[int], float]:
    """
    Runs the CSP + A* search described above.
    Returns (placed_entries, unscheduled_task_ids, total_lateness_minutes).
    """
    now = now or datetime.utcnow()
    ordered = sorted(tasks, key=lambda t: (t.deadline, -t.priority))

    occupied: List[Tuple[datetime, datetime]] = list(fixed_occupied or [])
    placed: List[PlacedEntry] = []
    unscheduled: List[int] = []
    total_lateness = 0.0

    for task in ordered:
        entry = _a_star_best_slot(now, task, occupied, work_start_hour, work_end_hour)
        if entry is None:
            unscheduled.append(task.id)
            continue
        placed.append(entry)
        occupied.append((entry.start_time, entry.end_time))
        total_lateness += max(0.0, (entry.end_time - task.deadline).total_seconds() / 60.0)

    return placed, unscheduled, total_lateness
