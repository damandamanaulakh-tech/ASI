"""The sequence execution kernel — the owner's corrections made runnable.

Protocol: ``docs/method/01C_SEQUENCE_PROTOCOL.md``. His rule that this module
exists to enforce:

    "Without the ledger, closure is philosophy. With the ledger, closure
    becomes machine-executable."

The six core objects, exactly as he specified them:

    Threshold      why NOW — separated from trigger, carried on edges
    EntityOutcome  what happened to the thing followed — orthogonal to
                   whether the sequence finished
    SpawnContract  a child must know why it exists; close_condition is not
                   acceptance_condition
    Ledger         the open-sequence register; the barrier law; no reopen
    DriverOrigin   why a sequence was opened — Want beside Need, never inside
                   the spine
    Controller     who or what performs the transition — mandatory

The invariants enforced here:
  - THE BARRIER LAW: no dependent edge may cross a closure barrier while a
    required predecessor/child contract remains open. The parent SUSPENDS at
    the barrier; its independent branches keep moving.
  - No in-place loop: unresolved work spawns a NEW sequence; nothing recycles
    inside itself.
  - No reopen: a closed sequence is never reopened. New work creates a new
    sequence that references the closed one.
  - CLOSURE is a sequence word. Entities persist, cohere, degrade, terminate.
"""
from __future__ import annotations

import enum
from dataclasses import dataclass, field
from typing import Callable, Optional


# ------------------------------------------------------------------ vocabularies

class DriverOrigin(enum.Enum):
    """Why a sequence was opened. Want is a driver, never a spine stage."""
    NATURAL_DYNAMICS = "natural dynamics"
    NEED = "need"                      # viability imposes a condition
    WANT = "want"                      # preference creates a desired difference
    EXTERNAL_DEMAND = "external demand"
    GOAL = "goal"                      # represented target condition
    OPPORTUNITY = "opportunity"
    CURIOSITY = "curiosity"            # uncertainty itself motivates
    DAMAGE = "damage/deviation"        # restoration requirement
    RELATIONAL = "relational"          # produced by interaction between systems


class Controller(enum.Enum):
    """Who or what performs the transition. Mandatory on every sequence."""
    NONE_NATURAL = "none / natural dynamics"
    SELF = "self"
    DISTRIBUTED_SELF = "distributed self"
    EXTERNAL = "external"
    JOINT = "joint"
    META = "meta-controller"


class ThresholdType(enum.Enum):
    VALUE = "value"                    # voltage > / < X
    RANGE = "range"                    # enter / leave viable band
    TIME = "time"                      # deadline · duration · age
    EVENT = "event"                    # collision · message · child returns
    COUNT_QUORUM = "count/quorum"      # N children closed · majority
    CONFIDENCE = "confidence/proof"    # evidence >= required confidence
    STATE = "state"                    # entity enters condition X
    ABSENCE = "absence"                # expected thing has not occurred
    COMPOSITE = "composite"            # A AND B · A OR B · A unless C


class SequenceClosure(enum.Enum):
    """Terminal states of a SEQUENCE. Never used for entities."""
    SUCCESS = "closed success"
    FAILURE = "closed failure"
    PARTIAL = "closed partial"
    UNKNOWN = "closed unknown"
    UNAVAILABLE = "closed unavailable"
    NOT_APPLICABLE = "closed not-applicable"


class EntityOutcome(enum.Enum):
    """What happened to the thing followed. Orthogonal to SequenceClosure:
    a destruction sequence closes SUCCESS with the entity TERMINATED; a repair
    sequence closes FAILURE with the entity still existing, DEGRADED."""
    PERSISTS = "persists"
    MODIFIED = "modified"
    DEGRADED = "degraded"
    REPAIRED = "repaired"
    TRANSFORMED = "transformed"        # identity continuity decision required
    SPLIT = "split"
    MERGED = "merged"
    CONSUMED = "consumed/incorporated"
    TERMINATED = "terminated/destroyed"
    NEW_INSTANTIATED = "new entity instantiated"
    ABSENT = "absent"
    UNKNOWN = "unknown"
    NOT_APPLICABLE = "not applicable"


