from __future__ import annotations

import argparse
import random
import sys
import time
from collections import deque
from dataclasses import dataclass, field

# --------------------------------------------------------------------------
# configuration
# --------------------------------------------------------------------------

N = 11                      # maze grid size
BUFFER = 2                  # drawn Manhattan buffer around each mouse
COLLIDE_DIST = BUFFER - 1   # a step landing this close to a higher rank = verge of collision (d <= 1)
CLEAR_DIST = BUFFER + 1     # a yielding mouse resumes only once it is this far away (d >= 3)
WARN_TIERS = (6, 5, 4, 3)   # escalating proximity warnings
STUCK_LIMIT = 3             # consecutive YIELD ticks before an active back-off
STALL_LIMIT = 4             # ticks with nobody moving at all before the gridlock breaker fires
BACKSTACK_MAX = 400         # cap on remembered path history per mouse
LOOP_CHANCE = 0.10          # extra wall removals, so alternate routes exist

PRIORITY = (0, 1, 2)

MICE_DEF = [
    {"id": 0, "label": "ALPHA"},
    {"id": 1, "label": "BRAVO"},
    {"id": 2, "label": "CHARLIE"},
]


def rank_of(mouse_id: int) -> int:
    """0 = highest priority."""
    return PRIORITY.index(mouse_id)


def outranks(a: int, b: int) -> bool:
    return rank_of(a) < rank_of(b)


def higher_than(mouse_id: int):
    """Ids that outrank `mouse_id`, in rank order (highest first)."""
    return PRIORITY[: rank_of(mouse_id)]


# --------------------------------------------------------------------------
# geometry helpers
# --------------------------------------------------------------------------

Cell = tuple  # (x, y)


def manhattan(a: Cell, b: Cell) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def proximity_tier(d: int):
    """Tightest warning threshold a distance falls at or inside (None if clear)."""
    if d <= BUFFER:
        return None
    tier = None
    for w in WARN_TIERS:
        if d <= w:
            tier = w
    return tier


# --------------------------------------------------------------------------
# maze generation -- recursive backtracker, then punched loops
# --------------------------------------------------------------------------

DIRS = [(0, -1, "N", "S"), (0, 1, "S", "N"), (1, 0, "E", "W"), (-1, 0, "W", "E")]


def generate_maze(n: int, rng: random.Random):
    """Returns maze[y][x] = dict of wall flags {'N','S','E','W'} -> bool."""
    cells = [[{"N": True, "S": True, "E": True, "W": True} for _ in range(n)] for _ in range(n)]
    visited = [[False] * n for _ in range(n)]

    stack = [(0, 0)]
    visited[0][0] = True
    while stack:
        cx, cy = stack[-1]
        dirs = DIRS[:]
        rng.shuffle(dirs)
        moved = False
        for dx, dy, d, opp in dirs:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < n and 0 <= ny < n and not visited[ny][nx]:
                cells[cy][cx][d] = False
                cells[ny][nx][opp] = False
                visited[ny][nx] = True
                stack.append((nx, ny))
                moved = True
                break
        if not moved:
            stack.pop()

    # punch extra loops so alternate routes exist -- makes avoidance interesting
    for y in range(n):
        for x in range(n):
            if rng.random() < LOOP_CHANCE and x < n - 1 and cells[y][x]["E"]:
                cells[y][x]["E"] = False
                cells[y][x + 1]["W"] = False
            if rng.random() < LOOP_CHANCE and y < n - 1 and cells[y][x]["S"]:
                cells[y][x]["S"] = False
                cells[y + 1][x]["N"] = False
    return cells


def neighbors(maze, cell: Cell):
    x, y = cell
    c = maze[y][x]
    out = []
    if not c["N"]:
        out.append((x, y - 1))
    if not c["S"]:
        out.append((x, y + 1))
    if not c["E"]:
        out.append((x + 1, y))
    if not c["W"]:
        out.append((x - 1, y))
    return out


def make_shadow(avoid, radius: int):
    if not avoid or radius < 0:
        return lambda cell: False
    avoid = list(avoid)
    return lambda cell: any(manhattan(cell, a) <= radius for a in avoid)


