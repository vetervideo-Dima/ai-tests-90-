"""
Nested rotating hexagons with bouncing balls.

Five colored balls start in the innermost hexagon. Every hexagon except the
outermost has one randomly chosen missing wall, so balls can escape outward
(and fall back in). Physics: gravity, air friction, wall friction with ball
spin (angular momentum), and momentum transfer from the rotating walls.

Run:  python nested_hexagons.py      (only needs the standard library / tkinter)
"""
import math
import random
import tkinter as tk

# ----------------------------- adjustable parameters -----------------------------
WIDTH, HEIGHT = 800, 800
GRAVITY = 900.0                 # px / s^2  (downwards)
AIR_FRICTION = 0.15             # linear damping per second (0 = none)
WALL_FRICTION = 0.25            # Coulomb friction coefficient at walls
RESTITUTION = 0.85              # bounciness (1 = perfectly elastic)
HEX_SIZES = [70, 130, 190, 250, 310, 370]          # circumradius, inner -> outer
ROT_SPEEDS = [1.2, -0.8, 0.55, -0.4, 0.25, -0.12]  # rad / s, one per hexagon
BALL_RADIUS = 9
BALL_COLORS = ["#ff4d4d", "#ffb84d", "#4dff88", "#4dc3ff", "#c34dff"]
SUBSTEPS = 8
FPS = 60
# ----------------------------------------------------------------------------------

CX, CY = WIDTH / 2, HEIGHT / 2


class Hexagon:
    def __init__(self, radius, omega, has_gap):
        self.radius = radius
        self.omega = omega
        self.angle = random.uniform(0, 2 * math.pi)
        self.gap = random.randrange(6) if has_gap else None

    def vertices(self):
        return [(CX + self.radius * math.cos(self.angle + k * math.pi / 3),
                 CY + self.radius * math.sin(self.angle + k * math.pi / 3)) for k in range(6)]

    def walls(self):
        v = self.vertices()
        return [(v[k], v[(k + 1) % 6]) for k in range(6) if k != self.gap]


class Ball:
    def __init__(self, x, y, color):
        self.x, self.y = x, y
        self.vx, self.vy = random.uniform(-150, 150), random.uniform(-150, 0)
        self.w = 0.0                       # angular velocity (rad/s)
        self.r = BALL_RADIUS
        self.m = 1.0
        self.I = 0.5 * self.m * self.r ** 2  # solid disc
        self.color = color
        self.rot = 0.0                     # drawn spin angle


def collide_wall(b, a, c, omega):
    """Collide ball b with segment a-c that rotates with angular speed omega about the center."""
    ax, ay = a
    ex, ey = c[0] - ax, c[1] - ay
    L2 = ex * ex + ey * ey
    t = max(0.0, min(1.0, ((b.x - ax) * ex + (b.y - ay) * ey) / L2))
    px, py = ax + t * ex, ay + t * ey          # closest point on the wall
    dx, dy = b.x - px, b.y - py
    d = math.hypot(dx, dy)
    if d >= b.r or d == 0:
        return
    nx, ny = dx / d, dy / d                    # normal pointing towards the ball
    # push the ball out of the wall
    b.x += nx * (b.r - d)
    b.y += ny * (b.r - d)
    # velocity of the wall at the contact point (rotation about the center)
    wvx, wvy = -omega * (py - CY), omega * (px - CX)
    rvx, rvy = b.vx - wvx, b.vy - wvy
    vn = rvx * nx + rvy * ny
    if vn >= 0:
        return
    tx, ty = -ny, nx
    jn = -(1 + RESTITUTION) * vn * b.m
    # slip velocity of ball surface relative to wall (includes spin)
    slip = (rvx * tx + rvy * ty) - b.r * b.w
    jt = -slip * b.m / 3.0                     # impulse to stop slip for a solid disc
    jt = max(-WALL_FRICTION * jn, min(WALL_FRICTION * jn, jt))
    b.vx += (jn * nx + jt * tx) / b.m
    b.vy += (jn * ny + jt * ty) / b.m
    b.w += -b.r * jt / b.I


def collide_balls(b1, b2):
    dx, dy = b2.x - b1.x, b2.y - b1.y
    d = math.hypot(dx, dy)
    rr = b1.r + b2.r
    if d >= rr or d == 0:
        return
    nx, ny = dx / d, dy / d
    overlap = (rr - d) / 2
    b1.x -= nx * overlap; b1.y -= ny * overlap
    b2.x += nx * overlap; b2.y += ny * overlap
    vn = (b2.vx - b1.vx) * nx + (b2.vy - b1.vy) * ny
    if vn >= 0:
        return
    j = -(1 + RESTITUTION) * vn / 2
    b1.vx -= j * nx; b1.vy -= j * ny
    b2.vx += j * nx; b2.vy += j * ny


class App:
    def __init__(self, root):
        self.c = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="#0d0d14", highlightthickness=0)
        self.c.pack()
        n = len(HEX_SIZES)
        self.hexes = [Hexagon(HEX_SIZES[i], ROT_SPEEDS[i % len(ROT_SPEEDS)], i < n - 1) for i in range(n)]
        inner = HEX_SIZES[0] * 0.5
        self.balls = [Ball(CX + random.uniform(-inner, inner) * 0.6,
                           CY + random.uniform(-inner, inner) * 0.6, col) for col in BALL_COLORS]
        self.dt = 1.0 / FPS
        self.tick()

    def step(self, dt):
        for h in self.hexes:
            h.angle += h.omega * dt
        damp = math.exp(-AIR_FRICTION * dt)
        for b in self.balls:
            b.vy += GRAVITY * dt
            b.vx *= damp; b.vy *= damp
            b.w *= damp
            b.x += b.vx * dt
            b.y += b.vy * dt
            b.rot += b.w * dt
        for h in self.hexes:
            walls = h.walls()
            for b in self.balls:
                for a, c in walls:
                    collide_wall(b, a, c, h.omega)
        for i in range(len(self.balls)):
            for j in range(i + 1, len(self.balls)):
                collide_balls(self.balls[i], self.balls[j])

    def draw(self):
        c = self.c
        c.delete("all")
        n = len(self.hexes)
        for i, h in enumerate(self.hexes):
            shade = int(90 + 140 * (1 - i / max(1, n - 1)))
            col = "#%02x%02x%02x" % (shade // 2, shade, 255)
            for a, b in h.walls():
                c.create_line(a[0], a[1], b[0], b[1], fill=col, width=3, capstyle=tk.ROUND)
        for b in self.balls:
            c.create_oval(b.x - b.r, b.y - b.r, b.x + b.r, b.y + b.r, fill=b.color, outline="")
            # a small line shows the ball's spin
            c.create_line(b.x, b.y, b.x + b.r * math.cos(b.rot), b.y + b.r * math.sin(b.rot),
                          fill="#0d0d14", width=2)

    def tick(self):
        sub = self.dt / SUBSTEPS
        for _ in range(SUBSTEPS):
            self.step(sub)
        self.draw()
        self.c.after(int(1000 / FPS), self.tick)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Nested Rotating Hexagons")
    App(root)
    root.mainloop()