class RowState(enum.Enum):
    OPEN = "open"
    SUSPENDED = "suspended"            # waiting at a closure barrier
    CLOSED = "closed"


# ------------------------------------------------------------------ threshold

#: The recheck contract — the answer to "re-checked WHEN?". A dormant edge
#: waits for one of these, never for a vague "later".
RECHECK_WHEN = ("child returns", "resource-state changes",
                "deadline reached", "external event received")


@dataclass
class Threshold:
    """The condition that must become true before a transition may fire.

    A trigger is something that happened; the threshold is what must hold.
    A condition can exist for years without causing a transition — this
    object is the "why now".
    """
    kind: ThresholdType
    condition: str
    predicate: Optional[Callable[[dict], bool]] = None

    def satisfied(self, context: dict) -> Optional[bool]:
        """True/False when evaluable; None when no evaluator was supplied.
        None is not success: the edge stays dormant and says why."""
        if self.predicate is None:
            return None
        return bool(self.predicate(context))


@dataclass
class Edge:
    """An executable transition. Thresholds live on edges, not as stages."""
    source: str
    target: str
    activation_event: str
    threshold: Threshold
    evaluator: str = "self"
    status: str = "dormant"

    def try_fire(self, context: dict) -> bool:
        ok = self.threshold.satisfied(context)
        if ok is None:
            self.status = f"dormant (no evaluator; recheck when: {', '.join(RECHECK_WHEN)})"
            return False
        if not ok:
            self.status = f"dormant (threshold not met: {self.threshold.condition})"
            return False
        self.status = "fired"
        return True


# ------------------------------------------------------------------ contracts

class ContractError(ValueError):
    """A spawn without a stated reason or close/acceptance condition."""


class SequenceClosedError(RuntimeError):
    """Raised on any attempt to reopen. A closed sequence is never reopened;
    new work creates a new sequence that references it."""


class BarrierError(RuntimeError):
    """A dependent edge tried to cross a barrier with required work open."""


@dataclass
class SpawnContract:
    """A child must know exactly why it exists and what completion means.

    close_condition is the child's own finish line ("search completed").
    acceptance_condition is the parent's requirement ("usable water found").
    They are not identical: a child may close FAILURE honestly while the
    parent's requirement stays unresolved.
    """
    child_sequence_id: str
    parent_sequence_id: str
    parent_node_id: str
    spawn_reason: str
    close_condition: str
    acceptance_condition: str
    requested_result: str = ""
    return_schema: str = ""
    scope: str = ""
    context_snapshot: dict = field(default_factory=dict)
    controller: Controller = Controller.SELF
    activation_condition: str = ""
    required: bool = True
    epistemic_requirement: str = ""
    proof_depth: int = 0
    dependencies: tuple = ()
    deadline_or_time_condition: str = ""
    termination_policy: str = ""

    def __post_init__(self) -> None:
        for f in ("spawn_reason", "close_condition", "acceptance_condition"):
            if not getattr(self, f).strip():
                raise ContractError(f"spawn contract missing {f} — a child "
                                    "must know why it exists and what done means")


@dataclass
class ClosurePacket:
    """What a closing sequence returns. Carries BOTH statuses — one for the
    sequence, one for the entity — never one word doing two jobs."""
    sequence_closure: SequenceClosure
    entity_outcome: EntityOutcome
    result_set: dict = field(default_factory=dict)
    effects: list = field(default_factory=list)
    trace_memory: dict = field(default_factory=dict)
    evidence: list = field(default_factory=list)
    unresolved_conditions: list = field(default_factory=list)
    reusable_capability: list = field(default_factory=list)
    next_sequence_seeds: list = field(default_factory=list)


# ------------------------------------------------------------------ the ledger

