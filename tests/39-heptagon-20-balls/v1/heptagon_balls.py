"""
20 balls bouncing inside a spinning heptagon.

- Pure Python physics (no pygame): gravity, air drag, restitution, Coulomb friction,
  ball spin (angular velocity), ball-ball and ball-wall impulse-based collisions.
- The heptagon rotates at 360 degrees per 5 seconds; walls move, so the wall
  velocity at the contact point is included in the collision response.
- Rendering with tkinter. The number on each ball rotates with the ball's spin.

Allowed libs only: tkinter, math, numpy, dataclasses, typing, sys.
"""

import math
import sys
import tkinter as tk
from dataclasses import dataclass, field
from typing import List, Tuple

import numpy as np

# ----------------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------------
WIDTH, HEIGHT = 800, 800
CX, CY = WIDTH / 2.0, HEIGHT / 2.0

HEPTAGON_RADIUS = 350.0          # circumradius of the heptagon (px)
HEPTAGON_SIDES = 7
SPIN_SPEED = 2.0 * math.pi / 5.0  # rad/s  (360 deg per 5 s)

NUM_BALLS = 20
BALL_RADIUS = 18.0
BALL_MASS = 1.0
BALL_INERTIA = 0.5 * BALL_MASS * BALL_RADIUS ** 2  # solid disc

GRAVITY = 1000.0                 # px/s^2 (downwards on screen)
WALL_RESTITUTION = 0.72
BALL_RESTITUTION = 0.85
WALL_FRICTION = 0.35             # Coulomb coefficient ball-wall
BALL_FRICTION = 0.15             # Coulomb coefficient ball-ball
AIR_DRAG = 0.05                  # linear drag (1/s)
SPIN_DAMPING = 0.3               # angular damping (1/s)
RESTING_SPEED = 25.0             # below this normal speed, no bounce (settle)

# Max speed so that a ball can never fly higher than the heptagon radius:
# h = v^2 / (2 g)  ->  v_max = sqrt(2 g R)
MAX_SPEED = math.sqrt(2.0 * GRAVITY * (HEPTAGON_RADIUS - BALL_RADIUS))

FPS = 60
DT = 1.0 / FPS
SUBSTEPS = 8

COLORS = [
    "#f8b862", "#f6ad49", "#f39800", "#f08300", "#ec6d51",
    "#ee7948", "#ed6d3d", "#ec6800", "#ec6800", "#ee7800",
    "#eb6238", "#ea5506", "#ea5506", "#eb6101", "#e49e61",
    "#e45e32", "#e17b34", "#dd7a56", "#db8449", "#d66a35",
]


# ----------------------------------------------------------------------------
# Data
# ----------------------------------------------------------------------------
@dataclass
class Ball:
    number: int
    color: str
    pos: np.ndarray
    vel: np.ndarray
    radius: float = BALL_RADIUS
    mass: float = BALL_MASS
    inertia: float = BALL_INERTIA
    angle: float = 0.0       # radians
    omega: float = 0.0       # angular velocity, rad/s
    items: Tuple[int, int, int] = field(default=(0, 0, 0))


def perp(v: np.ndarray) -> np.ndarray:
    """Rotate a 2D vector by +90 degrees (in the math sense of the chosen axes)."""
    return np.array([-v[1], v[0]])


def cross(a: np.ndarray, b: np.ndarray) -> float:
    return float(a[0] * b[1] - a[1] * b[0])


# ----------------------------------------------------------------------------
# Heptagon
# ----------------------------------------------------------------------------
class Heptagon:
    def __init__(self, center: np.ndarray, radius: float, sides: int, spin: float):
        self.center = center
        self.radius = radius
        self.sides = sides
        self.spin = spin
        self.angle = 0.0

    def update(self, dt: float) -> None:
        self.angle = (self.angle + self.spin * dt) % (2.0 * math.pi)

    def vertices(self) -> List[np.ndarray]:
        out = []
        for k in range(self.sides):
            a = self.angle + 2.0 * math.pi * k / self.sides - math.pi / 2.0
            out.append(self.center + self.radius * np.array([math.cos(a), math.sin(a)]))
        return out

    def wall_velocity(self, point: np.ndarray) -> np.ndarray:
        """Velocity of the (rigidly rotating) wall at a given point."""
        return self.spin * perp(point - self.center)

    def edges(self):
        """Yield (a, b, inward_normal) for each edge."""
        verts = self.vertices()
        n = len(verts)
        for i in range(n):
            a = verts[i]
            b = verts[(i + 1) % n]
            edge = b - a
            length = np.linalg.norm(edge)
            normal = perp(edge) / length
            # make the normal point to the inside (towards the center)
            if np.dot(self.center - a, normal) < 0:
                normal = -normal
            yield a, b, normal


