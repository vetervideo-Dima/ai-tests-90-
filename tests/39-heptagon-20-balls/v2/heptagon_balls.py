"""
20 balls bouncing inside a spinning heptagon  (v2).

- Pure Python physics (no pygame): gravity, air drag, restitution, Coulomb friction,
  ball spin, impulse-based ball-ball and ball-wall collisions.
- The heptagon rotates at exactly 360 degrees per 5 seconds of *real* time:
  the simulation uses a fixed-step accumulator driven by the wall clock.
- The wall velocity at the contact point is included in the collision response.
- tkinter rendering; the number (and a marker) on each ball rotates with its spin.
- Keys: Space = pause, R = restart (drop again from the centre), Esc = quit.

Allowed libs only: tkinter, math, numpy, dataclasses, typing, sys.
"""

import math
import sys
import time
import tkinter as tk
from dataclasses import dataclass, field
from typing import List, Tuple

import numpy as np

# ----------------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------------
WIDTH, HEIGHT = 800, 800
CX, CY = WIDTH / 2.0, HEIGHT / 2.0

HEPTAGON_RADIUS = 350.0           # circumradius (px)
HEPTAGON_SIDES = 7
SPIN_SPEED = 2.0 * math.pi / 5.0  # rad/s  (360 deg per 5 s)

NUM_BALLS = 20
BALL_RADIUS = 18.0
BALL_MASS = 1.0
BALL_INERTIA = 0.5 * BALL_MASS * BALL_RADIUS ** 2  # solid disc

GRAVITY = 1000.0                  # px/s^2
WALL_RESTITUTION = 0.72
BALL_RESTITUTION = 0.85
WALL_FRICTION = 0.35
BALL_FRICTION = 0.15
AIR_DRAG = 0.05
SPIN_DAMPING = 0.3
RESTING_SPEED = 25.0

# bounce height h = v^2/(2g) must stay below the heptagon radius
MAX_SPEED = math.sqrt(2.0 * GRAVITY * (HEPTAGON_RADIUS - BALL_RADIUS))

PHYSICS_HZ = 480                  # fixed physics step
PHYS_DT = 1.0 / PHYSICS_HZ
MAX_STEPS_PER_FRAME = 24          # avoid spiral of death
FRAME_MS = 16

COLORS = [
    "#f8b862", "#f6ad49", "#f39800", "#f08300", "#ec6d51",
    "#ee7948", "#ed6d3d", "#ec6800", "#ec6800", "#ee7800",
    "#eb6238", "#ea5506", "#ea5506", "#eb6101", "#e49e61",
    "#e45e32", "#e17b34", "#dd7a56", "#db8449", "#d66a35",
]