@dataclass
class _Row:
    seq_id: str
    parent_id: Optional[str]
    parent_node: Optional[str]
    required: bool
    controller: Controller
    contract: Optional[SpawnContract]
    state: RowState = RowState.OPEN
    driver: DriverOrigin = DriverOrigin.NEED
    packet: Optional[ClosurePacket] = None
    accepted: Optional[bool] = None
    references: tuple = ()             # closed sequences this one builds on


class Ledger:
    """The open-sequence register. The enforcement mechanism.

    Enforces: the barrier law, required-children-terminal before parent node
    close, accepted returns, and no reopen — ever.
    """

    def __init__(self) -> None:
        self._rows: dict[str, _Row] = {}
        self.archive: list[str] = []

    # -- opening ----------------------------------------------------------
    def open_root(self, seq_id: str, *, driver: DriverOrigin,
                  controller: Controller,
                  references: tuple = ()) -> None:
        if seq_id in self._rows:
            raise ValueError(f"{seq_id} already on the ledger")
        for ref in references:
            row = self._rows.get(ref)
            if row is not None and row.state is not RowState.CLOSED:
                raise ValueError(f"{seq_id} may only reference CLOSED "
                                 f"sequences; {ref} is {row.state.value}")
        self._rows[seq_id] = _Row(seq_id, None, None, True, controller, None,
                                  driver=driver, references=references)

    def spawn(self, contract: SpawnContract,
              driver: DriverOrigin = DriverOrigin.NEED) -> None:
        parent = self._row(contract.parent_sequence_id)
        if parent.state is RowState.CLOSED:
            raise SequenceClosedError(
                f"{parent.seq_id} is closed and is never reopened — open a "
                "new sequence that references it instead")
        self._rows[contract.child_sequence_id] = _Row(
            contract.child_sequence_id, contract.parent_sequence_id,
            contract.parent_node_id, contract.required, contract.controller,
            contract, driver=driver)
        # the parent SUSPENDS at the barrier; other branches keep moving
        parent.state = RowState.SUSPENDED

    # -- queries ----------------------------------------------------------
    def _row(self, seq_id: str) -> _Row:
        if seq_id not in self._rows:
            raise KeyError(f"{seq_id} not on the ledger")
        return self._rows[seq_id]

    def state(self, seq_id: str) -> RowState:
        return self._row(seq_id).state

    def required_open_children(self, parent_id: str,
                               parent_node: Optional[str] = None) -> list[str]:
        return [r.seq_id for r in self._rows.values()
                if r.parent_id == parent_id and r.required
                and r.state is not RowState.CLOSED
                and (parent_node is None or r.parent_node == parent_node)]

    def all_required_returns_accepted(self, parent_id: str,
                                      parent_node: Optional[str] = None) -> bool:
        """Per node: every required child closed, and the requirement met by
        at least one ACCEPTED return. A child that closed FAILURE does not
        block forever — it is a superseded attempt with its packet on record,
        exactly the availability re-sequence: locate fails, build fails,
        substitute succeeds, the node closes."""
        by_node: dict[Optional[str], list[_Row]] = {}
        for r in self._rows.values():
            if (r.parent_id == parent_id and r.required
                    and (parent_node is None or r.parent_node == parent_node)):
                by_node.setdefault(r.parent_node, []).append(r)
        for rows in by_node.values():
            if any(r.state is not RowState.CLOSED for r in rows):
                return False
            if not any(r.accepted for r in rows):
                return False            # all attempts closed, none met the need
        return True

    def can_cross(self, seq_id: str, node: str) -> bool:
        """THE BARRIER LAW. False while required child contracts at this node
        remain open or unaccepted. Other nodes of the same sequence are free —
        independent branches progress."""
        return (not self.required_open_children(seq_id, node)
                and self.all_required_returns_accepted(seq_id, node))

    def open_rows(self) -> list[str]:
        return [r.seq_id for r in self._rows.values()
                if r.state is not RowState.CLOSED]

    # -- closing ----------------------------------------------------------
    def close(self, seq_id: str, packet: ClosurePacket,
              accepted: Optional[bool] = None) -> ClosurePacket:
        """Close a sequence with its packet. Refuses while required children
        are open. `accepted` records the PARENT's acceptance_condition verdict
        — independent of the child's own closure status."""
        row = self._row(seq_id)
        if row.state is RowState.CLOSED:
            raise SequenceClosedError(
                f"{seq_id} is already closed and is never reopened")
        blockers = self.required_open_children(seq_id)
        if blockers:
            raise BarrierError(
                f"{seq_id} cannot close: required children open: {blockers}")
        row.state = RowState.CLOSED
        row.packet = packet
        if accepted is None and row.contract is not None:
            # honest default: a FAILURE close does not satisfy acceptance
            accepted = packet.sequence_closure is SequenceClosure.SUCCESS
        row.accepted = accepted
        parent = self._rows.get(row.parent_id) if row.parent_id else None
        if parent is None:
            self.archive.append(seq_id)          # root closed → archive
        elif parent.state is RowState.SUSPENDED:
            if not self.required_open_children(parent.seq_id):
                parent.state = RowState.OPEN     # barrier lifts; parent resumes
        return packet

    def finished(self) -> bool:
        """The only condition under which the whole run is finished:
        an empty open set. Everything closed, no open node."""
        return not self.open_rows()