# ----------------------------------------------------------------------------
# Physics
# ----------------------------------------------------------------------------
class World:
    def __init__(self):
        self.center = np.array([CX, CY])
        self.heptagon = Heptagon(self.center, HEPTAGON_RADIUS, HEPTAGON_SIDES, SPIN_SPEED)
        self.balls: List[Ball] = []
        rng = np.random.default_rng()
        for i in range(NUM_BALLS):
            # All balls start at the heptagon center (tiny jitter so the
            # collision normals are defined) with a small random kick.
            jitter = rng.uniform(-1.0, 1.0, 2) * 2.0
            vel = np.array([rng.uniform(-60.0, 60.0), rng.uniform(-30.0, 0.0)])
            self.balls.append(Ball(i + 1, COLORS[i], self.center + jitter, vel))

    # ---------------------------------------------------------------- walls
    def collide_walls(self, ball: Ball) -> None:
        hep = self.heptagon
        for a, b, n in hep.edges():
            dist = float(np.dot(ball.pos - a, n))
            if dist >= ball.radius:
                continue
            # Also check projection lies near the segment (convex polygon -> fine)
            edge = b - a
            t = np.dot(ball.pos - a, edge) / np.dot(edge, edge)
            if t < -0.1 or t > 1.1:
                continue

            # positional correction
            ball.pos = ball.pos + n * (ball.radius - dist)

            r_c = -n * ball.radius                     # contact offset from center
            contact = ball.pos + r_c
            v_wall = hep.wall_velocity(contact)
            v_contact = ball.vel + ball.omega * perp(r_c)
            v_rel = v_contact - v_wall

            vn = float(np.dot(v_rel, n))
            if vn >= 0:
                continue

            e = WALL_RESTITUTION if -vn > RESTING_SPEED else 0.0
            jn = -(1.0 + e) * vn * ball.mass

            tangent = perp(n)
            vt = float(np.dot(v_rel, tangent))
            rt = cross(r_c, tangent)
            k_t = 1.0 / ball.mass + rt * rt / ball.inertia
            jt = -vt / k_t
            max_f = WALL_FRICTION * jn
            jt = max(-max_f, min(max_f, jt))

            impulse = jn * n + jt * tangent
            ball.vel = ball.vel + impulse / ball.mass
            ball.omega += cross(r_c, impulse) / ball.inertia

    # ---------------------------------------------------------------- balls
    def collide_balls(self) -> None:
        balls = self.balls
        nb = len(balls)
        min_d = 2.0 * BALL_RADIUS
        for i in range(nb):
            a = balls[i]
            for j in range(i + 1, nb):
                b = balls[j]
                delta = b.pos - a.pos
                d2 = float(delta[0] * delta[0] + delta[1] * delta[1])
                if d2 >= min_d * min_d:
                    continue
                d = math.sqrt(d2)
                if d < 1e-9:
                    n = np.array([1.0, 0.0])
                    d = 0.0
                else:
                    n = delta / d

                # positional correction (split by inverse mass)
                overlap = min_d - d
                inv_a, inv_b = 1.0 / a.mass, 1.0 / b.mass
                inv_sum = inv_a + inv_b
                a.pos = a.pos - n * overlap * (inv_a / inv_sum)
                b.pos = b.pos + n * overlap * (inv_b / inv_sum)

                r_a = n * a.radius
                r_b = -n * b.radius
                va = a.vel + a.omega * perp(r_a)
                vb = b.vel + b.omega * perp(r_b)
                v_rel = va - vb
                vn = float(np.dot(v_rel, n))
                if vn <= 0:           # separating
                    continue

                e = BALL_RESTITUTION if vn > RESTING_SPEED else 0.0
                jn = (1.0 + e) * vn / inv_sum
                a.vel = a.vel - jn * n * inv_a
                b.vel = b.vel + jn * n * inv_b

                # friction -> spin
                tangent = perp(n)
                vt = float(np.dot(v_rel, tangent))
                ra_t = cross(r_a, tangent)
                rb_t = cross(r_b, tangent)
                k_t = inv_sum + ra_t * ra_t / a.inertia + rb_t * rb_t / b.inertia
                jt = -vt / k_t
                max_f = BALL_FRICTION * jn
                jt = max(-max_f, min(max_f, jt))
                p = jt * tangent
                a.vel = a.vel + p * inv_a
                a.omega += cross(r_a, p) / a.inertia
                b.vel = b.vel - p * inv_b
                b.omega += cross(r_b, -p) / b.inertia

    # ---------------------------------------------------------------- step
    def step(self, dt: float) -> None:
        h = dt / SUBSTEPS
        g = np.array([0.0, GRAVITY])
        drag = math.exp(-AIR_DRAG * h)
        spin_drag = math.exp(-SPIN_DAMPING * h)
        for _ in range(SUBSTEPS):
            self.heptagon.update(h)
            for ball in self.balls:
                ball.vel = (ball.vel + g * h) * drag
                speed = float(np.linalg.norm(ball.vel))
                if speed > MAX_SPEED:
                    ball.vel = ball.vel * (MAX_SPEED / speed)
                ball.pos = ball.pos + ball.vel * h
                ball.omega *= spin_drag
                ball.angle += ball.omega * h
            self.collide_balls()
            for ball in self.balls:
                self.collide_walls(ball)


