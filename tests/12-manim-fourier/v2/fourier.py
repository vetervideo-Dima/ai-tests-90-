"""
fourier.py - A three-scene Manim Community Edition explainer of the Fourier transform
(in the spirit of 3Blue1Brown's "winding machine").

Scenes
  1. SignalFromSines  - a signal built by adding three pure sine waves
  2. WindingMachine   - the signal wound around a circle at varying winding
                        frequencies, with a moving center-of-mass dot
  3. SpectrumSpikes   - sweeping the winding frequency and plotting how far the
                        center of mass is from the origin: spikes appear at the
                        three hidden frequencies

Requirements
  pip install manim          # Manim Community v0.18+  (LaTeX needed for MathTex)

Render commands
  # quick low-quality previews (480p15), opens the video when done
  manim -pql fourier.py SignalFromSines
  manim -pql fourier.py WindingMachine
  manim -pql fourier.py SpectrumSpikes

  # high quality (1080p60), all three scenes in one go
  manim -qh -a fourier.py

  # optional: stitch the three high-quality renders into one video
  #   (paths shown are Manim's default output folders)
  printf "file '%s'\n" media/videos/fourier/1080p60/SignalFromSines.mp4 \
      media/videos/fourier/1080p60/WindingMachine.mp4 \
      media/videos/fourier/1080p60/SpectrumSpikes.mp4 > list.txt
  ffmpeg -f concat -safe 0 -i list.txt -c copy fourier_full.mp4
"""

from functools import lru_cache

from manim import *
import numpy as np

# --------------------------------------------------------------------------
# Look & feel
# --------------------------------------------------------------------------
config.background_color = "#0b1020"
FONT = "Inter"                   # Pango falls back to a default sans if missing
Text.set_default(font=FONT)
GRID_COLOR = "#2a3352"

# --------------------------------------------------------------------------
# Shared signal definition
# --------------------------------------------------------------------------
FREQS = [1.0, 2.0, 3.0]          # cycles per second (Hz)
AMPS = [1.0, 0.5, 0.75]          # amplitudes
COLORS = [BLUE, GREEN, ORANGE]
SIGNAL_COLOR = YELLOW
COM_COLOR = RED

T_MAX = 4.0                      # length of the time window (seconds)
F_MAX = 4.0                      # largest winding frequency we sweep to


def component(t, i):
    return AMPS[i] * np.sin(2 * PI * FREQS[i] * t)


def signal(t):
    return sum(component(t, i) for i in range(len(FREQS)))


# dense samples used for the winding curve and the center of mass
T_SAMPLES = np.linspace(0, T_MAX, 2400)
G_SAMPLES = signal(T_SAMPLES)
G_MAX = float(np.abs(G_SAMPLES).max())


@lru_cache(maxsize=4096)
def _com_cached(f_key):
    f = f_key / 1e5
    return complex(np.mean(G_SAMPLES * np.exp(-2j * PI * f * T_SAMPLES)))


def center_of_mass(f):
    """(1/T) * integral_0^T g(t) e^{-2 pi i f t} dt, approximated by a mean."""
    return _com_cached(int(round(f * 1e5)))


def com_point(f, center, scale):
    c = center_of_mass(f)
    return center + scale * np.array([c.real, c.imag, 0.0])


def glow_curve(points, color, width=2.5, glow=True):
    """A polyline with a soft additive-looking glow (stacked translucent strokes)."""
    group = VGroup()
    if glow:
        for w, op in ((width * 5, 0.06), (width * 2.6, 0.14)):
            group.add(VMobject(stroke_color=color, stroke_width=w, stroke_opacity=op)
                      .set_points_as_corners(points))
    group.add(VMobject(stroke_color=color, stroke_width=width).set_points_as_corners(points))
    return group


def glow_dot(point, color, radius=0.1):
    return VGroup(
        Dot(point, radius=radius * 3.2, color=color, fill_opacity=0.10),
        Dot(point, radius=radius * 1.9, color=color, fill_opacity=0.22),
        Dot(point, radius=radius, color=color),
        Dot(point, radius=radius * 0.4, color=WHITE, fill_opacity=0.85),
    ).set_z_index(5)


