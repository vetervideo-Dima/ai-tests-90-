#!/usr/bin/env python3
"""
Ball bouncing inside a spinning hexagon  (v2).

Physics
- Gravity + linear air drag.
- Ball is a rigid solid sphere with its own spin (angular velocity).
- Collisions are resolved with impulses in the frame of the moving wall:
  wall surface velocity = omega x r, so the spinning hexagon throws the ball.
  Normal impulse uses restitution (zeroed for slow resting contacts -> no jitter),
  tangential impulse is Coulomb friction (|Jt| <= mu * Jn) and spins the ball.
- Fixed-timestep integration driven by the real clock (accumulator),
  so the speed of the simulation does not depend on the frame rate.

Uses only the Python standard library (tkinter). Run:  python3 hexagon_ball.py
Controls:  Space / click - kick,  R - reset,  Up/Down - spin speed,
           S - reverse spin,  P - pause,  Esc - quit
"""

import math
import random
import time
import tkinter as tk

# ---------------------------------------------------------------- settings
WIDTH, HEIGHT = 800, 800
CENTER = (WIDTH / 2, HEIGHT / 2)
HEX_RADIUS = 300            # center-to-vertex distance of the INNER wall surface (px)
WALL_THICKNESS = 14         # drawn outside the collision surface
BALL_RADIUS = 18            # px

GRAVITY = 1500.0            # px/s^2 (downwards, +y)
AIR_DRAG = 0.15             # 1/s, linear air drag
ANGULAR_DRAG = 0.4          # 1/s, ball spin decay in air
RESTITUTION = 0.85          # normal bounce coefficient
REST_SPEED = 40.0           # px/s: below this normal speed, contact is inelastic (no jitter)
WALL_FRICTION = 0.35        # Coulomb friction coefficient
INERTIA_FACTOR = 0.4        # I = k*m*R^2, solid sphere = 2/5
ANGULAR_SPEED = math.radians(60)  # rad/s, hexagon spin

PHYSICS_HZ = 480            # fixed physics step
MAX_FRAME_DT = 0.05         # clamp long frames (window drag etc.)
TRAIL_LEN = 22

BG = "#0b0d16"


# ---------------------------------------------------------------- vector helpers
def add(a, b): return (a[0] + b[0], a[1] + b[1])
def sub(a, b): return (a[0] - b[0], a[1] - b[1])
def mul(a, s): return (a[0] * s, a[1] * s)
def dot(a, b): return a[0] * b[0] + a[1] * b[1]
def cross(a, b): return a[0] * b[1] - a[1] * b[0]
def length(a): return math.hypot(a[0], a[1])


def mix(c1, c2, t):
    """Blend two #rrggbb colours."""
    a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    return "#%02x%02x%02x" % tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


