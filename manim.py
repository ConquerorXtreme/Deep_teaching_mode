from manimlib import *
import numpy as np
from manim import *

class ElectricChargeAndCoulombsLaw(Scene):
    def construct(self):
        # Title and introduction
        title = Text("Electric Charge and Coulomb's Law", font_size=40)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # Part 1: Subatomic particles and their charges
        self.explain_subatomic_particles()
        
        # Part 2: Like charges repel, unlike charges attract
        self.demonstrate_charge_interactions()
        
        # Part 3: Coulomb's Law visualization
        self.explain_coulombs_law()
        
        # Conclusion
        conclusion = Text("Good luck with your exam!", font_size=36)
        conclusion.to_edge(DOWN)
        self.play(Write(conclusion))
        self.wait(2)

    def explain_subatomic_particles(self):
        subtitle = Text("Subatomic Particles and Charge", font_size=32)
        subtitle.next_to(self.camera.frame_width * UP / 4, DOWN)
        
        self.play(Write(subtitle))
        
        # Create particles
        electron = Circle(radius=0.5, color=BLUE, fill_opacity=0.8)
        electron_label = Text("Electron (-)").scale(0.7)
        electron_label.next_to(electron, DOWN)
        electron_group = VGroup(electron, electron_label).move_to(LEFT * 3)
        
        proton = Circle(radius=0.5, color=RED, fill_opacity=0.8)
        proton_label = Text("Proton (+)").scale(0.7)
        proton_label.next_to(proton, DOWN)
        proton_group = VGroup(proton, proton_label)
        
        neutron = Circle(radius=0.5, color=RED, fill_opacity=0.8)
        neutron_label = Text("Neutron (0)").scale(0.7)
        neutron_label.next_to(neutron, DOWN)
        neutron_group = VGroup(neutron, neutron_label).move_to(RIGHT * 3)
        
        # Show particles
        self.play(FadeIn(electron_group))
        self.play(FadeIn(proton_group))
        self.play(FadeIn(neutron_group))
        self.wait(1)
        
        # Information about charges
        charge_info = Text("• Electrons carry negative charge\n• Protons carry positive charge\n• Neutrons have no charge\n• Charge is quantized (e = 1.602 × 10⁻¹⁹ C)\n• Charge is conserved", 
                          font_size=24, line_spacing=0.5)
        charge_info.to_edge(DOWN, buff=1)
        
        self.play(Write(charge_info))
        self.wait(2)
        
        self.play(
            FadeOut(subtitle),
            FadeOut(electron_group),
            FadeOut(proton_group),
            FadeOut(neutron_group),
            FadeOut(charge_info)
        )

    def demonstrate_charge_interactions(self):
        subtitle = Text("Charge Interactions", font_size=32)
        subtitle.next_to(self.camera.frame_width * UP / 4, DOWN)
        
        self.play(Write(subtitle))
        
        # Create positive and negative charges
        pos_charge1 = Circle(radius=0.5, color=RED, fill_opacity=0.8)
        pos_charge1_label = Text("+", font_size=40, color=WHITE)
        pos_charge1_group = VGroup(pos_charge1, pos_charge1_label).move_to(LEFT * 2.5 + UP * 1.5)
        
        pos_charge2 = Circle(radius=0.5, color=RED, fill_opacity=0.8)
        pos_charge2_label = Text("+", font_size=40, color=WHITE)
        pos_charge2_group = VGroup(pos_charge2, pos_charge2_label).move_to(LEFT * 1 + UP * 1.5)
        
        neg_charge1 = Circle(radius=0.5, color=BLUE, fill_opacity=0.8)
        neg_charge1_label = Text("−", font_size=40, color=WHITE)
        neg_charge1_group = VGroup(neg_charge1, neg_charge1_label).move_to(RIGHT * 1 + UP * 1.5)
        
        neg_charge2 = Circle(radius=0.5, color=BLUE, fill_opacity=0.8)
        neg_charge2_label = Text("−", font_size=40, color=WHITE)
        neg_charge2_group = VGroup(neg_charge2, neg_charge2_label).move_to(RIGHT * 2.5 + UP * 1.5)
        
        # Show charges
        self.play(
            FadeIn(pos_charge1_group),
            FadeIn(pos_charge2_group),
            FadeIn(neg_charge1_group),
            FadeIn(neg_charge2_group)
        )
        
        # Like charges repel
        pos_repel_arrow1 = Arrow(start=pos_charge1.get_center(), end=pos_charge1.get_center() + LEFT * 0.8, color=YELLOW)
        pos_repel_arrow2 = Arrow(start=pos_charge2.get_center(), end=pos_charge2.get_center() + RIGHT * 0.8, color=YELLOW)
        
        neg_repel_arrow1 = Arrow(start=neg_charge1.get_center(), end=neg_charge1.get_center() + LEFT * 0.8, color=YELLOW)
        neg_repel_arrow2 = Arrow(start=neg_charge2.get_center(), end=neg_charge2.get_center() + RIGHT * 0.8, color=YELLOW)
        
        repel_label = Text("Like charges repel", font_size=28).next_to(VGroup(pos_charge1_group, pos_charge2_group, neg_charge1_group, neg_charge2_group), UP)
        
        self.play(
            Write(repel_label),
            GrowArrow(pos_repel_arrow1),
            GrowArrow(pos_repel_arrow2),
            GrowArrow(neg_repel_arrow1),
            GrowArrow(neg_repel_arrow2)
        )
        self.wait(1.5)
        
        self.play(
            FadeOut(pos_repel_arrow1),
            FadeOut(pos_repel_arrow2),
            FadeOut(neg_repel_arrow1),
            FadeOut(neg_repel_arrow2),
            FadeOut(repel_label)
        )
        
        # Unlike charges attract
        pos_charge3 = Circle(radius=0.5, color=RED, fill_opacity=0.8)
        pos_charge3_label = Text("+", font_size=40, color=WHITE)
        pos_charge3_group = VGroup(pos_charge3, pos_charge3_label).move_to(LEFT * 1.5 + DOWN * 1)
        
        neg_charge3 = Circle(radius=0.5, color=BLUE, fill_opacity=0.8)
        neg_charge3_label = Text("−", font_size=40, color=WHITE)
        neg_charge3_group = VGroup(neg_charge3, neg_charge3_label).move_to(RIGHT * 1.5 + DOWN * 1)
        
        self.play(
            FadeOut(pos_charge1_group),
            FadeOut(pos_charge2_group),
            FadeOut(neg_charge1_group),
            FadeOut(neg_charge2_group),
            FadeIn(pos_charge3_group),
            FadeIn(neg_charge3_group)
        )
        
        attract_arrow1 = Arrow(start=pos_charge3.get_center(), end=pos_charge3.get_center() + RIGHT * 0.8, color=YELLOW)
        attract_arrow2 = Arrow(start=neg_charge3.get_center(), end=neg_charge3.get_center() + LEFT * 0.8, color=YELLOW)
        
        attract_label = Text("Unlike charges attract", font_size=28).next_to(VGroup(pos_charge3_group, neg_charge3_group), UP)
        
        self.play(
            Write(attract_label),
            GrowArrow(attract_arrow1),
            GrowArrow(attract_arrow2)
        )
        self.wait(1.5)
        
        self.play(
            FadeOut(subtitle),
            FadeOut(pos_charge3_group),
            FadeOut(neg_charge3_group),
            FadeOut(attract_arrow1),
            FadeOut(attract_arrow2),
            FadeOut(attract_label)
        )

    def explain_coulombs_law(self):
        subtitle = Text("Coulomb's Law", font_size=32)
        subtitle.next_to(self.camera.frame_width * UP / 4, DOWN)
        
        self.play(Write(subtitle))
        
        # Formula
        formula = Text(r"F = k \frac{|q_1 q_2|}{r^2}", font_size=40)
        formula.move_to(UP * 2)
        
        formula_description = Text(
            "Where:\nF = electric force\nk = Coulomb's constant (8.99 × 10⁹ Nm²/C²)\nq₁, q₂ = magnitudes of charges\nr = distance between charges",
            font_size=24, line_spacing=0.5
        )
        formula_description.next_to(formula, DOWN, buff=0.5)
        
        self.play(Write(formula))
        self.play(Write(formula_description))
        self.wait(1.5)
        
        # Example visual
        charge1 = Circle(radius=0.5, color=RED, fill_opacity=0.8)
        charge1_label = Text("+2C", font_size=24, color=WHITE)
        charge1_group = VGroup(charge1, charge1_label).move_to(LEFT * 2.5 + DOWN * 0.5)
        
        charge2 = Circle(radius=0.5, color=BLUE, fill_opacity=0.8)
        charge2_label = Text("-3C", font_size=24, color=WHITE)
        charge2_group = VGroup(charge2, charge2_label).move_to(RIGHT * 2.5 + DOWN * 0.5)
        
        distance_line = Line(charge1.get_center(), charge2.get_center(), color=WHITE)
        distance_label = Text("r = 0.5m", font_size=24).next_to(distance_line, DOWN, buff=0.2)
        
        force_arrow1 = Arrow(start=charge1.get_center(), end=charge1.get_center() + RIGHT * 1, color=YELLOW, max_tip_length_to_length_ratio=0.2)
        force_arrow2 = Arrow(start=charge2.get_center(), end=charge2.get_center() + LEFT * 1, color=YELLOW, max_tip_length_to_length_ratio=0.2)
        
        self.play(
            FadeIn(charge1_group),
            FadeIn(charge2_group)
        )
        # self.play(
        #     ShowCreationThenDestruction(distance_line),
        #     Write(distance_label)
        # )
        self.wait(1)
        
        result = Text("Force = 216 × 10⁹ N (attractive)", font_size=28, color=YELLOW)
        result.next_to(VGroup(charge1_group, charge2_group), DOWN, buff=0.5)
        
        self.play(
            GrowArrow(force_arrow1),
            GrowArrow(force_arrow2),
            Write(result)
        )
        
        # Important points
        points = Text(
            "• Force is along the line joining the charges\n• Force is directly proportional to product of charges\n• Force is inversely proportional to square of distance\n• Like charges repel, unlike charges attract",
            font_size=24, line_spacing=0.5
        )
        points.to_edge(DOWN, buff=0.5)
        
        self.play(Write(points))
        self.wait(2)
        
        self.play(
            FadeOut(subtitle),
            FadeOut(formula),
            FadeOut(formula_description),
            FadeOut(charge1_group),
            FadeOut(charge2_group),
            FadeOut(distance_line),
            FadeOut(distance_label),
            FadeOut(force_arrow1),
            FadeOut(force_arrow2),
            FadeOut(result),
            FadeOut(points)
        )

# Use this class to run the animation
# if __name__ == "__main__":
#     scene = ElectricChargeAndCoulombsLaw()
#     scene.render()