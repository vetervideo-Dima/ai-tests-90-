"""
Pythagorean theorem — visual proof in Manim Community Edition.

Render (medium quality, ~40 s):
    manim -pqm pythagoras.py PythagoreanTheorem

High quality:
    manim -pqh pythagoras.py PythagoreanTheorem
"""
from manim import *
import numpy as np

# 3Blue1Brown-like palette
BG = "#0e1117"
A_COLOR = BLUE_C      # side a
B_COLOR = YELLOW_C    # side b
C_COLOR = TEAL_C      # hypotenuse c
TRI_COLOR = GREY_B


class PythagoreanTheorem(Scene):
    def construct(self):
        self.camera.background_color = BG

        # ---------------------------------------------------------------
        # Part 1: title
        # ---------------------------------------------------------------
        title = Text("The Pythagorean Theorem", font_size=44, weight=BOLD)
        title.to_edge(UP)
        self.play(Write(title), run_time=1.5)
        self.wait(0.5)

        # ---------------------------------------------------------------
        # Part 2: right triangle with labelled sides
        # ---------------------------------------------------------------
        unit = 0.55
        a, b = 3, 4  # legs
        A = np.array([0, 0, 0])
        B = np.array([b * unit, 0, 0])
        C = np.array([0, a * unit, 0])
        tri = Polygon(A, B, C, color=WHITE, stroke_width=4,
                      fill_color=TRI_COLOR, fill_opacity=0.35)
        tri_group = VGroup(tri)
        shift = np.array([-0.9, -0.6, 0])
        tri.shift(shift)
        A, B, C = A + shift, B + shift, C + shift

        right_angle = RightAngle(Line(A, B), Line(A, C), length=0.25,
                                 color=WHITE, stroke_width=3)

        lab_a = MathTex("a", color=A_COLOR).next_to(Line(A, C), LEFT, buff=0.15)
        lab_b = MathTex("b", color=B_COLOR).next_to(Line(A, B), DOWN, buff=0.15)
        hyp_mid = (B + C) / 2
        hyp_normal = np.array([a, b, 0]) / np.linalg.norm([a, b])
        lab_c = MathTex("c", color=C_COLOR).move_to(hyp_mid + 0.3 * hyp_normal)

        self.play(Create(tri), run_time=1.5)
        self.play(Create(right_angle),
                  FadeIn(lab_a, shift=0.2 * RIGHT),
                  FadeIn(lab_b, shift=0.2 * UP),
                  FadeIn(lab_c, shift=0.2 * DL), run_time=1)
        self.wait(0.5)

        # ---------------------------------------------------------------
        # Part 3: squares on each side
        # ---------------------------------------------------------------
        def square_on(p, q, color):
            """Square built outward on segment p->q (outside = right side of p->q)."""
            d = q - p
            n = np.array([d[1], -d[0], 0])  # rotate -90 deg
            return Polygon(p, q, q + n, p + n, color=color, stroke_width=3,
                           fill_color=color, fill_opacity=0.45)

        # vertices are ordered so the squares are drawn outward
        sq_a = square_on(C, A, A_COLOR)   # on leg a (left)
        sq_b = square_on(A, B, B_COLOR)   # on leg b (bottom)
        sq_c = square_on(B, C, C_COLOR)   # on hypotenuse

        txt_a2 = MathTex("a^2", color=WHITE).move_to(sq_a.get_center())
        txt_b2 = MathTex("b^2", color=WHITE).move_to(sq_b.get_center())
        txt_c2 = MathTex("c^2", color=WHITE).move_to(sq_c.get_center())

        self.play(DrawBorderThenFill(sq_a), Write(txt_a2), run_time=1.3)
        self.play(DrawBorderThenFill(sq_b), Write(txt_b2), run_time=1.3)
        self.play(DrawBorderThenFill(sq_c), Write(txt_c2), run_time=1.3)
        self.wait(0.7)

        # ---------------------------------------------------------------
        # Part 4: morph labels into the equation
        # ---------------------------------------------------------------
        equation = MathTex("a^2", "+", "b^2", "=", "c^2", font_size=60)
        equation[0].set_color(A_COLOR)
        equation[2].set_color(B_COLOR)
        equation[4].set_color(C_COLOR)
        equation.to_edge(DOWN, buff=0.5)

        self.play(
            TransformFromCopy(txt_a2, equation[0]),
            TransformFromCopy(txt_b2, equation[2]),
            TransformFromCopy(txt_c2, equation[4]),
            FadeIn(equation[1]), FadeIn(equation[3]),
            run_time=2,
        )
        self.play(Indicate(equation, color=WHITE, scale_factor=1.1))
        self.wait(1)

        # Morph the two small squares "into" the big one (area intuition)
        ghost_a = sq_a.copy()
        ghost_b = sq_b.copy()
        self.play(
            ghost_a.animate.move_to(sq_c.get_center()).rotate(
                np.arctan2(a, b)).set_opacity(0.3),
            ghost_b.animate.move_to(sq_c.get_center()).rotate(
                np.arctan2(a, b)).set_opacity(0.3),
            run_time=1.5,
        )
        self.play(
            Transform(VGroup(ghost_a, ghost_b), sq_c.copy().set_fill(opacity=0.0)),
            sq_c.animate.set_fill(opacity=0.8),
            run_time=1.5,
        )
        self.play(FadeOut(ghost_a), FadeOut(ghost_b), sq_c.animate.set_fill(opacity=0.45))
        self.wait(0.5)

        # Clear for part 2
        part1 = VGroup(tri, right_angle, lab_a, lab_b, lab_c,
                       sq_a, sq_b, sq_c, txt_a2, txt_b2, txt_c2)
        self.play(
            FadeOut(part1, shift=LEFT),
            equation.animate.scale(0.8).to_corner(UR).shift(DOWN * 0.9),
            run_time=1.2,
        )

        subtitle = Text("Rearrangement proof", font_size=32, color=GREY_A)
        subtitle.next_to(title, DOWN, buff=0.15)
        self.play(FadeIn(subtitle, shift=DOWN * 0.2))

        # ---------------------------------------------------------------
        # Part 5: rearrangement proof
        # Big square of side (a+b); four copies of the triangle inside.
        # ---------------------------------------------------------------
        s = 0.5                      # scale for proof
        A_ = a * s
        B_ = b * s
        L = A_ + B_                  # side of big square
        origin = np.array([-L / 2 - 1.2, -L / 2 - 0.4, 0])

        def P(x, y):
            return origin + np.array([x, y, 0])

        big_sq = Polygon(P(0, 0), P(L, 0), P(L, L), P(0, L),
                         color=WHITE, stroke_width=4)
        lbl_side = VGroup(
            MathTex("a", color=A_COLOR, font_size=32).next_to(Line(P(0, 0), P(A_, 0)), DOWN, buff=0.1),
            MathTex("b", color=B_COLOR, font_size=32).next_to(Line(P(A_, 0), P(L, 0)), DOWN, buff=0.1),
        )
        self.play(Create(big_sq), FadeIn(lbl_side), run_time=1.2)

        tri_style = dict(color=WHITE, stroke_width=2,
                         fill_color=GREY_D, fill_opacity=0.9)

        # Configuration 1: tilted square c^2 in the middle
        # Corners of inner square on each edge: (A_,0), (L,A_), (B_,L), (0,B_)
        conf1 = [
            Polygon(P(0, 0), P(A_, 0), P(0, B_), **tri_style),
            Polygon(P(L, 0), P(L, A_), P(A_, 0), **tri_style),
            Polygon(P(L, L), P(B_, L), P(L, A_), **tri_style),
            Polygon(P(0, L), P(0, B_), P(B_, L), **tri_style),
        ]
        tris = VGroup(*conf1)
        self.play(LaggedStart(*[FadeIn(t, scale=0.8) for t in tris],
                              lag_ratio=0.25), run_time=2)

        inner_c = Polygon(P(A_, 0), P(L, A_), P(B_, L), P(0, B_),
                          stroke_width=0, fill_color=C_COLOR, fill_opacity=0.6)
        lbl_c2 = MathTex("c^2", font_size=48).move_to(inner_c.get_center())
        self.play(FadeIn(inner_c), Write(lbl_c2), run_time=1.2)
        self.wait(1)

        # Configuration 2: triangles slide to form two rectangles,
        # leaving squares a^2 (bottom-left) and b^2 (top-right).
        conf2 = [
            # rectangle at bottom-right: [A_, L] x [0, A_]  -> two triangles
            Polygon(P(A_, 0), P(L, 0), P(A_, A_), **tri_style),
            Polygon(P(L, A_), P(A_, A_), P(L, 0), **tri_style),
            # rectangle at top-left: [0, A_] x [A_, L]
            Polygon(P(0, A_), P(A_, A_), P(0, L), **tri_style),
            Polygon(P(A_, L), P(0, L), P(A_, A_), **tri_style),
        ]

        self.play(FadeOut(inner_c), FadeOut(lbl_c2), run_time=0.6)
        self.play(
            *[Transform(t, target) for t, target in zip(tris, conf2)],
            run_time=3, rate_func=smooth,
        )

        sq_a2 = Polygon(P(0, 0), P(A_, 0), P(A_, A_), P(0, A_),
                        stroke_width=0, fill_color=A_COLOR, fill_opacity=0.6)
        sq_b2 = Polygon(P(A_, A_), P(L, A_), P(L, L), P(A_, L),
                        stroke_width=0, fill_color=B_COLOR, fill_opacity=0.6)
        lbl_a2 = MathTex("a^2", font_size=40).move_to(sq_a2.get_center())
        lbl_b2 = MathTex("b^2", font_size=48).move_to(sq_b2.get_center())
        self.play(FadeIn(sq_a2), FadeIn(sq_b2), Write(lbl_a2), Write(lbl_b2),
                  run_time=1.2)
        self.wait(1)

        # Conclusion: same big square minus same four triangles
        reasoning = VGroup(
            MathTex(r"(a+b)^2 - 4\cdot\tfrac{1}{2}ab", font_size=36),
            MathTex(r"= c^2", font_size=36, color=C_COLOR),
            MathTex(r"= a^2 + b^2", font_size=36),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        reasoning[2][0][1:3].set_color(A_COLOR)
        reasoning[2][0][4:6].set_color(B_COLOR)
        reasoning.next_to(big_sq, RIGHT, buff=0.9).shift(DOWN * 0.3)
        for line in reasoning:
            self.play(Write(line), run_time=1.0)
        self.wait(0.8)

        # Final: bring the theorem to center
        final_eq = MathTex("a^2", "+", "b^2", "=", "c^2", font_size=80)
        final_eq[0].set_color(A_COLOR)
        final_eq[2].set_color(B_COLOR)
        final_eq[4].set_color(C_COLOR)
        everything = VGroup(big_sq, lbl_side, tris, sq_a2, sq_b2,
                            lbl_a2, lbl_b2, reasoning, subtitle)
        self.play(FadeOut(everything), ReplacementTransform(equation, final_eq),
                  run_time=1.5)
        box = SurroundingRectangle(final_eq, color=C_COLOR, buff=0.3,
                                   corner_radius=0.15)
        self.play(Create(box), run_time=1)
        self.wait(2)
