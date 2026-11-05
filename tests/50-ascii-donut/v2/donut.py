#!/usr/bin/env python3
# MATH: a torus point is a circle of radius r (θ) centred R from the axis, swept around the y-axis (φ):
#   P(θ,φ) = ((R + r·cosθ)·cosφ, r·sinθ, −(R + r·cosθ)·sinφ); the unit normal N(θ,φ) is the same with R→0, r→1.
# Each frame P and N are spun by the rotation matrices Rz(B)·Rx(A) (A, B grow with time).
# Perspective projection: x' = cx + 2·K1·x/(K2+z), y' = cy − K1·y/(K2+z); the 2 fixes the ~1:2 cell aspect.
# Blinn-Phong: L = amb + kd·max(0, N·Ŝ) + ks·max(0, N·Ĥ)^n, Ĥ = norm(Ŝ + V̂); L indexes the ramp ".,-~:;=!*#$@".
# Z-buffer: per cell keep ooz = 1/(K2+z) (larger = closer); a sample is plotted only if it beats the stored ooz.
# Planet: sphere of radius ρ centred on an inclined circular orbit C(t) = a·(cos ωt, sin ωt·sin i, sin ωt·cos i),
#   surface S = C + ρ·n(u,v) with n the unit sphere direction, which is also its normal; it shares the z-buffer.
# Colour: normalised depth d = (ooz − ooz_min)/(ooz_max − ooz_min) blends with L to pick an ANSI-256 entry.
# Stars sit at ooz = 0 (infinitely far), drift with parallax and twinkle with b = ½ + ½·sin(ω_k·t + φ_k).
"""Rotating ASCII donut + orbiting planet + twinkling starfield. Python 3, stdlib only.
Ctrl+C (or q / Esc) to quit."""

import math
import os
import random
import select
import shutil
import signal
import sys
import time

RAMP = ".,-~:;=!*#$@"
FPS = 30.0
FRAME = 1.0 / FPS

# ANSI-256 gradients, ordered dark/far -> bright/near
TORUS_PAL = [53, 89, 90, 125, 126, 161, 162, 198, 204, 209, 215, 216, 222, 223, 229, 230, 231]
OCEAN_PAL = [18, 19, 20, 26, 27, 32, 33, 39, 38, 45, 81, 117, 159]
LAND_PAL = [22, 28, 34, 64, 70, 76, 106, 112, 148, 154, 190, 193]
ICE_PAL = [60, 103, 146, 152, 189, 195, 231]
ATMO_COL = 87
ORBIT_COL = 237
STAR_TINTS = [(244, 255), (67, 153), (136, 229), (240, 250)]   # (dim, bright)

R1, R2 = 1.0, 2.0          # tube radius, ring radius
K2 = 11.0                  # viewer distance
ORBIT_A = 4.9              # planet orbit radius (clear of the torus: R1+R2 = 3)
ORBIT_I = math.radians(24) # orbit inclination
PLANET_R = 0.85
OMEGA = 0.6                # planet angular speed (rad/s)

_ln = math.sqrt(1.0 + 1.3 * 1.3 + 1.0)
LIGHT = (-1.0 / _ln, 1.3 / _ln, -1.0 / _ln)       # from upper-left, towards the viewer
_hx, _hy, _hz = LIGHT[0], LIGHT[1], LIGHT[2] - 1.0  # half vector with V = (0,0,-1)
_hn = math.sqrt(_hx * _hx + _hy * _hy + _hz * _hz)
HALF = (_hx / _hn, _hy / _hn, _hz / _hn)

resized = True


def on_winch(signum, frame):
    global resized
    resized = True


def on_term(signum, frame):
    raise KeyboardInterrupt


def term_size():
    s = shutil.get_terminal_size((80, 24))
    return max(24, s.columns), max(10, s.lines)