def mix(hex_color: str, other: str, t: float) -> str:
    a = [int(hex_color[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(other[i:i + 2], 16) for i in (1, 3, 5)]
    c = [round(a[k] + (b[k] - a[k]) * t) for k in range(3)]
    return "#%02x%02x%02x" % tuple(c)


# ----------------------------------------------------------------------------
# Data (plain floats: far faster than tiny numpy arrays in tight loops)
# ----------------------------------------------------------------------------
@dataclass
class Ball:
    number: int
    color: str
    x: float
    y: float
    vx: float
    vy: float
    radius: float = BALL_RADIUS
    mass: float = BALL_MASS
    inertia: float = BALL_INERTIA
    angle: float = 0.0
    omega: float = 0.0
    items: Tuple[int, ...] = field(default=())


# ----------------------------------------------------------------------------
# Heptagon
# ----------------------------------------------------------------------------
class Heptagon:
    def __init__(self, cx: float, cy: float, radius: float, sides: int, spin: float):
        self.cx, self.cy = cx, cy
        self.radius = radius
        self.sides = sides
        self.spin = spin
        self.angle = 0.0
        self.apothem = radius * math.cos(math.pi / sides)

    def update(self, dt: float) -> None:
        self.angle = (self.angle + self.spin * dt) % (2.0 * math.pi)

    def vertices(self, radius: float = None) -> np.ndarray:
        r = self.radius if radius is None else radius
        k = np.arange(self.sides)
        a = self.angle + 2.0 * math.pi * k / self.sides - math.pi / 2.0
        return np.stack([self.cx + r * np.cos(a), self.cy + r * np.sin(a)], axis=1)

    def inward_normals(self) -> List[Tuple[float, float]]:
        """Inward unit normal of each edge (edge k between vertex k and k+1)."""
        out = []
        for k in range(self.sides):
            mid = self.angle + 2.0 * math.pi * (k + 0.5) / self.sides - math.pi / 2.0
            out.append((-math.cos(mid), -math.sin(mid)))
        return out


# ----------------------------------------------------------------------------
# Physics
# ----------------------------------------------------------------------------
class World:
    def __init__(self, seed=None):
        self.hep = Heptagon(CX, CY, HEPTAGON_RADIUS, HEPTAGON_SIDES, SPIN_SPEED)
        self.time = 0.0
        self.balls: List[Ball] = []
        rng = np.random.default_rng(seed)
        for i in range(NUM_BALLS):
            jx, jy = rng.uniform(-2.0, 2.0, 2)
            vx = float(rng.uniform(-60.0, 60.0))
            vy = float(rng.uniform(-30.0, 0.0))
            self.balls.append(Ball(i + 1, COLORS[i], CX + float(jx), CY + float(jy), vx, vy))

    def collide_walls(self, normals) -> None:
        hep = self.hep
        cx, cy, spin, apo = hep.cx, hep.cy, hep.spin, hep.apothem
        for b in self.balls:
            r = b.radius
            for nx, ny in normals:
                # distance from the ball centre to the edge line along the inward normal
                dist = apo + (b.x - cx) * nx + (b.y - cy) * ny
                if dist >= r:
                    continue
                pen = r - dist
                b.x += nx * pen
                b.y += ny * pen

                # contact point and the wall velocity there (rigid rotation)
                px, py = b.x - nx * r, b.y - ny * r
                wvx, wvy = -spin * (py - cy), spin * (px - cx)
                # ball surface velocity at contact: v + w x r_c, r_c = -n r
                svx = b.vx + b.omega * (ny * r)
                svy = b.vy - b.omega * (nx * r)
                rvx, rvy = svx - wvx, svy - wvy

                vn = rvx * nx + rvy * ny
                if vn >= 0.0:
                    continue
                e = WALL_RESTITUTION if -vn > RESTING_SPEED else 0.0
                jn = -(1.0 + e) * vn * b.mass

                tx, ty = -ny, nx
                vt = rvx * tx + rvy * ty
                k_t = 1.0 / b.mass + r * r / b.inertia
                jt = -vt / k_t
                lim = WALL_FRICTION * jn
                if jt > lim:
                    jt = lim
                elif jt < -lim:
                    jt = -lim

                b.vx += (jn * nx + jt * tx) / b.mass
                b.vy += (jn * ny + jt * ty) / b.mass
                b.omega += -r * jt / b.inertia

    def collide_balls(self) -> None:
        balls = self.balls
        nb = len(balls)
        min_d = 2.0 * BALL_RADIUS
        min_d2 = min_d * min_d
        for i in range(nb):
            a = balls[i]
            for j in range(i + 1, nb):
                b = balls[j]
                dx, dy = b.x - a.x, b.y - a.y
                d2 = dx * dx + dy * dy
                if d2 >= min_d2:
                    continue
                d = math.sqrt(d2)
                if d < 1e-9:
                    nx, ny, d = 1.0, 0.0, 0.0
                else:
                    nx, ny = dx / d, dy / d

                inv_a, inv_b = 1.0 / a.mass, 1.0 / b.mass
                inv_sum = inv_a + inv_b
                corr = (min_d - d) / inv_sum
                a.x -= nx * corr * inv_a
                a.y -= ny * corr * inv_a
                b.x += nx * corr * inv_b
                b.y += ny * corr * inv_b

                ra, rb = a.radius, b.radius
                tx, ty = -ny, nx
                rvx = (a.vx - b.vx)
                rvy = (a.vy - b.vy)
                vn = rvx * nx + rvy * ny
                if vn <= 0.0:
                    continue
                vt = rvx * tx + rvy * ty + ra * a.omega + rb * b.omega

                e = BALL_RESTITUTION if vn > RESTING_SPEED else 0.0
                jn = (1.0 + e) * vn / inv_sum
                a.vx -= jn * nx * inv_a
                a.vy -= jn * ny * inv_a
                b.vx += jn * nx * inv_b
                b.vy += jn * ny * inv_b

                k_t = inv_sum + ra * ra / a.inertia + rb * rb / b.inertia
                jt = -vt / k_t
                lim = BALL_FRICTION * jn
                if jt > lim:
                    jt = lim
                elif jt < -lim:
                    jt = -lim
                a.vx += jt * tx * inv_a
                a.vy += jt * ty * inv_a
                b.vx -= jt * tx * inv_b
                b.vy -= jt * ty * inv_b
                a.omega += ra * jt / a.inertia
                b.omega += rb * jt / b.inertia

    def step(self, h: float) -> None:
        self.time += h
        self.hep.update(h)
        drag = math.exp(-AIR_DRAG * h)
        spin_drag = math.exp(-SPIN_DAMPING * h)
        gh = GRAVITY * h
        vmax2 = MAX_SPEED * MAX_SPEED
        for b in self.balls:
            b.vx *= drag
            b.vy = (b.vy + gh) * drag
            s2 = b.vx * b.vx + b.vy * b.vy
            if s2 > vmax2:
                k = MAX_SPEED / math.sqrt(s2)
                b.vx *= k
                b.vy *= k
            b.x += b.vx * h
            b.y += b.vy * h
            b.omega *= spin_drag
            b.angle += b.omega * h
        self.collide_balls()
        self.collide_walls(self.hep.inward_normals())


# ----------------------------------------------------------------------------
# Rendering
# ----------------------------------------------------------------------------
BG = "#14141b"
PANEL = "#22222c"
RIM = "#f3e3c3"


class App:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("20 balls in a spinning heptagon")
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg=BG, highlightthickness=0)
        self.canvas.pack()
        self.paused = False
        self.fps = 0.0
        self.build()
        root.bind("<Escape>", lambda e: root.destroy())
        root.bind("<space>", self.toggle_pause)
        root.bind("<r>", lambda e: self.build())
        root.bind("<R>", lambda e: self.build())
        self.last = time.perf_counter()
        self.acc = 0.0
        self.tick()

    def toggle_pause(self, _e=None):
        self.paused = not self.paused
        self.last = time.perf_counter()

    def build(self) -> None:
        cv = self.canvas
        cv.delete("all")
        self.world = World()
        # soft outer glow rings + floor panel
        self.glow = [cv.create_polygon(0, 0, 0, 0, 0, 0, outline=mix("#f39800", BG, t),
                                       fill="", width=w, joinstyle=tk.ROUND)
                     for t, w in ((0.9, 26), (0.8, 16), (0.62, 9))]
        self.hep_item = cv.create_polygon(0, 0, 0, 0, 0, 0, outline=RIM, fill=PANEL,
                                          width=5, joinstyle=tk.ROUND)
        self.inner = cv.create_polygon(0, 0, 0, 0, 0, 0, outline="#2d2d39", fill="", width=2)
        self.center_dot = cv.create_oval(CX - 3, CY - 3, CX + 3, CY + 3, fill="#55556a", outline="")
        for b in self.world.balls:
            shadow = cv.create_oval(0, 0, 0, 0, fill="#0d0d12", outline="")
            body = cv.create_oval(0, 0, 0, 0, fill=b.color, outline=mix(b.color, "#000000", 0.45),
                                  width=1.5)
            shade = cv.create_arc(0, 0, 0, 0, start=200, extent=140, style=tk.CHORD,
                                  fill=mix(b.color, "#000000", 0.18), outline="")
            hi = cv.create_oval(0, 0, 0, 0, fill=mix(b.color, "#ffffff", 0.55), outline="")
            disc = cv.create_oval(0, 0, 0, 0, fill=mix(b.color, "#ffffff", 0.8), outline="")
            mark = cv.create_line(0, 0, 0, 0, fill=mix(b.color, "#000000", 0.55), width=2,
                                  capstyle=tk.ROUND)
            text = cv.create_text(0, 0, text=str(b.number), fill="#2a1406",
                                  font=("Helvetica", 11, "bold"))
            b.items = (shadow, body, shade, hi, disc, mark, text)
        self.hud = cv.create_text(16, HEIGHT - 14, anchor="sw", fill="#8a8aa0",
                                  font=("Helvetica", 11),
                                  text="")
        self.acc = 0.0
        self.last = time.perf_counter()

    def draw(self) -> None:
        cv = self.canvas
        w = self.world
        verts = w.hep.vertices().ravel().tolist()
        for g in self.glow:
            cv.coords(g, *verts)
        cv.coords(self.hep_item, *verts)
        cv.coords(self.inner, *w.hep.vertices(HEPTAGON_RADIUS - 14).ravel().tolist())
        for b in w.balls:
            shadow, body, shade, hi, disc, mark, text = b.items
            x, y, r = b.x, b.y, b.radius
            cv.coords(shadow, x - r + 3, y - r + 5, x + r + 3, y + r + 5)
            cv.coords(body, x - r, y - r, x + r, y + r)
            cv.coords(shade, x - r + 1, y - r + 1, x + r - 1, y + r - 1)
            cv.coords(hi, x - r * 0.62, y - r * 0.72, x - r * 0.12, y - r * 0.32)
            dr = r * 0.58
            cv.coords(disc, x - dr, y - dr, x + dr, y + dr)
            # spin marker on the rim (rotates with the ball)
            ca, sa = math.cos(b.angle - math.pi / 2), math.sin(b.angle - math.pi / 2)
            cv.coords(mark, x + ca * r * 0.68, y + sa * r * 0.68, x + ca * r * 0.92, y + sa * r * 0.92)
            cv.coords(text, x, y)
            cv.itemconfigure(text, angle=(-math.degrees(b.angle)) % 360.0)
        deg = math.degrees(w.hep.angle)
        cv.itemconfigure(self.hud, text="t = %5.1f s   heptagon %5.1f°   %2.0f fps   "
                                        "[Space] pause  [R] restart  [Esc] quit"
                                        % (w.time, deg, self.fps))

    def tick(self) -> None:
        now = time.perf_counter()
        frame = now - self.last
        self.last = now
        if frame > 0:
            self.fps = self.fps * 0.9 + (1.0 / frame) * 0.1
        if not self.paused:
            self.acc += min(frame, MAX_STEPS_PER_FRAME * PHYS_DT)
            steps = 0
            while self.acc >= PHYS_DT and steps < MAX_STEPS_PER_FRAME:
                self.world.step(PHYS_DT)
                self.acc -= PHYS_DT
                steps += 1
        self.draw()
        spent = (time.perf_counter() - now) * 1000.0
        self.root.after(max(1, int(FRAME_MS - spent)), self.tick)


def main() -> int:
    root = tk.Tk()
    root.resizable(False, False)
    root.configure(bg=BG)
    App(root)
    root.mainloop()
    return 0


if __name__ == "__main__":
    sys.exit(main())
