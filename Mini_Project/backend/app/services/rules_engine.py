"""
Module 2 — Reasoning & Conflict Resolution
Syllabus mapping: Unit III (propositional & first-order logic,
                             forward/backward chaining, resolution)

A small hand-written knowledge base of scheduling rules. Facts are
derived from the current generated schedule + task list, forward
chaining is run once to discover every conflict (perceive -> reason),
and backward chaining is run on demand per-conflict to produce a
human-readable "why was this flagged?" derivation trace.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional, Tuple

PRIORITY_LABEL = {1: "Low", 2: "Medium", 3: "High"}


@dataclass
class Fact:
    predicate: str          # e.g. "overlap", "overdue", "priority_gt"
    args: tuple              # e.g. (task_a_id, task_b_id)
    support: List[str]       # human-readable premises that produced this fact
    rule: str                # name of the rule that fired


@dataclass
class DetectedConflict:
    conflict_type: str
    task_a_id: Optional[int]
    task_b_id: Optional[int]
    description: str
    suggestion: str
    trace: List[str]


def _fmt_task(t) -> str:
    return f'"{t.title}" (priority={PRIORITY_LABEL.get(t.priority, t.priority)}, category={t.category})'


def forward_chain(schedule_entries: List, tasks_by_id: Dict[int, object], now: Optional[datetime] = None) -> List[DetectedConflict]:
    """
    Forward chaining: apply every rule to the current fact base
    (schedule + tasks) until no new conflict facts are produced.
    Rule set (R1-R11) is intentionally small and explicit so it can be
    demoed/explained in a viva.
    """
    now = now or datetime.utcnow()
    conflicts: List[DetectedConflict] = []

    # ---- R1-R4: overlap detection + priority-based resolution ----
    entries = sorted(schedule_entries, key=lambda e: e.start_time)
    for i in range(len(entries)):
        for j in range(i + 1, len(entries)):
            a, b = entries[i], entries[j]
            if a.start_time < b.end_time and b.start_time < a.end_time:
                task_a = tasks_by_id.get(a.task_id)
                task_b = tasks_by_id.get(b.task_id)
                if not task_a or not task_b:
                    continue
                trace = [
                    f"R1: scheduled({task_a.title}) at [{a.start_time.strftime('%a %H:%M')}-{a.end_time.strftime('%H:%M')}]",
                    f"R1: scheduled({task_b.title}) at [{b.start_time.strftime('%a %H:%M')}-{b.end_time.strftime('%H:%M')}]",
                    f"R1: IF task_A.time overlaps task_B.time THEN conflict(A, B)  -->  overlap({task_a.title}, {task_b.title}) is TRUE",
                ]
                if task_a.priority > task_b.priority:
                    trace.append(f"R2: IF conflict(A,B) AND priority(A) > priority(B) THEN suggest(reschedule B)  -->  priority({task_a.title})={task_a.priority} > priority({task_b.title})={task_b.priority}")
                    suggestion = f'Reschedule {_fmt_task(task_b)} — it has lower priority than {_fmt_task(task_a)}.'
                elif task_b.priority > task_a.priority:
                    trace.append(f"R3: IF conflict(A,B) AND priority(B) > priority(A) THEN suggest(reschedule A)  -->  priority({task_b.title})={task_b.priority} > priority({task_a.title})={task_a.priority}")
                    suggestion = f'Reschedule {_fmt_task(task_a)} — it has lower priority than {_fmt_task(task_b)}.'
                else:
                    later = task_b if b.start_time > a.start_time else task_a
                    trace.append(f"R4: IF conflict(A,B) AND priority(A) == priority(B) THEN suggest(reschedule later task)  -->  {later.title} starts later")
                    suggestion = f'Reschedule {_fmt_task(later)} — equal priority, it was placed later.'

                conflicts.append(DetectedConflict(
                    conflict_type="overlap",
                    task_a_id=task_a.id,
                    task_b_id=task_b.id,
                    description=f'"{task_a.title}" overlaps "{task_b.title}" on {a.start_time.strftime("%a %d %b")}.',
                    suggestion=suggestion,
                    trace=trace,
                ))

    # ---- R5-R6: overdue detection ----
    for task in tasks_by_id.values():
        if task.status != "completed" and task.deadline < now:
            trace = [
                f"R5: deadline({task.title}) = {task.deadline.strftime('%a %d %b %H:%M')} < now = {now.strftime('%a %d %b %H:%M')}",
                f"R5: status({task.title}) = '{task.status}' != 'completed'",
                f"R5: IF task.deadline < current_time AND task.status != complete THEN overdue(task)  -->  overdue({task.title}) is TRUE",
                f"R6: IF overdue(task) THEN suggest(immediate action)",
            ]
            conflicts.append(DetectedConflict(
                conflict_type="overdue",
                task_a_id=task.id,
                task_b_id=None,
                description=f'"{task.title}" is overdue (deadline was {task.deadline.strftime("%a %d %b %H:%M")}).',
                suggestion=f'Complete {_fmt_task(task)} immediately or push the deadline.',
                trace=trace,
            ))

    # ---- R7-R8: deadline overrun by the generated schedule itself ----
    for e in entries:
        task = tasks_by_id.get(e.task_id)
        if task and e.end_time > task.deadline and task.status != "completed":
            trace = [
                f"R7: scheduled_end({task.title}) = {e.end_time.strftime('%a %H:%M')} > deadline({task.title}) = {task.deadline.strftime('%a %H:%M')}",
                f"R7: IF scheduled_end(task) > deadline(task) THEN conflict_deadline_overrun(task)  -->  TRUE",
                f"R8: IF conflict_deadline_overrun(task) THEN suggest(shorten or reschedule earlier)",
            ]
            conflicts.append(DetectedConflict(
                conflict_type="deadline_overrun",
                task_a_id=task.id,
                task_b_id=None,
                description=f'The generated slot for "{task.title}" finishes after its own deadline.',
                suggestion=f'Shorten {_fmt_task(task)} or free up an earlier slot.',
                trace=trace,
            ))

    return conflicts


def backward_chain_explain(conflict, tasks_by_id: Dict[int, object]) -> List[str]:
    """
    Backward chaining: start from the goal fact conflict(conflict.id)
    and recursively ask "which rule's consequent matches this goal, and
    are its premises satisfied?" — reconstructing the derivation stored
    on the conflict at detection time. If the raw trace is unavailable,
    re-derive it from the current facts.
    """
    if conflict.rule_trace:
        import json
        try:
            return json.loads(conflict.rule_trace)
        except Exception:
            pass

    # Fallback re-derivation directly from current facts.
    steps = [f"GOAL: explain conflict({conflict.id}) of type '{conflict.conflict_type}'"]
    task_a = tasks_by_id.get(conflict.task_a_id) if conflict.task_a_id else None
    task_b = tasks_by_id.get(conflict.task_b_id) if conflict.task_b_id else None
    if task_a:
        steps.append(f"BACKWARD: is task_A={task_a.title} part of a matching rule consequent? checking premises...")
    if task_b:
        steps.append(f"BACKWARD: is task_B={task_b.title} part of a matching rule consequent? checking premises...")
    steps.append(f"CONCLUSION: {conflict.description}")
    steps.append(f"SUGGESTED FIX: {conflict.suggestion}")
    return steps