# ----------------------------------------------------------------------------
# Rendering
# ----------------------------------------------------------------------------
class App:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("20 balls in a spinning heptagon")
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="#1b1b22",
                                highlightthickness=0)
        self.canvas.pack()
        self.world = World()

        flat = [c for v in self.world.heptagon.vertices() for c in v]
        self.hep_item = self.canvas.create_polygon(*flat, outline="#f0e6d2",
                                                   fill="#24242e", width=4)
        for ball in self.world.balls:
            x, y = ball.pos
            r = ball.radius
            oval = self.canvas.create_oval(x - r, y - r, x + r, y + r,
                                           fill=ball.color, outline="#3a2010", width=1.5)
            mark = self.canvas.create_line(x, y, x, y - r, fill="#5a2a10", width=2)
            text = self.canvas.create_text(x, y, text=str(ball.number),
                                           fill="#1e1208", font=("Helvetica", 12, "bold"))
            ball.items = (oval, mark, text)

        self.root.bind("<Escape>", lambda e: self.root.destroy())
        self.tick()

    def draw(self) -> None:
        cv = self.canvas
        flat = [c for v in self.world.heptagon.vertices() for c in v]
        cv.coords(self.hep_item, *flat)
        for ball in self.world.balls:
            oval, mark, text = ball.items
            x, y = ball.pos
            r = ball.radius
            cv.coords(oval, x - r, y - r, x + r, y + r)
            # spin marker: a radius line rotating with the ball
            mx = x + math.cos(ball.angle - math.pi / 2) * r * 0.9
            my = y + math.sin(ball.angle - math.pi / 2) * r * 0.9
            cv.coords(mark, x, y, mx, my)
            cv.coords(text, x, y)
            # Tk text angle is counter-clockwise; our y-axis points down
            try:
                cv.itemconfigure(text, angle=-math.degrees(ball.angle) % 360)
            except tk.TclError:
                pass

    def tick(self) -> None:
        self.world.step(DT)
        self.draw()
        self.root.after(int(1000 / FPS), self.tick)


def main() -> int:
    root = tk.Tk()
    root.resizable(False, False)
    App(root)
    root.mainloop()
    return 0


if __name__ == "__main__":
    sys.exit(main())