def bfs_path(maze, start: Cell, goal: Cell, avoid=(), radius: int = 0):
    """Shortest path start -> goal (excluding start), refusing shadowed cells.

    The start is exempt: a mouse already standing inside a shadow still has to
    be able to walk out of it. Returns [] when no such path exists.
    """
    shadowed = make_shadow(avoid, radius)
    if shadowed(goal):
        return []

    prev = {start: None}
    q = deque([start])
    found = False
    while q:
        cur = q.popleft()
        if cur == goal:
            found = True
            break
        for nb in neighbors(maze, cur):
            if nb in prev or shadowed(nb):
                continue
            prev[nb] = cur
            q.append(nb)
    if not found:
        return []

    path = []
    cur = goal
    while cur != start:
        path.append(cur)
        cur = prev[cur]
    path.reverse()
    return path


def bfs_nearest_frontier(maze, start: Cell, explored, excluded, avoid=(), radius: int = 0):
    """Closest cell by true maze distance that is unexplored, unclaimed this tick,
    and reachable without cutting through a higher rank's shadow."""
    shadowed = make_shadow(avoid, radius)
    seen = {start}
    q = deque([start])
    while q:
        cur = q.popleft()
        if not explored[cur[1]][cur[0]] and cur not in excluded and not shadowed(cur):
            return cur
        for nb in neighbors(maze, cur):
            if nb in seen or shadowed(nb):
                continue
            seen.add(nb)
            q.append(nb)
    return None


# --------------------------------------------------------------------------
# agents
# --------------------------------------------------------------------------

@dataclass
class Mouse:
    id: int
    label: str
    pos: Cell
    prev_pos: Cell
    rank: int                       # 1 = highest priority
    target: Cell | None = None
    status: str = "SEARCHING"       # SEARCHING | CLAIM | YIELD | BACKOFF | WAIT | DONE
    steps: int = 0
    stuck: int = 0                  # consecutive ticks spent yielding
    yielding_to: int | None = None  # id of the higher rank this mouse is stopped for
    forced_vacate: int | None = None  # id of a higher rank that needs this exact cell
    trail: list = field(default_factory=list)
    back_stack: list = field(default_factory=list)  # remembered path, most recent last


# --------------------------------------------------------------------------
# simulation
# --------------------------------------------------------------------------