class Scene:
    def __init__(self, w, h):
        self.w, self.h = w, h - 1               # last line is the status bar
        self.cx, self.cy = self.w / 2.0, self.h / 2.0
        ext = R1 + R2
        reach = ORBIT_A + PLANET_R
        # fit: torus vertically, orbit horizontally (x has the 2x aspect factor)
        k_v = self.h * 0.47 * (K2 - ext) / ext
        k_h = self.w * 0.48 * (K2 - ORBIT_A) / (2.0 * reach)
        self.K1 = max(1.0, min(k_v, k_h))
        self.ooz_min = 1.0 / (K2 + reach)
        self.ooz_max = 1.0 / (K2 - reach)
        self._build_torus()
        self._build_sphere()
        self._build_orbit()
        self._build_stars()

    # ---------- geometry caches (rebuilt on resize) ----------
    def _build_torus(self):
        # sample density so neighbouring samples land < 1 cell apart
        scale = 2.0 * self.K1 / (K2 - R1 - R2)
        n_phi = int(min(900, max(90, 2 * math.pi * (R1 + R2) * scale * 1.05)))
        n_th = int(min(300, max(30, 2 * math.pi * R1 * scale * 1.15)))
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
        n_v = int(min(140, max(16, math.pi * rad * 1.5)))
        n_u = int(min(280, max(32, 2 * math.pi * rad * 1.5)))
        pts = []
        for i in range(1, n_v):
            v = math.pi * i / n_v
            sv, cv = math.sin(v), math.cos(v)
            ice = abs(cv) > 0.86
            for j in range(n_u):
                u = 2 * math.pi * j / n_u
                pts.append((sv * math.cos(u), cv, sv * math.sin(u), u, v, ice))
        self.sphere = pts

    def _build_orbit(self):
        n = int(max(80, 2 * math.pi * ORBIT_A * 2.0 * self.K1 / K2 * 0.45))
        si, ci = math.sin(ORBIT_I), math.cos(ORBIT_I)
        self.orbit = []
        for k in range(n):
            a = 2 * math.pi * k / n
            self.orbit.append((ORBIT_A * math.cos(a), ORBIT_A * math.sin(a) * si,
                               ORBIT_A * math.sin(a) * ci))

    def _build_stars(self):
        rnd = random.Random(1234)
        count = max(24, self.w * self.h // 34)
        self.stars = []
        for _ in range(count):
            depth = rnd.random()                     # 0 far .. 1 near (parallax speed)
            tint = STAR_TINTS[rnd.randrange(len(STAR_TINTS))]
            self.stars.append((rnd.uniform(0, self.w), rnd.randrange(self.h),
                               rnd.uniform(0, 2 * math.pi), rnd.uniform(0.6, 3.0),
                               0.15 + 1.1 * depth * depth, tint))

    # ---------- per-frame ----------
    def render(self, t):
        w, h = self.w, self.h
        size = w * h
        chars = [" "] * size
        cols = [0] * size
        zbuf = [0.0] * size
        K1, cx, cy = self.K1, self.cx, self.cy
        lx, ly, lz = LIGHT
        hx, hy, hz = HALF
        nramp = len(RAMP)
        omin = self.ooz_min
        orng = self.ooz_max - self.ooz_min

        # stars (ooz = 0 -> behind everything), slow parallax drift to the left
        for (sx, sy, ph, sp, drift, tint) in self.stars:
            b = 0.5 + 0.5 * math.sin(t * sp + ph)
            if b < 0.22:
                continue
            x = int((sx - drift * t) % w)
            p = sy * w + x
            if b < 0.55:
                chars[p] = "."
                cols[p] = tint[0]
            elif b < 0.88:
                chars[p] = "+"
                cols[p] = tint[0] if b < 0.7 else tint[1]
            else:
                chars[p] = "*"
                cols[p] = tint[1]

        # faint orbit path (dotted)
        for (ox, oy, oz) in self.orbit:
            ooz = 1.0 / (K2 + oz)
            xp = int(cx + 2.0 * K1 * ooz * ox)
            yp = int(cy - K1 * ooz * oy)
            if 0 <= xp < w and 0 <= yp < h:
                p = yp * w + xp
                if ooz > zbuf[p]:
                    zbuf[p] = ooz
                    chars[p] = "."
                    cols[p] = ORBIT_COL if oz > 0 else ORBIT_COL + 3

        # torus
        A = t * 0.9
        B = t * 0.45
        cA, sA, cB, sB = math.cos(A), math.sin(A), math.cos(B), math.sin(B)
        npal = len(TORUS_PAL)
        tpal = TORUS_PAL
        for (x, y, z, nx, ny, nz) in self.torus:
            y1 = y * cA - z * sA                 # Rx(A)
            z1 = y * sA + z * cA
            ooz = 1.0 / (K2 + z1)
            x2 = x * cB - y1 * sB                # Rz(B)
            xp = int(cx + 2.0 * K1 * ooz * x2)
            if xp < 0 or xp >= w:
                continue
            y2 = x * sB + y1 * cB
            yp = int(cy - K1 * ooz * y2)
            if yp < 0 or yp >= h:
                continue
            p = yp * w + xp
            if ooz <= zbuf[p]:
                continue
            zbuf[p] = ooz
            ny1 = ny * cA - nz * sA
            nz1 = ny * sA + nz * cA
            nx2 = nx * cB - ny1 * sB
            ny2 = nx * sB + ny1 * cB
            d = nx2 * lx + ny2 * ly + nz1 * lz
            if d > 0:
                s = nx2 * hx + ny2 * hy + nz1 * hz
                if s > 0:
                    s = s * s
                    s = s * s
                    s = s * s * s * s            # ^16
                else:
                    s = 0.0
                lum = 0.08 + 0.72 * d + 0.45 * s
            else:
                lum = 0.08
            if lum > 1.0:
                lum = 1.0
            ci = int(lum * nramp)
            chars[p] = RAMP[ci if ci < nramp else nramp - 1]
            k = int(((ooz - omin) / orng * 0.35 + lum * 0.65) * npal)
            cols[p] = tpal[k if k < npal else npal - 1]

        # planet
        ang = t * OMEGA
        si, co = math.sin(ORBIT_I), math.cos(ORBIT_I)
        pcx = ORBIT_A * math.cos(ang)
        pcy = ORBIT_A * math.sin(ang) * si
        pcz = ORBIT_A * math.sin(ang) * co
        spin = t * 0.7
        nop, nlp, nip = len(OCEAN_PAL), len(LAND_PAL), len(ICE_PAL)
        sin = math.sin
        for (nx, ny, nz, u, v, ice) in self.sphere:
            if nz > 0.2:                          # far hemisphere: back-face cull
                continue
            X = pcx + PLANET_R * nx
            Z = pcz + PLANET_R * nz
            ooz = 1.0 / (K2 + Z)
            xp = int(cx + 2.0 * K1 * ooz * X)
            if xp < 0 or xp >= w:
                continue
            yp = int(cy - K1 * ooz * (pcy + PLANET_R * ny))
            if yp < 0 or yp >= h:
                continue
            p = yp * w + xp
            if ooz <= zbuf[p]:
                continue
            zbuf[p] = ooz
            d = nx * lx + ny * ly + nz * lz
            lum = 0.1 + 0.9 * (d if d > 0 else 0.0)
            ci = int(lum * nramp)
            chars[p] = RAMP[ci if ci < nramp else nramp - 1]
            if nz > -0.28 and d > -0.2:           # lit limb: atmosphere glow
                cols[p] = ATMO_COL
                continue
            if ice:
                pal, n = ICE_PAL, nip
            else:
                uu = u + spin
                land = (sin(3 * uu) * sin(2 * v + 0.5) + 0.5 * sin(5 * uu + 1.3) * sin(3 * v + 1.0)) > 0.22
                pal, n = (LAND_PAL, nlp) if land else (OCEAN_PAL, nop)
            k = int(((ooz - omin) / orng * 0.3 + lum * 0.7) * n)
            cols[p] = pal[k if k < n else n - 1]

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


def key_pressed(fd):
    """Non-blocking check for q / Esc (only when stdin is a tty in non-canonical mode)."""
    try:
        r, _, _ = select.select([fd], [], [], 0)
        if r:
            data = os.read(fd, 32)
            return b"q" in data or b"Q" in data or b"\x1b" in data
    except Exception:
        pass
    return False


def main():
    global resized
    if hasattr(signal, "SIGWINCH"):
        signal.signal(signal.SIGWINCH, on_winch)
    signal.signal(signal.SIGTERM, on_term)

    out = sys.stdout
    if os.name == "nt":                       # enable ANSI on Windows 10+
        os.system("")
    old_tty = None
    fd = None
    try:
        import termios
        fd = sys.stdin.fileno()
        old_tty = termios.tcgetattr(fd)
        new = termios.tcgetattr(fd)
        new[3] &= ~(termios.ECHO | termios.ICANON)
        new[6][termios.VMIN] = 0
        new[6][termios.VTIME] = 0
        termios.tcsetattr(fd, termios.TCSADRAIN, new)
    except Exception:
        old_tty = None
        fd = None

    out.write("\x1b[?1049h\x1b[?25l\x1b[?7l\x1b[2J")   # alt screen, hide cursor, no autowrap
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
            if fd is not None and key_pressed(fd):
                break
            t = frame_start - t0
            buf = scene.render(t)
            status = " donut.py  %dx%d  %4.1f fps  q / Ctrl+C to quit" % (scene.w, scene.h + 1, fps_est)
            out.write(buf + "\x1b[38;5;244m" + status[: scene.w - 1] + "\x1b[K")
            out.flush()
            now = time.perf_counter()
            dt = now - last
            last = now
            if dt > 0:
                fps_est = fps_est * 0.9 + (1.0 / dt) * 0.1
            spare = FRAME - (time.perf_counter() - frame_start)
            if spare > 0:
                time.sleep(spare)
    except KeyboardInterrupt:
        pass
    finally:
        out.write("\x1b[0m\x1b[?7h\x1b[?25h\x1b[?1049l")
        out.flush()
        if old_tty is not None:
            try:
                import termios
                termios.tcsetattr(fd, termios.TCSADRAIN, old_tty)
            except Exception:
                pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
