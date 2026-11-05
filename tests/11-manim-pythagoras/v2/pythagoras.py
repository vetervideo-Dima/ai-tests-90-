"""
Pythagorean theorem — visual proof in Manim Community Edition (v2).

Part 1: right triangle, squares on each side, and an area-preserving morph
        (Euclid's altitude split): a^2 and b^2 reshape into the two
        rectangles that tile c^2  ->  a^2 + b^2 = c^2.
Part 2: rearrangement proof — four congruent triangles *slide* (pure
        translations) inside the (a+b)x(a+b) square.

Render (medium quality, ~40 s):
    manim -pqm pythagoras.py PythagoreanTheorem
High quality:
    manim -pqh pythagoras.py PythagoreanTheorem
"""
from manim import *
import numpy as np

# 3Blue1Brown-like palette
BG = "#0b0f19"
A_COLOR = "#58C4DD"   # BLUE_C
B_COLOR = "#F4D345"   # YELLOW
C_COLOR = "#5CD0B3"   # TEAL
TRI_FILL = "#3b4252"
TRI_STROKE = "#d8dee9"


def outward_square(p, q, color, opacity=0.45):
    """Square on segment p->q, built on the right-hand side of p->q."""
    d = q - p
    n = np.array([d[1], -d[0], 0.0])
    return Polygon(p, q, q + n, p + n, color=color, stroke_width=3,
                   fill_color=color, fill_opacity=opacity), n


