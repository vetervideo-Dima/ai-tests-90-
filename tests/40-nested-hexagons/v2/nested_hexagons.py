"""
Nested rotating hexagons with bouncing balls  (v2).

Five colored balls start in the innermost hexagon. Every hexagon except the
outermost has exactly one randomly chosen missing wall, so balls can pass
between rings. Physics: gravity, air friction, Coulomb wall friction with ball
spin (angular momentum), momentum transfer from rotating walls, ball-ball
collisions.

Run:  python nested_hexagons.py        (standard library only: tkinter)

Keys:  G/g gravity +/-   F/f friction +/-   S/s rotation speed +/-
       ]/[ hexagon size +/-   R new layout   Space pause   Esc quit
"""
import math
import random
import time
import tkinter as tk

# ----------------------------- adjustable parameters -----------------------------
WIDTH, HEIGHT = 800, 800
GRAVITY = 500.0                 # px / s^2 (downwards)
AIR_FRICTION = 0.08             # linear damping per second (0 = none)
WALL_FRICTION = 0.70            # Coulomb friction coefficient at walls
RESTITUTION = 0.92              # bounciness (1 = perfectly elastic)
HEX_SIZES = [70, 125, 180, 235, 290, 345]          # circumradius, inner -> outer
ROT_SPEEDS = [1.4, -1.1, 0.9, -0.8, 0.7, -1.3]    # rad / s, one per hexagon
SPEED_SCALE = 1.0               # global multiplier for all rotation speeds
SIZE_SCALE = 1.0                # global multiplier for all hexagon sizes
BALL_RADIUS = 9
BALL_COLORS = ["#ff5a5f", "#ffb547", "#5cff9d", "#4dc9ff", "#c77dff"]
SUBSTEPS = 10
MAX_SPEED = 2200.0              # px / s, guards against tunnelling
TRAIL = 14                      # trail length in frames
FPS = 60
BG = "#0b0c14"
# ----------------------------------------------------------------------------------

CX, CY = WIDTH / 2, HEIGHT / 2


def hex_to_rgb(h):
    return int(h[1:3], 16), int(h[3:5], 16), int(h[5:7], 16)


def mix(c1, c2, t):
    a, b = hex_to_rgb(c1), hex_to_rgb(c2)
    return "#%02x%02x%02x" % tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


class Hexagon:
    def __init__(self, radius, omega, has_gap):
        self.base_radius = radius
        self.base_omega = omega
        self.angle = random.uniform(0, 2 * math.pi)
        self.gap = random.randrange(6) if has_gap else None

    @property
    def radius(self):
        return self.base_radius * SIZE_SCALE

    @property
    def omega(self):
        return self.base_omega * SPEED_SCALE

    def vertices(self):
        r = self.radius
        return [(CX + r * math.cos(self.angle + k * math.pi / 3),
                 CY + r * math.sin(self.angle + k * math.pi / 3)) for k in range(6)]

    def walls(self):
        v = self.vertices()
        return [(v[k], v[(k + 1) % 6]) for k in range(6) if k != self.gap]


class Ball:
    def __init__(self, x, y, color):
        self.x, self.y = x, y
        self.vx, self.vy = random.uniform(-220, 220), random.uniform(-260, -60)
        self.w = 0.0                         # angular velocity (rad/s)
        self.r = BALL_RADIUS
        self.m = 1.0
        self.I = 0.5 * self.m * self.r ** 2  # solid disc
        self.color = color
        self.rot = random.uniform(0, 6.28)   # drawn spin angle
        self.trail = []


def collide_wall(b, a, c, omega):
    """Collide ball b with segment a-c rotating at omega about the centre."""
    ax, ay = a
    ex, ey = c[0] - ax, c[1] - ay
    L2 = ex * ex + ey * ey
    t = max(0.0, min(1.0, ((b.x - ax) * ex + (b.y - ay) * ey) / L2))
    px, py = ax + t * ex, ay + t * ey
    dx, dy = b.x - px, b.y - py
    d2 = dx * dx + dy * dy
    if d2 >= b.r * b.r:
        return
    d = math.sqrt(d2)
    if d < 1e-9:                       # centre exactly on the wall: use the wall normal
        nx, ny = -ey / math.sqrt(L2), ex / math.sqrt(L2)
    else:
        nx, ny = dx / d, dy / d
    b.x += nx * (b.r - d)
    b.y += ny * (b.r - d)
    wvx, wvy = -omega * (py - CY), omega * (px - CX)   # wall velocity at contact
    rvx, rvy = b.vx - wvx, b.vy - wvy
    vn = rvx * nx + rvy * ny
    if vn >= 0:
        return
    tx, ty = -ny, nx
    e = RESTITUTION if vn < -30 else 0.0               # no micro-bounces when resting
    jn = -(1 + e) * vn * b.m
    slip = (rvx * tx + rvy * ty) - b.r * b.w
    jt = -slip * b.m / 3.0
    lim = WALL_FRICTION * jn
    jt = max(-lim, min(lim, jt))
    b.vx += (jn * nx + jt * tx) / b.m
    b.vy += (jn * ny + jt * ty) / b.m
    b.w += -b.r * jt / b.I