# ---------------------------------------------------------------- simulation
class Simulation:
    def __init__(self):
        self.angle = 0.0
        self.omega = ANGULAR_SPEED
        self.impacts = []          # (x, y, strength) collected for the renderer
        self.reset()

    def reset(self):
        self.pos = (CENTER[0] + random.uniform(-60, 60), CENTER[1] - 120)
        self.vel = (random.uniform(-250, 250), random.uniform(-100, 100))
        self.spin = 0.0            # ball angular velocity, rad/s
        self.ball_angle = 0.0

    def kick(self):
        self.vel = add(self.vel, (random.uniform(-500, 500), -900))

    def hexagon_vertices(self, radius=HEX_RADIUS):
        cx, cy = CENTER
        return [
            (cx + radius * math.cos(self.angle + i * math.pi / 3),
             cy + radius * math.sin(self.angle + i * math.pi / 3))
            for i in range(6)
        ]

    def wall_velocity_at(self, point):
        # velocity of a point of a rigid body rotating about CENTER: v = omega x r
        rx, ry = sub(point, CENTER)
        return (-self.omega * ry, self.omega * rx)

    def step(self, dt):
        self.angle = (self.angle + self.omega * dt) % (2 * math.pi)

        vx, vy = self.vel
        vy += GRAVITY * dt
        drag = math.exp(-AIR_DRAG * dt)
        self.vel = (vx * drag, vy * drag)
        self.pos = add(self.pos, mul(self.vel, dt))
        self.spin *= math.exp(-ANGULAR_DRAG * dt)
        self.ball_angle += self.spin * dt

        verts = self.hexagon_vertices()
        for i in range(6):
            self.collide_with_wall(verts[i], verts[(i + 1) % 6])

    def collide_with_wall(self, a, b):
        # The hexagon is convex and the ball is inside, so the infinite line of
        # each edge is enough: signed distance along the inward normal.
        edge = sub(b, a)
        e_len = length(edge)
        n = (-edge[1] / e_len, edge[0] / e_len)
        if dot(n, sub(CENTER, a)) < 0:
            n = (-n[0], -n[1])

        signed = dot(sub(self.pos, a), n)
        if signed >= BALL_RADIUS:
            return

        # positional correction (push back inside)
        self.pos = add(self.pos, mul(n, BALL_RADIUS - signed))

        # contact point and relative velocity of the contact point vs the wall
        r = mul(n, -BALL_RADIUS)                       # ball center -> contact
        contact = add(self.pos, r)
        v_wall = self.wall_velocity_at(contact)
        v_contact = add(self.vel, (-self.spin * r[1], self.spin * r[0]))
        v_rel = sub(v_contact, v_wall)
        vn = dot(v_rel, n)
        if vn >= 0:
            return                                     # already separating

        # normal impulse (unit mass); no bounce for slow contacts -> resting
        e = RESTITUTION if -vn > REST_SPEED else 0.0
        jn = -(1 + e) * vn
        self.vel = add(self.vel, mul(n, jn))

        # tangential (friction) impulse, also changes ball spin
        t = (-n[1], n[0])
        v_contact = add(self.vel, (-self.spin * r[1], self.spin * r[0]))
        vt = dot(sub(v_contact, v_wall), t)
        inv_inertia = 1.0 / (INERTIA_FACTOR * BALL_RADIUS ** 2)
        rt = cross(r, t)
        k = 1.0 + rt * rt * inv_inertia                # effective inverse mass
        jt = -vt / k
        max_jt = WALL_FRICTION * jn
        jt = max(-max_jt, min(max_jt, jt))
        self.vel = add(self.vel, mul(t, jt))
        self.spin += rt * jt * inv_inertia

        if jn > 250:
            self.impacts.append((contact[0], contact[1], min(1.0, jn / 2500)))