class PythagoreanTheorem(Scene):
    def construct(self):
        self.camera.background_color = BG

        # ------------------------------------------------------------ title
        title = Text("The Pythagorean Theorem", font_size=50, weight=BOLD)
        self.play(Write(title), run_time=1.3)
        self.play(title.animate.scale(0.6).to_corner(UL, buff=0.35),
                  run_time=0.8)

        # ------------------------------------------------------- triangle
        u = 0.6
        a, b = 3, 4
        c = 5
        shift = np.array([-3.4, -0.75, 0.0])
        A = np.array([0.0, 0.0, 0.0]) + shift          # right angle
        B = np.array([b * u, 0.0, 0.0]) + shift
        C = np.array([0.0, a * u, 0.0]) + shift

        tri = Polygon(A, B, C, color=TRI_STROKE, stroke_width=4,
                      fill_color=TRI_FILL, fill_opacity=0.9)
        right_angle = RightAngle(Line(A, B), Line(A, C), length=0.22,
                                 color=TRI_STROKE, stroke_width=3)
        centroid = (A + B + C) / 3

        def side_label(tex, p, q, color):
            mid = (p + q) / 2
            inward = centroid - mid
            inward /= np.linalg.norm(inward)
            return MathTex(tex, color=color, font_size=36).move_to(mid + 0.28 * inward)

        lab_a = side_label("a", C, A, A_COLOR)
        lab_b = side_label("b", A, B, B_COLOR)
        lab_c = side_label("c", B, C, C_COLOR)

        self.play(DrawBorderThenFill(tri), run_time=1.2)
        self.play(Create(right_angle),
                  LaggedStart(*[FadeIn(l, scale=0.6) for l in (lab_a, lab_b, lab_c)],
                              lag_ratio=0.25), run_time=1.0)

        # ---------------------------------------------------------- squares
        sq_a, n_a = outward_square(C, A, A_COLOR)
        sq_b, n_b = outward_square(A, B, B_COLOR)
        sq_c, n_c = outward_square(B, C, C_COLOR, opacity=0.18)

        t_a2 = MathTex("a^2", font_size=40).move_to(sq_a)
        t_b2 = MathTex("b^2", font_size=44).move_to(sq_b)
        t_c2 = MathTex("c^2", font_size=52).move_to(sq_c)

        for sq, t in ((sq_a, t_a2), (sq_b, t_b2), (sq_c, t_c2)):
            self.play(DrawBorderThenFill(sq), Write(t), run_time=0.9)
        self.wait(0.3)

        # ------------------------------------------ morph: a^2 + b^2 -> c^2
        # Foot of the altitude from the right angle onto the hypotenuse.
        BC = C - B
        H = B + np.dot(A - B, BC) / np.dot(BC, BC) * BC
        altitude = DashedLine(A, H + n_c, color=WHITE, stroke_width=2,
                              dash_length=0.08).set_opacity(0.7)
        self.play(Create(altitude), run_time=0.8)

        # Rectangles inside c^2 with areas a^2 (at C) and b^2 (at B)
        rect_a = Polygon(C, H, H + n_c, C + n_c, color=A_COLOR, stroke_width=3,
                         fill_color=A_COLOR, fill_opacity=0.6)
        rect_b = Polygon(H, B, B + n_c, H + n_c, color=B_COLOR, stroke_width=3,
                         fill_color=B_COLOR, fill_opacity=0.6)

        morph_a = sq_a.copy()
        morph_b = sq_b.copy()
        lab_ma = t_a2.copy()
        lab_mb = t_b2.copy()
        self.play(FadeOut(t_c2), run_time=0.4)
        self.add(morph_a, lab_ma)
        self.play(Transform(morph_a, rect_a), lab_ma.animate.move_to(rect_a),
                  run_time=1.8, rate_func=smooth)
        self.add(morph_b, lab_mb)
        self.play(Transform(morph_b, rect_b), lab_mb.animate.move_to(rect_b),
                  run_time=1.8, rate_func=smooth)
        self.wait(0.4)

        equation = MathTex("a^2", "+", "b^2", "=", "c^2", font_size=72)
        equation[0].set_color(A_COLOR)
        equation[2].set_color(B_COLOR)
        equation[4].set_color(C_COLOR)
        equation.move_to(np.array([3.9, 0.3, 0]))
        note = Text("same area", font_size=26, color=GREY_B).next_to(equation, DOWN, buff=0.35)

        self.play(
            TransformFromCopy(lab_ma, equation[0]),
            TransformFromCopy(lab_mb, equation[2]),
            FadeIn(equation[1], shift=0.2 * UP),
            FadeIn(equation[3], shift=0.2 * UP),
            TransformFromCopy(VGroup(morph_a, morph_b), equation[4]),
            run_time=1.8,
        )
        self.play(FadeIn(note, shift=0.15 * UP),
                  Circumscribe(equation, color=C_COLOR, fade_out=True), run_time=1.2)
        self.wait(0.6)

        part1 = VGroup(tri, right_angle, lab_a, lab_b, lab_c, sq_a, sq_b, sq_c,
                       t_a2, t_b2, altitude, morph_a, morph_b, lab_ma, lab_mb, note)
        subtitle = Text("Proof by rearrangement", font_size=28, color=GREY_A)
        subtitle.next_to(title, DOWN, aligned_edge=LEFT, buff=0.15)
        self.play(FadeOut(part1, shift=0.5 * LEFT),
                  equation.animate.scale(0.6).to_corner(UR, buff=0.45),
                  FadeIn(subtitle, shift=0.15 * DOWN),
                  run_time=1.2)

        # ------------------------------------------------ rearrangement proof
        s = 0.72
        A_, B_ = a * s, b * s
        L = A_ + B_
        origin = np.array([-L / 2 - 2.4, -L / 2 - 0.35, 0.0])

        def P(x, y):
            return origin + np.array([x, y, 0.0])

        big_sq = Polygon(P(0, 0), P(L, 0), P(L, L), P(0, L),
                         color=WHITE, stroke_width=4)

        def brace_label(p, q, tex, color, direction):
            br = BraceBetweenPoints(p, q, direction=direction, buff=0.08,
                                    color=GREY_B)
            lb = MathTex(tex, color=color, font_size=32).next_to(br, direction, buff=0.08)
            return VGroup(br, lb)

        braces = VGroup(
            brace_label(P(0, 0), P(A_, 0), "a", A_COLOR, DOWN),
            brace_label(P(A_, 0), P(L, 0), "b", B_COLOR, DOWN),
            brace_label(P(0, 0), P(0, B_), "b", B_COLOR, LEFT),
            brace_label(P(0, B_), P(0, L), "a", A_COLOR, LEFT),
        )
        self.play(Create(big_sq), FadeIn(braces, lag_ratio=0.2), run_time=1.2)

        def tri_poly(*pts):
            return Polygon(*pts, color=TRI_STROKE, stroke_width=2.5,
                           fill_color=TRI_FILL, fill_opacity=1.0)

        # Configuration 1: the four triangles leave a tilted c^2 square
        t1 = tri_poly(P(0, 0), P(A_, 0), P(0, B_))
        t2 = tri_poly(P(L, 0), P(L, A_), P(A_, 0))
        t3 = tri_poly(P(L, L), P(B_, L), P(L, A_))
        t4 = tri_poly(P(0, L), P(0, B_), P(B_, L))
        tris = VGroup(t1, t2, t3, t4)

        inner_c = Polygon(P(A_, 0), P(L, A_), P(B_, L), P(0, B_),
                          stroke_width=0, fill_color=C_COLOR, fill_opacity=0.55)
        lbl_c2 = MathTex("c^2", font_size=56).move_to(inner_c)

        self.add(inner_c)  # behind the triangles
        self.play(LaggedStart(*[FadeIn(t, shift=0.3 * (t.get_center() - big_sq.get_center()))
                                for t in tris], lag_ratio=0.2),
                  FadeIn(inner_c), run_time=1.6)
        self.play(Write(lbl_c2), run_time=0.7)

        eq_right = np.array([3.0, 1.6, 0])
        area1 = MathTex(r"(a+b)^2", "=", r"4\cdot\tfrac12 ab", "+", "c^2", font_size=44)
        area1[4].set_color(C_COLOR)
        area1.move_to(eq_right)
        self.play(Write(area1), run_time=1.4)
        self.wait(1.0)

        # Configuration 2: slide the triangles (pure translations)
        self.play(FadeOut(inner_c), FadeOut(lbl_c2), run_time=0.5)
        self.play(t1.animate.shift(P(0, A_) - P(0, 0)), run_time=1.3)
        self.play(t3.animate.shift(P(A_, L) - P(L, L)), run_time=1.3)
        self.play(t4.animate.shift(P(A_, A_) - P(0, L)), run_time=1.5)

        sq_a2 = Polygon(P(0, 0), P(A_, 0), P(A_, A_), P(0, A_),
                        stroke_width=0, fill_color=A_COLOR, fill_opacity=0.6)
        sq_b2 = Polygon(P(A_, A_), P(L, A_), P(L, L), P(A_, L),
                        stroke_width=0, fill_color=B_COLOR, fill_opacity=0.6)
        lbl_a2 = MathTex("a^2", font_size=44).move_to(sq_a2)
        lbl_b2 = MathTex("b^2", font_size=56).move_to(sq_b2)
        self.bring_to_back(sq_a2, sq_b2)
        self.play(FadeIn(sq_a2), FadeIn(sq_b2), Write(lbl_a2), Write(lbl_b2),
                  run_time=1.0)

        area2 = MathTex(r"(a+b)^2", "=", r"4\cdot\tfrac12 ab", "+", "a^2", "+", "b^2",
                        font_size=44)
        area2[4].set_color(A_COLOR)
        area2[6].set_color(B_COLOR)
        area2.next_to(area1, DOWN, buff=0.5, aligned_edge=LEFT)
        self.play(Write(area2), run_time=1.2)

        # Same big square, same four triangles -> what is left must be equal
        common = VGroup(
            SurroundingRectangle(area1[0:3], color=GREY_B, buff=0.08, stroke_width=2),
            SurroundingRectangle(area2[0:3], color=GREY_B, buff=0.08, stroke_width=2),
        )
        self.play(Create(common), run_time=0.8)
        concl = MathTex(r"\Rightarrow\;", "c^2", "=", "a^2", "+", "b^2", font_size=52)
        concl[1].set_color(C_COLOR)
        concl[3].set_color(A_COLOR)
        concl[5].set_color(B_COLOR)
        concl.next_to(area2, DOWN, buff=0.7)
        self.play(TransformFromCopy(area1[4], concl[1]),
                  TransformFromCopy(VGroup(area2[4], area2[5], area2[6]), concl[3:6]),
                  FadeIn(concl[0]), FadeIn(concl[2]), run_time=1.5)
        self.wait(1.0)

        final_eq = MathTex("a^2", "+", "b^2", "=", "c^2", font_size=96)
        final_eq[0].set_color(A_COLOR)
        final_eq[2].set_color(B_COLOR)
        final_eq[4].set_color(C_COLOR)
        final_eq.move_to(UP * 0.2)

        rest = VGroup(big_sq, braces, tris, sq_a2, sq_b2, lbl_a2, lbl_b2,
                      area1, area2, common, concl, subtitle)
        self.play(FadeOut(rest, shift=0.3 * DOWN),
                  ReplacementTransform(equation, final_eq),
                  run_time=1.5)
        box = SurroundingRectangle(final_eq, color=C_COLOR, buff=0.35,
                                   corner_radius=0.18, stroke_width=4)
        qed = Text("Q.E.D.", font_size=30, color=GREY_B).next_to(box, DOWN, buff=0.4)
        self.play(Create(box), FadeIn(qed, shift=0.2 * UP), run_time=1.1)
        self.wait(2.0)