class Simulation:
    def __init__(self, size: int = N, seed: int | None = None, log_size: int = 40):
        self.n = size
        self.rng = random.Random(seed)
        self.log_size = log_size
        self.events: deque = deque(maxlen=log_size)
        self.reset()

    # ---------------- setup ----------------

    def reset(self):
        n = self.n
        self.maze = generate_maze(n, self.rng)
        starts = [(0, 0), (n - 1, 0), (0, n - 1)]

        self.mice = []
        for i, d in enumerate(MICE_DEF):
            pos = starts[i % len(starts)]
            self.mice.append(
                Mouse(
                    id=d["id"],
                    label=d["label"],
                    pos=pos,
                    prev_pos=pos,
                    rank=rank_of(d["id"]) + 1,
                    trail=[pos],
                )
            )

        self.explored = [[False] * n for _ in range(n)]
        self.total_cells = n * n
        self.explored_count = 0
        for m in self.mice:
            if not self.explored[m.pos[1]][m.pos[0]]:
                self.explored[m.pos[1]][m.pos[0]] = True
                self.explored_count += 1

        self.tick_count = 0
        self.yield_count = 0
        self.conflicts = []          # [(i, j, distance)] for this tick, for drawing
        self.pair_warn = {(0, 1): None, (0, 2): None, (1, 2): None}
        self.done_logged = False
        self.stall_ticks = 0
        self.events.clear()
        chain = " > ".join(MICE_DEF[i]["label"] for i in PRIORITY)
        self.log("info", f"New maze - priority locked {chain}")

    def log(self, kind: str, msg: str):
        self.events.append((self.tick_count, kind, msg))

    @property
    def finished(self) -> bool:
        return self.explored_count >= self.total_cells

    # ---------------- back-off ----------------

    def back_off_step(self, m: Mouse, threat: Cell, live_final):
        """Pick one step that opens distance from `threat`, preferring the mouse's
        own remembered path (ground it knows is walkable and already explored)."""
        here = manhattan(m.pos, threat)
        nbs = neighbors(self.maze, m.pos)
        adjacent = set(nbs)
        occupied = {live_final[j] for j in range(len(self.mice)) if j != m.id}

        def free(c):
            return c not in occupied

        # Drop remembered cells that are no longer one step away -- a mouse that
        # sidestepped during an earlier back-off has left its recorded route, and
        # those stale entries must never be treated as a legal single move.
        while m.back_stack and m.back_stack[-1] not in adjacent:
            m.back_stack.pop()

        if m.back_stack:
            retreat = m.back_stack[-1]
            if free(retreat) and manhattan(retreat, threat) > here:
                return retreat, True

        # remembered path doesn't help (or is blocked) -- take the legal neighbour
        # that opens up the most distance instead of freezing.
        best, best_d = None, here
        for nb in nbs:
            if not free(nb):
                continue
            d = manhattan(nb, threat)
            if d > best_d:
                best, best_d = nb, d
        if best is not None:
            return best, False

        # pinned in a dead end: no cell increases the gap. Take a sideways step
        # that at least holds the distance (never straight back the way we came)
        # so the mouse keeps its options open instead of freezing until the other
        # mouse happens to wander off.
        for nb in nbs:
            if free(nb) and nb != m.prev_pos and manhattan(nb, threat) >= here:
                return nb, False
        return None, False

    def _commit_move(self, m: Mouse, cell: Cell, status: str, live_final, from_stack=False):
        if from_stack and m.back_stack:
            m.back_stack.pop()
        m.prev_pos = m.pos
        m.pos = cell
        m.steps += 1
        m.trail.append(cell)
        if len(m.trail) > 18:
            m.trail.pop(0)
        if not self.explored[cell[1]][cell[0]]:
            self.explored[cell[1]][cell[0]] = True
            self.explored_count += 1
        m.status = status
        live_final[m.id] = cell

    def break_stall(self):
        """Physical gridlock: everyone is blocking everyone and nobody can plan a
        way out. Rank cannot settle a head-on jam in a one-wide corridor -- someone
        has to reverse. The LOWEST-ranked mouse that still has anywhere to go steps
        aside, which keeps the pecking order intact wherever it can still apply."""
        for mid in reversed(PRIORITY):
            m = self.mice[mid]
            others = [o.pos for o in self.mice if o.id != mid]
            cands = [nb for nb in neighbors(self.maze, m.pos) if nb not in others]
            if not cands:
                continue
            best = max(cands, key=lambda c: sum(manhattan(c, o) for o in others))
            m.yielding_to = None
            m.forced_vacate = None
            m.stuck = 0
            self._commit_move(m, best, "BACKOFF", [o.pos for o in self.mice])
            self.stall_ticks = 0
            self.log("warn", f"gridlock - {m.label} steps aside to {best}")
            return

    # ---------------- the tick ----------------

    def tick(self):
        if self.finished:
            for m in self.mice:
                m.status = "DONE"
                m.target = None
            if not self.done_logged:
                self.done_logged = True
                self.log("info", "Shared map complete - every cell has been explored")
            return

        self.tick_count += 1
        self.conflicts = []
        positions_before = [m.pos for m in self.mice]

        live_final = [m.pos for m in self.mice]  # current-tick committed positions
        claimed = set()                          # frontier cells already spoken for

        # STATIC priority: ALPHA plans first, then BRAVO, then CHARLIE -- every
        # single tick. Because the order never rotates, whoever plans earlier has
        # already committed its cell by the time a lower rank looks at the board,
        # so the higher rank always wins a contested node by construction.
        for idx in PRIORITY:
            m = self.mice[idx]
            higher_ids = higher_than(m.id)                 # rank order, highest first
            higher_pos = [live_final[j] for j in higher_ids]

            # ---- 1. clearance: has the mouse I stopped for moved out of reach?
            if m.yielding_to is not None:
                d = manhattan(m.pos, live_final[m.yielding_to])
                if d >= CLEAR_DIST:
                    self.log(
                        "info",
                        f"{m.label} clear of {self.mice[m.yielding_to].label} "
                        f"(d={d}) - resuming on its rerouted target",
                    )
                    m.yielding_to = None
                    m.stuck = 0

            # ---- 2. a higher rank demanded the exact cell this mouse is parked
            # on. Rank decides it: this one moves, no negotiation.
            if m.forced_vacate is not None:
                boss = m.forced_vacate
                m.forced_vacate = None
                cell, from_stack = self.back_off_step(m, live_final[boss], live_final)
                if cell is not None:
                    m.stuck = 0
                    self._commit_move(m, cell, "BACKOFF", live_final, from_stack)
                    self.log(
                        "warn",
                        f"{m.label} vacates for {self.mice[boss].label} -> {cell}",
                    )
                    continue
                # genuinely cornered -- fall through and hold

            # ---- 3. claim a frontier. A mouse that is yielding searches through a
            # corridor that stays clear of every higher rank, so its target is
            # rerouted AWAY from them instead of dragging it back to the same node.
            keep_clear = BUFFER if m.yielding_to is not None else 0
            prev_target = m.target
            target = bfs_nearest_frontier(
                self.maze, m.pos, self.explored, claimed, higher_pos, keep_clear
            )
            rerouted = target is not None
            if target is None:  # no clear corridor
                target = bfs_nearest_frontier(self.maze, m.pos, self.explored, claimed)
            if target is None:  # last resort: share a frontier with someone else
                target = bfs_nearest_frontier(self.maze, m.pos, self.explored, set())
            m.target = target

            if target is None:
                m.status = "DONE"
                live_final[idx] = m.pos
                continue
            claimed.add(target)

            if rerouted and m.yielding_to is not None and prev_target and prev_target != target:
                self.log(
                    "info",
                    f"{m.label} rerouted -> {target}, routed clear of "
                    f"{self.mice[m.yielding_to].label}",
                )

            # ---- 4. still stopped for a higher rank: stay put until it is clear.
            if m.yielding_to is not None:
                threat = live_final[m.yielding_to]
                m.stuck += 1
                self.yield_count += 1
                self.conflicts.append((idx, m.yielding_to, manhattan(m.pos, threat)))

                # held too long -- stop waiting politely and open up distance
                if m.stuck >= STUCK_LIMIT:
                    cell, from_stack = self.back_off_step(m, threat, live_final)
                    if cell is not None:
                        boss_label = self.mice[m.yielding_to].label
                        m.stuck = 0
                        self._commit_move(m, cell, "BACKOFF", live_final, from_stack)
                        self.log(
                            "warn",
                            f"{m.label} still boxed in after {STUCK_LIMIT} ticks - "
                            f"backing away from {boss_label}",
                        )
                        continue
                m.status = "YIELD"
                live_final[idx] = m.pos
                continue

            # ---- 5. plan one step. Prefer a route that goes around every cell a
            # mouse is standing in, so a vacate order is only ever issued when the
            # maze genuinely offers no way past.
            occupied_cells = [live_final[o.id] for o in self.mice if o.id != m.id]
            path = bfs_path(self.maze, m.pos, target, occupied_cells, 0)
            if not path:
                path = bfs_path(self.maze, m.pos, target, higher_pos, 0)
            if not path:
                path = bfs_path(self.maze, m.pos, target)
            desired = path[0] if path else m.pos

            # ---- 6. physical occupancy: two mice never share a cell, whatever
            # their rank.
            occupant = next(
                (o for o in self.mice if o.id != m.id and live_final[o.id] == desired), None
            )
            if occupant is not None and outranks(m.id, occupant.id):
                taken = {live_final[o.id] for o in self.mice if o.id != occupant.id}
                has_room = any(nb not in taken for nb in neighbors(self.maze, occupant.pos))
                if has_room:
                    # I outrank whoever is parked on my node -- it is mine, they clear out.
                    occupant.forced_vacate = m.id
                    occupant.yielding_to = m.id
                    m.status = "WAIT"
                    self.conflicts.append((idx, occupant.id, 0))
                    live_final[idx] = m.pos
                    self.log(
                        "warn",
                        f"{m.label} claims {desired} - {occupant.label} ordered off the node",
                    )
                    continue
                # The node is mine by rank, but the mouse standing on it is boxed in
                # and has nowhere to go. Rank cannot move a mouse that physically
                # cannot move, so the claimer opens the room itself instead of
                # wedging the corridor shut for both of them.
                cell, from_stack = self.back_off_step(m, occupant.pos, live_final)
                if cell is not None:
                    self.conflicts.append((idx, occupant.id, 1))
                    self._commit_move(m, cell, "BACKOFF", live_final, from_stack)
                    self.log(
                        "warn",
                        f"{m.label} makes room - {occupant.label} is boxed in at "
                        f"{occupant.pos} with no exit",
                    )
                    continue
                m.status = "WAIT"
                self.conflicts.append((idx, occupant.id, 0))
                live_final[idx] = m.pos
                continue

            # ---- 7. verge of collision -- measured ONLY against higher ranks.
            # A mouse never gives way to something below it in the chain.
            blockers = [j for j in higher_ids if manhattan(desired, live_final[j]) <= COLLIDE_DIST]
            if blockers and desired != m.pos:
                boss = blockers[0]  # highest-ranked of the blockers
                for j in blockers:
                    self.conflicts.append((idx, j, manhattan(desired, live_final[j])))
                m.yielding_to = boss
                m.stuck = 1
                self.yield_count += 1
                m.status = "YIELD"
                live_final[idx] = m.pos

                # reroute immediately, so the stopped mouse is already aimed elsewhere
                away = bfs_nearest_frontier(
                    self.maze, m.pos, self.explored, claimed, [live_final[boss]], BUFFER
                )
                if away is not None:
                    m.target = away
                    claimed.add(away)
                tail = f" - rerouting to {away}" if away else " - no clear reroute yet"
                self.log(
                    "warn",
                    f"{m.label} yields {desired} to {self.mice[boss].label} - "
                    f"stopped until d>={CLEAR_DIST}{tail}",
                )
                continue

            # ---- 8. clear to move
            m.back_stack.append(m.pos)
            if len(m.back_stack) > BACKSTACK_MAX:
                m.back_stack.pop(0)
            m.stuck = 0
            self._commit_move(m, desired, "CLAIM" if desired == target else "SEARCHING", live_final)

        # ---- escalating proximity warnings (6 -> 5 -> 4 -> 3), independent of the
        # yield logic above: advance notice before two mice ever contest a node.
        for i, j in ((0, 1), (0, 2), (1, 2)):
            d = manhattan(self.mice[i].pos, self.mice[j].pos)
            tier = proximity_tier(d)
            prev = self.pair_warn[(i, j)]
            if tier is not None and tier != prev and (prev is None or tier < prev):
                self.log(
                    "warn",
                    f"{self.mice[i].label} <-> {self.mice[j].label} closing in - "
                    f"Manhattan distance {d} (<={tier})",
                )
            self.pair_warn[(i, j)] = tier

        # ---- gridlock watchdog: if nobody has physically moved for several ticks
        # the swarm is wedged, and no amount of re-planning will free it.
        if all(positions_before[i] == self.mice[i].pos for i in range(len(self.mice))):
            self.stall_ticks += 1
        else:
            self.stall_ticks = 0
        if self.stall_ticks >= STALL_LIMIT:
            self.break_stall()

        if self.finished and not self.done_logged:
            self.done_logged = True
            self.log("info", "Shared map complete - every cell has been explored")


