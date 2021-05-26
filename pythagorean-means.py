from manimlib.imports import *
from projects.check_formula_by_txt import *

AB_PROPORTION = 0.25
LINE_LENGTH = 6
COMPASS_RUN_TIME = 3
COMPASS_RATE = linear

class CheckFormula(CheckFormulaByTXT):
    CONFIG = {
        'text': TexMobject(
                    r'=\sqrt{%s - %s}' % (
                        r'\dfrac{a^2 + b^2 + 2ab}{4}',
                        r'\dfrac{a^2 + b^2 - 2ab}{4}'
                    )
                )[0]
    }

class CheckFormula2(CheckFormulaByTXT):
    CONFIG = {
        'text': TexMobject(
            r'=\sqrt{\left(%s\right)^2-\left(%s\right)^2}' % (
                r'\dfrac{a+b}{2}', r'\dfrac{a-b}{2}'
            )
        )[0]
    }


class PythagoreanMeans(Scene):
    def construct(self):
        self.get_lines()
        self.get_arithmetic_mean()
        self.draw_semicircular_arc()
        self.get_quadratic_mean()
        self.get_geometric_mean()
        self.animate_gm_formula()
        # self.get_harmonic_mean()

    def get_lines(self):
        self.a = Line([0.,0.,0.], [LINE_LENGTH/(1.+AB_PROPORTION),0.,0.])
        self.b = Line(
            [LINE_LENGTH/(1.+AB_PROPORTION),0.,0.],
            [LINE_LENGTH,0.,0.]
        )
        self.lines = VGroup(self.a, self.b)
        self.lines.move_to([0.,0.,0.])

        # Add braces and labels
        self.brace_a = Brace(self.a, DOWN, buff = SMALL_BUFF)
        self.brace_b = Brace(self.b, DOWN, buff = SMALL_BUFF)
        self.label_a = self.brace_a.get_tex('a')
        self.label_b = self.brace_b.get_tex('b')
        self.labels = VGroup(
            self.brace_a, self.brace_b,
            self.label_a, self.label_b
        )

        # Animate lines and labels
        self.play(ShowCreation(self.a))
        self.play(GrowFromCenter(self.brace_a), FadeIn(self.label_a))
        self.wait()
        self.play(ShowCreation(self.b), GrowFromCenter(self.brace_b),
            FadeIn(self.label_b)
        )
        self.wait()

    def get_arithmetic_mean(self):

        # Setup line and labels
        self.am_line = Line(
            self.a.get_start(), self.lines.get_center(),
            color = RED_A)
        self.brace_am = Brace(self.am_line, UP, buff = SMALL_BUFF)
        self.brace_am.set_color(RED_A)
        self.label_mean = self.brace_am.get_tex(r'\frac{a+b}{2}')
        self.label_mean.set_color(RED_A)
        self.label_am = self.brace_am.get_text(r'AM')
        self.label_am.set_color(RED_A)
        self.arithmetic_mean = TextMobject(r'AM', r' = arithmetic mean')
        self.arithmetic_mean.set_color(RED_A)
        self.arithmetic_mean.to_edge(LEFT)
        self.arithmetic_mean.shift(1.25*DOWN + SMALL_BUFF*RIGHT)

        # Animate
        self.play(ShowCreation(self.am_line))
        self.play(GrowFromCenter(self.brace_am), Write(self.label_mean))
        self.wait()
        self.play(ReplacementTransform(self.label_mean, self.label_am))
        self.wait()
        self.play(
            ReplacementTransform
            (self.label_am.copy(),
                self.arithmetic_mean[0]
            )
        )
        self.play(Write(self.arithmetic_mean[1]))
        self.wait(2)
        self.play(FadeOut(self.label_am), FadeOut(self.brace_am))

    def draw_semicircular_arc(self):
        tip = Dot(color = YELLOW)
        tip.move_to(self.am_line.get_start())
        self.semicircle = VMobject()
        self.semicircle.set_points_as_corners([tip.get_center(), tip.get_center()])

        def update_path(path):
            previous_path = path.copy()
            previous_path.add_points_as_corners([tip.get_center()])
            path.become(previous_path)

        self.semicircle.add_updater(update_path)

        self.play(FadeIn(tip))
        self.add(self.semicircle)
        self.play(
            Rotating(tip, radians = -TAU/2, about_point = ORIGIN,
                run_time=COMPASS_RUN_TIME, rate_func = COMPASS_RATE),
            Rotating(self.am_line, radians = -TAU/2, about_point = ORIGIN,
                run_time=COMPASS_RUN_TIME, rate_func = COMPASS_RATE)
        )
        self.semicircle.remove_updater(update_path)
        self.play(FadeOut(tip))
        self.play(Rotating(self.am_line, radians = TAU/4,
            about_point = ORIGIN, run_time = 1, rate_func=smooth))
        self.wait()

        self.add(self.semicircle)

    def get_quadratic_mean(self):
        # Setup lines, labels, and braces
        self.qm_line = Line(self.am_line.get_start(),
            self.b.get_start()
            ).set_color(YELLOW)
        diff_line = Line(self.am_line.get_end(),
            self.b.get_start()
            ).set_color(BLUE)
        brace_diff = Brace(diff_line, DOWN,
            buff = 4*SMALL_BUFF).set_color(BLUE)
        label_diff = brace_diff.get_tex(
            r'\dfrac{a+b}{2}', '-b').set_color(BLUE)
        new_label_diff = brace_diff.get_tex(r'\dfrac{a-b}{2}').set_color(BLUE)
        qm_slope = self.qm_line.get_slope()
        brace_qm = Brace(self.qm_line, (UP-RIGHT*qm_slope)/(1.+ qm_slope**2), buff = SMALL_BUFF)
        label_qm = brace_qm.get_text('QM').set_color(YELLOW)
        label_qm.move_to(brace_qm.get_center() + (1+SMALL_BUFF)*RIGHT/2)
        label_copy = label_qm.copy()
        quad_formula = TextMobject('QM',
            r' $=\sqrt{\left(\dfrac{a+b}{2}\right)^2 + \left(\dfrac{a-b}{2}\right)^2}$'
            ).set_color(YELLOW)
        quad_formula.move_to(3*DOWN)
        quad_formula_intermediate = TextMobject('QM',
            r' $=\sqrt{\dfrac{a^2 + b^2 + 2ab}{4} + \dfrac{a^2 + b^2 - 2ab}{4}}$'
            ).set_color(YELLOW)
        quad_formula_intermediate.move_to(3*DOWN)
        quad_formula_final = TextMobject('QM',
            r' $=\sqrt{\dfrac{a^2 + b^2}{2}}$'
            ).set_color(YELLOW)
        quad_formula_final.move_to(3*DOWN)
        self.quad_formula = TextMobject(r'QM', ' = quadratic mean').set_color(YELLOW)
        self.quad_formula.to_edge(LEFT)
        self.quad_formula.shift(DOWN * 2 + RIGHT * SMALL_BUFF)

        # Animate
        self.play(ShowCreation(self.qm_line))
        self.wait()
        self.play(FadeIn(diff_line))
        self.play(GrowFromCenter(brace_diff), Write(label_diff))
        self.wait()
        self.play(ReplacementTransform(label_diff, new_label_diff))
        self.wait(2)
        self.play(FadeOut(brace_diff), FadeOut(new_label_diff))
        self.play(Write(label_qm))
        self.wait()
        self.play(ApplyMethod(label_copy.move_to, quad_formula[0].get_center()))
        self.add(quad_formula[0])
        self.remove(label_copy)
        self.play(Write(quad_formula[1]))
        self.wait(2)
        self.play(ReplacementTransform(quad_formula[0], quad_formula_intermediate[0]),
        ReplacementTransform(quad_formula[1], quad_formula_intermediate[1]))
        self.wait(2)
        self.play(ReplacementTransform(quad_formula_intermediate[0],
            quad_formula_final[0]), ReplacementTransform(quad_formula_intermediate[1],
                quad_formula_final[1])
            )
        self.wait(2)
        self.play(ReplacementTransform(quad_formula_final[0], self.quad_formula[0]),
                    FadeOut(quad_formula_final[1]))
        self.play(Write(self.quad_formula[1]))
        self.play(FadeOut(diff_line), FadeOut(label_qm))
        self.wait(2)

    def get_geometric_mean(self):
        # Setup lines
        gm_length = (self.a.get_length() * self.b.get_length())**0.5
        self.gm_line = Line(self.b.get_start(),
            self.b.get_start()+[0., gm_length, 0.], color = TEAL)

        # Animate
        self.play(ShowCreation(self.gm_line))
        self.wait()

    def animate_gm_formula(self):
        # Setup Tex and Text
        brace_gm = Brace(self.gm_line, LEFT, buff = SMALL_BUFF).set_color(TEAL)
        label_gm = brace_gm.get_tex(r'{\rm GM}').set_color(TEAL)
        label_gm.bg=BackgroundRectangle(label_gm, fill_opacity=0.8)
        label_copy = label_gm.copy()
        label_gm_group = VGroup(label_gm.bg, label_gm)
        avg = r'\dfrac{a+b}{2}'
        half_diff = r'\dfrac{a-b}{2}'

        gm = TexMobject(r'\text{GM}')
        gm.set_color(TEAL)
        gm.move_to(3*DOWN)

        rhs_1 = TexMobject(
            r'=\sqrt{\left(%s\right)^2-\left(%s\right)^2}' % (avg, half_diff)
        )
        rhs_1.set_color(TEAL)
        rhs_1.next_to(gm, RIGHT)

        rhs_intermediate = TexMobject(
            r'=\sqrt{%s - %s}' % (
                r'\dfrac{a^2 + b^2 + 2ab}{4}',
                r'\dfrac{a^2 + b^2 - 2ab}{4}'
            )
        )
        rhs_intermediate.set_color(TEAL)
        rhs_intermediate.next_to(gm, RIGHT)

        rhs_final = TexMobject(r'{\rm GM}', r'=\sqrt{ab}').set_color(TEAL)
        rhs_final.next_to(gm, RIGHT)

        # Get individual pieces of above equations
        a_group_1 = VGroup(rhs_1[0][4], rhs_intermediate[0][3])
        b_group_1 = VGroup(rhs_1[0][6], rhs_intermediate[0][6])
        pluses_1 = VGroup(rhs_1[0][5], rhs_intermediate[0][5])
        a_group_2 = VGroup(rhs_1[0][13], rhs_intermediate[0][15])
        b_group_2 = VGroup(rhs_1[0][15], rhs_intermediate[0][18])
        minus_to_plus = VGroup(rhs_1[0][14], rhs_intermediate[0][17])
        plus_2ab = VGroup(*[rhs_intermediate[0][i] for i in range(8, 12)])
        minus_2ab = VGroup(*[rhs_intermediate[0][i] for i in range(20, 24)])
        denoms_1 = VGroup(
            VGroup(*[rhs_1[0][i] for i in [7,8]]),
            VGroup(*[rhs_intermediate[0][i] for i in [12,13]])
        )
        denoms_2 = VGroup(
            VGroup(*[rhs_1[0][i] for i in [16,17]]),
            VGroup(*[rhs_intermediate[0][i] for i in [24,25]])
        )

        square_roots = VGroup(
            VGroup(*[rhs_1[0][i] for i in range(2)]),
            VGroup(*[rhs_intermediate[0][i] for i in range(2)])
        )
        squared_1 = VGroup(*[rhs_1[0][i] for i in [9,-1]])
        squared_2 = VGroup(
            VGroup(*[rhs_intermediate[0][i] for i in [3, 6]]),
            VGroup(*[rhs_intermediate[0][i] for i in [3, 6]])
        )


        self.gm_formula = TextMobject('GM', r' = geometric mean').set_color(TEAL)
        self.gm_formula.to_edge(LEFT)
        self.gm_formula.shift(2.75*DOWN + SMALL_BUFF * RIGHT)

        # Animate
        self.play(GrowFromCenter(brace_gm), FadeIn(label_gm_group))
        self.wait()
        self.play(ReplacementTransform(label_copy, gm))
        self.play(Write(rhs_1))
        self.wait()
        self.play(ReplacementTransform(square_roots[0], square_roots[1]))
        items = [a_group_1, b_group_1, a_group_2, b_group_2, pluses_1,
            minus_to_plus, denoms_1, denoms_2]
        self.play(*[ReplacementTransform(item[0], item[1]) for item in items])
        self.play(Write(plus_2ab), Write(minus_2ab))
        self.wait()
        # self.play(ApplyMethod(gm_formula_final[0].move_to, self.gm_formula[0].get_center()),
        #     FadeOut(gm_formula_final[1]))
        # self.play(Write(self.gm_formula[1]))
        # self.play(FadeOut(brace_gm), FadeOut(label_gm_group))
        self.wait(2)

    def get_harmonic_mean(self):
        # Setup lines and formulae
        radius = Line(self.am_line.get_end(), self.gm_line.get_end())
        d1 = Dot()
        harmonic_mean = 2./(1/self.a.get_length() + 1/self.b.get_length())
        avg = (self.a.get_length() + self.b.get_length())/2
        d1.move_to(radius.get_end()/avg*(avg-harmonic_mean))
        intersecting_line = Line(d1.get_center(), self.gm_line.get_start())
        right_angle = RightAngle(intersecting_line, radius,
            length = LINE_LENGTH/32., quadrant = (1,-1)
        )
        self.hm_line = Line(d1.get_center(), self.gm_line.get_end(), color = PINK)
        self.hm_formula = TextMobject('HM', r' = harmonic mean').set_color(PINK)
        self.hm_formula.to_edge(LEFT)
        self.hm_formula.shift(3.5*DOWN + SMALL_BUFF * RIGHT)

        prop_form = TexMobject(
            r'{ {\rm HM} \over {\rm GM} }', '=', r'{ {\rm GM} \over {\rm AM} }'
        )
        HM = VGroup(prop_form[0][0], prop_form[0][1])
        gm_denom = VGroup(prop_form[0][-1], prop_form[0][-2])
        gm_num = VGroup(prop_form[2][0], prop_form[2][1])
        am_denom = VGroup(prop_form[2][-1], prop_form[2][-2])
        GM2 = TexMobject(r'{\rm GM}','^2')
        GM2[0].set_color(TEAL)

        prop_form.shift(2*DOWN + 2*RIGHT)
        HM.set_color(PINK)
        gm_num.set_color(TEAL)
        gm_denom.set_color(TEAL)
        am_denom.set_color(RED_A)

        # Animate
        self.play(ShowCreation(radius))
        self.wait()
        self.play(ShowCreation(intersecting_line), ShowCreation(right_angle))
        self.wait()
        self.play(ShowCreation(self.hm_line))
        self.wait()
        lines = [self.hm_line, self.gm_line, self.gm_line, radius]
        dests = [HM, gm_denom, gm_num, am_denom]
        for line, dest in zip(lines, dests):
            self.play(ReplacementTransform(line.copy(), dest))
        self.play(Write(prop_form[0][2]), Write(prop_form[1]), Write(prop_form[2][2]))
        self.wait(2)
        self.play(
            ApplyMethod(gm_denom.move_to, gm_num)
        )
        GM2.move_to(gm_num[1].get_center()+SMALL_BUFF*LEFT)
        GM2 = VGroup(gm_num, GM2[1])
        self.remove(gm_denom)
        self.play(Write(GM2[1]))
        self.play(ApplyMethod(HM.move_to, prop_form[0][2].get_center()),
            FadeOut(prop_form[0][2])
        )
        equals = TexMobject(r'= {2ab \over {a+b}}')
        equals.next_to(HM)
        num = VGroup(*[equals[0][i] for i in [2,3]]).set_color(TEAL)
        denom = VGroup(*[equals[0][i] for i in [1,-1,-2,-3]]).set_color(RED_A)
        self.play(
            ReplacementTransform(GM2, num),
            ReplacementTransform(prop_form[2][2], equals[0][4])
        )
        self.play(ReplacementTransform(am_denom, denom))
        self.wait()
        denom = VGroup(equals[0][-3], equals[0][-2], equals[0][-1])
        hm_denom = TexMobject(r'{1 \over a}', '+', r'{1 \over b}')
        hm_denom.next_to(equals[0][4], DOWN)
        self.play(*[ApplyMethod(denom[i].move_to, hm_denom[i][-1]) for i in range(3)])
        self.play(Write(hm_denom), FadeOut(equals[0][2]), FadeOut(equals[0][3]),
            ApplyMethod(equals[0][1].next_to, equals[0][4], UP, buff = 0))
        self.play(*[FadeOut(denom[i]) for i in range(3)])
        self.wait(2)
        self.play(ApplyMethod(HM.move_to, self.hm_formula[0]),
            *[FadeOut(item) for item in [hm_denom, equals[0][1], equals[0][4],
                prop_form[1]]])
        self.play(Write(self.hm_formula[1]))
        self.wait(2)
