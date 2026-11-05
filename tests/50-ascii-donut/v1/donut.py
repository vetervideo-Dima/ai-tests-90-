#!/usr/bin/env python3
# MATH: a torus point is a circle of radius r (θ) centred R from the axis, swept around the y-axis (φ):
#   P(θ,φ) = ((R + r·cosθ)·cosφ, r·sinθ, −(R + r·cosθ)·sinφ); the unit normal N(θ,φ) is the same with R→0, r→1.
# Each frame P and N are spun by the rotation matrices Rz(B)·Rx(A) (A, B grow with time).
# Perspective projection: x' = cx + 2·K1·x/(K2+z), y' = cy − K1·y/(K2+z); the 2 fixes the ~1:2 cell aspect.
# Lambert lighting: L = max(0, N·Ŝ) for a unit light vector Ŝ; ambient + L indexes the ramp ".,-~:;=!*#$@".
# Z-buffer: per cell keep ooz = 1/(K2+z) (larger = closer); a sample is plotted only if it beats the stored ooz.
# Planet: sphere of radius ρ centred on an inclined circular orbit C(t) = a·(cos ωt, sin ωt·sin i, sin ωt·cos i),
#   surface S = C + ρ·n(u,v) with n the unit sphere direction, which is also its normal; it shares the z-buffer.
# Colour: normalised depth d = (ooz − ooz_min)/(ooz_max − ooz_min) picks an ANSI-256 gradient entry (far→near).
# Stars sit at ooz = 0 (infinitely far) and twinkle with brightness b = ½ + ½·sin(ω_k·t + φ_k).
"""Rotating ASCII donut + orbiting planet + twinkling starfield. Python 3, stdlib only. Ctrl+C to quit."""

import math
import os
import random
import shutil
import signal
import sys
import time

RAMP = ".,-~:;=!*#$@"
FPS = 30.0
FRAME = 1.0 / FPS

# ANSI-256 gradients, ordered far -> near
TORUS_PAL = [53, 89, 125, 161, 162, 198, 199, 205, 209, 215, 221, 227, 229, 230]
OCEAN_PAL = [17, 18, 19, 20, 26, 27, 32, 33, 39, 45, 81, 117]
LAND_PAL = [22, 28, 34, 40, 70, 76, 82, 112, 118, 154, 156, 193]
ORBIT_COL = 238

R1, R2 = 1.0, 2.0          # tube radius, ring radius
K2 = 9.0                   # viewer distance
ORBIT_A = 3.9              # planet orbit radius
ORBIT_I = math.radians(22) # orbit inclination
PLANET_R = 0.62
OMEGA = 0.55               # planet angular speed (rad/s)

_ln = math.sqrt(1 + 1 + 1)
LIGHT = (-1 / _ln, 1 / _ln, -1 / _ln)   # from upper-left, towards the viewer

resized = True


def on_winch(signum, frame):
    global resized
    resized = True


def on_term(signum, frame):
    raise KeyboardInterrupt


def term_size():
    s = shutil.get_terminal_size((80, 24))
    return max(20, s.columns), max(8, s.lines)