# ---------------------------------------------------------------- rendering
class App:
    def __init__(self, root):
        self.root = root
        root.title("Ball in a Spinning Hexagon")
        root.configure(bg=BG)
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg=BG,
                                highlightthickness=0)
        self.canvas.pack()
        self.sim = Simulation()
        self.paused = False
        self.trail = []
        self.flashes = []          # [x, y, life, strength, item_id]

        c = self.canvas
        # glow rings behind the wall (fake bloom: wider, darker strokes)
        self.glow_ids = [
            c.create_polygon(0, 0, 0, 0, 0, 0, outline=mix(BG, "#29b6f6", k),
                             fill="", width=w, joinstyle=tk.ROUND)
            for w, k in ((34, 0.10), (24, 0.18))
        ]
        # wall = ring between outer and inner hexagon (collision surface is the inner one)
        self.wall_id = c.create_polygon(0, 0, 0, 0, 0, 0, fill="#1b6f9c",
                                        outline="", smooth=False)
        self.inner_id = c.create_polygon(0, 0, 0, 0, 0, 0, fill="#0f1220",
                                         outline="#7fdcff", width=2)
        self.trail_ids = [c.create_oval(0, 0, 0, 0, fill=BG, outline="")
                          for _ in range(TRAIL_LEN)]
        self.shadow_id = c.create_oval(0, 0, 0, 0, fill="#07080e", outline="")
        self.ball_id = c.create_oval(0, 0, 0, 0, fill="#ff7043",
                                     outline="#ffd0bf", width=2)
        self.hl_id = c.create_oval(0, 0, 0, 0, fill="#ffab91", outline="")
        self.mark_id = c.create_line(0, 0, 0, 0, fill="#5d1f0e", width=3,
                                     capstyle=tk.ROUND)
        self.info_id = c.create_text(14, 12, anchor="nw", fill="#9aa3c0",
                                     font=("Helvetica", 12), text="")

        root.bind("<space>", lambda e: self.sim.kick())
        c.bind("<Button-1>", lambda e: self.sim.kick())
        root.bind("r", lambda e: self.reset())
        root.bind("p", lambda e: self.toggle_pause())
        root.bind("s", lambda e: setattr(self.sim, "omega", -self.sim.omega))
        root.bind("<Up>", lambda e: self.change_spin(math.radians(15)))
        root.bind("<Down>", lambda e: self.change_spin(-math.radians(15)))
        root.bind("<Escape>", lambda e: root.destroy())

        self.dt = 1.0 / PHYSICS_HZ
        self.acc = 0.0
        self.last = time.perf_counter()
        self.fps = 0.0
        self.tick()

    @staticmethod
    def flatten(points):
        return [v for p in points for v in p]

    def reset(self):
        self.sim.reset()
        self.trail.clear()

    def toggle_pause(self):
        self.paused = not self.paused
        self.last = time.perf_counter()

    def change_spin(self, delta):
        self.sim.omega = max(-math.radians(360), min(math.radians(360), self.sim.omega + delta))

    # --- main loop
    def tick(self):
        now = time.perf_counter()
        frame = min(now - self.last, MAX_FRAME_DT)
        self.last = now
        if frame > 0:
            self.fps += (1.0 / frame - self.fps) * 0.05

        if not self.paused:
            self.acc += frame
            while self.acc >= self.dt:
                self.sim.step(self.dt)
                self.acc -= self.dt
            self.trail.append(self.sim.pos)
            del self.trail[:-TRAIL_LEN]

        self.draw(frame)
        self.root.after(8, self.tick)

    def draw(self, frame):
        c, sim = self.canvas, self.sim
        inner = sim.hexagon_vertices(HEX_RADIUS)
        outer = sim.hexagon_vertices(HEX_RADIUS + WALL_THICKNESS / math.cos(math.pi / 6))
        mid = sim.hexagon_vertices(HEX_RADIUS + WALL_THICKNESS * 0.6)
        for gid in self.glow_ids:
            c.coords(gid, *self.flatten(mid))
        c.coords(self.wall_id, *self.flatten(outer))
        c.coords(self.inner_id, *self.flatten(inner))

        # wall impact flashes
        for x, y, s in sim.impacts:
            rad = 10 + 26 * s
            fid = c.create_oval(x - rad, y - rad, x + rad, y + rad,
                                outline="#bff0ff", width=2, fill="")
            c.tag_lower(fid, self.trail_ids[0])
            self.flashes.append([x, y, 1.0, s, fid])
        sim.impacts.clear()
        alive = []
        for f in self.flashes:
            f[2] -= frame * 3.0
            if f[2] <= 0:
                c.delete(f[4])
                continue
            x, y, life, s, fid = f
            rad = (10 + 26 * s) * (1.6 - 0.6 * life)
            c.coords(fid, x - rad, y - rad, x + rad, y + rad)
            c.itemconfigure(fid, outline=mix(BG, "#bff0ff", life))
            alive.append(f)
        self.flashes = alive

        # trail
        n = len(self.trail)
        for i, tid in enumerate(self.trail_ids):
            if i < n - 1:
                x, y = self.trail[i]
                k = (i + 1) / n
                rad = BALL_RADIUS * (0.25 + 0.6 * k)
                c.coords(tid, x - rad, y - rad, x + rad, y + rad)
                c.itemconfigure(tid, fill=mix("#0f1220", "#b5462a", k * 0.7))
            else:
                c.coords(tid, 0, 0, 0, 0)

        # ball
        x, y = sim.pos
        r = BALL_RADIUS
        c.coords(self.shadow_id, x - r + 4, y - r + 6, x + r + 4, y + r + 6)
        c.coords(self.ball_id, x - r, y - r, x + r, y + r)
        c.coords(self.hl_id, x - r * 0.55, y - r * 0.6, x - r * 0.05, y - r * 0.15)
        a = sim.ball_angle
        c.coords(self.mark_id, x + math.cos(a) * r * 0.2, y + math.sin(a) * r * 0.2,
                 x + math.cos(a) * r * 0.8, y + math.sin(a) * r * 0.8)

        c.itemconfigure(
            self.info_id,
            text=f"hexagon spin: {math.degrees(sim.omega):+.0f}°/s    "
                 f"ball speed: {length(sim.vel):.0f} px/s    "
                 f"ball spin: {sim.spin / (2 * math.pi):+.1f} rev/s    "
                 f"{self.fps:.0f} fps{'   [PAUSED]' if self.paused else ''}\n"
                 "Space/click: kick   R: reset   ↑/↓: spin speed   S: reverse   P: pause   Esc: quit")


if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(False, False)
    App(root)
    root.mainloop()