# ------------------------------------------------------------------- the demo

def _demo() -> None:                    # pragma: no cover
    """The water example — close_condition vs acceptance_condition, the
    barrier, and the no-reopen law, end to end."""
    led = Ledger()
    led.open_root("S0", driver=DriverOrigin.NEED, controller=Controller.SELF)

    edge = Edge("state:thirsty", "node:DRINK", "reserves fell",
                Threshold(ThresholdType.RANGE, "hydration below viable band",
                          lambda c: c["hydration"] < 0.4))
    ctx = {"hydration": 0.35}
    print(f"threshold fires: {edge.try_fire(ctx)}  [{edge.status}]")

    print(f"can cross DRINK before children: {led.can_cross('S0', 'node:DRINK')}")

    c1 = SpawnContract("S0.1", "S0", "node:DRINK",
                       spawn_reason="no water available",
                       close_condition="search completed",
                       acceptance_condition="usable water found")
    led.spawn(c1)
    print(f"S0 after spawn: {led.state('S0').value}")
    print(f"barrier holds:  can cross = {led.can_cross('S0', 'node:DRINK')}")

    # child closes HONESTLY as failure — search done, no water
    led.close("S0.1", ClosurePacket(SequenceClosure.FAILURE,
                                    EntityOutcome.NOT_APPLICABLE,
                                    result_set={"found": None}))
    print(f"S0.1 closed FAILURE; accepted={led._row('S0.1').accepted} "
          f"→ can cross = {led.can_cross('S0', 'node:DRINK')}")

    c2 = SpawnContract("S0.2", "S0", "node:DRINK",
                       spawn_reason="locate failed — build access",
                       close_condition="dig completed",
                       acceptance_condition="usable water found")
    led.spawn(c2)
    led.close("S0.2", ClosurePacket(SequenceClosure.SUCCESS,
                                    EntityOutcome.NEW_INSTANTIATED,
                                    result_set={"found": "well"}))
    print(f"S0.2 closed SUCCESS → can cross = {led.can_cross('S0', 'node:DRINK')}")

    led.close("S0", ClosurePacket(SequenceClosure.SUCCESS,
                                  EntityOutcome.PERSISTS,
                                  next_sequence_seeds=["maintain the well"]))
    print(f"root archived: {led.archive}  finished: {led.finished()}")

    try:
        led.spawn(SpawnContract("S0.3", "S0", "node:DRINK",
                                spawn_reason="x", close_condition="y",
                                acceptance_condition="z"))
    except SequenceClosedError as e:
        print(f"no reopen: {e}")


if __name__ == "__main__":              # pragma: no cover
    _demo()