def collide_balls(b1, b2):
    dx, dy = b2.x - b1.x, b2.y - b1.y
    rr = b1.r + b2.r
    d2 = dx * dx + dy * dy
    if d2 >= rr * rr or d2 == 0:
        return
    d = math.sqrt(d2)
    nx, ny = dx / d, dy / d
    o = (rr - d) / 2
    b1.x -= nx * o; b1.y -= ny * o
    b2.x += nx * o; b2.y += ny * o
    vn = (b2.vx - b1.vx) * nx + (b2.vy - b1.vy) * ny
    if vn >= 0:
        return
    j = -(1 + RESTITUTION) * vn / 2
    b1.vx -= j * nx; b1.vy -= j * ny
    b2.vx += j * nx; b2.vy += j * ny


class World:
    def __init__(self):
        self.reset()

    def reset(self):
        n = len(HEX_SIZES)
        self.hexes = [Hexagon(HEX_SIZES[i], ROT_SPEEDS[i % len(ROT_SPEEDS)], i < n - 1) for i in range(n)]
        self.balls = []
        for col in BALL_COLORS:   # random non-overlapping positions inside the innermost hexagon
            for _ in range(100):
                a, rr = random.uniform(0, 6.28), random.uniform(0, HEX_SIZES[0] * SIZE_SCALE * 0.55)
                x, y = CX + rr * math.cos(a), CY + rr * math.sin(a)
                if all(math.hypot(x - o.x, y - o.y) > 2.2 * BALL_RADIUS for o in self.balls):
                    break
            self.balls.append(Ball(x, y, col))

    def step(self, dt):
        for h in self.hexes:
            h.angle += h.omega * dt
        damp = math.exp(-AIR_FRICTION * dt)
        for b in self.balls:
            b.vy += GRAVITY * dt
            b.vx *= damp; b.vy *= damp; b.w *= damp
            s = math.hypot(b.vx, b.vy)
            if s > MAX_SPEED:
                b.vx *= MAX_SPEED / s; b.vy *= MAX_SPEED / s
            b.x += b.vx * dt
            b.y += b.vy * dt
            b.rot += b.w * dt
        for h in self.hexes:
            walls, om = h.walls(), h.omega
            for b in self.balls:
                # cheap broad phase: only walls of a ring the ball is near
                r = math.hypot(b.x - CX, b.y - CY)
                if r < h.radius * 0.866 - b.r - 2 or r > h.radius + b.r + 2:
                    continue
                for a, c in walls:
                    collide_wall(b, a, c, om)
        bs = self.balls
        for i in range(len(bs)):
            for j in range(i + 1, len(bs)):
                collide_balls(bs[i], bs[j])
        # safety net: never let a ball leave the closed outer hexagon
        outer = self.hexes[-1].radius * 0.866 - BALL_RADIUS
        for b in bs:
            r = math.hypot(b.x - CX, b.y - CY)
            if r > self.hexes[-1].radius:
                b.x, b.y = CX + (b.x - CX) * outer / r, CY + (b.y - CY) * outer / r
                b.vx, b.vy = -b.vx * 0.5, -b.vy * 0.5