# precomputed spectrum |center of mass| on a frequency grid
F_GRID = np.linspace(0, F_MAX, 801)
SPECTRUM = np.array([abs(center_of_mass(f)) for f in F_GRID])


def wound_points(f, t_end, center, radius_scale, n_total=1600):
    """Points of the signal wound around `center` at winding frequency f."""
    t_end = max(t_end, 1e-3)
    n = max(2, int(n_total * t_end / T_MAX))
    ts = np.linspace(0, t_end, n)
    g = signal(ts)
    ang = -2 * PI * f * ts                       # clockwise winding
    pts = np.column_stack([g * np.cos(ang), g * np.sin(ang), np.zeros_like(ts)])
    return pts * radius_scale + center


def show_caption(scene, text, old=None, font_size=28):
    """Replace the bottom caption with a new one."""
    label = Text(text, font_size=font_size, color="#e8ecf8")
    if label.width > config.frame_width - 1.2:
        label.scale_to_fit_width(config.frame_width - 1.2)
    box = RoundedRectangle(corner_radius=0.18, width=label.width + 0.6,
                           height=label.height + 0.36, stroke_width=1,
                           stroke_color="#3a4670", fill_color="#141b33", fill_opacity=0.9)
    new = VGroup(box, label).to_edge(DOWN, buff=0.22)
    label.move_to(box)
    if old is None:
        scene.play(FadeIn(new, shift=0.2 * UP), run_time=0.8)
    else:
        scene.play(FadeOut(old, shift=0.2 * UP), FadeIn(new, shift=0.2 * UP), run_time=0.8)
    return new


def make_polar_backdrop(center, radius):
    disc = Circle(radius=radius, stroke_width=0, fill_color="#121a33",
                  fill_opacity=0.8).move_to(center)
    rings = VGroup(*[Circle(radius=radius * k, color=GRID_COLOR, stroke_width=1).move_to(center)
                     for k in (0.25, 0.5, 0.75)])
    ring = Circle(radius=radius, color="#5a6690", stroke_width=2).move_to(center)
    h = Line(center + LEFT * (radius + 0.3), center + RIGHT * (radius + 0.3),
             color="#5a6690", stroke_width=1.5)
    v = Line(center + DOWN * (radius + 0.3), center + UP * (radius + 0.3),
             color="#5a6690", stroke_width=1.5)
    origin = Dot(center, radius=0.04, color=WHITE)
    return VGroup(disc, rings, ring, h, v, origin)