# --------------------------------------------------------------------------
# terminal renderer (no GUI required)
# --------------------------------------------------------------------------

ANSI = {"ALPHA": "\033[96m", "BRAVO": "\033[95m", "CHARLIE": "\033[93m"}
RESET = "\033[0m"
DIM = "\033[90m"
RED = "\033[91m"
GREEN = "\033[92m"


def render_text(sim: Simulation, color: bool = True) -> str:
    """ASCII maze: walls as box characters, mice as their rank digit."""
    n = sim.n
    at = {m.pos: m for m in sim.mice}
    out = []

    top = "+" + "".join("---+" for _ in range(n))
    out.append(top)
    for y in range(n):
        mid, bot = "|", "+"
        for x in range(n):
            m = at.get((x, y))
            if m:
                tag = str(m.rank)
                if color:
                    col = RED if m.yielding_to is not None else ANSI[m.label]
                    body = f" {col}{tag}{RESET} "
                else:
                    body = f" {tag} "
            elif sim.explored[y][x]:
                body = f" {GREEN}.{RESET} " if color else " . "
            else:
                body = "   "
            mid += body + ("|" if sim.maze[y][x]["E"] else " ")
            bot += ("---+" if sim.maze[y][x]["S"] else "   +")
        out.append(mid)
        out.append(bot)

    chain = "  >  ".join(f"P{i+1} {MICE_DEF[mid]['label']}" for i, mid in enumerate(PRIORITY))
    out.append("")
    out.append(f"priority (fixed): {chain}")
    out.append(f"tick {sim.tick_count}   yields {sim.yield_count}   "
               f"explored {sim.explored_count}/{sim.total_cells}")
    out.append("")
    for m in sim.mice:
        col = ANSI[m.label] if color else ""
        rst = RESET if color else ""
        line = f"  {col}P{m.rank} {m.label:<8}{rst} {str(m.pos):<9} {m.status:<9}"
        if m.yielding_to is not None:
            boss = sim.mice[m.yielding_to]
            line += (f" stopped for {boss.label} (d={manhattan(m.pos, boss.pos)}, "
                     f"clears at {CLEAR_DIST})")
        elif m.target:
            line += f" -> frontier {m.target}"
        out.append(line)

    out.append("")
    for t, kind, msg in list(sim.events)[-6:]:
        col = (RED if kind == "warn" else GREEN) if color else ""
        rst = RESET if color else ""
        out.append(f"  {DIM if color else ''}t{t:<4}{rst}{col}{msg}{rst}")
    return "\n".join(out)


