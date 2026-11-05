#!/usr/bin/env python3
"""
Ball bouncing inside a spinning hexagon.

- Gravity pulls the ball down.
- Air friction (drag) slowly damps the motion.
- Collisions with the rotating walls are resolved in the wall's moving frame:
  the wall surface velocity (omega x r) is taken into account, so the spinning
  hexagon "throws" the ball realistically. Restitution damps the normal
  component, Coulomb-like friction damps the tangential (sliding) component.

Uses only the Python standard library (tkinter). Run:  python3 hexagon_ball.py
Controls:  Space - kick the ball,  R - reset,  Up/Down - change spin speed,  Esc - quit
"""

import math
import random
import tkinter as tk

# ---------------------------------------------------------------- settings
WIDTH, HEIGHT = 800, 800
CENTER = (WIDTH / 2, HEIGHT / 2)
HEX_RADIUS = 300            # center-to-vertex distance (px)
BALL_RADIUS = 18            # px

GRAVITY = 1500.0            # px/s^2 (downwards, +y)
AIR_DRAG = 0.15             # 1/s, linear air friction
RESTITUTION = 0.85          # normal bounce coefficient
WALL_FRICTION = 0.25        # tangential friction coefficient at contact
ANGULAR_SPEED = math.radians(60)  # rad/s, hexagon spin

FPS = 120
SUBSTEPS = 4                # physics substeps per frame for stability


# ---------------------------------------------------------------- vector helpers
def add(a, b): return (a[0] + b[0], a[1] + b[1])
def sub(a, b): return (a[0] - b[0], a[1] - b[1])
def mul(a, s): return (a[0] * s, a[1] * s)
def dot(a, b): return a[0] * b[0] + a[1] * b[1]
def length(a): return math.hypot(a[0], a[1])


def closest_point_on_segment(p, a, b):
    ab = sub(b, a)
    t = dot(sub(p, a), ab) / dot(ab, ab)
    t = max(0.0, min(1.0, t))
    return add(a, mul(ab, t))


# ---------------------------------------------------------------- simulation
class Simulation:
    def __init__(self):
        self.angle = 0.0
        self.omega = ANGULAR_SPEED
        self.reset()

    def reset(self):
        self.pos = (CENTER[0] + random.uniform(-60, 60), CENTER[1] - 120)
        self.vel = (random.uniform(-250, 250), random.uniform(-100, 100))

    def kick(self):
        self.vel = add(self.vel, (random.uniform(-500, 500), -900))

    def hexagon_vertices(self):
        cx, cy = CENTER
        return [
            (cx + HEX_RADIUS * math.cos(self.angle + i * math.pi / 3),
             cy + HEX_RADIUS * math.sin(self.angle + i * math.pi / 3))
            for i in range(6)
        ]

    def wall_velocity_at(self, point):
        # velocity of a point on a rigid body rotating about CENTER: v = omega x r
        rx, ry = sub(point, CENTER)
        return (-self.omega * ry, self.omega * rx)

    def step(self, dt):
        # rotate hexagon
        self.angle = (self.angle + self.omega * dt) % (2 * math.pi)

        # integrate ball (semi-implicit Euler)
        vx, vy = self.vel
        vy += GRAVITY * dt
        drag = math.exp(-AIR_DRAG * dt)
        vx *= drag
        vy *= drag
        self.vel = (vx, vy)
        self.pos = add(self.pos, mul(self.vel, dt))

        # collide against each wall
        verts = self.hexagon_vertices()
        for i in range(6):
            a = verts[i]
            b = verts[(i + 1) % 6]
            self.collide_with_wall(a, b)

    def collide_with_wall(self, a, b):
        closest = closest_point_on_segment(self.pos, a, b)
        diff = sub(self.pos, closest)
        dist = length(diff)

        # inward normal of the wall (pointing toward the hexagon center)
        edge = sub(b, a)
        n = (-edge[1], edge[0])
        n_len = length(n)
        n = (n[0] / n_len, n[1] / n_len)
        if dot(n, sub(CENTER, a)) < 0:
            n = (-n[0], -n[1])

        # signed distance from the wall line along the inward normal
        signed = dot(sub(self.pos, a), n)

        if dist < BALL_RADIUS or signed < BALL_RADIUS:
            # only react if ball is actually near this segment (not its extension)
            if dist > BALL_RADIUS * 2 and signed >= 0:
                return

            # push the ball back inside
            penetration = BALL_RADIUS - signed
            if penetration > 0:
                self.pos = add(self.pos, mul(n, penetration))

            # relative velocity w.r.t. the moving wall
            contact = closest_point_on_segment(self.pos, a, b)
            v_wall = self.wall_velocity_at(contact)
            v_rel = sub(self.vel, v_wall)
            vn = dot(v_rel, n)

            if vn < 0:  # moving into the wall
                v_normal = mul(n, vn)
                v_tangent = sub(v_rel, v_normal)

                # bounce: reverse and damp normal component
                new_normal = mul(n, -vn * RESTITUTION)

                # friction: reduce tangential sliding, limited by normal impulse
                t_len = length(v_tangent)
                if t_len > 1e-9:
                    friction_dv = min(WALL_FRICTION * abs(vn) * (1 + RESTITUTION), t_len)
                    new_tangent = mul(v_tangent, (t_len - friction_dv) / t_len)
                else:
                    new_tangent = v_tangent

                v_rel_new = add(new_normal, new_tangent)
                self.vel = add(v_rel_new, v_wall)


# ---------------------------------------------------------------- rendering
class App:
    def __init__(self, root):
        self.root = root
        root.title("Ball in a Spinning Hexagon")
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="#101018",
                                highlightthickness=0)
        self.canvas.pack()
        self.sim = Simulation()

        self.hex_id = self.canvas.create_polygon(
            *self.flatten(self.sim.hexagon_vertices()),
            outline="#4fc3f7", fill="", width=5)
        x, y = self.sim.pos
        r = BALL_RADIUS
        self.ball_id = self.canvas.create_oval(x - r, y - r, x + r, y + r,
                                               fill="#ff7043", outline="#ffccbc", width=2)
        self.info_id = self.canvas.create_text(
            12, 12, anchor="nw", fill="#9aa0b5", font=("Helvetica", 12),
            text="")

        root.bind("<space>", lambda e: self.sim.kick())
        root.bind("r", lambda e: self.sim.reset())
        root.bind("<Up>", lambda e: self.change_spin(math.radians(15)))
        root.bind("<Down>", lambda e: self.change_spin(-math.radians(15)))
        root.bind("<Escape>", lambda e: root.destroy())

        self.frame_ms = int(1000 / FPS)
        self.tick()

    @staticmethod
    def flatten(points):
        return [c for p in points for c in p]

    def change_spin(self, delta):
        self.sim.omega += delta

    def tick(self):
        dt = 1.0 / FPS
        for _ in range(SUBSTEPS):
            self.sim.step(dt / SUBSTEPS)

        self.canvas.coords(self.hex_id, *self.flatten(self.sim.hexagon_vertices()))
        x, y = self.sim.pos
        r = BALL_RADIUS
        self.canvas.coords(self.ball_id, x - r, y - r, x + r, y + r)
        self.canvas.itemconfigure(
            self.info_id,
            text=f"spin: {math.degrees(self.sim.omega):.0f}°/s   "
                 f"speed: {length(self.sim.vel):.0f} px/s\n"
                 "Space: kick   R: reset   ↑/↓: spin   Esc: quit")

        self.root.after(self.frame_ms, self.tick)


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