# --------------------------------------------------------------------------
# Scene 1 - building the signal
# --------------------------------------------------------------------------
class SignalFromSines(Scene):
    def construct(self):
        title = Text("1 · A signal built from three sines", font_size=36, weight=SEMIBOLD).to_edge(UP)
        self.play(Write(title))
        cap = show_caption(self, "Start with three pure tones, each with its own frequency.")

        axis_cfg = {"include_ticks": False, "stroke_width": 2}
        comp_axes = VGroup(*[
            Axes(x_range=[0, T_MAX, 1], y_range=[-1.2, 1.2, 1], x_length=5.2,
                 y_length=1.2, tips=False, axis_config=axis_cfg)
            for _ in range(3)
        ])
        comp_axes.arrange(DOWN, buff=0.65).to_edge(LEFT, buff=0.6).shift(0.25 * DOWN)

        comp_graphs = VGroup()
        comp_labels = VGroup()
        for i, ax in enumerate(comp_axes):
            graph = ax.plot(lambda t, i=i: component(t, i), x_range=[0, T_MAX, 0.005],
                            color=COLORS[i], stroke_width=3)
            label = MathTex(rf"{AMPS[i]:g}\,\sin(2\pi\cdot {FREQS[i]:g}\,t)",
                            font_size=28, color=COLORS[i])
            label.next_to(ax, UP, buff=0.08).align_to(ax, LEFT)
            comp_graphs.add(graph)
            comp_labels.add(label)

        for ax, graph, label in zip(comp_axes, comp_graphs, comp_labels):
            self.play(Create(ax), Write(label), run_time=0.7)
            self.play(Create(graph), run_time=1.4, rate_func=linear)

        cap = show_caption(self, "Add them together, point by point.", cap)

        sum_ax = Axes(x_range=[0, T_MAX, 1], y_range=[-2.4, 2.4, 1], x_length=6.2,
                      y_length=3.6, tips=False, axis_config=axis_cfg)
        sum_ax.move_to(RIGHT * 3.3 + DOWN * 0.25)
        t_label = sum_ax.get_x_axis_label(MathTex("t", font_size=30))
        self.play(Create(sum_ax), FadeIn(t_label))

        # copies of the components slide onto the big axes
        moved = VGroup(*[
            sum_ax.plot(lambda t, i=i: component(t, i), x_range=[0, T_MAX, 0.005],
                        color=COLORS[i], stroke_width=2, stroke_opacity=0.8)
            for i in range(3)
        ])
        self.play(*[TransformFromCopy(comp_graphs[i], moved[i]) for i in range(3)],
                  run_time=1.6)
        self.wait(0.4)

        sum_graph = sum_ax.plot(signal, x_range=[0, T_MAX, 0.004],
                                color=SIGNAL_COLOR, stroke_width=4)
        sum_label = MathTex(r"g(t) = \sum_{k=1}^{3} A_k \sin(2\pi f_k t)",
                            font_size=32, color=SIGNAL_COLOR)
        sum_label.next_to(sum_ax, UP, buff=0.15)
        sum_glow = VGroup(*[sum_ax.plot(signal, x_range=[0, T_MAX, 0.004], color=SIGNAL_COLOR,
                                        stroke_width=w, stroke_opacity=op)
                            for w, op in ((18, 0.05), (9, 0.12))])
        self.play(ReplacementTransform(moved, sum_graph), Write(sum_label), run_time=2)
        self.play(FadeIn(sum_glow), run_time=0.6)
        self.wait(0.5)

        # a sweeping probe shows the sum really is pointwise
        probe_t = ValueTracker(0.05)
        probe_line = always_redraw(lambda: DashedLine(
            sum_ax.c2p(probe_t.get_value(), -2.4), sum_ax.c2p(probe_t.get_value(), 2.4),
            color=GREY_B, stroke_width=1.5))
        probe_dot = always_redraw(lambda: glow_dot(
            sum_ax.c2p(probe_t.get_value(), signal(probe_t.get_value())),
            SIGNAL_COLOR, radius=0.07))
        comp_dots = VGroup(*[
            always_redraw(lambda i=i: Dot(
                comp_axes[i].c2p(probe_t.get_value(), component(probe_t.get_value(), i)),
                color=COLORS[i], radius=0.06))
            for i in range(3)
        ])
        self.play(FadeIn(probe_line), FadeIn(probe_dot), FadeIn(comp_dots))
        self.play(probe_t.animate.set_value(T_MAX - 0.05), run_time=4, rate_func=linear)
        self.play(FadeOut(probe_line), FadeOut(probe_dot), FadeOut(comp_dots))

        cap = show_caption(self, "The sum looks messy, yet the three frequencies are hidden inside.", cap)
        self.wait(1.5)
        cap = show_caption(self, "How can we pull them back out? Wind the signal around a circle.", cap)
        self.wait(1.5)
        self.play(*[FadeOut(m) for m in self.mobjects])