def run_text(sim: Simulation, tick_ms: int, max_ticks: int, color: bool = True):
    try:
        while sim.tick_count < max_ticks:
            sys.stdout.write("\033[H\033[J" if color else "\n" * 3)
            sys.stdout.write(render_text(sim, color) + "\n")
            sys.stdout.flush()
            if sim.finished:
                break
            sim.tick()
            time.sleep(tick_ms / 1000)
    except KeyboardInterrupt:
        pass
    print(f"\nfinished in {sim.tick_count} ticks, {sim.yield_count} yield-ticks")


# --------------------------------------------------------------------------
# self test -- checks the priority contract holds over many random mazes
# --------------------------------------------------------------------------

def selftest(runs: int = 300, size: int = N, max_ticks: int = 5000) -> bool:
    overlaps = inversions = teleports = incomplete = 0
    total_ticks = 0
    seen_status = set()

    for r in range(runs):
        sim = Simulation(size=size, seed=r)
        while not sim.finished and sim.tick_count < max_ticks:
            before = [m.pos for m in sim.mice]
            sim.tick()
            for i in range(len(sim.mice)):
                seen_status.add(sim.mice[i].status)
                # a mouse never yields to a lower rank
                yt = sim.mice[i].yielding_to
                if yt is not None and rank_of(yt) > rank_of(sim.mice[i].id):
                    inversions += 1
                # every move is one cell
                if manhattan(before[i], sim.mice[i].pos) > 1:
                    teleports += 1
                # no two mice share a cell
                for j in range(i + 1, len(sim.mice)):
                    if sim.mice[i].pos == sim.mice[j].pos:
                        overlaps += 1
        total_ticks += sim.tick_count
        if not sim.finished:
            incomplete += 1

    ok = overlaps == inversions == teleports == incomplete == 0
    print(f"runs={runs}  avg ticks={total_ticks / runs:.1f}")
    print(f"  cell overlaps ............ {overlaps}")
    print(f"  priority inversions ...... {inversions}")
    print(f"  illegal moves ............ {teleports}")
    print(f"  runs that never finished . {incomplete}")
    print(f"  statuses exercised ....... {', '.join(sorted(seen_status))}")
    print("PASS" if ok else "FAIL")
    return ok


# --------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="Swarm micromouse with static priority.")
    ap.add_argument("--no-color", action="store_true", help="plain ASCII, no ANSI colour")
    ap.add_argument("--selftest", action="store_true", help="headless invariant check")
    ap.add_argument("--size", type=int, default=N, help="maze size (default 11)")
    ap.add_argument("--seed", type=int, default=None, help="random seed")
    ap.add_argument("--tick-ms", type=int, default=320, help="ms per tick")
    ap.add_argument("--runs", type=int, default=300, help="runs for --selftest")
    ap.add_argument("--max-ticks", type=int, default=5000)
    args = ap.parse_args()

    if args.selftest:
        sys.exit(0 if selftest(args.runs, args.size) else 1)

    sim = Simulation(size=args.size, seed=args.seed)
    run_text(sim, args.tick_ms, args.max_ticks, color=not args.no_color)


if __name__ == "__main__":
    main()