class Scene:
    def __init__(self, w, h):
        self.w, self.h = w, h - 1               # last line is the status bar
        self.cx, self.cy = self.w / 2.0, self.h / 2.0
        ext = R1 + R2
        # vertical fit for the torus, horizontal fit for the planet orbit
        k_v = self.h * 0.46 * (K2 - ext) / ext
        k_h = self.w * 0.47 * (K2 - ORBIT_A) / (2.0 * (ORBIT_A + PLANET_R))
        self.K1 = max(1.0, min(k_v, k_h))
        self.ooz_min = 1.0 / (K2 + ORBIT_A + PLANET_R)
        self.ooz_max = 1.0 / (K2 - ORBIT_A - PLANET_R)
        self._build_torus()
        self._build_sphere()
        self._build_orbit()
        self._build_stars()

    # ---------- geometry caches (rebuilt on resize) ----------
    def _build_torus(self):
        # choose sample density so neighbouring samples land < 1 cell apart
        scale = 2.0 * self.K1 / (K2 - R1 - R2)
        n_phi = int(min(900, max(90, 2 * math.pi * (R1 + R2) * scale * 1.1)))
        n_th = int(min(300, max(30, 2 * math.pi * R1 * scale * 1.2)))
        pts = []
        for i in range(n_th):
            th = 2 * math.pi * i / n_th
            ct, st = math.cos(th), math.sin(th)
            for j in range(n_phi):
                ph = 2 * math.pi * j / n_phi
                cp, sp = math.cos(ph), math.sin(ph)
                cx = R2 + R1 * ct
                pts.append((cx * cp, R1 * st, -cx * sp, ct * cp, st, -ct * sp))
        self.torus = pts

    def _build_sphere(self):
        rad = PLANET_R * 2.0 * self.K1 / (K2 - ORBIT_A)
        n_v = int(min(120, max(16, math.pi * rad * 1.4)))
        n_u = int(min(240, max(32, 2 * math.pi * rad * 1.4)))
        pts = []
        for i in range(1, n_v):
            v = math.pi * i / n_v
            sv, cv = math.sin(v), math.cos(v)
            for j in range(n_u):
                u = 2 * math.pi * j / n_u
                pts.append((sv * math.cos(u), cv, sv * math.sin(u), u, v))
        self.sphere = pts

    def _build_orbit(self):
        n = int(max(60, 2 * math.pi * ORBIT_A * 2.0 * self.K1 / K2 * 0.5))
        si, ci = math.sin(ORBIT_I), math.cos(ORBIT_I)
        self.orbit = []
        for k in range(n):
            a = 2 * math.pi * k / n
            self.orbit.append((ORBIT_A * math.cos(a), ORBIT_A * math.sin(a) * si,
                               ORBIT_A * math.sin(a) * ci))

    def _build_stars(self):
        rnd = random.Random(1234)
        count = max(20, self.w * self.h // 38)
        self.stars = [(rnd.randrange(self.w), rnd.randrange(self.h),
                       rnd.uniform(0, 2 * math.pi), rnd.uniform(0.6, 3.2))
                      for _ in range(count)]

    # ---------- per-frame ----------
    def depth_idx(self, ooz, n):
        d = (ooz - self.ooz_min) / (self.ooz_max - self.ooz_min)
        k = int(d * n)
        return 0 if k < 0 else (n - 1 if k >= n else k)

    def render(self, t):
        w, h = self.w, self.h
        size = w * h
        chars = [" "] * size
        cols = [0] * size
        zbuf = [0.0] * size
        K1, cx, cy = self.K1, self.cx, self.cy
        lx, ly, lz = LIGHT
        nramp = len(RAMP)

        # stars (ooz = 0 -> behind everything)
        for (sx, sy, ph, sp) in self.stars:
            b = 0.5 + 0.5 * math.sin(t * sp + ph)
            if b < 0.25:
                continue
            p = sy * w + sx
            chars[p] = "." if b < 0.6 else ("+" if b < 0.9 else "*")
            cols[p] = 236 + int(b * 19)

        # faint orbit path
        for (ox, oy, oz) in self.orbit:
            ooz = 1.0 / (K2 + oz)
            xp = int(cx + 2.0 * K1 * ooz * ox)
            yp = int(cy - K1 * ooz * oy)
            if 0 <= xp < w and 0 <= yp < h:
                p = yp * w + xp
                if ooz > zbuf[p]:
                    zbuf[p] = ooz
                    chars[p] = "."
                    cols[p] = ORBIT_COL

        # torus
        A = t * 0.9
        B = t * 0.45
        cA, sA, cB, sB = math.cos(A), math.sin(A), math.cos(B), math.sin(B)
        npal = len(TORUS_PAL)
        omin = self.ooz_min
        orng = self.ooz_max - self.ooz_min
        for (x, y, z, nx, ny, nz) in self.torus:
            # Rx(A)
            y1 = y * cA - z * sA
            z1 = y * sA + z * cA
            # Rz(B)
            x2 = x * cB - y1 * sB
            y2 = x * sB + y1 * cB
            ooz = 1.0 / (K2 + z1)
            xp = int(cx + 2.0 * K1 * ooz * x2)
            yp = int(cy - K1 * ooz * y2)
            if xp < 0 or xp >= w or yp < 0 or yp >= h:
                continue
            p = yp * w + xp
            if ooz <= zbuf[p]:
                continue
            zbuf[p] = ooz
            ny1 = ny * cA - nz * sA
            nz1 = ny * sA + nz * cA
            nx2 = nx * cB - ny1 * sB
            ny2 = nx * sB + ny1 * cB
            L = nx2 * lx + ny2 * ly + nz1 * lz
            lum = 0.12 + 0.88 * (L if L > 0 else 0.0)
            ci = int(lum * nramp)
            chars[p] = RAMP[ci if ci < nramp else nramp - 1]
            k = int((ooz - omin) / orng * npal * 0.55 + lum * npal * 0.45)
            cols[p] = TORUS_PAL[k if k < npal else npal - 1]

        # planet
        ang = t * OMEGA
        si, ci_ = math.sin(ORBIT_I), math.cos(ORBIT_I)
        pcx = ORBIT_A * math.cos(ang)
        pcy = ORBIT_A * math.sin(ang) * si
        pcz = ORBIT_A * math.sin(ang) * ci_
        spin = t * 0.8
        nop = len(OCEAN_PAL)
        for (nx, ny, nz, u, v) in self.sphere:
            L = nx * lx + ny * ly + nz * lz
            if nz > 0.35:                       # far hemisphere: cheap back-face cull
                continue
            X = pcx + PLANET_R * nx
            Y = pcy + PLANET_R * ny
            Z = pcz + PLANET_R * nz
            ooz = 1.0 / (K2 + Z)
            xp = int(cx + 2.0 * K1 * ooz * X)
            yp = int(cy - K1 * ooz * Y)
            if xp < 0 or xp >= w or yp < 0 or yp >= h:
                continue
            p = yp * w + xp
            if ooz <= zbuf[p]:
                continue
            zbuf[p] = ooz
            lum = 0.1 + 0.9 * (L if L > 0 else 0.0)
            ci = int(lum * nramp)
            chars[p] = RAMP[ci if ci < nramp else nramp - 1]
            uu = u + spin
            land = (math.sin(3 * uu) * math.sin(2 * v + 0.5) + 0.5 * math.sin(5 * uu + 1.3) * math.cos(3 * v)) > 0.25
            pal = LAND_PAL if land else OCEAN_PAL
            dk = (ooz - omin) / orng
            k = int((dk * 0.4 + lum * 0.6) * nop)
            cols[p] = pal[k if k < nop else nop - 1]

        # compose rows with minimal colour escapes
        out = ["\x1b[H"]
        for row in range(h):
            base = row * w
            last = -1
            seg = []
            for c in range(w):
                ch = chars[base + c]
                if ch != " ":
                    col = cols[base + c]
                    if col != last:
                        seg.append("\x1b[38;5;%dm" % col)
                        last = col
                seg.append(ch)
            out.append("".join(seg))
            out.append("\n")
        return "".join(out)


def main():
    global resized
    if hasattr(signal, "SIGWINCH"):
        signal.signal(signal.SIGWINCH, on_winch)
    signal.signal(signal.SIGTERM, on_term)

    out = sys.stdout
    old_tty = None
    try:
        import termios
        fd = sys.stdin.fileno()
        old_tty = termios.tcgetattr(fd)
        new = termios.tcgetattr(fd)
        new[3] &= ~(termios.ECHO | termios.ICANON)
        termios.tcsetattr(fd, termios.TCSADRAIN, new)
    except Exception:
        old_tty = None

    out.write("\x1b[?1049h\x1b[?25l\x1b[2J")
    out.flush()
    scene = None
    t0 = time.perf_counter()
    fps_est = FPS
    last = t0
    try:
        while True:
            frame_start = time.perf_counter()
            if resized or scene is None or (scene.w, scene.h + 1) != term_size():
                resized = False
                w, h = term_size()
                scene = Scene(w, h)
                out.write("\x1b[0m\x1b[2J")
            t = frame_start - t0
            buf = scene.render(t)
            status = " donut.py  %dx%d  %4.1f fps  Ctrl+C to quit" % (scene.w, scene.h + 1, fps_est)
            out.write(buf + "\x1b[38;5;244m" + status[: scene.w - 1] + "\x1b[K")
            out.flush()
            now = time.perf_counter()
            dt = now - last
            last = now
            if dt > 0:
                fps_est = fps_est * 0.9 + (1.0 / dt) * 0.1
            spare = FRAME - (now - frame_start)
            if spare > 0:
                time.sleep(spare)
    except KeyboardInterrupt:
        pass
    finally:
        out.write("\x1b[0m\x1b[?25h\x1b[?1049l")
        out.flush()
        if old_tty is not None:
            try:
                import termios
                termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, old_tty)
            except Exception:
                pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