# --------------------------------------------------------------------------
# Scene 2 - the winding machine
# --------------------------------------------------------------------------
class WindingMachine(Scene):
    def construct(self):
        title = Text("2 · Winding the signal around a circle", font_size=36, weight=SEMIBOLD).to_edge(UP)
        self.play(Write(title))

        # left: the signal in time
        axis_cfg = {"include_ticks": False, "stroke_width": 2}
        sig_ax = Axes(x_range=[0, T_MAX, 1], y_range=[-2.4, 2.4, 1], x_length=5.4,
                      y_length=2.4, tips=False, axis_config=axis_cfg)
        sig_ax.move_to(LEFT * 3.7 + UP * 1.2)
        sig_graph = sig_ax.plot(signal, x_range=[0, T_MAX, 0.004],
                                color=SIGNAL_COLOR, stroke_width=3)
        sig_label = MathTex("g(t)", font_size=30, color=SIGNAL_COLOR)
        sig_label.next_to(sig_ax, UP, buff=0.1).align_to(sig_ax, LEFT)

        # right: the circle
        center = RIGHT * 3.4 + DOWN * 0.25
        radius = 2.5
        scale = radius / G_MAX
        backdrop = make_polar_backdrop(center, radius)

        f = ValueTracker(0.5)
        t_end = ValueTracker(0.0)

        wound = always_redraw(lambda: glow_curve(
            wound_points(f.get_value(), t_end.get_value(), center, scale), SIGNAL_COLOR, 2.5))

        # readouts
        f_text = Text("winding frequency  f =", font_size=26)
        f_num = DecimalNumber(f.get_value(), num_decimal_places=2, font_size=34, color=TEAL_B)
        f_unit = Text("cycles / s", font_size=26)
        f_row = VGroup(f_text, f_num, f_unit).arrange(RIGHT, buff=0.15)
        f_row.next_to(sig_ax, DOWN, buff=0.6).align_to(sig_ax, LEFT)
        f_num.add_updater(lambda m: m.set_value(f.get_value()))

        self.play(Create(sig_ax), Write(sig_label), Create(sig_graph), FadeIn(backdrop))
        cap = show_caption(self, "Time becomes angle, the signal's value becomes distance from the center.")

        # pens tracing both pictures at once
        pen_sig = always_redraw(lambda: glow_dot(
            sig_ax.c2p(t_end.get_value(), signal(t_end.get_value())), WHITE, radius=0.07))
        pen_circ = always_redraw(lambda: glow_dot(
            wound_points(f.get_value(), t_end.get_value(), center, scale)[-1],
            WHITE, radius=0.07))
        pen_link = always_redraw(lambda: DashedLine(
            center, wound_points(f.get_value(), t_end.get_value(), center, scale)[-1],
            color=GREY_B, stroke_width=1.5, dash_length=0.08))
        self.add(wound)
        self.play(FadeIn(pen_sig), FadeIn(pen_circ), FadeIn(pen_link), FadeIn(f_row))
        self.play(t_end.animate.set_value(T_MAX), run_time=6, rate_func=linear)
        self.play(FadeOut(pen_sig), FadeOut(pen_circ), FadeOut(pen_link))

        cap = show_caption(self, "Now change how fast we wind: the winding frequency f.", cap)
        self.play(f.animate.set_value(0.8), run_time=3)

        # center of mass
        com_dot = always_redraw(lambda: glow_dot(
            com_point(f.get_value(), center, scale), COM_COLOR, radius=0.11))
        com_line = always_redraw(lambda: Line(
            center, com_point(f.get_value(), center, scale), color=COM_COLOR,
            stroke_width=3.5).set_z_index(4))
        com_trail = TracedPath(lambda: com_point(f.get_value(), center, scale),
                               stroke_color=COM_COLOR, stroke_width=3, dissipating_time=1.2,
                               stroke_opacity=[0, 0.8])
        com_text = Text("distance of center of mass =", font_size=26, color=COM_COLOR)
        com_num = DecimalNumber(abs(center_of_mass(f.get_value())), num_decimal_places=3,
                                font_size=34, color=COM_COLOR)
        # a bar that visualises the same distance
        bar_bg = RoundedRectangle(corner_radius=0.06, width=5.4, height=0.16, stroke_width=0,
                                  fill_color=GRID_COLOR, fill_opacity=1)
        bar = always_redraw(lambda: RoundedRectangle(
            corner_radius=0.06, height=0.16, stroke_width=0, fill_color=COM_COLOR, fill_opacity=1,
            width=max(0.02, 5.4 * abs(center_of_mass(f.get_value())) / 0.6))
            .align_to(bar_bg, LEFT).align_to(bar_bg, UP))
        com_row = VGroup(com_text, com_num).arrange(RIGHT, buff=0.15)
        com_row.next_to(f_row, DOWN, buff=0.35).align_to(f_row, LEFT)
        com_num.add_updater(lambda m: m.set_value(abs(center_of_mass(f.get_value()))))
        bar_bg.next_to(com_row, DOWN, buff=0.25).align_to(com_row, LEFT)

        cap = show_caption(self, "Give the wire mass. The red dot is its center of mass.", cap)
        self.add(com_trail)
        self.play(FadeIn(com_dot, scale=0.5), Create(com_line), FadeIn(com_row),
                  FadeIn(bar_bg), FadeIn(bar))
        self.wait(1)

        cap = show_caption(self, "Off-frequency, the loops balance out and the dot hugs the center.", cap)
        self.play(f.animate.set_value(0.92), run_time=2.5)
        cap = show_caption(self, "At f = 1 the loops line up, and the center of mass leaps outward!", cap)
        self.play(f.animate.set_value(1.0), run_time=2, rate_func=smooth)
        self.play(Indicate(com_dot, color=COM_COLOR, scale_factor=1.8))
        self.wait(1)

        cap = show_caption(self, "Keep winding... the dot falls back toward the origin.", cap)
        self.play(f.animate.set_value(1.5), run_time=3)
        cap = show_caption(self, "f = 2: another frequency in the signal, another jump.", cap)
        self.play(f.animate.set_value(2.0), run_time=3)
        self.play(Indicate(com_dot, color=COM_COLOR, scale_factor=1.8))
        self.wait(0.6)
        self.play(f.animate.set_value(2.5), run_time=2.5)
        cap = show_caption(self, "f = 3: the third tone pulls the dot out once more.", cap)
        self.play(f.animate.set_value(3.0), run_time=2.5)
        self.play(Indicate(com_dot, color=COM_COLOR, scale_factor=1.8))
        self.wait(1)

        cap = show_caption(self, "Matching frequencies push the center of mass away from the center.", cap)
        self.wait(2)
        f_num.clear_updaters()
        com_num.clear_updaters()
        self.play(*[FadeOut(m) for m in self.mobjects])