class App:
    def __init__(self, root):
        self.root = root
        self.c = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg=BG, highlightthickness=0)
        self.c.pack()
        self.world = World()
        self.paused = False
        self.build_items()
        for k in "GgFfSs[]Rr":
            root.bind(k, self.key)
        root.bind("<space>", lambda e: setattr(self, "paused", not self.paused))
        root.bind("<Escape>", lambda e: root.destroy())
        self.last = time.perf_counter()
        self.acc = 0.0
        self.tick()

    # -- canvas items are created once and only moved afterwards (much faster than delete("all")) --
    def build_items(self):
        c = self.c
        c.delete("all")
        n = len(self.world.hexes)
        self.hex_items = []
        for i, h in enumerate(self.world.hexes):
            t = i / max(1, n - 1)
            col = mix("#7ef0ff", "#6a5cff", t)
            glow = mix(BG, col, 0.28)
            items = []
            for _ in range(6):
                g = c.create_line(0, 0, 0, 0, fill=glow, width=9, capstyle=tk.ROUND)
                ln = c.create_line(0, 0, 0, 0, fill=col, width=3, capstyle=tk.ROUND)
                items.append((g, ln))
            self.hex_items.append(items)
        self.ball_items = []
        for b in self.world.balls:
            trail = [c.create_line(0, 0, 0, 0, fill=mix(BG, b.color, (k + 1) / TRAIL * 0.7),
                                   width=max(1, int(b.r * 1.6 * (k + 1) / TRAIL)), capstyle=tk.ROUND)
                     for k in range(TRAIL)]
            glow = c.create_oval(0, 0, 0, 0, fill=mix(BG, b.color, 0.3), outline="")
            body = c.create_oval(0, 0, 0, 0, fill=b.color, outline="")
            hl = c.create_oval(0, 0, 0, 0, fill=mix(b.color, "#ffffff", 0.6), outline="")
            spin = c.create_line(0, 0, 0, 0, fill=mix(b.color, "#000000", 0.55), width=2)
            self.ball_items.append((trail, glow, body, hl, spin))
        self.hud = c.create_text(14, 12, anchor="nw", fill="#8b90b0", font=("Helvetica", 11))

    def key(self, e):
        global GRAVITY, WALL_FRICTION, AIR_FRICTION, SPEED_SCALE, SIZE_SCALE
        k = e.keysym if len(e.keysym) > 1 else e.char
        if k == "G": GRAVITY = min(3000, GRAVITY + 100)
        elif k == "g": GRAVITY = max(0, GRAVITY - 100)
        elif k == "F": WALL_FRICTION = min(1.5, WALL_FRICTION + 0.05); AIR_FRICTION = min(1, AIR_FRICTION + 0.02)
        elif k == "f": WALL_FRICTION = max(0, WALL_FRICTION - 0.05); AIR_FRICTION = max(0, AIR_FRICTION - 0.02)
        elif k == "S": SPEED_SCALE = min(4, SPEED_SCALE + 0.1)
        elif k == "s": SPEED_SCALE = max(-4, SPEED_SCALE - 0.1)
        elif k in ("bracketright", "]"): SIZE_SCALE = min(1.12, SIZE_SCALE + 0.04)
        elif k in ("bracketleft", "["): SIZE_SCALE = max(0.7, SIZE_SCALE - 0.04)
        elif k in "Rr":
            self.world.reset(); self.build_items()

    def draw(self):
        c = self.c
        for h, items in zip(self.world.hexes, self.hex_items):
            v = h.vertices()
            for k, (g, ln) in enumerate(items):
                if k == h.gap:
                    c.itemconfigure(g, state="hidden"); c.itemconfigure(ln, state="hidden")
                    continue
                a, b = v[k], v[(k + 1) % 6]
                c.coords(g, a[0], a[1], b[0], b[1]); c.coords(ln, a[0], a[1], b[0], b[1])
        for b, (trail, glow, body, hl, spin) in zip(self.world.balls, self.ball_items):
            b.trail.append((b.x, b.y))
            if len(b.trail) > TRAIL + 1:
                b.trail.pop(0)
            pts = b.trail
            off = TRAIL + 1 - len(pts)
            for k, it in enumerate(trail):
                i = k - off
                if 0 <= i < len(pts) - 1:
                    c.coords(it, pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1])
                else:
                    c.coords(it, -50, -50, -50, -50)
            r = b.r
            c.coords(glow, b.x - r * 1.9, b.y - r * 1.9, b.x + r * 1.9, b.y + r * 1.9)
            c.coords(body, b.x - r, b.y - r, b.x + r, b.y + r)
            c.coords(hl, b.x - r * 0.55, b.y - r * 0.6, b.x - r * 0.1, b.y - r * 0.15)
            c.coords(spin, b.x + r * 0.2 * math.cos(b.rot), b.y + r * 0.2 * math.sin(b.rot),
                     b.x + r * 0.9 * math.cos(b.rot), b.y + r * 0.9 * math.sin(b.rot))
        c.itemconfigure(self.hud, text=(
            f"gravity {GRAVITY:.0f}  [G/g]    friction {WALL_FRICTION:.2f}/{AIR_FRICTION:.2f}  [F/f]    "
            f"rotation x{SPEED_SCALE:.1f}  [S/s]    size x{SIZE_SCALE:.2f}  [ ] ]    R reset   Space pause"
            + ("   — PAUSED" if self.paused else "")))

    def tick(self):
        now = time.perf_counter()
        frame = min(now - self.last, 0.05)          # real-time step, clamped after stalls
        self.last = now
        if not self.paused:
            sub = frame / SUBSTEPS
            for _ in range(SUBSTEPS):
                self.world.step(sub)
        self.draw()
        self.root.after(max(1, int(1000 / FPS - (time.perf_counter() - now) * 1000)), self.tick)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Nested Rotating Hexagons")
    root.configure(bg=BG)
    root.resizable(False, False)
    App(root)
    root.mainloop()