# --------------------------------------------------------------------------
# Scene 3 - the spectrum
# --------------------------------------------------------------------------
class SpectrumSpikes(Scene):
    def construct(self):
        title = Text("3 · The spectrum: spikes at the hidden frequencies", font_size=36, weight=SEMIBOLD).to_edge(UP)
        self.play(Write(title))

        # left: small winding machine
        center = LEFT * 4.4 + DOWN * 0.3
        radius = 2.0
        scale = radius / G_MAX
        backdrop = make_polar_backdrop(center, radius)
        f = ValueTracker(0.0)

        wound = always_redraw(lambda: glow_curve(
            wound_points(f.get_value(), T_MAX, center, scale), SIGNAL_COLOR, 2))
        com_dot = always_redraw(lambda: glow_dot(
            com_point(f.get_value(), center, scale), COM_COLOR, radius=0.1))
        com_line = always_redraw(lambda: Line(
            center, com_point(f.get_value(), center, scale), color=COM_COLOR,
            stroke_width=3).set_z_index(4))

        # right: spectrum axes
        axes = Axes(
            x_range=[0, F_MAX, 1], y_range=[0, 0.6, 0.2], x_length=6.8, y_length=4.2,
            tips=False,
            axis_config={"stroke_width": 2, "color": "#8892b8"},
            x_axis_config={"include_numbers": True, "font_size": 28},
            y_axis_config={"include_numbers": True, "font_size": 24,
                           "decimal_number_config": {"num_decimal_places": 1}},
        )
        axes.move_to(RIGHT * 2.7 + DOWN * 0.3)
        x_lab = axes.get_x_axis_label(MathTex("f", font_size=32))
        y_lab = Text("distance of center of mass", font_size=24, color=COM_COLOR)
        grid = VGroup(*[DashedLine(axes.c2p(0, y), axes.c2p(F_MAX, y), color=GRID_COLOR,
                                   stroke_width=1, dash_length=0.06) for y in (0.2, 0.4, 0.6)])
        y_lab.next_to(axes, UP, buff=0.15).align_to(axes, LEFT)

        def spectrum_curve():
            k = max(2, int(np.searchsorted(F_GRID, f.get_value())) + 1)
            pts = [axes.c2p(F_GRID[j], SPECTRUM[j]) for j in range(k)]
            area = Polygon(axes.c2p(0, 0), *pts, axes.c2p(F_GRID[k - 1], 0),
                           stroke_width=0, fill_color=COM_COLOR, fill_opacity=0.16)
            return VGroup(area, glow_curve(pts, COM_COLOR, 3.5))

        spec = always_redraw(spectrum_curve)
        spec_dot = always_redraw(lambda: glow_dot(
            axes.c2p(f.get_value(), abs(center_of_mass(f.get_value()))), COM_COLOR, radius=0.08))
        spec_cursor = always_redraw(lambda: DashedLine(
            axes.c2p(f.get_value(), 0), axes.c2p(f.get_value(), 0.6),
            color=TEAL_B, stroke_width=1.5, stroke_opacity=0.6, dash_length=0.07))

        f_row = VGroup(Text("winding frequency  f =", font_size=24),
                       DecimalNumber(0, num_decimal_places=2, font_size=32, color=TEAL_B))
        f_row.arrange(RIGHT, buff=0.15).next_to(backdrop, UP, buff=0.15)
        f_row[1].add_updater(lambda m: m.set_value(f.get_value()))

        self.play(FadeIn(backdrop), Create(axes), FadeIn(grid), FadeIn(x_lab), FadeIn(y_lab))
        self.add(wound, com_line, com_dot, f_row)
        cap = show_caption(self, "Sweep the winding frequency and record the center of mass's distance.")
        self.add(spec, spec_cursor, spec_dot)
        self.play(f.animate.set_value(F_MAX), run_time=14, rate_func=linear)
        self.play(FadeOut(spec_cursor), FadeOut(spec_dot), run_time=0.5)

        cap = show_caption(self, "Spikes appear at f = 1, 2 and 3: exactly the tones we started with.", cap)
        markers = VGroup()
        for i, fk in enumerate(FREQS):
            h = abs(center_of_mass(fk))
            top = axes.c2p(fk, h)
            dline = DashedLine(axes.c2p(fk, 0), top, color=COLORS[i], stroke_width=2)
            lab = MathTex(rf"{fk:g}\,\text{{Hz}}", font_size=30, color=COLORS[i])
            lab.next_to(top, UP, buff=0.32)
            self.play(Create(dline), Flash(top, color=COLORS[i], flash_radius=0.3),
                      FadeIn(lab, shift=0.2 * DOWN), run_time=0.9)
            markers.add(dline, lab)
        self.wait(1)

        cap = show_caption(self, "Each spike's height is half that tone's amplitude: its strength.", cap)
        amp_labels = VGroup()
        for i, fk in enumerate(FREQS):
            al = MathTex(rf"A = {AMPS[i]:g}", font_size=26, color=COLORS[i])
            al.next_to(markers[2 * i + 1], UP, buff=0.12)
            amp_labels.add(al)
        self.play(LaggedStart(*[FadeIn(a, shift=0.1 * UP) for a in amp_labels], lag_ratio=0.3))
        self.wait(1.5)

        # the formula replaces the winding machine
        f_row[1].clear_updaters()
        formula = MathTex(
            r"\hat g(f) = \frac{1}{T}\int_0^T g(t)\, e^{-2\pi i f t}\, dt",
            font_size=40)
        formula.move_to(center + RIGHT * 0.55)
        formula_box = SurroundingRectangle(formula, buff=0.3, corner_radius=0.15,
                                           color="#3a4670", fill_color="#141b33",
                                           fill_opacity=0.9, stroke_width=1.5)
        brace_text = Text("winding + center of mass", font_size=24, color=GREY_A)
        brace_text.next_to(formula, DOWN, buff=0.55)
        self.play(FadeOut(VGroup(wound, com_line, com_dot, backdrop, f_row)),
                  FadeIn(formula_box), Write(formula), FadeIn(brace_text, shift=0.2 * UP),
                  run_time=2)
        cap = show_caption(self, "That is the Fourier transform: from time to frequency.", cap)
        self.play(Circumscribe(formula, color=YELLOW))
        self.wait(2.5)
        self.play(*[FadeOut(m) for m in self.mobjects])
