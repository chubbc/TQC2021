from manim import *

config.background_color = "#161c20"

toc=Group(
    Tex("1.~Decoding Pauli noise"),
    Tex("2.~Tensor network decoding"),
    Tex("3.~Contracting 2D tensor networks"),
    Tex("4.~","Sweepline"," Contraction"),
    Tex("5.~Numerics"),
    Tex("6.~Results"),
    Tex("7.~Conclusion"),
).arrange(DOWN,aligned_edge=LEFT,buff=0.5).move_to(ORIGIN)

class Title(Scene):
    def construct(self):
        title = Tex(r"\bfseries\textsc{General tensor network decoding \\of 2D Pauli codes}").scale(1.25).shift(2.5*UP)
        arxiv = Tex(r"\bfseries\texttt{arXiv:2101.04125}").scale(.75).shift(1.5*UP)
        name = Tex("Christopher T.\ Chubb")
        ethz=SVGMobject("ethz_logo_white.svg").scale(1/3).next_to(1.5*DOWN,LEFT,buff=2.5)
        udes=SVGMobject("Université_de_Sherbrooke_(logo).svg").scale(1/3).next_to(1.5*DOWN,RIGHT,buff=2.5)

        self.play(FadeIn(name))
        self.wait()

        self.play(FadeIn(title),FadeIn(arxiv))
        self.wait()

        self.play(Write(ethz,run_time=2))
        self.play(Write(udes,run_time=1))
        self.wait()

        self.remove(title,arxiv,name,ethz,udes)
        self.wait()

        self.play(FadeIn(toc))
        self.wait()

        self.play(toc[0].animate.scale(1.2).set_color(YELLOW))
        self.wait()

        for i in range(1,7):
            self.play(toc[i].animate.scale(1.2).set_color(YELLOW),toc[i-1].animate.scale(1/1.2).set_color(WHITE))
            self.wait()

        self.play(toc[-1].animate.scale(1/1.2).set_color(WHITE))

class MLD(Scene):
    def construct(self):
        heading = toc[0].copy().move_to(ORIGIN).scale(1.5).to_corner(UP)
        self.add(toc)
        self.wait()
        self.play(FadeOut(toc), ReplacementTransform(toc[0],heading))
        self.wait()

        heading_maxprob = Tex("Which is the most likely ", "error","?")
        heading_maxprob[1].set_color(YELLOW)

        self.play(FadeIn(heading_maxprob))
        self.wait()

        self.play(heading_maxprob.animate.shift(2*UP))
        paulitoprob=MathTex("\\text{Error}","\\to","\\text{Probability}")
        paulitoprob[0].set_color(YELLOW)
        paulitoprob[2].set_color(RED)
        self.play(FadeIn(paulitoprob[0]))
        self.play(TransformFromCopy(paulitoprob[0],paulitoprob[2]),FadeIn(paulitoprob[1]))
        self.wait()

        pauli=MathTex("{\\bigotimes}_{i}P_i").next_to(paulitoprob[1],LEFT).set_color(YELLOW)
        iid=MathTex("{\\prod}_{i}p_i(","P_i",")").next_to(paulitoprob[1],RIGHT)
        iid[0].set_color(RED)
        iid[1].set_color(YELLOW)
        iid[2].set_color(RED)
        self.play(
            Transform(paulitoprob[0],pauli),
            Transform(paulitoprob[2],iid)
        )
        self.wait()

        corr=MathTex("{\\prod}_{j}\phi_j(","P_{R_j}",")").next_to(paulitoprob[1],RIGHT)
        corr[0].set_color(RED)
        corr[1].set_color(YELLOW)
        corr[2].set_color(RED)
        self.play(
            Transform(paulitoprob[2],corr)
        )
        self.wait()

        self.play(
            Transform(paulitoprob[0],Tex("Error").set_color(YELLOW).next_to(paulitoprob[1],LEFT)),
            Transform(paulitoprob[2],Tex("Probability").set_color(RED).next_to(paulitoprob[1],RIGHT)),
        )
        self.wait()


        h=[0.680,0.305,0.734,0.218,0.260,0.673,0.634,0.926,0.513,0.267,0.451,
        0.571,0.347,0.721,0.241,0.352,0.387,0.213,0.950,0.704,0.494,0.582,0.860,
        0.853,0.442,0.796,0.937,0.912,0.211,0.221,0.056,0.201,0.425,0.159,0.264,
        0.961,0.270,0.398,0.438,0.840]
        H=[sum(h[0:10]),sum(h[10:20]),sum(h[20:30]),sum(h[30:40])]
        maxh=35;
        maxH=2;
        l=40;

        bar=VGroup()
        for i in range(l):
            bar+=Rectangle(width=0.25,height=2*h[i],color=YELLOW).set_fill(YELLOW,opacity=0.25).next_to([i/4-(l-1)/8,-2,0],UP).set_stroke(width=2)
        self.play(paulitoprob.animate.shift(UP),TransformFromCopy(paulitoprob[0],bar))
        self.wait()

        self.play(
            bar[maxh].animate.set_stroke(color=YELLOW),
            bar[maxh].animate.set_fill(YELLOW,opacity=.75)
        )
        self.wait()

        maxprob=MathTex("\mathop{\mathrm{arg\,max}}","_E"," \mathrm{Pr}(", "E", ")").shift(3*DOWN)
        maxprob[1].set_color(YELLOW)
        maxprob[2].set_color(RED)
        maxprob[3].set_color(YELLOW)
        maxprob[4].set_color(RED)

        self.play(TransformFromCopy(bar[maxh],maxprob))
        self.wait()

        anims=[]
        for i in range(0,10):
            anims.append(bar[i].animate.shift(0.75*LEFT))
        for i in range(10,20):
            anims.append(bar[i].animate.shift(0.25*LEFT))
        for i in range(20,30):
            anims.append(bar[i].animate.shift(0.25*RIGHT))
        for i in range(30,40):
            anims.append(bar[i].animate.shift(0.75*RIGHT))
        self.play(*anims)
        self.wait()

        self.play(Circumscribe(bar[0:10]))
        self.play(Circumscribe(bar[10:20]))
        self.play(Circumscribe(bar[20:30]))
        self.play(Circumscribe(bar[30:40]))
        self.wait()

        heading_maxlike = Tex("Which is the most likely ", "error class","?").shift(2*UP)
        heading_maxlike[1].set_color(BLUE)
        self.play(Transform(heading_maxprob,heading_maxlike))
        self.wait()

        classtoprob=Tex("Error class").next_to(paulitoprob[1],LEFT).set_color(BLUE).shift(RIGHT/2)
        self.play(
            Transform(paulitoprob[0],classtoprob),
            paulitoprob[1].animate.shift(RIGHT/2),
            paulitoprob[2].animate.shift(RIGHT/2)
        )
        self.wait()

        bar2=VGroup()
        for i in range(4):
            bar2+=Rectangle(width=2.5,height=H[i]/5,color=BLUE).set_fill(BLUE,opacity=0.25).next_to([1.25*(2*i-3),-2,0],UP).set_stroke(width=2)
        self.play(
            Transform(bar[0:10],bar2[0]),
            Transform(bar[10:20],bar2[1]),
            Transform(bar[20:30],bar2[2]),
            Transform(bar[30:40],bar2[3])
        )
        self.wait()

        maxlike=MathTex(
            "\mathop{\mathrm{arg\,max}}",
            "_{\overline{E}}",
            " \mathrm{Pr}(",
            "\overline{E}",
            ")").shift(3*DOWN)
        maxlike[1].set_color(BLUE)
        maxlike[2].set_color(RED)
        maxlike[3].set_color(BLUE)
        maxlike[4].set_color(RED)
        self.play(
            bar2[maxH].animate.set_fill(BLUE,opacity=.75),
            Transform(maxprob,maxlike)
        )
        self.wait()

        self.play(
            FadeOut(paulitoprob),
            FadeOut(bar),
            FadeOut(heading_maxprob),
            FadeOut(bar2),
            FadeOut(maxprob),
            maxlike.animate.shift(3.5*UP)
        )
        self.wait()

        mld=Tex("Maximum likelihood condition").shift(1.75*UP)
        sr=SurroundingRectangle(maxlike,color=WHITE,buff=0.25)
        self.play(FadeIn(mld),FadeIn(sr))
        self.wait()

        self.play(Circumscribe(maxlike[2:5],color=WHITE))
        self.wait()

        coset1=MathTex(
            r"\mathrm{Pr}(",
            r"\overline E",
            r")"
        )#.scale(1)
        coset1[0].set_color(RED)
        coset1[1].set_color(BLUE)
        coset1[2].set_color(RED)
        coset2=MathTex(
            r":=\sum_{",
            r"E",
            r"\in",
            r"\overline E}",
            r"\mathrm{Pr}(",
            r"E",
            r")"
        ).next_to(coset1,RIGHT)#.scale(1).next_to([-.5,-1.75,0],RIGHT)
        coset2[0].set_color(WHITE)
        coset2[1].set_color(YELLOW)
        coset2[2].set_color(WHITE)
        coset2[3].set_color(BLUE)
        coset2[4].set_color(RED)
        coset2[5].set_color(YELLOW)
        coset2[6].set_color(RED)
        coset3=MathTex(
            r"=",
            r"\sum_{S\in\mathrm{Stab}}",
            r"\mathrm{Pr}(",
            r"E",
            r"S",
            r")"
        ).next_to(coset2,RIGHT)#.scale(1).next_to([-.5,-3,0],RIGHT)
        coset3[0].set_color(WHITE)
        coset3[1].set_color(WHITE)
        coset3[2].set_color(RED)
        coset3[3].set_color(YELLOW)
        coset3[4].set_color(WHITE)
        coset3[5].set_color(RED)

        coset1.shift(0.25*UP)
        coset=VGroup(coset1,coset2,coset3).move_to(2*DOWN)

        self.play(TransformFromCopy(maxlike[2:5],coset1))
        self.wait()

        self.play(Write(coset2))
        self.wait()

        self.play(Write(coset3))
        self.wait()

        self.play(Circumscribe(coset3[1],color=WHITE))
        self.wait()

        self.play(
            FadeOut(coset),
            FadeOut(heading),
            FadeOut(mld),
            FadeOut(sr),
            FadeOut(maxlike)
        )
        self.wait()

class TN(Scene):
    def construct(self):
        heading = toc[1].copy().move_to(ORIGIN).scale(1.5).to_corner(UP)
        self.play(FadeIn(toc))
        self.wait()
        self.play(FadeOut(toc), ReplacementTransform(toc[1],heading))
        self.wait()

        flow1=Group(
            Tex("Class prob.", color=YELLOW),
            Arrow(LEFT,RIGHT),
            Tex("Tensor network", color=RED),
            Tex("?")
        )
        flow1[1].next_to(flow1[0],RIGHT)
        flow1[2].next_to(flow1[1],RIGHT)
        flow1[3].next_to(flow1[1],UP)
        flow1.move_to(ORIGIN)

        self.play(Write(flow1[0]))
        self.wait()

        self.play(Write(flow1[2]))
        self.wait()

        self.play(Write(flow1[1]),Write(flow1[3]))
        self.wait()

        self.play(flow1.animate.shift(2*UP))


        fp=Group(
            ImageMobject("FerrisPoulin.png"),
            # Tex(r"PRL \textbf{113}, 030501 (2014)\\\texttt{arXiv:1312.4578}\qquad\texttt{doi:10/gjs9p7}").scale(0.75)
            Tex(r"\texttt{arXiv:1312.4578}\qquad\texttt{doi:10/gjs9p7}").scale(0.75)
        )
        fp[0].height=4
        fp.arrange(DOWN).shift(DOWN)
        self.play(FadeIn(fp))
        self.wait()

        bsv=Group(
            ImageMobject("BravyiSucharaVargo.png"),
            # Tex(r"PRA \textbf{90}, 032326 (2014)\\\texttt{arXiv:1405.4883}\qquad\texttt{doi:10/cv7n}").scale(0.75)
            Tex(r"\texttt{arXiv:1405.4883}\qquad\texttt{doi:10/cv7n}").scale(0.75)
        )
        bsv[0].height=4
        bsv.arrange(DOWN).shift(DOWN)
        self.play(FadeOut(fp))
        self.play(FadeIn(bsv))
        self.wait()

        flow2=Group(
            Tex("Class prob.", color=YELLOW),
            Arrow(ORIGIN,RIGHT),
            Tex("Stat mech model", color=BLUE),
            Arrow(ORIGIN,RIGHT),
            Tex("Tensor network", color=RED)
        )
        for i in range(1,5):
            flow2[i].next_to(flow2[i-1],RIGHT)
        flow2.move_to(flow1)
        cf=Group(
            ImageMobject("ChubbFlammia.png").scale(.75),
            # Tex(r"AIHP(D), 8 (2) 269\textendash 321 (2021)\\\texttt{arXiv:1809.10704}\qquad\texttt{doi:10/gj3pqb}").scale(0.75)
            Tex(r"\texttt{arXiv:1809.10704}\qquad\texttt{doi:10/gj3pqb}").scale(0.75)
        )
        cf[0].height=4
        cf.arrange(DOWN).shift(DOWN)
        self.play(FadeOut(bsv))
        self.play(
            ReplacementTransform(flow1[0],flow2[0]),
            ReplacementTransform(flow1[2],flow2[4]),
            FadeOut(flow1[1]),
            FadeOut(flow1[3]),
            FadeIn(flow2[1]),
            FadeIn(flow2[2]),
            FadeIn(flow2[3]),
            FadeIn(cf)
        )
        self.wait()

        # self.play(Circumscribe(cf))
        # self.wait()

        flow3=Group(
            Tex("Class prob.", color=YELLOW),
            Arrow(ORIGIN,DOWN),
            Tex("Stat mech model", color=BLUE),
            Arrow(ORIGIN,DOWN),
            Tex("Tensor network", color=RED)
        )
        for i in range(1,5):
            flow3[i].next_to(flow3[i-1],DOWN,buff=.75)
        flow3.move_to(0.5*DOWN)
        self.play(FadeOut(cf))
        self.play(*[ReplacementTransform(flow2[i],flow3[i]) for i in range(5)])
        self.wait()

        self.play(
            Transform(flow3[0],Tex(r"Class probabilities of a\\local Pauli code").set_color(YELLOW).move_to(flow3[0]))
        )
        self.wait()

        self.play(
            Transform(flow3[2],Tex(r"Partition functions of a\\local stat mech model").set_color(BLUE).move_to(flow3[2])),
            Transform(flow3[1],Tex("=").rotate(90*DEGREES).set_color(WHITE).move_to(flow3[1])),
        )
        self.wait()

        self.play(
            Transform(flow3[4],Tex(r"Contraction of a\\local tensor network").set_color(RED).move_to(flow3[4])),
            Transform(flow3[3],Tex("=").rotate(90*DEGREES).set_color(WHITE).move_to(flow3[3])),
        )
        self.wait()

        flow4=Group(
            Tex(r"Class probabilities of a\\2D local Pauli code", color=YELLOW),
            Arrow(ORIGIN,DOWN),
            Tex(r"Partition functions of a\\2D local stat mech model", color=BLUE),
            Arrow(ORIGIN,DOWN),
            Tex(r"Contraction of a\\2D local tensor network", color=RED)
        )
        for i in range(5):
            flow4[i].move_to(flow3[i])
        self.play(FadeOut(flow3),FadeIn(flow4))
        self.wait()

        # self.play(FadeOut(heading),FadeOut(flow4))
        self.play(FadeOut(flow4))
        self.wait()

        cf.height=5
        cf.move_to(DOWN/2)
        self.play(FadeIn(cf))
        self.wait()
        self.play(FadeOut(cf))
        self.wait()

        DIAG=np.array([1/2,np.sqrt(3)/2,0])
        MID=(2*RIGHT+2*DIAG)/3

        CC=VGroup(
            Polygon(DIAG,ORIGIN,RIGHT,MID,stroke_width=0,color=BLUE).set_fill(opacity=1),
            Polygon(DIAG+RIGHT,MID,RIGHT,2*RIGHT,stroke_width=0,color=GREEN).set_fill(opacity=1),
            Polygon(2*DIAG,DIAG,MID,DIAG+RIGHT,stroke_width=0,color=RED).set_fill(opacity=1),
            Polygon(DIAG,ORIGIN,RIGHT,MID,color=BLACK),
            Polygon(DIAG+RIGHT,MID,RIGHT,2*RIGHT,color=BLACK),
            Polygon(2*DIAG,DIAG,MID,DIAG+RIGHT,color=BLACK),
            Circle(0.05,BLACK).move_to(ORIGIN).set_fill(WHITE,opacity=1),
            Circle(0.05,BLACK).move_to(RIGHT).set_fill(WHITE,opacity=1),
            Circle(0.05,BLACK).move_to(2*RIGHT).set_fill(WHITE,opacity=1),
            Circle(0.05,BLACK).move_to(DIAG).set_fill(WHITE,opacity=1),
            Circle(0.05,BLACK).move_to(DIAG+RIGHT).set_fill(WHITE,opacity=1),
            Circle(0.05,BLACK).move_to(2*DIAG).set_fill(WHITE,opacity=1),
            Circle(0.05,BLACK).move_to(MID).set_fill(WHITE,opacity=1),
        ).move_to(3*LEFT+DOWN/2).scale(2)

        TN=Group(
            Line(ORIGIN,MID,color=BLUE),
            Line(DIAG,MID/2,color=BLUE),
            Line(RIGHT,MID/2,color=BLUE),
            Circle(0.1,BLUE).move_to(MID/2).set_fill(BLUE_E,opacity=1),
            Line(2*RIGHT,MID,color=GREEN),
            Line(RIGHT,RIGHT+MID/2,color=GREEN),
            Line(DIAG+RIGHT,RIGHT+MID/2,color=GREEN),
            Circle(0.1,GREEN).move_to(MID/2+RIGHT).set_fill(GREEN_E,opacity=1),
            Line(DIAG,DIAG+MID/2,color=RED),
            Line(RIGHT+DIAG,DIAG+MID/2,color=RED),
            Line(2*DIAG,MID,color=RED),
            Circle(0.1,RED).move_to(DIAG+MID/2).set_fill(RED_E,opacity=1),
            Circle(0.1,GRAY).move_to(ORIGIN).set_fill(opacity=1),
            Circle(0.1,GRAY).move_to(RIGHT).set_fill(opacity=1),
            Circle(0.1,GRAY).move_to(2*RIGHT).set_fill(opacity=1),
            Circle(0.1,GRAY).move_to(DIAG).set_fill(opacity=1),
            Circle(0.1,GRAY).move_to(DIAG+RIGHT).set_fill(opacity=1),
            Circle(0.1,GRAY).move_to(2*DIAG).set_fill(opacity=1),
            Circle(0.1,GRAY).move_to(MID).set_fill(opacity=1),
        ).move_to(3*RIGHT+DOWN/2).scale(2)


        # self.add(CC)
        self.play(Write(CC))
        self.wait()

        self.play(*[Indicate(c) for c in CC[-7:]])
        self.play(*[Write(t) for t in TN[-7:]],run_time=0.5)
        self.wait()

        self.add_foreground_mobjects(TN[-7:])

        for i in range(3):
            self.play(ShowPassingFlash(CC[3+i].copy().set_stroke(width=10).set_color(YELLOW),time_width=.5))
            self.play(
                Write(TN[4*i]),
                Write(TN[4*i+1]),
                Write(TN[4*i+2]),
                Write(TN[4*i+3]),
                run_time=0.5
            )
        self.wait()
        self.remove_foreground_mobjects(TN[-7:])

        self.play(FadeOut(TN),FadeOut(CC),FadeOut(heading))
        self.wait()

class Contract(Scene):
    def construct(self):
        heading = toc[2].copy().move_to(ORIGIN).scale(1.5).to_corner(UP)
        self.play(FadeIn(toc))
        self.wait()
        self.play(FadeOut(toc), ReplacementTransform(toc[2],heading))
        self.wait()

        t=Group(
            Tex("1D:").next_to(UP,LEFT),
            MathTex("\\textsc P").next_to(UP,RIGHT),
            Tex("2D:").next_to(ORIGIN,LEFT),
            MathTex("\\textsc{\#P}\\text{-complete}").next_to(ORIGIN,RIGHT),
            Tex("3D:").next_to(DOWN,LEFT),
            MathTex("\\textsc{\#P}\\text{-complete}").next_to(DOWN,RIGHT),
            Tex("\\vdots~").next_to(2*DOWN+LEFT/3,LEFT),
            MathTex("\\textsc{\#P}\\text{-complete}").next_to(2*DOWN,RIGHT),
        ).move_to(RIGHT/2+DOWN/2)

        t[1].set_color(YELLOW)
        t[3].set_color(RED)
        t[5].set_color(RED)
        t[7].set_color(RED)

        self.play(FadeIn(t[0:2]))
        self.wait()

        self.play(FadeIn(t[2:4]))
        self.wait()

        self.play(FadeIn(t[4:]))
        self.wait()

        self.play(FadeOut(t))
        self.wait()

        a=1.5     # lattice spacing
        r=.75   # MPS square radius
        w=5   # thinner line thickness
        ww=20  # thicker line thickness

        MPS1=Group(
            Line(2*a*LEFT,2*a*RIGHT),
            Line(-2*a*RIGHT,-2*a*RIGHT+UP,stroke_width=w),
            Line(-1*a*RIGHT,-1*a*RIGHT+UP,stroke_width=w),
            Line( 0*a*RIGHT, 0*a*RIGHT+UP,stroke_width=w),
            Line(+1*a*RIGHT,+1*a*RIGHT+UP,stroke_width=w),
            Line(+2*a*RIGHT,+2*a*RIGHT+UP,stroke_width=w),
            Square(r).set_fill("#9999ff",opacity=1).move_to(-2*a*RIGHT),
            Square(r).set_fill("#9999ff",opacity=1).move_to(-1*a*RIGHT),
            Square(r).set_fill("#9999ff",opacity=1).move_to( 0*a*RIGHT),
            Square(r).set_fill("#9999ff",opacity=1).move_to(+1*a*RIGHT),
            Square(r).set_fill("#9999ff",opacity=1).move_to(+2*a*RIGHT),
            Tex("\\textbf{Matrix Product State}").move_to(DOWN)
        ).move_to(DOWN)

        self.play(FadeIn(MPS1[6:-1]))
        self.add_foreground_mobjects(MPS1[6:-1])
        self.play(FadeIn(MPS1[:6]))
        self.wait()

        self.play(FadeIn(MPS1[-1]))
        self.wait()

        bonds=Group(
            Tex("Bonds").move_to(UP).set_color(YELLOW),
            Triangle(color=YELLOW).scale(0.2).set_fill(YELLOW,opacity=1).rotate(60*DEGREES).move_to(-1.5*a*RIGHT-0.5*UP),
            Triangle(color=YELLOW).scale(0.2).set_fill(YELLOW,opacity=1).rotate(60*DEGREES).move_to(-0.5*a*RIGHT-0.5*UP),
            Triangle(color=YELLOW).scale(0.2).set_fill(YELLOW,opacity=1).rotate(60*DEGREES).move_to(+0.5*a*RIGHT-0.5*UP),
            Triangle(color=YELLOW).scale(0.2).set_fill(YELLOW,opacity=1).rotate(60*DEGREES).move_to(+1.5*a*RIGHT-0.5*UP),
        )
        self.play(FadeIn(bonds[0]),FadeIn(bonds[1:],shift=DOWN))
        self.wait()


        self.remove_foreground_mobjects(MPS1[6:-1])

        self.play(FadeOut(MPS1),FadeOut(bonds))
        self.wait()


        vc=Group(
            ImageMobject("VerstraeteCirac.png"),
            Tex(r"\texttt{arXiv:cond-mat/0407066}").scale(0.75)
        )
        vc[0].height=4
        vc.arrange(DOWN).move_to(DOWN)
        self.play(FadeIn(vc))
        self.wait()



        bsv_small=Group(
            ImageMobject("BravyiSucharaVargo_small.png"),
            Tex(r"\texttt{arXiv:1405.4883}\qquad\texttt{doi:10/cv7n}").scale(0.75)
        )
        t1_small=Group(
            ImageMobject("Tucket1_small.png"),
            Tex(r"\texttt{arXiv:1708.08474}\qquad\texttt{doi:10/gc4c4r}").scale(0.75)
        )
        t2_small=Group(
            ImageMobject("Tucket2_small.png"),
            Tex(r"\texttt{arXiv:1812.08186}\qquad\texttt{doi:10/ggz6m2}").scale(0.75)
        )
        bsv_small[0].height=1
        t1_small[0].height=1
        t2_small[0].height=1

        smalls=Group(
            bsv_small.arrange(DOWN,buff=0.1),
            t1_small.arrange(DOWN,buff=0.1),
            t2_small.arrange(DOWN,buff=0.1)
        ).arrange(DOWN,buff=.5).move_to(DOWN/2)

        self.play(FadeOut(vc))
        self.wait()

        self.play(FadeIn(smalls[0]))
        self.wait()

        self.play(FadeIn(smalls[1]))
        self.wait()

        self.play(FadeIn(smalls[2]))
        self.wait()

        self.play(FadeOut(smalls))
        self.wait()



        a=1.5     # lattice spacing
        r=.75   # MPS square radius
        g=0.1   # gap between multi-edges

        # Square(r).set_fill("#9999ff",opacity=1).move_to(+2*a*RIGHT),

        TN_ten=Group(*[
            Group(*[
                Square(r).set_fill("#ff9999",opacity=1).move_to([i*a,j*a,0])
            for j in range(4)])
        for i in range(4)])
        TN_ver=Group(*[Line([0,i*a,0],[3*a,i*a,0]) for i in range(4)])
        TN_hor=Group(*[Line([j*a,0,0],[j*a,3*a,0]) for j in range(4)])

        self.add_foreground_mobjects(TN_ten)

        TN=Group(TN_ten,TN_hor,TN_ver).move_to(DOWN/2)

        self.play(FadeIn(TN[0]))
        self.play(FadeIn(TN[1]),FadeIn(TN[2]))
        self.wait()

        self.play(Indicate(TN_ten[0]))
        self.wait()

        MPS=Group(*[
            Square(r).set_fill("#9999ff",opacity=1).move_to([0,j*a,0])
        for j in range(4)]).move_to(TN_ten[0])
        self.play(ReplacementTransform(TN_ten[0],MPS))
        self.wait()

        # self.play(Circumscribe(MPS))
        # self.wait()
        #
        # self.play(Circumscribe(TN_ten[1:]))
        # self.wait()

        self.play( *[Circumscribe(Group(MPS[j],TN_ten[1][j]),run_time=2) for j in range(4)] )
        # for j in range(4):
        #     self.play(Circumscribe(Group(
        #         MPS[3-j],
        #         TN_ten[1][3-j]
        #     )))
        self.wait()

        self.play(
            MPS[0].animate.set_fill("#ff66ff"),
            MPS[1].animate.set_fill("#ff66ff"),
            MPS[2].animate.set_fill("#ff66ff"),
            MPS[3].animate.set_fill("#ff66ff"),
            FadeOut(TN_ten[1],target_position=MPS),
            TN_hor[1].animate.shift((a-g)*LEFT),
            TN_hor[0].animate.shift(g*LEFT),
        )
        self.wait()

        bondarrows=Group(*[
            Triangle(color=YELLOW).scale(0.2).set_fill(YELLOW,opacity=1).rotate(-30*DEGREES).move_to(i*a*UP)
        for i in range(3)]).move_to(MPS).shift(0.5*RIGHT)

        self.play(FadeIn(bondarrows,shift=LEFT))
        self.wait()

        self.play(FadeOut(bondarrows))
        self.wait()

        self.play(
            MPS[0].animate.set_fill("#9999ff"),
            MPS[1].animate.set_fill("#9999ff"),
            MPS[2].animate.set_fill("#9999ff"),
            MPS[3].animate.set_fill("#9999ff"),
            TN_hor[1].animate.shift(g*LEFT),
            TN_hor[0].animate.shift(g*RIGHT),
        )
        self.remove(TN_hor[1])
        self.wait()


        self.play(
            MPS[0].animate.set_fill("#ff66ff"),
            MPS[1].animate.set_fill("#ff66ff"),
            MPS[2].animate.set_fill("#ff66ff"),
            MPS[3].animate.set_fill("#ff66ff"),
            FadeOut(TN_ten[2],target_position=MPS),
            TN_hor[2].animate.shift((2*a-g)*LEFT),
            TN_hor[0].animate.shift(g*LEFT),
        )
        self.wait()
        self.play(
            MPS[0].animate.set_fill("#9999ff"),
            MPS[1].animate.set_fill("#9999ff"),
            MPS[2].animate.set_fill("#9999ff"),
            MPS[3].animate.set_fill("#9999ff"),
            TN_hor[2].animate.shift(g*LEFT),
            TN_hor[0].animate.shift(g*RIGHT),
        )
        self.remove(TN_hor[2])
        self.wait()

        self.play(
            MPS[0].animate.set_fill("#ff66ff"),
            MPS[1].animate.set_fill("#ff66ff"),
            MPS[2].animate.set_fill("#ff66ff"),
            MPS[3].animate.set_fill("#ff66ff"),
            FadeOut(TN_ten[3],target_position=MPS),
            TN_hor[3].animate.shift((3*a-g)*LEFT),
            TN_hor[0].animate.shift(g*LEFT),
            Uncreate(TN_ver[0]),
            Uncreate(TN_ver[1]),
            Uncreate(TN_ver[2]),
            Uncreate(TN_ver[3]),
        )
        self.wait()
        self.play(
            MPS[0].animate.set_fill("#9999ff"),
            MPS[1].animate.set_fill("#9999ff"),
            MPS[2].animate.set_fill("#9999ff"),
            MPS[3].animate.set_fill("#9999ff"),
            TN_hor[3].animate.shift(g*LEFT),
            TN_hor[0].animate.shift(g*RIGHT),
        )
        self.remove(TN_hor[3])
        self.wait()


        self.play(
            FadeOut(MPS[3],target_position=MPS[2]),
            FadeOut(MPS[0],target_position=MPS[1]),
            TN_hor[0].animate.scale(0.5)
        )
        self.wait()

        res_ten=Square(r).set_fill("#9999ff",opacity=1).move_to(MPS[1]).shift(a*UP/2)

        self.play(
            FadeOut(MPS[1],target_position=res_ten),
            FadeOut(MPS[2],target_position=res_ten),
            FadeIn(res_ten),
            TN_hor[0].animate.scale(0)
        )
        self.remove(TN_hor[0])
        self.wait()

        self.play(res_ten.animate.shift(1.5*a*RIGHT))
        self.wait()

        self.play(FadeOut(res_ten),FadeOut(heading))
        self.wait()

class Sweep(Scene):
    def construct(self):
        heading = toc[3].copy().move_to(ORIGIN).scale(1.5).to_corner(UP)
        self.play(FadeIn(toc))
        self.wait()
        self.play(FadeOut(toc), ReplacementTransform(toc[3],heading))
        self.wait()

        limit1=Tex("What are the limitations of the existing MPS method?").shift(2*UP)
        self.play(Write(limit1))
        self.wait()

        limit2=Tex(r"\textbullet~How do we define `columns'\\~for irregular networks?").scale(.75).set_color(YELLOW)
        limit3=Tex(r"\textbullet~How do we find `columns'\\algorithmically?~\quad\qquad\qquad").scale(0.75).set_color(BLUE)

        limit2.move_to(4*LEFT)
        limit3.move_to(1.5*DOWN).align_to(limit2,LEFT)

        self.play(Write(limit2))
        self.wait()

        # x=[3,1,5,2,0,6,4]
        # y=[0,1,2,3,4,5,6]
        # e=[(0,1),(0,2),(1,3),(1,4),(2,3),(2,5),(3,4),(3,6),(3,5),(4,6),(5,6)]

        # x=[1.3,1.7,1.3,1.7,1.3,1.7,1.3,1.7,1.3,1.7,1.4,1.4,1.5,1.5,1.6,1.6,1.327334057309241,1.3221724303769817,1.5950713440283102,1.4250898835772197,1.4470979756368474,1.5148043249596257,1.6125741957061144,1.3264894857318028,1.3283588384409861]
        # y=[1.3,1.3,1.4,1.4,1.5,1.5,1.6,1.6,1.7,1.7,1.3,1.7,1.3,1.7,1.3,1.7,1.3247479046840802,1.6142097727812774,1.3158523627928371,1.3952350690273065,1.6093049797951562,1.5239301506422678,1.5619755915790123,1.3402473440521137,1.6945637842150307]
        # e=[(1, 3),(1, 18),(1, 14),(10, 23),(10, 19),(10, 12),(10, 16),(6, 8),(6, 17),(8, 24),(8, 11),(8, 17),(7, 22),(7, 9),(7, 15),(2, 23),(2, 4),(2, 19),(19, 21),(19, 23),(13, 22),(13, 15),(13, 20),(11, 13),(11, 24),(11, 20),(11, 17),(17, 24),(17, 20),(15, 22),(20, 22),(20, 21),(9, 15),(18, 21),(18, 19),(16, 23),(21, 22),(5, 22),(5, 7),(5, 21),(3, 18),(3, 21),(3, 5),(4, 17),(4, 6),(4, 21),(4, 20),(4, 19),(12, 18),(12, 14),(12, 19),(14, 18),(0, 2),(0, 16),(0, 10),(0, 23)]

        x=[1.3,1.7,1.3,1.7,1.3,1.7,1.3,1.7,1.3,1.7,1.3,1.7,1.3,1.7,1.3,1.7,1.3,1.7,1.3,1.7,1.3444444444444446,1.3444444444444446,1.3888888888888888,1.3888888888888888,1.4333333333333333,1.4333333333333333,1.4777777777777779,1.4777777777777779,1.5222222222222221,1.5222222222222221,1.5666666666666667,1.5666666666666667,1.6111111111111112,1.6111111111111112,1.6555555555555554,1.6555555555555554,1.3146813455822222,1.6912318334888399,1.5850679390100162,1.6319041184368146,1.5632087030796582,1.3416744470853277,1.305245260397479,1.3811807139547028,1.569732522555214,1.5785703957531692,1.6133768961582222,1.370792387719675,1.530272418142219,1.3056797657862247,1.4041724456267217,1.3806761576857094,1.3521130704205586,1.6875568789065925,1.5407077986943307,1.4664156431599455,1.312469896388232,1.333653349987466,1.4765216656769649,1.3141972728230162,1.6109951956925297,1.3058567568855493,1.450966636453833,1.5969861759376947,1.4607555525784381,1.4247069038002123,1.4381532553562153,1.3287438309458095,1.5106084295516307,1.4433715587469933,1.6259024727635076,1.5473531511714207,1.6501312873591296,1.6246685939241396,1.6434257877961684,1.4955602831683201,1.4635552909349492,1.4499980598752185,1.3702106338933064,1.683032389939865,1.5080595538334756,1.4354133855200084,1.5709643711990129,1.5574387438211326,1.3535311121777251,1.3792891538734415,1.358499083532044,1.5943229148270064,1.653097921417943,1.4651973129733942,1.5702280107423296,1.535439447882288,1.4868458849361934,1.4395202229401662,1.672350891060311,1.6895922250618451,1.3158083310050592,1.3629271216283554,1.49377095517567,1.3855970089329892]
        y=[1.3,1.3,1.3444444444444446,1.3444444444444446,1.3888888888888888,1.3888888888888888,1.4333333333333333,1.4333333333333333,1.4777777777777779,1.4777777777777779,1.5222222222222221,1.5222222222222221,1.5666666666666667,1.5666666666666667,1.6111111111111112,1.6111111111111112,1.6555555555555554,1.6555555555555554,1.7,1.7,1.3,1.7,1.3,1.7,1.3,1.7,1.3,1.7,1.3,1.7,1.3,1.7,1.3,1.7,1.3,1.7,1.5113452063287771,1.4511336497881024,1.4057566700292579,1.4477286572000834,1.5978347288919257,1.5234947157417724,1.5670646552922136,1.3598802812388457,1.492522325435982,1.627550821948484,1.362535735717852,1.4792866329042915,1.3556228022353756,1.3720582944547748,1.4669270404028365,1.433934769345092,1.5531813433020358,1.651996056147321,1.6820481405154526,1.4547148843312103,1.472789354825991,1.4618178025321447,1.4545264059178775,1.3404986235678609,1.348067427930161,1.5711414081903796,1.3335821603949216,1.662273584837917,1.4713300385008048,1.3897202061426563,1.3271343085213245,1.5710479693322343,1.5351186633914506,1.64427984499828,1.3082307046745767,1.338714238384548,1.309310794439587,1.367351013475362,1.5844767556471793,1.6276639188355855,1.4027458341739096,1.3204534059287927,1.6282588726180156,1.5948070390587552,1.3179928368288134,1.6597584769377647,1.4494037784652756,1.6134630080742174,1.6946445695269203,1.392562409917996,1.4457265765701024,1.4959687909385995,1.6549067684382384,1.3784802486485463,1.573721113430063,1.3094752535248082,1.5959336238216797,1.5020366704935635,1.6839143728565418,1.4570994392495145,1.5160991563849382,1.4281432635629987,1.4412238481653536,1.6504295417711745]
        e=[(1, 3),(1, 34),(1, 72),(88, 94),(10, 42),(10, 36),(10, 12),(10, 96),(28, 30),(28, 91),(28, 80),(56, 57),(30, 91),(30, 71),(30, 60),(30, 32),(69, 99),(69, 92),(69, 75),(69, 78),(69, 81),(32, 70),(32, 34),(32, 60),(25, 27),(25, 81),(48, 76),(48, 80),(48, 71),(48, 98),(48, 89),(83, 92),(3, 73),(3, 5),(3, 72),(92, 93),(53, 79),(53, 88),(53, 94),(49, 59),(49, 85),(76, 98),(76, 89),(79, 88),(39, 87),(39, 82),(39, 73),(39, 95),(33, 88),(33, 35),(33, 63),(78, 99),(78, 92),(78, 84),(70, 72),(75, 92),(75, 83),(11, 74),(11, 13),(11, 39),(11, 87),(15, 53),(15, 79),(15, 17),(61, 67),(20, 22),(20, 59),(20, 43),(9, 39),(9, 95),(9, 11),(9, 37),(87, 90),(71, 91),(71, 80),(27, 69),(27, 75),(27, 81),(27, 29),(4, 6),(4, 49),(4, 97),(4, 85),(62, 77),(62, 65),(62, 80),(62, 66),(62, 89),(14, 67),(14, 16),(14, 61),(14, 78),(40, 83),(40, 68),(40, 92),(40, 90),(40, 45),(67, 96),(67, 78),(38, 46),(38, 82),(38, 39),(38, 73),(38, 98),(38, 71),(38, 48),(45, 74),(45, 54),(45, 88),(45, 63),(45, 83),(45, 90),(84, 99),(24, 77),(24, 66),(24, 26),(54, 63),(54, 75),(54, 83),(65, 76),(65, 85),(65, 66),(65, 89),(41, 67),(41, 52),(41, 57),(41, 47),(41, 96),(57, 86),(58, 68),(58, 98),(58, 64),(7, 9),(7, 39),(7, 37),(19, 35),(19, 94),(13, 74),(13, 79),(13, 15),(51, 65),(51, 97),(51, 85),(51, 86),(17, 53),(17, 94),(17, 19),(68, 98),(68, 92),(68, 93),(68, 90),(34, 70),(34, 72),(82, 98),(82, 87),(16, 18),(16, 78),(16, 21),(16, 84),(63, 88),(64, 68),(64, 93),(43, 59),(43, 49),(43, 65),(43, 85),(43, 66),(36, 41),(36, 57),(36, 96),(36, 56),(44, 82),(44, 68),(44, 98),(44, 87),(44, 90),(12, 42),(12, 61),(12, 14),(85, 97),(66, 77),(0, 59),(0, 2),(0, 20),(29, 54),(29, 31),(29, 75),(46, 71),(46, 60),(46, 73),(31, 54),(31, 33),(31, 63),(81, 99),(6, 8),(6, 97),(6, 57),(6, 86),(6, 56),(42, 67),(42, 61),(42, 96),(74, 90),(74, 79),(74, 88),(74, 87),(8, 36),(8, 10),(8, 56),(86, 97),(2, 59),(2, 49),(2, 4),(60, 70),(60, 71),(60, 73),(60, 72),(37, 39),(37, 95),(47, 52),(47, 57),(47, 86),(47, 93),(47, 50),(47, 51),(35, 88),(35, 94),(80, 91),(80, 89),(18, 21),(50, 65),(50, 64),(50, 93),(50, 55),(50, 51),(21, 84),(21, 23),(5, 39),(5, 73),(5, 7),(23, 25),(23, 99),(23, 81),(23, 84),(72, 73),(52, 67),(52, 92),(52, 93),(52, 78),(22, 24),(22, 66),(22, 43),(26, 62),(26, 77),(26, 80),(26, 28),(55, 76),(55, 65),(55, 98),(55, 64),(55, 58)]
        randnet=VGroup(
            *[Line([x[ee[0]],y[ee[0]],0],[x[ee[1]],y[ee[1]],0]) for ee in e],
            # *[Circle(0.005,color=WHITE).set_fill("#9999ff",opacity=1).move_to([x[i],y[i],0]) for i in range(len(x))]
        ).set_color(RED)
        randnet.height=4
        randnet.move_to(3*RIGHT+DOWN)

        # self.play(Write(randnet))
        self.play(*[Write(r) for r in randnet])
        self.wait()

        # self.play(Unwrite(randnet))
        self.play(*[Unwrite(r) for r in randnet])
        self.wait()


        self.play(Write(limit3))
        self.wait()

        squashed=Group(
            ImageMobject("Tucket2_small.png"),
            Tex(r"\texttt{arXiv:1812.08186}\qquad\texttt{doi:10/ggz6m2}").scale(0.5),
            ImageMobject("SquashedColour.png")
        )
        squashed[0].width=6
        squashed[2].width=6
        squashed[1].next_to(squashed[0],DOWN,buff=0.1)
        squashed[2].next_to(squashed[1],DOWN)
        squashed.move_to(3*RIGHT+DOWN)

        self.play(FadeIn(squashed))
        self.wait()

        self.play(FadeOut(squashed))
        self.wait()

        self.play(
            limit2.animate.shift(4*RIGHT),
            limit3.animate.shift(4*RIGHT)
        )
        self.wait()

        self.play(Circumscribe(Group(limit2,limit3),color=WHITE))
        self.wait()

        self.play(FadeOut(limit2),FadeOut(limit3))
        self.play(FadeOut(limit1))
        self.wait()

        self.play(Circumscribe(heading[1]))

        x=[3,1,5,2,0,6,4]
        y=[0,1,2,3,4,5,6]
        e=[(0,1),(0,2),(1,3),(1,4),(2,3),(2,5),(3,4),(3,5),(3,6),(4,6),(5,6)]

        sweep_example=Group(
            DashedLine([-8,-3.5,0],[-8,3.5,0], dash_length=0.25).shift(RIGHT),
            Rectangle(height=7, width=14 ,color=WHITE),
            *[Circle(0.25,color=WHITE).set_fill(GREEN,opacity=1).move_to([1.5*(y[i]-3),.9*(x[i]-3),0]) for i in range(7)]
        ).scale(0.75).move_to(DOWN/2)

        self.play(FadeIn(sweep_example[2:]))
        self.wait()
        self.add_foreground_mobjects(sweep_example[2:])

        self.play(FadeIn(sweep_example[0].shift(RIGHT/2),shift=RIGHT/2))
        self.wait()

        self.play(sweep_example[0].animate.shift(1.375*RIGHT))
        self.wait()

        # self.play(Flash(sweep_example[2],line_length=0.5,color=GREEN))
        # self.play(FadeOut(sweep_example[2]))
        self.play(
            Flash(sweep_example[2],line_length=0.25,color=GREEN),
            FadeOut(sweep_example[2])
        )
        self.wait()

        for i in range(3,9):
            self.play(sweep_example[0].animate.shift(1.125*RIGHT))
            self.play(
                Flash(sweep_example[i],line_length=0.25,color=GREEN),
                FadeOut(sweep_example[i])
            )
        self.play(sweep_example[0].animate.shift(1.125*RIGHT))
        self.play(FadeOut(sweep_example[0],shift=RIGHT/2))
        self.wait()

        self.remove(sweep_example[0])

        sweep_l=DashedLine([-7*.75,-3.5*.75-.5,0],[-7*.75,3.5*.75-.5,0], dash_length=0.25*.75)
        sweep_t=Group(*[
            Circle(0.25,color=WHITE).set_fill("#ff9999",opacity=1).move_to([.75*1.5*(y[i]-3),.75*.9*(x[i]-3)-.5,0])
        for i in range(7)])
        sweep_e=Group(*[
            Line([.75*1.5*(y[ee[0]]-3),.75*(x[ee[0]]-3)-.5,0],[.75*1.5*(y[ee[1]]-3),.75*.9*(x[ee[1]]-3)-.5,0])
        for ee in e])


        self.play(FadeIn(sweep_t))
        self.add_foreground_mobjects(sweep_t)
        self.play(FadeIn(sweep_e))
        self.wait()

        self.play(FadeIn(sweep_l.shift(RIGHT/2),shift=RIGHT/2))
        self.wait()

        self.play(sweep_l.animate.shift(1.375*RIGHT))
        self.wait()

        new_ten=Circle(0.25,color=WHITE).set_fill("#ff66ff",opacity=1).move_to([-4.5,-0.5,0])

        self.play(
            ReplacementTransform(sweep_t[0],new_ten),
            Transform(sweep_e[0],Line(new_ten.get_center(),sweep_e[0].end)),
            Transform(sweep_e[1],Line(new_ten.get_center(),sweep_e[1].end)),
        )
        self.wait()
        mps=VGroup(
            Line([-4.5,-0.5-.25,0],[-4.5,-0.5+.25,0]),
            Square(0.75*.75,color=WHITE).set_fill("#9999ff",opacity=1).move_to([-4.5,-0.5-.5,0]),
            Square(0.75*.75,color=WHITE).set_fill("#9999ff",opacity=1).move_to([-4.5,-0.5+.5,0]),
        )
        self.play(
            ReplacementTransform(new_ten,mps),
            Transform(sweep_e[0],Line(mps[1].get_right(),sweep_e[0].end)),
            Transform(sweep_e[1],Line(mps[2].get_right(),sweep_e[1].end)),
        )
        self.wait()


        self.play(sweep_l.animate.shift(1.125*RIGHT))
        self.wait()
        self.play(
            Uncreate(sweep_e[0]),
            Transform(mps[1],Circle(0.25,color=WHITE).set_fill("#ff66ff",opacity=1).move_to(mps[1])),
            FadeOut(sweep_t[1],target_position=mps[1]),
            Transform(sweep_e[2],Line([-4.5,-0.5-.5,0],sweep_e[2].end)),
            Transform(sweep_e[3],Line([-4.5,-0.5-.5,0],sweep_e[3].end)),
        )
        self.wait()
        oldmps=mps
        mps=VGroup(
            Line([-4.5,-0.5-1,0],[-4.5,-0.5+1,0]),
            Square(0.75*.75,color=WHITE).set_fill("#9999ff",opacity=1).move_to([-4.5,-0.5-1,0]),
            Square(0.75*.75,color=WHITE).set_fill("#9999ff",opacity=1).move_to([-4.5,-0.5  ,0]),
            Square(0.75*.75,color=WHITE).set_fill("#9999ff",opacity=1).move_to([-4.5,-0.5+1,0]),
        )
        self.play(
            ReplacementTransform(oldmps[0],mps[0]),
            ReplacementTransform(oldmps[1],mps[1:3]),
            ReplacementTransform(oldmps[2],mps[3]),
            Transform(sweep_e[1],Line(mps[3].get_right(),sweep_e[1].end)),
            Transform(sweep_e[2],Line(mps[2].get_right(),sweep_e[2].end)),
            Transform(sweep_e[3],Line(mps[1].get_right(),sweep_e[3].end)),
        )
        self.wait()


        self.play(sweep_l.animate.shift(1.125*RIGHT))
        self.wait()
        self.play(
            Uncreate(sweep_e[1]),
            Transform(mps[3],Circle(0.25,color=WHITE).set_fill("#ff66ff",opacity=1).move_to(mps[3])),
            FadeOut(sweep_t[2],target_position=mps[3]),
            Transform(sweep_e[4],Line(mps[3].get_center(),sweep_e[4].end)),
            Transform(sweep_e[5],Line(mps[3].get_center(),sweep_e[5].end)),
        )
        self.wait()
        oldmps=mps
        mps=VGroup(
            Line([-4.5,-0.5-1.5,0],[-4.5,-0.5+1.5,0]),
            Square(0.75*.75,color=WHITE).set_fill("#9999ff",opacity=1).move_to([-4.5,-0.5-1.5,0]),
            Square(0.75*.75,color=WHITE).set_fill("#9999ff",opacity=1).move_to([-4.5,-0.5-0.5,0]),
            Square(0.75*.75,color=WHITE).set_fill("#9999ff",opacity=1).move_to([-4.5,-0.5+0.5,0]),
            Square(0.75*.75,color=WHITE).set_fill("#9999ff",opacity=1).move_to([-4.5,-0.5+1.5,0]),
        )
        self.play(
            ReplacementTransform(oldmps[0],mps[0]),
            ReplacementTransform(oldmps[1],mps[1]),
            ReplacementTransform(oldmps[2],mps[2]),
            ReplacementTransform(oldmps[3],mps[3:5]),
            Transform(sweep_e[5],Line(mps[4].get_right(),sweep_e[5].end)),
            Transform(sweep_e[4],Line(mps[3].get_right(),sweep_e[4].end)),
            Transform(sweep_e[2],Line(mps[2].get_right(),sweep_e[2].end)),
            Transform(sweep_e[3],Line(mps[1].get_right(),sweep_e[3].end)),
        )
        self.wait()

        self.play(sweep_l.animate.shift(1.125*RIGHT))
        self.wait()
        self.play(
            Uncreate(sweep_e[4]),
            Uncreate(sweep_e[2]),
            Transform(mps[2:4],Circle(0.25,color=WHITE).set_fill("#ff66ff",opacity=1).move_to(mps[3]).shift(0.5*DOWN)),
            FadeOut(sweep_t[3],target_position=mps[3]),
            Transform(sweep_e[6],Line(mps[3].get_center()+0.5*DOWN,sweep_e[6].end)),
            Transform(sweep_e[7],Line(mps[3].get_center()+0.5*DOWN,sweep_e[7].end)),
            Transform(sweep_e[8],Line(mps[3].get_center()+0.5*DOWN,sweep_e[8].end)),
        )
        self.wait()
        oldmps=mps
        mps=VGroup(
            Line([-4.5,-0.5-2,0],[-4.5,-0.5+2,0]),
            Square(0.75*.75,color=WHITE).set_fill("#9999ff",opacity=1).move_to([-4.5,-0.5-2,0]),
            Square(0.75*.75,color=WHITE).set_fill("#9999ff",opacity=1).move_to([-4.5,-0.5-1,0]),
            Square(0.75*.75,color=WHITE).set_fill("#9999ff",opacity=1).move_to([-4.5,-0.5  ,0]),
            Square(0.75*.75,color=WHITE).set_fill("#9999ff",opacity=1).move_to([-4.5,-0.5+1,0]),
            Square(0.75*.75,color=WHITE).set_fill("#9999ff",opacity=1).move_to([-4.5,-0.5+2,0]),
        )
        self.play(
            ReplacementTransform(oldmps[0],mps[0]),
            ReplacementTransform(oldmps[1],mps[1]),
            ReplacementTransform(oldmps[2],mps[2:5]),
            ReplacementTransform(oldmps[4],mps[5]),
            Transform(sweep_e[5],Line(mps[5].get_right(),sweep_e[5].end)),
            Transform(sweep_e[7],Line(mps[4].get_right(),sweep_e[7].end)),
            Transform(sweep_e[8],Line(mps[3].get_right(),sweep_e[8].end)),
            Transform(sweep_e[6],Line(mps[2].get_right(),sweep_e[6].end)),
            Transform(sweep_e[3],Line(mps[1].get_right(),sweep_e[3].end)),
        )
        self.wait()

        self.play(sweep_l.animate.shift(1.125*RIGHT))
        self.wait()
        self.play(
            Uncreate(sweep_e[3]),
            Uncreate(sweep_e[6]),
            Transform(mps[1:3],Circle(0.25,color=WHITE).set_fill("#ff66ff",opacity=1).move_to(mps[1])),
            FadeOut(sweep_t[4],target_position=mps[1]),
            Transform(sweep_e[9],Line(mps[1].get_center(),sweep_e[9].end)),
        )
        self.wait()
        oldmps=mps
        mps=VGroup(
            Line([-4.5,-0.5-1.5,0],[-4.5,-0.5+1.5,0]),
            Square(0.75*.75,color=WHITE).set_fill("#9999ff",opacity=1).move_to([-4.5,-0.5-1.5,0]),
            Square(0.75*.75,color=WHITE).set_fill("#9999ff",opacity=1).move_to([-4.5,-0.5-0.5,0]),
            Square(0.75*.75,color=WHITE).set_fill("#9999ff",opacity=1).move_to([-4.5,-0.5+0.5,0]),
            Square(0.75*.75,color=WHITE).set_fill("#9999ff",opacity=1).move_to([-4.5,-0.5+1.5,0]),
        )
        self.play(
            ReplacementTransform(oldmps,mps),
            Transform(sweep_e[5],Line(mps[4].get_right(),sweep_e[5].end)),
            Transform(sweep_e[7],Line(mps[3].get_right(),sweep_e[7].end)),
            Transform(sweep_e[8],Line(mps[2].get_right(),sweep_e[8].end)),
            Transform(sweep_e[9],Line(mps[1].get_right(),sweep_e[9].end)),
        )
        self.wait()


        self.play(sweep_l.animate.shift(1.125*RIGHT))
        self.wait()
        self.play(
            Uncreate(sweep_e[5]),
            Uncreate(sweep_e[7]),
            Transform(mps[3:5],Circle(0.25,color=WHITE).set_fill("#ff66ff",opacity=1).move_to(mps[4])),
            FadeOut(sweep_t[5],target_position=mps[4]),
            Transform(sweep_e[10],Line(mps[4].get_center(),sweep_e[10].end)),
        )
        self.wait()
        oldmps=mps
        mps=VGroup(
            Line([-4.5,-0.5-1,0],[-4.5,-0.5+1,0]),
            Square(0.75*.75,color=WHITE).set_fill("#9999ff",opacity=1).move_to([-4.5,-0.5-1,0]),
            Square(0.75*.75,color=WHITE).set_fill("#9999ff",opacity=1).move_to([-4.5,-0.5  ,0]),
            Square(0.75*.75,color=WHITE).set_fill("#9999ff",opacity=1).move_to([-4.5,-0.5+1,0]),
        )
        self.play(
            ReplacementTransform(oldmps[0],mps[0]),
            ReplacementTransform(oldmps[1],mps[1]),
            ReplacementTransform(oldmps[2],mps[2]),
            ReplacementTransform(oldmps[3],mps[3]),
            Transform(sweep_e[10],Line(mps[3].get_right(),sweep_e[10].end)),
            Transform(sweep_e[8],Line(mps[2].get_right(),sweep_e[8].end)),
            Transform(sweep_e[9],Line(mps[1].get_right(),sweep_e[9].end)),
        )
        self.wait()


        self.play(sweep_l.animate.shift(1.125*RIGHT))
        self.wait()
        self.play(
            Uncreate(sweep_e[10]),
            Uncreate(sweep_e[8]),
            Uncreate(sweep_e[9]),
            Transform(mps,Circle(0.25,color=WHITE).set_fill("#ff66ff",opacity=1).move_to(mps[2])),
            FadeOut(sweep_t[6],target_position=mps[1]),
        )
        self.wait()

        self.play(FadeOut(sweep_l,shift=0.5*RIGHT),mps.animate.move_to(DOWN/2))
        self.wait()
        self.remove(sweep_l)

        self.play(
            FadeOut(mps),
            FadeOut(heading)
        )
        self.wait()

class Codes(Scene):
    def construct(self):
        heading = toc[4].copy().move_to(ORIGIN).scale(1.5).to_corner(UP)
        self.play(FadeIn(toc))
        self.wait()
        self.play(FadeOut(toc), ReplacementTransform(toc[4],heading))
        self.wait()

        subheading = Tex("Noise models").next_to(heading,DOWN,buff=.5)
        self.play(FadeIn(subheading))
        self.wait()

        noise=Group(
            Tex(
                "Bit-flip:",
                "Phase-flip:",
                "Depolarising:",
                "BB84:"
            ).arrange(DOWN, aligned_edge=LEFT),
            MathTex(
                r"\mathcal{E}(\rho)=(1-p)\rho+pX\rho X",
                r"\mathcal{E}(\rho)=(1-p)\rho+pZ\rho Z",
                r"\mathcal{E}(\rho)=(1-p)\rho+\frac p3\left(X\rho X+Y\rho Y+Z\rho Z\right)",
                r"\mathcal{E}(\rho)=(1-p_X)(1-p_Z)\rho+p_X(1-p_Z)X\rho X",
                r"\qquad+p_Xp_ZY\rho Y+(1-p_X)p_ZZ\rho Z",
            ).arrange(DOWN, aligned_edge=LEFT).shift(RIGHT)
        ).scale(.75).arrange(RIGHT, aligned_edge=UP, buff=1).shift(DOWN/2)
        for i in range(4):
            noise[0][i].set_y(noise[1][i].get_y())
        for j in range(2):
            noise[j][0].set_color(BLUE)
            noise[j][1].set_color(RED)
            noise[j][2].set_color(YELLOW)
            noise[j][3].set_color(PURPLE)
        noise[1][4].set_color(PURPLE).shift(1.2*RIGHT)

        for i in range(3):
            self.play(Write(noise[0][i]),Write(noise[1][i]))
            self.wait()
        self.play(Write(noise[0][3]),Write(noise[1][3]),Write(noise[1][4]))
        self.wait()

        self.play(*[Unwrite(nn) for n in noise for nn in n])
        self.wait()

        # self.play(FadeOut(subheading))
        # subheading = Tex("Surface codes").move_to(subheading)
        # self.play(FadeIn(subheading))
        self.play(Transform(subheading,Tex("Surface codes").move_to(subheading)))
        self.wait()

        # surface code
        x=[1.4463898881324913,1.5638248714655472,1.3282490658725337,1.6195938767241282,1.4384854990362534,1.6530292463265768,1.5689437514564988,1.3092014468249147,1.451743425192652,1.5695784244721736,1.5893504750784146,1.3305522503256937,1.4863363854134686,1.6812389964767795,1.6251686283838207,1.3663443039677718,1.4908005598039804,1.5936955066348426,1.6649642077932725,1.5976401781668608,1.5193155976903812,1.4105174643974265,1.6245291057789888,1.6305394543332483,1.3115046312780745,1.5130484974976968,1.6369873630523755,1.6250524015856795,1.311798368897606,1.6812389964767795,1.48816285217529,1.4026130753011887,1.4499169584308305,1.6144107124246478,1.4273422690848723,1.6446816643027724,1.3025969220726912,1.3577979960890818,1.5615143873372725,1.6130297412068602,1.54822032129628,1.5489928995033235,1.6077585715212017,1.3601011805422416,1.6052224214393822,1.6112052197612305,1.5108976614080856,1.3955994965647884,1.6690174194856848,1.3092014468249147,1.4807068124090854,1.3686474884209316,1.3141015533507658,1.6840118268408917,1.5078479984112096,1.6621913774291606,]
        y=[1.590031792569832,1.5537040239353477,1.3991593401166302,1.5230886837567406,1.621862689078226,1.4215718465996972,1.389856542285033,1.4199926734499637,1.4029888528980947,1.5885853784024924,1.454560643110242,1.6177656700585024,1.46264435045457,1.5878340757433724,1.4813707674918755,1.3991593401166302,1.5066589695476524,1.596948593740829,1.384486391307344,1.3936589523863454,1.4831074764226646,1.4823663307980937,1.3835040013153026,1.605979297926983,1.596932336725169,1.5472364225364021,1.389187982521334,1.405440104480354,1.4897613165551824,1.5461674090767057,1.430939796598046,1.4308638939731544,1.4346934067546186,1.3788024101013125,1.590031792569832,1.541637447300591,1.5281019764385524,1.499597086713455,1.4662594648511735,1.5806160028175347,1.4178074859849847,1.6139486735119404,1.398360543600336,1.5515367499886608,1.410810255458043,1.622311888850277,1.6139486735119404,1.5859347735501084,1.4537521219590197,1.4616593401166302,1.5821177770035464,1.6177656700585024,1.5625343131637213,1.4053197246406774,1.4029509436999517,1.6086674090767057,]
        e=[(1, 25),(2, 15),(2, 7),(3, 35),(3, 1),(4, 0),(5, 27),(5, 48),(6, 40),(7, 49),(9, 17),(9, 1),(11, 51),(11, 24),(12, 32),(12, 20),(13, 55),(14, 10),(14, 3),(15, 31),(16, 20),(16, 25),(17, 39),(18, 26),(19, 33),(19, 42),(19, 6),(21, 31),(21, 16),(21, 37),(22, 33),(22, 42),(23, 39),(24, 52),(26, 22),(27, 26),(27, 44),(28, 49),(29, 35),(29, 13),(30, 8),(30, 12),(32, 31),(32, 8),(34, 4),(34, 0),(34, 47),(36, 28),(36, 52),(37, 28),(37, 43),(38, 20),(38, 10),(38, 40),(39, 35),(41, 46),(41, 9),(44, 10),(44, 42),(45, 23),(45, 17),(46, 50),(47, 51),(47, 43),(48, 14),(50, 0),(50, 25),(52, 43),(53, 5),(53, 18),(54, 30),(54, 40),(55, 23),]
        lattice=VGroup(
            *[Line([x[ee[0]],y[ee[0]],0],[x[ee[1]],y[ee[1]],0]) for ee in e],
        ).set_color(WHITE).move_to(DOWN).set_height(4)#.stretch_to_fit_height(4)#.stretch_to_fit_width(4)
        self.play(*[Write(l) for l in lattice])
        self.wait()
        face=[47,48,49,50,67]
        facelabs=Group(
            MathTex("Z").scale(0.75).move_to(lattice[47]).shift(0.25*LEFT),
            MathTex("Z").scale(0.75).move_to(lattice[48]).shift(0.23*LEFT),
            MathTex("Z").scale(0.75).move_to(lattice[49]).shift([.08,-.28,0]),
            MathTex("Z").scale(0.75).move_to(lattice[50]).shift([0.25,0,0]),
            MathTex("Z").scale(0.75).move_to(lattice[67]).shift([0.1,0.3,0]),
        ).set_color(BLUE)
        vert=[0,21,66]
        vertlabs=Group(
            MathTex("X").scale(0.75).move_to(lattice[0]).shift([-.05,0.25,0]),
            MathTex("X").scale(0.75).move_to(lattice[21]).shift([0.2,-0.1,0]),
            MathTex("X").scale(0.75).move_to(lattice[66]).shift([-.2,-.2,0]),
        ).set_color(RED)

        self.play(
            # *[FadeIn(lattice[f].copy().set_stroke(width=10).set_color(BLUE)) for f in face],
            *[lattice[f].animate.set_stroke(width=10).set_color(BLUE) for f in face],
            *[FadeIn(f) for f in facelabs]
        )
        self.wait()

        self.play(
            *[lattice[v].animate.set_stroke(width=10).set_color(RED) for v in vert],
            *[FadeIn(v) for v in vertlabs]
        )
        self.wait()

        self.play(*[Unwrite(l) for l in lattice],FadeOut(facelabs),FadeOut(vertlabs))
        self.wait()

        # Square
        x=[1.0,1.0,1.0,1.0,1.0,1.0,1.0,2.0,2.0,2.0,2.0,2.0,2.0,2.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,4.0,4.0,4.0,4.0,4.0,4.0,4.0,5.0,5.0,5.0,5.0,5.0,5.0,5.0,6.0,6.0,6.0,6.0,6.0,6.0,6.0,7.0,7.0,7.0,7.0,7.0,7.0,7.0,8.0,8.0,8.0,8.0,8.0,8.0,8.0,]
        y=[1.0,2.0,3.0,4.0,5.0,6.0,7.0,1.0,2.0,3.0,4.0,5.0,6.0,7.0,1.0,2.0,3.0,4.0,5.0,6.0,7.0,1.0,2.0,3.0,4.0,5.0,6.0,7.0,1.0,2.0,3.0,4.0,5.0,6.0,7.0,1.0,2.0,3.0,4.0,5.0,6.0,7.0,1.0,2.0,3.0,4.0,5.0,6.0,7.0,1.0,2.0,3.0,4.0,5.0,6.0,7.0,]
        e=[(0, 7),(1, 8),(2, 9),(3, 10),(4, 11),(5, 12),(6, 13),(7, 8),(7, 14),(7, 0),(8, 9),(8, 1),(8, 15),(8, 7),(9, 8),(9, 2),(9, 16),(9, 10),(10, 3),(10, 9),(10, 11),(10, 17),(11, 12),(11, 18),(11, 10),(11, 4),(12, 11),(12, 13),(12, 5),(12, 19),(13, 6),(13, 12),(13, 20),(14, 15),(14, 7),(14, 21),(15, 22),(15, 8),(15, 16),(15, 14),(16, 17),(16, 9),(16, 15),(16, 23),(17, 24),(17, 18),(17, 16),(17, 10),(18, 25),(18, 19),(18, 11),(18, 17),(19, 12),(19, 26),(19, 18),(19, 20),(20, 13),(20, 27),(20, 19),(21, 22),(21, 28),(21, 14),(22, 23),(22, 15),(22, 21),(22, 29),(23, 22),(23, 30),(23, 24),(23, 16),(24, 23),(24, 25),(24, 31),(24, 17),(25, 24),(25, 26),(25, 18),(25, 32),(26, 25),(26, 33),(26, 27),(26, 19),(27, 34),(27, 26),(27, 20),(28, 35),(28, 21),(28, 29),(29, 22),(29, 36),(29, 30),(29, 28),(30, 29),(30, 31),(30, 37),(30, 23),(31, 24),(31, 30),(31, 38),(31, 32),(32, 25),(32, 31),(32, 33),(32, 39),(33, 34),(33, 26),(33, 40),(33, 32),(34, 41),(34, 33),(34, 27),(35, 42),(35, 36),(35, 28),(36, 35),(36, 37),(36, 43),(36, 29),(37, 36),(37, 30),(37, 38),(37, 44),(38, 31),(38, 39),(38, 37),(38, 45),(39, 46),(39, 38),(39, 32),(39, 40),(40, 33),(40, 41),(40, 39),(40, 47),(41, 34),(41, 48),(41, 40),(42, 49),(42, 35),(42, 43),(43, 42),(43, 36),(43, 50),(43, 44),(44, 45),(44, 37),(44, 51),(44, 43),(45, 46),(45, 52),(45, 38),(45, 44),(46, 53),(46, 39),(46, 47),(46, 45),(47, 46),(47, 54),(47, 48),(47, 40),(48, 41),(48, 47),(48, 55),(49, 42),(50, 43),(51, 44),(52, 45),(53, 46),(54, 47),(55, 48),]
        lattice=VGroup(
            *[Line([x[ee[0]],y[ee[0]],0],[x[ee[1]],y[ee[1]],0]) for ee in e],
            # *[Circle(0.005,color=WHITE).set_fill("#9999ff",opacity=1).move_to([x[i],y[i],0]) for i in range(len(x))]
        ).set_color(YELLOW).move_to(DOWN).stretch_to_fit_height(4).stretch_to_fit_width(4)
        lattice_text=Tex("Square").next_to(lattice,UP).set_color(YELLOW)
        self.play(FadeIn(lattice_text),*[Write(l) for l in lattice])
        self.wait()
        self.play(FadeOut(lattice_text),*[Unwrite(l) for l in lattice])
        self.wait()

        if True:
            # Triangular
            x=[1.0,1.0,1.0,1.0,2.0,2.0,2.0,2.0,3.0,3.0,3.0,3.0,4.0,4.0,4.0,4.0,5.0,5.0,5.0,5.0,6.0,6.0,6.0,6.0,7.0,7.0,7.0,7.0,8.0,8.0,8.0,8.0,]
            y=[1.0,2.0,3.0,4.0,1.0,2.0,3.0,4.0,1.0,2.0,3.0,4.0,1.0,2.0,3.0,4.0,1.0,2.0,3.0,4.0,1.0,2.0,3.0,4.0,1.0,2.0,3.0,4.0,1.0,2.0,3.0,4.0,]
            e=[(0, 4),(1, 4),(1, 5),(2, 6),(2, 5),(3, 6),(3, 7),(4, 8),(4, 1),(4, 5),(4, 0),(5, 6),(5, 8),(5, 9),(5, 1),(5, 2),(5, 4),(6, 3),(6, 9),(6, 2),(6, 10),(6, 7),(6, 5),(7, 6),(7, 3),(7, 10),(7, 11),(8, 12),(8, 9),(8, 4),(8, 5),(9, 6),(9, 8),(9, 13),(9, 12),(9, 10),(9, 5),(10, 6),(10, 13),(10, 9),(10, 7),(10, 14),(10, 11),(11, 15),(11, 10),(11, 7),(11, 14),(12, 8),(12, 13),(12, 9),(12, 16),(13, 12),(13, 9),(13, 16),(13, 10),(13, 14),(13, 17),(14, 13),(14, 18),(14, 15),(14, 10),(14, 11),(14, 17),(15, 18),(15, 14),(15, 11),(15, 19),(16, 12),(16, 13),(16, 20),(16, 17),(17, 13),(17, 18),(17, 16),(17, 21),(17, 14),(17, 20),(18, 22),(18, 19),(18, 15),(18, 14),(18, 21),(18, 17),(19, 22),(19, 15),(19, 18),(19, 23),(20, 24),(20, 16),(20, 21),(20, 17),(21, 25),(21, 22),(21, 24),(21, 18),(21, 20),(21, 17),(22, 19),(22, 25),(22, 26),(22, 18),(22, 21),(22, 23),(23, 22),(23, 26),(23, 27),(23, 19),(24, 25),(24, 28),(24, 20),(24, 21),(25, 22),(25, 24),(25, 28),(25, 26),(25, 21),(25, 29),(26, 22),(26, 25),(26, 30),(26, 29),(26, 27),(26, 23),(27, 30),(27, 31),(27, 26),(27, 23),(28, 25),(28, 24),(29, 25),(29, 26),(30, 26),(30, 27),(31, 27),]
            primal=VGroup(
                *[Line([x[ee[0]],y[ee[0]],0],[x[ee[1]],y[ee[1]],0]) for ee in e],
                # *[Circle(0.005,color=WHITE).set_fill("#9999ff",opacity=1).move_to([x[i],y[i],0]) for i in range(len(x))]
            ).move_to(3*LEFT+DOWN).set_color(BLUE).stretch_to_fit_height(4).stretch_to_fit_width(4)
            primal_text=Tex("Triangular").next_to(primal,UP).set_color(BLUE)
            x=[1.0,1.0,1.0,1.0,1.0,1.0,1.0,2.0,2.0,2.0,2.0,2.0,2.0,2.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,4.0,4.0,4.0,4.0,4.0,4.0,4.0,5.0,5.0,5.0,5.0,5.0,5.0,5.0,6.0,6.0,6.0,6.0,6.0,6.0,6.0,7.0,7.0,7.0,7.0,7.0,7.0,7.0,8.0,8.0,8.0,8.0,8.0,8.0,8.0,]
            y=[1.0,2.0,3.0,4.0,5.0,6.0,7.0,1.0,2.0,3.0,4.0,5.0,6.0,7.0,1.0,2.0,3.0,4.0,5.0,6.0,7.0,1.0,2.0,3.0,4.0,5.0,6.0,7.0,1.0,2.0,3.0,4.0,5.0,6.0,7.0,1.0,2.0,3.0,4.0,5.0,6.0,7.0,1.0,2.0,3.0,4.0,5.0,6.0,7.0,1.0,2.0,3.0,4.0,5.0,6.0,7.0,]
            e=[(0, 7),(1, 8),(2, 9),(3, 10),(4, 11),(5, 12),(6, 13),(7, 15),(7, 14),(7, 0),(8, 1),(8, 15),(8, 16),(9, 2),(9, 16),(9, 17),(10, 3),(10, 18),(10, 17),(11, 18),(11, 4),(11, 19),(12, 20),(12, 5),(12, 19),(13, 6),(13, 20),(14, 7),(14, 21),(15, 22),(15, 8),(15, 7),(16, 8),(16, 9),(16, 23),(17, 24),(17, 9),(17, 10),(18, 25),(18, 10),(18, 11),(19, 12),(19, 26),(19, 11),(20, 12),(20, 13),(20, 27),(21, 28),(21, 14),(21, 29),(22, 30),(22, 15),(22, 29),(23, 30),(23, 31),(23, 16),(24, 31),(24, 32),(24, 17),(25, 33),(25, 18),(25, 32),(26, 34),(26, 33),(26, 19),(27, 34),(27, 20),(28, 35),(28, 21),(29, 22),(29, 36),(29, 21),(30, 22),(30, 37),(30, 23),(31, 24),(31, 38),(31, 23),(32, 25),(32, 24),(32, 39),(33, 25),(33, 26),(33, 40),(34, 41),(34, 26),(34, 27),(35, 42),(35, 28),(35, 43),(36, 29),(36, 43),(36, 44),(37, 30),(37, 45),(37, 44),(38, 46),(38, 31),(38, 45),(39, 46),(39, 47),(39, 32),(40, 33),(40, 47),(40, 48),(41, 34),(41, 48),(42, 49),(42, 35),(43, 36),(43, 35),(43, 50),(44, 36),(44, 37),(44, 51),(45, 52),(45, 37),(45, 38),(46, 53),(46, 39),(46, 38),(47, 54),(47, 39),(47, 40),(48, 41),(48, 55),(48, 40),(49, 42),(50, 43),(51, 44),(52, 45),(53, 46),(54, 47),(55, 48),]
            dual=VGroup(
                *[Line([x[ee[0]],y[ee[0]],0],[x[ee[1]],y[ee[1]],0]) for ee in e],
                # *[Circle(0.005,color=WHITE).set_fill("#9999ff",opacity=1).move_to([x[i],y[i],0]) for i in range(len(x))]
            ).move_to(3*RIGHT+DOWN).set_color(RED).stretch_to_fit_height(4).stretch_to_fit_width(4)
            dual_text=Tex("Hexagonal").next_to(dual,UP).set_color(RED)
            self.play(FadeIn(primal_text),FadeIn(dual_text),*[Write(p) for p in primal],*[Write(d) for d in dual])
            self.wait()
            self.play(FadeOut(primal_text),FadeOut(dual_text),*[Unwrite(p) for p in primal],*[Unwrite(d) for d in dual])
            self.wait()

            # Kagome
            x=[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,1.0,1.0,1.0,1.0,2.0,2.0,2.0,2.0,2.0,2.0,2.0,2.0,2.0,3.0,3.0,3.0,3.0,3.0,4.0,4.0,4.0,4.0,4.0,4.0,4.0,4.0,4.0,5.0,5.0,5.0,5.0,5.0,6.0,6.0,6.0,6.0,6.0,6.0,6.0,6.0,6.0,7.0,7.0,7.0,7.0,7.0,8.0,8.0,8.0,8.0,8.0,8.0,8.0,8.0,8.0,]
            y=[0.0,1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,0.0,2.0,4.0,6.0,8.0,0.0,1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,0.0,2.0,4.0,6.0,8.0,0.0,1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,0.0,2.0,4.0,6.0,8.0,0.0,1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,0.0,2.0,4.0,6.0,8.0,0.0,1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,]
            e=[(0, 9),(1, 9),(2, 10),(3, 10),(4, 11),(5, 11),(6, 12),(7, 12),(8, 13),(9, 1),(9, 14),(9, 0),(10, 3),(10, 2),(10, 15),(10, 16),(11, 18),(11, 4),(11, 5),(11, 17),(12, 6),(12, 7),(12, 20),(12, 19),(13, 22),(13, 8),(13, 21),(14, 9),(14, 15),(14, 23),(15, 16),(15, 10),(15, 14),(15, 23),(16, 24),(16, 15),(16, 10),(16, 17),(17, 24),(17, 18),(17, 16),(17, 11),(18, 19),(18, 25),(18, 11),(18, 17),(19, 25),(19, 12),(19, 18),(19, 20),(20, 12),(20, 26),(20, 21),(20, 19),(21, 22),(21, 13),(21, 26),(21, 20),(22, 13),(22, 27),(22, 21),(23, 28),(23, 15),(23, 14),(24, 29),(24, 30),(24, 16),(24, 17),(25, 31),(25, 18),(25, 32),(25, 19),(26, 34),(26, 33),(26, 20),(26, 21),(27, 22),(27, 36),(27, 35),(28, 23),(28, 37),(28, 29),(29, 30),(29, 24),(29, 28),(29, 37),(30, 24),(30, 31),(30, 38),(30, 29),(31, 25),(31, 30),(31, 38),(31, 32),(32, 25),(32, 31),(32, 33),(32, 39),(33, 34),(33, 39),(33, 26),(33, 32),(34, 33),(34, 26),(34, 35),(34, 40),(35, 36),(35, 34),(35, 27),(35, 40),(36, 41),(36, 27),(36, 35),(37, 42),(37, 28),(37, 29),(38, 30),(38, 31),(38, 43),(38, 44),(39, 46),(39, 33),(39, 32),(39, 45),(40, 34),(40, 35),(40, 47),(40, 48),(41, 36),(41, 49),(41, 50),(42, 37),(42, 43),(42, 51),(43, 42),(43, 38),(43, 51),(43, 44),(44, 52),(44, 38),(44, 43),(44, 45),(45, 46),(45, 52),(45, 39),(45, 44),(46, 53),(46, 39),(46, 47),(46, 45),(47, 46),(47, 53),(47, 48),(47, 40),(48, 49),(48, 54),(48, 47),(48, 40),(49, 54),(49, 41),(49, 48),(49, 50),(50, 49),(50, 41),(50, 55),(51, 42),(51, 56),(51, 43),(52, 57),(52, 58),(52, 45),(52, 44),(53, 46),(53, 59),(53, 60),(53, 47),(54, 62),(54, 49),(54, 61),(54, 48),(55, 64),(55, 63),(55, 50),(56, 51),(57, 52),(58, 52),(59, 53),(60, 53),(61, 54),(62, 54),(63, 55),(64, 55),]
            primal=VGroup(
                *[Line([x[ee[0]],y[ee[0]],0],[x[ee[1]],y[ee[1]],0]) for ee in e],
                # *[Circle(0.005,color=WHITE).set_fill("#9999ff",opacity=1).move_to([x[i],y[i],0]) for i in range(len(x))]
            ).move_to(3*LEFT+DOWN).set_color(BLUE).stretch_to_fit_height(4).stretch_to_fit_width(4)
            primal_text=Tex("Kagome").next_to(primal,UP).set_color(BLUE)
            x=[-3.0,7.0,3.0,10.0,5.0,3.0,6.0,9.0,6.0,7.0,4.0,5.0,0.0,10.0,12.0,-3.0,-3.0,0.0,6.0,-1.0,-3.0,12.0,-3.0,8.0,0.0,1.0,9.0,9.0,10.0,-3.0,12.0,2.0,12.0,-3.0,4.0,3.0,5.0,7.0,8.0,-3.0,-1.0,9.0,2.0,0.0,12.0,8.0,12.0,10.0,1.0,6.0,-1.0,-1.0,2.0,2.0,4.0,1.0,8.0,1.0,3.0,12.0,7.0,4.0,5.0,12.0,]
            y=[1.0,1.0,6.0,7.0,2.0,9.0,6.0,3.0,9.0,9.0,1.0,8.0,3.0,1.0,2.0,6.0,4.0,9.0,3.0,5.0,3.0,9.0,9.0,5.0,0.0,7.0,6.0,0.0,4.0,0.0,5.0,8.0,3.0,9.0,7.0,0.0,0.0,7.0,8.0,7.0,0.0,9.0,5.0,6.0,6.0,0.0,0.0,9.0,4.0,0.0,2.0,8.0,2.0,0.0,4.0,9.0,2.0,1.0,3.0,8.0,4.0,9.0,5.0,0.0,]
            e=[(0, 24),(1, 18),(1, 27),(1, 49),(2, 31),(2, 25),(2, 34),(2, 42),(2, 62),(2, 54),(3, 41),(3, 44),(3, 26),(4, 18),(4, 58),(4, 49),(5, 31),(5, 55),(5, 34),(5, 61),(5, 11),(6, 37),(6, 34),(6, 60),(6, 62),(6, 11),(6, 23),(7, 13),(7, 14),(7, 60),(7, 56),(7, 23),(7, 28),(8, 37),(8, 38),(8, 9),(8, 61),(8, 11),(9, 8),(9, 41),(10, 35),(10, 58),(10, 49),(11, 5),(11, 6),(11, 8),(12, 19),(12, 50),(12, 57),(12, 48),(12, 52),(12, 16),(13, 27),(13, 7),(13, 46),(14, 7),(15, 19),(16, 12),(17, 25),(17, 31),(17, 33),(17, 55),(17, 51),(18, 4),(18, 60),(18, 56),(18, 1),(18, 62),(18, 54),(19, 43),(19, 15),(19, 12),(20, 50),(21, 47),(22, 51),(23, 6),(23, 7),(23, 26),(24, 0),(24, 40),(24, 50),(24, 57),(24, 53),(25, 43),(25, 2),(25, 17),(26, 28),(26, 30),(26, 37),(26, 38),(26, 23),(26, 3),(27, 13),(27, 56),(27, 1),(27, 63),(27, 45),(28, 32),(28, 7),(28, 26),(29, 40),(30, 26),(31, 5),(31, 2),(31, 17),(32, 28),(33, 17),(34, 5),(34, 6),(34, 2),(35, 36),(35, 10),(35, 52),(35, 53),(35, 57),(36, 35),(36, 49),(37, 6),(37, 8),(37, 26),(38, 8),(38, 41),(38, 26),(39, 43),(40, 24),(40, 29),(41, 59),(41, 38),(41, 47),(41, 9),(41, 3),(42, 58),(42, 43),(42, 2),(43, 25),(43, 19),(43, 39),(43, 51),(43, 48),(43, 42),(44, 3),(45, 27),(45, 49),(46, 13),(47, 41),(47, 21),(48, 58),(48, 43),(48, 12),(49, 36),(49, 4),(49, 1),(49, 10),(49, 45),(50, 24),(50, 20),(50, 12),(51, 43),(51, 22),(51, 17),(52, 58),(52, 35),(52, 12),(53, 35),(53, 24),(54, 58),(54, 18),(54, 2),(55, 5),(55, 17),(56, 18),(56, 27),(56, 7),(57, 35),(57, 24),(57, 12),(58, 48),(58, 4),(58, 10),(58, 52),(58, 42),(58, 54),(59, 41),(60, 18),(60, 6),(60, 7),(61, 5),(61, 8),(62, 18),(62, 6),(62, 2),(63, 27),]
            dual=VGroup(
                *[Line([x[ee[0]],y[ee[0]],0],[x[ee[1]],y[ee[1]],0]) for ee in e],
                # *[Circle(0.005,color=WHITE).set_fill("#9999ff",opacity=1).move_to([x[i],y[i],0]) for i in range(len(x))]
            ).move_to(3*RIGHT+DOWN).set_color(RED).stretch_to_fit_height(4).stretch_to_fit_width(4)
            dual_text=Tex("Rhombille").next_to(dual,UP).set_color(RED)
            self.play(FadeIn(primal_text),FadeIn(dual_text),*[Write(p) for p in primal],*[Write(d) for d in dual])
            self.wait()
            self.play(FadeOut(primal_text),FadeOut(dual_text),*[Unwrite(p) for p in primal],*[Unwrite(d) for d in dual])
            self.wait()

            # Trihexa
            x=[-5.0,-1.0,-3.0,-5.0,-7.0,-4.0,-5.0,-6.0,-1.0,-7.0,-8.0,-4.0,-2.0,-1.0,-5.0,-8.0,-3.0,-2.0,-6.0,-5.0,-2.0,-8.0,-1.0,-7.0,-8.0,-5.0,-3.0,-5.0,-3.0,-8.0,-8.0,-7.0,-4.0,-7.0,-2.0,-1.0,-1.0,-3.0,-8.0,-5.0,-4.0,-2.0,-1.0,-4.0,-8.0,-1.0,-4.0,-6.0,-1.0,-8.0,-3.0,-1.0,-5.0,-6.0,-4.0,-6.0,-4.0,-5.0,-8.0,-6.0,-3.0,-4.0,-8.0,-2.0,-4.0,-8.0,-2.0,-4.0,-5.0,-4.0,-1.0,-5.0,-5.0,-8.0,-6.0,-1.0,-4.0,-4.0,-7.0,-8.0,-5.0,-7.0,-6.0,-1.0,-3.0,-8.0,-2.0,-1.0,-5.0,-7.0,-1.0,-4.0,]
            y=[11.0,0.0,9.0,8.0,12.0,13.0,15.0,21.0,12.0,9.0,6.0,12.0,12.0,2.0,9.0,15.0,15.0,21.0,18.0,17.0,6.0,12.0,17.0,21.0,16.0,2.0,3.0,3.0,21.0,7.0,18.0,15.0,10.0,6.0,3.0,14.0,9.0,0.0,9.0,21.0,6.0,9.0,18.0,0.0,3.0,21.0,9.0,3.0,6.0,1.0,6.0,11.0,20.0,0.0,19.0,15.0,7.0,6.0,21.0,12.0,12.0,1.0,10.0,18.0,18.0,0.0,0.0,4.0,5.0,3.0,8.0,18.0,0.0,19.0,9.0,3.0,15.0,16.0,0.0,13.0,14.0,18.0,6.0,5.0,18.0,4.0,15.0,20.0,12.0,3.0,15.0,21.0,]
            e=[(0, 88),(0, 59),(0, 32),(1, 66),(2, 32),(2, 46),(2, 41),(3, 56),(3, 74),(3, 14),(4, 21),(4, 59),(4, 79),(5, 60),(5, 80),(5, 11),(6, 80),(6, 76),(6, 55),(7, 23),(7, 52),(7, 39),(8, 12),(9, 62),(9, 38),(9, 74),(10, 33),(11, 5),(11, 60),(11, 88),(12, 60),(12, 51),(12, 8),(13, 34),(14, 74),(14, 46),(14, 3),(15, 31),(16, 77),(16, 76),(16, 86),(17, 87),(17, 45),(17, 28),(18, 81),(18, 71),(18, 19),(19, 77),(19, 18),(19, 71),(20, 50),(20, 83),(20, 48),(21, 4),(22, 63),(23, 58),(23, 7),(24, 31),(25, 27),(25, 61),(25, 47),(26, 34),(26, 69),(26, 67),(27, 69),(27, 25),(27, 47),(28, 17),(28, 91),(29, 33),(30, 81),(31, 15),(31, 24),(31, 55),(32, 0),(32, 46),(32, 2),(33, 29),(33, 10),(33, 82),(34, 75),(34, 13),(34, 26),(35, 86),(36, 41),(37, 66),(37, 43),(37, 61),(38, 9),(39, 7),(39, 52),(39, 91),(40, 57),(40, 56),(40, 50),(41, 70),(41, 36),(41, 2),(42, 63),(43, 37),(43, 72),(43, 61),(44, 89),(45, 17),(46, 32),(46, 14),(46, 2),(47, 89),(47, 27),(47, 25),(48, 20),(49, 78),(50, 56),(50, 20),(50, 40),(51, 12),(52, 7),(52, 39),(52, 54),(53, 72),(53, 78),(54, 52),(54, 84),(54, 64),(55, 6),(55, 31),(55, 80),(56, 50),(56, 40),(56, 3),(57, 68),(57, 82),(57, 40),(58, 23),(59, 0),(59, 88),(59, 4),(60, 5),(60, 12),(60, 11),(61, 37),(61, 43),(61, 25),(62, 9),(63, 22),(63, 42),(63, 84),(64, 71),(64, 54),(64, 84),(65, 78),(66, 37),(66, 1),(67, 68),(67, 69),(67, 26),(68, 57),(68, 82),(68, 67),(69, 27),(69, 67),(69, 26),(70, 41),(71, 18),(71, 19),(71, 64),(72, 53),(72, 43),(73, 81),(74, 9),(74, 14),(74, 3),(75, 34),(76, 6),(76, 77),(76, 16),(77, 16),(77, 76),(77, 19),(78, 65),(78, 53),(78, 49),(79, 4),(80, 6),(80, 5),(80, 55),(81, 30),(81, 73),(81, 18),(82, 57),(82, 68),(82, 33),(83, 20),(84, 63),(84, 54),(84, 64),(85, 89),(86, 90),(86, 16),(86, 35),(87, 17),(88, 0),(88, 59),(88, 11),(89, 85),(89, 44),(89, 47),(90, 86),(91, 39),(91, 28),]
            primal=VGroup(
                *[Line([x[ee[0]],y[ee[0]],0],[x[ee[1]],y[ee[1]],0]) for ee in e],
                # *[Circle(0.005,color=WHITE).set_fill("#9999ff",opacity=1).move_to([x[i],y[i],0]) for i in range(len(x))]
            ).move_to(3*LEFT+DOWN).set_color(BLUE).stretch_to_fit_height(4).stretch_to_fit_width(4)
            primal_text=Tex("Truncated Hexagonal").next_to(primal,UP).set_color(BLUE)
            x=[3.0,13.0,14.0,24.0,9.0,15.0,17.0,15.0,24.0,16.0,9.0,20.0,29.0,17.0,10.0,19.0,9.0,21.0,20.0,15.0,5.0,12.0,13.0,6.0,18.0,28.0,25.0,26.0,28.0,3.0,12.0,14.0,23.0,24.0,3.0,12.0,22.0,4.0,11.0,30.0,25.0,27.0,4.0,18.0,21.0,18.0,23.0,29.0,30.0,22.0,8.0,27.0,7.0,5.0,6.0,16.0,8.0,26.0,21.0,11.0,6.0,19.0,10.0,30.0,27.0,7.0,]
            y=[9.0,4.0,8.0,3.0,3.0,6.0,8.0,9.0,9.0,7.0,6.0,8.0,8.0,5.0,7.0,7.0,9.0,9.0,5.0,3.0,5.0,3.0,7.0,3.0,6.0,4.0,7.0,8.0,7.0,3.0,9.0,5.0,8.0,6.0,6.0,6.0,4.0,7.0,8.0,6.0,4.0,6.0,4.0,3.0,6.0,9.0,5.0,5.0,3.0,7.0,5.0,9.0,7.0,8.0,6.0,4.0,8.0,5.0,3.0,5.0,9.0,4.0,4.0,9.0,3.0,4.0,]
            e=[(0, 60),(0, 37),(0, 53),(0, 54),(1, 35),(1, 21),(1, 19),(2, 30),(2, 5),(2, 7),(3, 36),(3, 40),(3, 64),(3, 44),(3, 46),(3, 33),(3, 58),(4, 21),(4, 23),(4, 10),(4, 62),(4, 54),(4, 50),(4, 65),(5, 30),(5, 31),(5, 2),(5, 35),(5, 7),(5, 19),(5, 55),(5, 43),(5, 9),(5, 22),(5, 24),(5, 13),(6, 45),(6, 24),(6, 7),(7, 45),(7, 30),(7, 5),(7, 24),(7, 6),(7, 2),(7, 9),(8, 17),(8, 41),(8, 26),(8, 51),(8, 27),(8, 33),(8, 32),(9, 5),(9, 24),(9, 7),(10, 50),(10, 52),(10, 35),(10, 4),(10, 16),(10, 54),(10, 56),(10, 21),(10, 59),(10, 60),(10, 62),(10, 14),(11, 45),(11, 17),(11, 44),(12, 39),(12, 51),(12, 63),(13, 5),(13, 24),(13, 43),(14, 35),(14, 10),(14, 16),(15, 45),(15, 24),(15, 44),(16, 60),(16, 30),(16, 10),(16, 35),(16, 38),(16, 56),(16, 14),(17, 45),(17, 49),(17, 8),(17, 11),(17, 44),(17, 33),(17, 32),(18, 24),(18, 44),(18, 58),(19, 35),(19, 21),(19, 5),(19, 31),(19, 43),(19, 55),(19, 1),(20, 34),(20, 23),(20, 54),(21, 35),(21, 4),(21, 10),(21, 62),(21, 59),(21, 19),(21, 1),(22, 35),(22, 30),(22, 5),(23, 34),(23, 20),(23, 4),(23, 42),(23, 54),(23, 65),(23, 29),(24, 15),(24, 5),(24, 6),(24, 18),(24, 7),(24, 58),(24, 43),(24, 44),(24, 9),(24, 45),(24, 61),(24, 13),(25, 41),(25, 48),(25, 64),(26, 41),(26, 8),(26, 33),(27, 41),(27, 51),(27, 8),(28, 41),(28, 39),(28, 51),(29, 23),(29, 42),(30, 35),(30, 16),(30, 5),(30, 38),(30, 7),(30, 2),(30, 22),(31, 35),(31, 5),(31, 19),(32, 17),(32, 8),(32, 33),(33, 49),(33, 32),(33, 3),(33, 17),(33, 40),(33, 57),(33, 41),(33, 8),(33, 44),(33, 26),(33, 64),(33, 46),(34, 37),(34, 23),(34, 20),(34, 42),(34, 54),(35, 30),(35, 31),(35, 1),(35, 5),(35, 16),(35, 38),(35, 19),(35, 21),(35, 59),(35, 22),(35, 10),(35, 14),(36, 3),(36, 44),(36, 58),(37, 34),(37, 54),(37, 0),(38, 35),(38, 30),(38, 16),(39, 47),(39, 41),(39, 51),(39, 12),(39, 28),(40, 64),(40, 33),(40, 3),(41, 47),(41, 48),(41, 51),(41, 33),(41, 39),(41, 57),(41, 8),(41, 25),(41, 26),(41, 64),(41, 27),(41, 28),(42, 34),(42, 23),(42, 29),(43, 61),(43, 5),(43, 24),(43, 19),(43, 55),(43, 13),(43, 58),(44, 49),(44, 15),(44, 33),(44, 3),(44, 36),(44, 17),(44, 18),(44, 58),(44, 45),(44, 24),(44, 11),(44, 46),(45, 17),(45, 15),(45, 24),(45, 6),(45, 7),(45, 11),(45, 44),(46, 44),(46, 33),(46, 3),(47, 41),(47, 48),(47, 39),(48, 47),(48, 41),(48, 25),(48, 64),(49, 17),(49, 44),(49, 33),(50, 10),(50, 4),(50, 54),(51, 41),(51, 39),(51, 8),(51, 63),(51, 27),(51, 12),(51, 28),(52, 60),(52, 10),(52, 54),(53, 60),(53, 54),(53, 0),(54, 50),(54, 0),(54, 52),(54, 34),(54, 37),(54, 4),(54, 53),(54, 20),(54, 60),(54, 10),(54, 23),(54, 65),(55, 5),(55, 43),(55, 19),(56, 60),(56, 10),(56, 16),(57, 41),(57, 64),(57, 33),(58, 61),(58, 36),(58, 24),(58, 43),(58, 18),(58, 44),(58, 3),(59, 35),(59, 21),(59, 10),(60, 10),(60, 16),(60, 53),(60, 54),(60, 0),(60, 52),(60, 56),(61, 24),(61, 43),(61, 58),(62, 21),(62, 4),(62, 10),(63, 51),(63, 12),(64, 57),(64, 48),(64, 41),(64, 25),(64, 40),(64, 33),(64, 3),(65, 23),(65, 4),(65, 54),]
            dual=VGroup(
                *[Line([x[ee[0]],y[ee[0]],0],[x[ee[1]],y[ee[1]],0]) for ee in e],
                # *[Circle(0.005,color=WHITE).set_fill("#9999ff",opacity=1).move_to([x[i],y[i],0]) for i in range(len(x))]
            ).move_to(3*RIGHT+DOWN).set_color(RED).stretch_to_fit_height(4).stretch_to_fit_width(4)
            dual_text=Tex("Asanoha").next_to(dual,UP).set_color(RED)
            self.play(FadeIn(primal_text),FadeIn(dual_text),*[Write(p) for p in primal],*[Write(d) for d in dual])
            self.wait()
            self.play(FadeOut(primal_text),FadeOut(dual_text),*[Unwrite(p) for p in primal],*[Unwrite(d) for d in dual])
            self.wait()

            # Triangulation
            x=[1.7,1.2583333333333333,1.3,1.6111111111111112,1.68552998512284,1.3638130813851537,1.6555555555555554,1.327830905829321,1.3785160239346557,1.32781893983922,1.7416666666666667,1.5222222222222221,1.6897375731855258,1.7416666666666667,1.7,1.2583333333333333,1.7416666666666667,1.5023988137720887,1.3432290764770953,1.348483995513108,1.4522600910642838,1.6757750540305847,1.6463982864886197,1.4836073856656573,1.3103959019896751,1.6357495306314251,1.6807666165073025,1.7,1.7,1.445860056659461,1.4333333333333333,1.7,1.7416666666666667,1.7416666666666667,1.401370763515577,1.5666666666666667,1.3,1.5501192113666247,1.3,1.343122771910268,1.5432674859652875,1.5228885791276034,1.429649282496557,1.2583333333333333,1.5222222222222221,1.6467854072128012,1.4637433846546588,1.3984920339521112,1.3315080301611573,1.3996298624253323,1.7,1.2583333333333333,1.7416666666666667,1.3888888888888888,1.7,1.5679816146974495,1.3444444444444446,1.658247153968764,1.481516763651312,1.2583333333333333,1.336797403002878,1.381883954934847,1.3444444444444446,1.6076632994050843,1.396458562129603,1.6636568662981182,1.3,1.7416666666666667,1.4407640687984025,1.3,1.6111111111111112,1.6309367211069552,1.6555555555555554,1.7416666666666667,1.2583333333333333,1.656986815803924,1.3,1.3087711212832103,1.3,1.2583333333333333,1.3,1.6012375885104932,1.5123594223666523,1.5378690391166192,1.593946139202455,1.2583333333333333,1.3888888888888888,1.4134362416464954,1.4333333333333333,1.7,1.4777777777777779,1.4214415605577142,1.5949609361797887,1.4777777777777779,1.5666666666666667,1.5383213746993751,]
            y=[1.34,1.522857142857143,1.5685714285714285,1.34,1.599409507641703,1.4341694091947392,1.34,1.5278532431967862,1.6160296931033584,1.5304008817839074,1.66,1.66,1.4979875660612338,1.3857142857142857,1.3857142857142857,1.6142857142857143,1.6142857142857143,1.5633424339185076,1.5600758059198305,1.52042732564029,1.35941270690215,1.4803405599315973,1.5632353063240334,1.4121265801346476,1.6011305854388245,1.3516779036642046,1.4557812508144927,1.5685714285714285,1.66,1.5487912462483424,1.34,1.522857142857143,1.477142857142857,1.5685714285714285,1.5967317211606509,1.66,1.4314285714285715,1.4573957909809567,1.66,1.360847366506369,1.5767154766874825,1.4672703681515267,1.393545197890512,1.4314285714285715,1.34,1.5963143285925407,1.46831300360128,1.6045620407317833,1.4965208012994249,1.4665105257109696,1.477142857142857,1.66,1.522857142857143,1.66,1.6142857142857143,1.5486533678746421,1.66,1.4899474014074288,1.4269868573799525,1.3857142857142857,1.6001404966298982,1.4965092817319108,1.34,1.6274576520333097,1.4082355791748538,1.4121383210512357,1.6142857142857143,1.4314285714285715,1.5781316322478258,1.34,1.66,1.4936102733987526,1.66,1.34,1.5685714285714285,1.5681218336687592,1.522857142857143,1.4115710786897273,1.477142857142857,1.477142857142857,1.3857142857142857,1.4952556299124036,1.4795739138371369,1.4424418988379015,1.3492828977306772,1.34,1.34,1.5216104913625281,1.66,1.4314285714285715,1.66,1.642017119872703,1.4720534673145775,1.34,1.34,1.5945056444043566,]
            e=[(0, 14),(0, 6),(0, 73),(1, 76),(2, 76),(2, 66),(2, 18),(2, 60),(2, 24),(2, 9),(2, 74),(3, 25),(3, 6),(3, 94),(3, 84),(4, 75),(4, 54),(4, 45),(4, 72),(4, 27),(5, 78),(5, 64),(5, 77),(5, 48),(5, 61),(5, 49),(5, 36),(5, 39),(6, 25),(6, 14),(6, 3),(6, 0),(6, 65),(7, 76),(7, 19),(7, 48),(7, 9),(8, 53),(8, 91),(8, 18),(8, 47),(8, 34),(8, 60),(8, 56),(9, 76),(9, 7),(9, 18),(9, 19),(9, 2),(10, 28),(11, 35),(11, 95),(11, 90),(12, 31),(12, 57),(12, 21),(12, 50),(13, 14),(14, 13),(14, 6),(14, 0),(14, 89),(14, 65),(15, 66),(16, 54),(17, 40),(17, 68),(17, 29),(17, 95),(17, 82),(17, 55),(17, 90),(18, 19),(18, 34),(18, 60),(18, 2),(18, 87),(18, 8),(18, 9),(19, 7),(19, 18),(19, 48),(19, 61),(19, 87),(19, 9),(20, 93),(20, 23),(20, 30),(20, 42),(21, 57),(21, 26),(21, 50),(21, 12),(22, 75),(22, 71),(22, 45),(22, 31),(22, 57),(22, 81),(22, 55),(23, 93),(23, 44),(23, 58),(23, 20),(23, 83),(23, 42),(24, 66),(24, 60),(24, 2),(25, 6),(25, 3),(25, 84),(25, 65),(26, 71),(26, 57),(26, 21),(26, 50),(26, 89),(26, 65),(27, 75),(27, 54),(27, 31),(27, 33),(27, 4),(28, 54),(28, 72),(28, 10),(29, 17),(29, 46),(29, 68),(29, 87),(29, 82),(30, 93),(30, 20),(30, 86),(30, 42),(31, 75),(31, 22),(31, 57),(31, 12),(31, 50),(31, 27),(31, 52),(32, 50),(33, 27),(34, 18),(34, 47),(34, 68),(34, 8),(34, 87),(34, 91),(35, 11),(35, 95),(35, 63),(35, 70),(36, 78),(36, 77),(36, 80),(36, 5),(36, 43),(37, 92),(37, 81),(37, 83),(37, 41),(37, 55),(37, 82),(38, 66),(38, 51),(38, 56),(39, 64),(39, 77),(39, 80),(39, 86),(39, 62),(39, 5),(39, 69),(40, 17),(40, 95),(40, 55),(40, 63),(41, 37),(41, 58),(41, 83),(41, 82),(42, 64),(42, 58),(42, 46),(42, 20),(42, 23),(42, 86),(42, 49),(42, 30),(43, 36),(44, 93),(44, 23),(44, 94),(44, 83),(45, 75),(45, 22),(45, 72),(45, 4),(45, 55),(45, 63),(46, 58),(46, 29),(46, 49),(46, 87),(46, 82),(46, 42),(47, 34),(47, 8),(47, 91),(48, 78),(48, 76),(48, 7),(48, 19),(48, 61),(48, 5),(49, 64),(49, 46),(49, 61),(49, 87),(49, 42),(49, 5),(50, 31),(50, 21),(50, 26),(50, 12),(50, 89),(50, 32),(51, 38),(52, 31),(53, 56),(53, 8),(53, 88),(53, 91),(54, 72),(54, 4),(54, 28),(54, 16),(54, 27),(55, 40),(55, 17),(55, 45),(55, 22),(55, 37),(55, 81),(55, 82),(55, 63),(56, 66),(56, 60),(56, 8),(56, 38),(56, 53),(57, 71),(57, 31),(57, 22),(57, 21),(57, 12),(57, 26),(58, 46),(58, 23),(58, 83),(58, 41),(58, 42),(58, 82),(59, 80),(60, 66),(60, 18),(60, 2),(60, 24),(60, 8),(60, 56),(61, 19),(61, 48),(61, 49),(61, 87),(61, 5),(62, 86),(62, 39),(62, 69),(63, 40),(63, 45),(63, 72),(63, 35),(63, 95),(63, 55),(63, 70),(64, 86),(64, 49),(64, 39),(64, 5),(64, 42),(65, 25),(65, 71),(65, 14),(65, 6),(65, 92),(65, 84),(65, 26),(65, 89),(66, 15),(66, 60),(66, 2),(66, 24),(66, 38),(66, 56),(67, 89),(68, 91),(68, 17),(68, 34),(68, 29),(68, 87),(68, 90),(69, 85),(69, 80),(69, 62),(69, 39),(70, 72),(70, 35),(70, 63),(71, 22),(71, 57),(71, 92),(71, 81),(71, 26),(71, 65),(72, 54),(72, 45),(72, 4),(72, 28),(72, 63),(72, 70),(73, 0),(74, 2),(75, 45),(75, 22),(75, 31),(75, 4),(75, 27),(76, 78),(76, 7),(76, 48),(76, 1),(76, 2),(76, 9),(77, 80),(77, 36),(77, 39),(77, 5),(78, 76),(78, 48),(78, 79),(78, 36),(78, 5),(79, 78),(80, 77),(80, 59),(80, 36),(80, 39),(80, 69),(81, 37),(81, 71),(81, 22),(81, 92),(81, 55),(82, 17),(82, 37),(82, 58),(82, 46),(82, 29),(82, 41),(82, 55),(83, 37),(83, 44),(83, 58),(83, 23),(83, 92),(83, 94),(83, 84),(83, 41),(84, 25),(84, 3),(84, 92),(84, 94),(84, 83),(84, 65),(85, 69),(86, 64),(86, 62),(86, 39),(86, 42),(86, 30),(87, 18),(87, 19),(87, 46),(87, 68),(87, 34),(87, 61),(87, 49),(87, 29),(88, 53),(88, 90),(88, 91),(89, 14),(89, 67),(89, 50),(89, 26),(89, 65),(90, 11),(90, 17),(90, 68),(90, 95),(90, 88),(90, 91),(91, 53),(91, 47),(91, 68),(91, 34),(91, 8),(91, 88),(91, 90),(92, 37),(92, 71),(92, 81),(92, 83),(92, 84),(92, 65),(93, 44),(93, 23),(93, 20),(93, 30),(94, 44),(94, 3),(94, 84),(94, 83),(95, 11),(95, 40),(95, 17),(95, 35),(95, 63),(95, 90),]
            primal=VGroup(
                *[Line([x[ee[0]],y[ee[0]],0],[x[ee[1]],y[ee[1]],0]) for ee in e],
                # *[Circle(0.005,color=WHITE).set_fill("#9999ff",opacity=1).move_to([x[i],y[i],0]) for i in range(len(x))]
            ).move_to(3*LEFT+DOWN).set_color(BLUE).stretch_to_fit_height(4).stretch_to_fit_width(4)
            primal_text=Tex("Rand.\\ Triangulation").next_to(primal,UP).set_color(BLUE)
            y=[1.3185499485561805,1.634138732432697,1.6826615757180967,1.3212710271283845,1.6074767737717783,1.6715962748355502,1.6261908653686892,1.425603162908829,1.2791666666666668,1.2791666666666668,1.5609830622210108,1.4441842238896083,1.5275799502787304,1.6951766617076134,1.4185236913201582,1.3743719546424427,1.7208333333333332,1.3962821577937532,1.6566501638610072,1.3539586602030376,1.404998911171683,1.7208333333333332,1.3157311016641844,1.3143742573034227,1.324194734222788,1.5422526426685026,1.3866338353133632,1.6851851851851851,1.433353455701453,1.4858731902242077,1.339844003943141,1.4649244772711754,1.6803618468927983,1.5145662156681663,1.5378826381449417,1.6311175120439996,1.3172979643978262,1.4868727642660673,1.617521313893454,1.3677981384750082,1.303465300663225,1.7208333333333332,1.6626236492970656,1.4551722530754994,1.6730708072845577,1.7208333333333332,1.2791666666666668,1.3092729799464067,1.392792940467448,1.3266754931599911,1.5061659887497472,1.6451940538547796,1.3590683554937193,1.2791666666666668,1.5729708000226073,1.6677950340975147,1.536958943203616,1.7208333333333332,1.4630076464099842,1.5055882550485225,1.3317737038487703,1.3197796453301596,1.4384142356313914,1.3029237070944033,1.6298515078616207,1.6851851851851851,1.3291890721182373,1.7208333333333334,1.500997729477863,1.6247766553572502,1.6584534013041254,1.605205829898854,1.370616452422663,1.6500568365017816,1.5951470257276206,1.5127737915664585,1.6682151468191277,1.421192130957231,1.4544570673917985,1.5284557376202936,1.613602260314997,1.338568991526211,1.6631007360465218,1.6808389336422547,1.5821059120189689,1.4071014526751344,1.5708837802570421,1.3983166863355583,1.2791666666666666,1.590574638993411,1.2791666666666668,1.381775632915111,1.5755920381662876,1.6935888721691008,1.3157311016641844,1.4410132276535386,1.6856622719346415,1.6885042090720368,1.3683831045455663,1.6814744942684736,1.6203884361329568,1.473987621226924,1.5434867494769087,1.5279958914789171,1.4583031436008425,1.4712150848359062,1.4736468867827563,1.4172905015729265,1.6878856220993725,1.3860120272130558,1.3148148148148149,1.566160614995247,1.2791666666666668,1.6855138901792956,1.4310075098588495,1.4945357952218856,1.5630840533565824,1.636668087391147,1.6745865937282913,1.4466611357112982,1.4145545942599789,1.3528475011382097,1.3105026767203858,1.3761567409762534,1.6965791910618417,1.7208333333333332,1.542403421196088,1.6090450819324122,1.3994832061481606,1.3588187017478672,1.6516539841616995,1.3236826721054384,1.3812680640314836,1.3532526237939926,1.3347112803938828,1.3270806158157742,1.408579235683831,1.573112804858189,1.514091460631845,1.335940977167862,]
            x=[1.5270370892792788,1.343892634554735,1.5035973701086018,1.4475802792553891,1.5908084495001642,1.4753564040511729,1.5173670698783965,1.4854780068915927,1.5,1.5457142857142856,1.457297052377812,1.6540057066242344,1.530523238543429,1.5940888834996152,1.565491281590335,1.59094574006128,1.4542857142857142,1.639348937658687,1.4797796418735583,1.5044858028905417,1.3805935923551218,1.637142857142857,1.589947503546717,1.362187217406885,1.4257230197710127,1.374147299612634,1.4363051713601875,1.6447619047619046,1.549511123286232,1.4582912582727898,1.5369680044480092,1.410886211801704,1.6245650739758055,1.3981894929908496,1.562903759493544,1.3710330408153724,1.3860442436367941,1.530569198001329,1.4111582286988302,1.4010841182919875,1.5946625760986557,1.5,1.6185746120780813,1.3883614949757697,1.379284202255174,1.5457142857142858,1.4085714285714286,1.540609817737493,1.6057744849985973,1.5762625770403857,1.6059493594409548,1.5155976603767385,1.4757331640753584,1.5914285714285714,1.5842754988651446,1.5514047609499784,1.4557026859901283,1.362857142857143,1.5634217708048919,1.4579437131228719,1.4692776892123405,1.5157437291177847,1.364319301597554,1.4095713119441948,1.459267353921522,1.3552380952380954,1.3469491221687895,1.5914285714285714,1.4271851121175005,1.64915255067777,1.4538432817548272,1.5357147680370264,1.6453432310344527,1.5758904895284445,1.64915255067777,1.6381685481347856,1.5253466168628684,1.60562682442706,1.3464709023007166,1.4680800243232068,1.346986933798294,1.4021959514636118,1.587948556634334,1.5787009232939635,1.4749016294026458,1.614436960588379,1.6273210988125555,1.4948767662684697,1.362857142857143,1.3430942992435593,1.4542857142857144,1.4657297388792065,1.4212594212943854,1.4547842264619737,1.6051855987848125,1.5129049137373836,1.553183468365777,1.4851569943785627,1.5340378743075496,1.4331160477647666,1.5694010009304054,1.4988927212289198,1.4952076908975787,1.5781878516701155,1.429615019623915,1.3705130956789324,1.6004913553887778,1.3578483992968373,1.4097603927313642,1.5594726728143364,1.6447619047619046,1.3772415988561928,1.6371428571428572,1.4710882226296491,1.4427895757342537,1.364042193378216,1.5995595910417162,1.62792399354195,1.4894251758000865,1.626716250706843,1.6540057066242344,1.5920819985510288,1.4988402670998084,1.3696943152270744,1.4993291886870779,1.4085714285714288,1.6381685481347856,1.486973123541911,1.620869617902615,1.34694912216879,1.3679387415718134,1.553016038758389,1.5128490329115765,1.625390063244419,1.5262271502069946,1.624808736971871,1.4227637675921117,1.5004349295893344,1.4455663747897933,1.5149337900455002,]
            e=[(0, 61),(0, 134),(0, 47),(1, 130),(1, 80),(2, 124),(2, 76),(2, 118),(3, 90),(3, 60),(3, 24),(4, 54),(4, 100),(4, 117),(5, 18),(5, 118),(5, 113),(6, 71),(6, 127),(6, 51),(7, 87),(7, 114),(7, 95),(8, 9),(8, 90),(8, 122),(9, 47),(9, 53),(9, 8),(10, 84),(10, 92),(10, 56),(11, 119),(11, 120),(12, 37),(12, 102),(12, 34),(13, 83),(13, 67),(13, 32),(14, 28),(14, 77),(14, 109),(15, 109),(15, 48),(15, 121),(16, 41),(16, 93),(16, 125),(17, 72),(17, 128),(17, 120),(18, 5),(18, 51),(18, 70),(19, 132),(19, 139),(19, 52),(20, 123),(20, 107),(20, 136),(21, 27),(21, 67),(22, 40),(22, 94),(22, 49),(23, 88),(23, 36),(23, 66),(24, 3),(24, 63),(24, 81),(25, 111),(25, 33),(26, 91),(26, 136),(26, 39),(27, 21),(27, 32),(28, 14),(28, 95),(28, 58),(29, 59),(29, 101),(29, 104),(30, 98),(30, 134),(30, 131),(31, 43),(31, 68),(31, 104),(32, 27),(32, 42),(32, 13),(33, 115),(33, 68),(33, 25),(34, 54),(34, 12),(34, 103),(35, 130),(35, 38),(35, 80),(36, 63),(36, 81),(36, 23),(37, 12),(37, 101),(37, 58),(38, 35),(38, 92),(38, 64),(39, 123),(39, 26),(39, 81),(40, 94),(40, 53),(40, 22),(41, 124),(41, 45),(41, 16),(42, 82),(42, 117),(42, 32),(43, 105),(43, 62),(43, 31),(44, 130),(44, 65),(44, 108),(45, 41),(45, 67),(45, 96),(46, 88),(46, 90),(46, 63),(47, 9),(47, 0),(47, 131),(48, 85),(48, 15),(48, 128),(49, 131),(49, 22),(49, 121),(50, 75),(50, 106),(50, 103),(51, 76),(51, 18),(51, 6),(52, 60),(52, 19),(52, 91),(53, 40),(53, 9),(53, 112),(54, 116),(54, 4),(54, 34),(55, 73),(55, 76),(55, 96),(56, 10),(56, 138),(56, 79),(57, 65),(57, 125),(58, 28),(58, 106),(58, 37),(59, 29),(59, 138),(59, 79),(60, 3),(60, 52),(60, 122),(61, 0),(61, 139),(61, 122),(62, 43),(62, 107),(62, 78),(63, 36),(63, 46),(63, 24),(64, 127),(64, 38),(64, 70),(65, 44),(65, 57),(66, 129),(66, 23),(67, 45),(67, 13),(67, 21),(68, 31),(68, 138),(68, 33),(69, 74),(69, 117),(70, 99),(70, 64),(70, 18),(71, 100),(71, 137),(71, 6),(72, 133),(72, 17),(73, 82),(73, 55),(73, 100),(74, 86),(74, 69),(75, 126),(75, 50),(76, 55),(76, 2),(76, 51),(77, 85),(77, 14),(77, 119),(78, 105),(78, 62),(79, 59),(79, 102),(79, 56),(80, 1),(80, 35),(80, 89),(81, 36),(81, 39),(81, 24),(82, 83),(82, 42),(82, 73),(83, 82),(83, 13),(83, 96),(84, 10),(84, 127),(84, 137),(85, 77),(85, 128),(85, 48),(86, 74),(86, 126),(86, 116),(87, 132),(87, 91),(87, 7),(88, 46),(88, 23),(89, 111),(89, 80),(90, 3),(90, 46),(90, 8),(91, 26),(91, 87),(91, 52),(92, 10),(92, 38),(92, 111),(93, 99),(93, 16),(93, 113),(94, 40),(94, 135),(94, 22),(95, 28),(95, 101),(95, 7),(96, 83),(96, 55),(96, 45),(97, 124),(97, 118),(97, 113),(98, 132),(98, 109),(98, 30),(99, 93),(99, 108),(99, 70),(100, 71),(100, 73),(100, 4),(101, 29),(101, 37),(101, 95),(102, 12),(102, 137),(102, 79),(103, 116),(103, 50),(103, 34),(104, 114),(104, 29),(104, 31),(105, 115),(105, 43),(105, 78),(106, 50),(106, 119),(106, 58),(107, 62),(107, 20),(108, 44),(108, 99),(108, 125),(109, 98),(109, 15),(109, 14),(110, 112),(110, 135),(111, 92),(111, 89),(111, 25),(112, 110),(112, 53),(113, 93),(113, 5),(113, 97),(114, 136),(114, 104),(114, 7),(115, 105),(115, 33),(116, 54),(116, 86),(116, 103),(117, 42),(117, 4),(117, 69),(118, 2),(118, 5),(118, 97),(119, 11),(119, 77),(119, 106),(120, 11),(120, 17),(121, 133),(121, 15),(121, 49),(122, 60),(122, 61),(122, 8),(123, 129),(123, 20),(123, 39),(124, 41),(124, 2),(124, 97),(125, 108),(125, 16),(125, 57),(126, 75),(126, 86),(127, 84),(127, 64),(127, 6),(128, 85),(128, 48),(128, 17),(129, 123),(129, 66),(130, 1),(130, 44),(130, 35),(131, 49),(131, 47),(131, 30),(132, 98),(132, 87),(132, 19),(133, 72),(133, 135),(133, 121),(134, 0),(134, 30),(134, 139),(135, 133),(135, 94),(135, 110),(136, 26),(136, 114),(136, 20),(137, 84),(137, 71),(137, 102),(138, 59),(138, 56),(138, 68),(139, 61),(139, 134),(139, 19),]
            dual=VGroup(
                *[Line([x[ee[0]],y[ee[0]],0],[x[ee[1]],y[ee[1]],0]) for ee in e],
                # *[Circle(0.005,color=WHITE).set_fill("#9999ff",opacity=1).move_to([x[i],y[i],0]) for i in range(len(x))]
            ).move_to(3*RIGHT+DOWN).set_color(RED).stretch_to_fit_height(4).stretch_to_fit_width(4)
            dual_text=Tex("Rand.\\ Trivalent").next_to(dual,UP).set_color(RED)
            self.play(FadeIn(primal_text),FadeIn(dual_text),*[Write(p) for p in primal],*[Write(d) for d in dual])
            self.wait()
            self.play(FadeOut(primal_text),FadeOut(dual_text),*[Unwrite(p) for p in primal],*[Unwrite(d) for d in dual])
            self.wait()

            # Quad
            x=[1.2375,1.7,1.5666666666666667,1.3666666666666667,1.7,1.3418472471427636,1.3,1.5,1.4267145516246174,1.4619347068485384,1.3627708707141455,1.390907991302533,1.7,1.2375,1.3662979632548176,1.386291691587208,1.425541741428291,1.3187580803922583,1.7625,1.2375,1.6555555555555557,1.5883314463118177,1.3627708707141455,1.2375,1.3441986421698784,1.7,1.3629567225621368,1.5324971694677263,1.3666666666666667,1.6333333333333333,1.5,1.7,1.4961042040474788,1.6333333333333333,1.3562742411767752,1.3,1.388643086614323,1.3,1.599163836134393,1.3,1.4290659466517324,1.599163836134393,1.7625,1.3662979632548176,1.7625,1.3,1.4333333333333333,1.4329646299214844,1.3944350838432054,1.4775319755032117,1.7625,1.3,1.4273009567227806,1.7625,1.5324971694677263,1.2375,1.6333333333333333,1.6333333333333333,1.7625,1.5666666666666667,1.7625,1.4325959265096353,1.4654617993892107,1.360605327535022,1.4333333333333333,1.4751805804760971,1.7,1.5883314463118177,1.7,1.632775890756262,1.2375,1.3281371205883876,1.2375,1.6555555555555557,1.3,1.4991967551483627,1.4996312965881509,1.496845360121248,1.3281371205883876,1.4294375373808121,1.498327672268786,]
            y=[1.3,1.3,1.3,1.7,1.6333333333333333,1.350234427977471,1.6333333333333333,1.3,1.3985364812355074,1.3701418016454197,1.3086849752995398,1.3863478955073814,1.7,1.7,1.62157866957023,1.3057899835330264,1.3173699505990795,1.4851086134718943,1.5,1.4333333333333333,1.6555555555555557,1.3854156620083644,1.3753516419662064,1.3666666666666667,1.6477191130468196,1.3666666666666667,1.5661610598520477,1.56145682634588,1.3,1.3666666666666667,1.7,1.4333333333333333,1.3086849752995398,1.7,1.4553258404156835,1.3666666666666667,1.6921635574912643,1.3,1.494790159679213,1.5,1.5182433885270787,1.4281234930125466,1.4333333333333333,1.6882453362368963,1.6333333333333333,1.7,1.3,1.6882453362368963,1.5659082564447382,1.6921635574912643,1.3,1.4333333333333333,1.4391197465537215,1.5666666666666667,1.3614568263458797,1.5,1.3,1.6333333333333333,1.3666666666666667,1.7,1.7,1.676490672473793,1.5497021625827763,1.402009708116032,1.7,1.3057899835330264,1.5,1.563193439786142,1.5666666666666667,1.4743045508972532,1.6333333333333333,1.4443295868745083,1.5666666666666667,1.3444444444444443,1.5666666666666667,1.5998014417218507,1.6882453362368963,1.3467612010969463,1.5109962535411752,1.3086849752995398,1.4229136526917596,]
            e=[(0, 37),(1, 50),(1, 25),(1, 56),(2, 32),(2, 7),(2, 56),(2, 29),(2, 54),(3, 45),(3, 64),(3, 36),(4, 44),(4, 12),(4, 68),(4, 20),(5, 10),(5, 35),(5, 22),(6, 45),(6, 24),(6, 74),(6, 70),(7, 46),(7, 65),(7, 2),(8, 9),(8, 52),(8, 11),(9, 16),(9, 8),(9, 77),(9, 80),(10, 15),(10, 16),(10, 5),(10, 37),(11, 34),(11, 16),(11, 8),(11, 63),(12, 60),(12, 4),(12, 33),(13, 45),(14, 24),(14, 61),(14, 26),(14, 74),(15, 10),(15, 28),(15, 79),(16, 32),(16, 10),(16, 9),(16, 11),(16, 79),(16, 22),(17, 39),(17, 71),(17, 78),(18, 66),(19, 51),(20, 57),(20, 4),(20, 33),(21, 41),(21, 29),(21, 54),(22, 16),(22, 5),(22, 51),(22, 63),(23, 35),(24, 6),(24, 43),(24, 14),(25, 31),(25, 1),(25, 73),(25, 58),(26, 48),(26, 78),(26, 14),(27, 75),(27, 80),(27, 59),(27, 67),(28, 15),(28, 46),(28, 37),(29, 31),(29, 73),(29, 2),(29, 21),(30, 64),(30, 49),(30, 59),(31, 25),(31, 41),(31, 42),(31, 29),(31, 66),(32, 16),(32, 77),(32, 65),(32, 2),(33, 12),(33, 59),(33, 20),(34, 48),(34, 71),(34, 52),(34, 78),(34, 11),(35, 5),(35, 23),(35, 51),(35, 37),(36, 47),(36, 43),(36, 3),(37, 0),(37, 10),(37, 35),(37, 28),(38, 69),(38, 80),(38, 68),(38, 67),(39, 55),(39, 17),(39, 51),(39, 74),(40, 48),(40, 52),(40, 62),(41, 69),(41, 31),(41, 80),(41, 21),(42, 31),(43, 45),(43, 24),(43, 61),(43, 36),(44, 4),(45, 6),(45, 43),(45, 13),(45, 3),(46, 7),(46, 28),(46, 79),(47, 64),(47, 49),(47, 61),(47, 36),(48, 34),(48, 40),(48, 61),(48, 26),(49, 47),(49, 76),(49, 30),(50, 1),(51, 39),(51, 71),(51, 35),(51, 19),(51, 22),(52, 34),(52, 40),(52, 8),(52, 80),(53, 68),(54, 77),(54, 2),(54, 80),(54, 21),(55, 39),(56, 1),(56, 73),(56, 2),(57, 20),(57, 67),(57, 68),(57, 59),(58, 25),(59, 76),(59, 57),(59, 27),(59, 30),(59, 33),(60, 12),(61, 47),(61, 76),(61, 48),(61, 43),(61, 62),(61, 14),(62, 75),(62, 40),(62, 61),(62, 80),(63, 71),(63, 11),(63, 22),(64, 47),(64, 3),(64, 30),(65, 32),(65, 7),(65, 79),(66, 31),(66, 18),(66, 68),(66, 69),(67, 38),(67, 57),(67, 27),(68, 38),(68, 57),(68, 66),(68, 53),(68, 4),(69, 38),(69, 41),(69, 66),(70, 6),(71, 34),(71, 17),(71, 51),(71, 63),(72, 74),(73, 25),(73, 56),(73, 29),(74, 39),(74, 6),(74, 72),(74, 78),(74, 14),(75, 76),(75, 62),(75, 27),(76, 75),(76, 49),(76, 61),(76, 59),(77, 32),(77, 9),(77, 54),(78, 34),(78, 17),(78, 26),(78, 74),(79, 46),(79, 16),(79, 65),(79, 15),(80, 38),(80, 41),(80, 9),(80, 52),(80, 62),(80, 27),(80, 54),]
            primal=VGroup(
                *[Line([x[ee[0]],y[ee[0]],0],[x[ee[1]],y[ee[1]],0]) for ee in e],
                # *[Circle(0.005,color=WHITE).set_fill("#9999ff",opacity=1).move_to([x[i],y[i],0]) for i in range(len(x))]
            ).move_to(3*LEFT+DOWN).set_color(BLUE).stretch_to_fit_height(4).stretch_to_fit_width(4)
            primal_text=Tex("Rand.\\ Quadrangulation").next_to(primal,UP).set_color(BLUE)
            y=[1.3890714240424487,1.6222222222222222,1.4002994352066764,1.4974012271765746,1.3378783297093888,1.26875,1.5545800310456808,1.327624151356174,1.26875,1.73125,1.26875,1.580207153944886,1.26875,1.6579849317226638,1.4594878627975607,1.4565660158331697,1.3849564827449978,1.6722222222222223,1.5109574846895073,1.3261545294642272,1.470106503111389,1.4609574846895073,1.73125,1.73125,1.5802071539448859,1.4988708490685214,1.3773476237972873,1.3604507920426263,1.5823578088234584,1.3554019291339516,1.3117238002451614,1.672222222222222,1.4535694718661807,1.3261545294642272,1.4010104602776141,1.5244979719677265,1.3328266406864522,1.4606809571306205,1.5094878627975605,1.5545800310456808,1.26875,1.3732326824998364,1.47422144440884,1.73125,1.3589811701506793,1.426274747800995,1.4550390937581275,1.327624151356174,1.405401929133952,1.73125,1.6722222222222223,1.52302835007578,1.6302071539448861,1.6222222222222222,1.6302071539448861,1.4303896890984458,1.672222222222222,1.3539323072420049,1.3393479516013356,1.4051254015750652,1.6579849317226638,1.73125,1.3117238002451614,1.26875,1.4017690570986234,1.403932307242005,]
            x=[1.6075346645852022,1.327777777777778,1.4198324909280733,1.3753183704450014,1.41375606757252,1.3333333333333333,1.3994774085146378,1.6173244456542624,1.5333333333333332,1.6666666666666665,1.6,1.353384788755228,1.4666666666666668,1.5089403443107832,1.3036187397081416,1.3101324711827962,1.3702697990471748,1.672222222222222,1.6951022234320403,1.3813965174859195,1.3357394821602462,1.6951022234320403,1.5333333333333332,1.6,1.6144958998663388,1.5334685208355667,1.6585084478319345,1.5245978525634112,1.4550329640701931,1.6951022234320403,1.515692883419934,1.3277777777777777,1.4076779205316021,1.3313965174859195,1.3101324711827962,1.6373759010761566,1.4739400735758152,1.6862862256097126,1.3036187397081416,1.5105885196257485,1.6666666666666665,1.337910248960574,1.628559903253829,1.3333333333333335,1.4220032577284012,1.368099032246847,1.482494737588834,1.6673244456542622,1.6951022234320403,1.4,1.6222222222222222,1.3292257506855916,1.5644958998663387,1.6722222222222223,1.4033847887552278,1.5775861200070966,1.3777777777777778,1.3036187397081416,1.5663506624075298,1.6862862256097126,1.4589403443107833,1.4666666666666668,1.4656928834199339,1.4000000000000001,1.4946493079853056,1.3036187397081416,]
            e=[(0, 27),(0, 26),(0, 58),(0, 55),(1, 56),(1, 11),(1, 31),(2, 32),(2, 45),(2, 64),(2, 44),(3, 32),(3, 20),(3, 51),(3, 6),(4, 19),(4, 62),(4, 44),(4, 16),(5, 33),(5, 63),(6, 11),(6, 54),(6, 3),(6, 28),(7, 26),(7, 58),(7, 10),(7, 47),(8, 10),(8, 12),(8, 30),(9, 23),(9, 17),(10, 40),(10, 7),(10, 8),(11, 51),(11, 6),(11, 1),(11, 54),(12, 8),(12, 62),(12, 63),(13, 60),(13, 52),(13, 22),(13, 28),(14, 38),(14, 15),(14, 65),(15, 38),(15, 14),(15, 20),(15, 34),(16, 4),(16, 41),(16, 45),(16, 44),(17, 9),(17, 53),(17, 50),(18, 37),(18, 35),(18, 21),(19, 33),(19, 4),(19, 41),(19, 63),(20, 15),(20, 51),(20, 45),(20, 3),(21, 37),(21, 48),(21, 18),(22, 61),(22, 23),(22, 13),(23, 9),(23, 22),(23, 50),(24, 39),(24, 35),(24, 52),(24, 53),(25, 39),(25, 35),(25, 42),(25, 46),(26, 7),(26, 0),(26, 59),(26, 47),(27, 0),(27, 36),(27, 58),(27, 64),(28, 60),(28, 39),(28, 6),(28, 13),(29, 48),(29, 59),(29, 47),(30, 36),(30, 62),(30, 8),(30, 58),(31, 43),(31, 1),(31, 56),(32, 45),(32, 46),(32, 2),(32, 3),(33, 19),(33, 5),(33, 41),(33, 57),(34, 15),(34, 41),(34, 57),(34, 65),(35, 42),(35, 24),(35, 18),(35, 25),(36, 27),(36, 62),(36, 44),(36, 30),(37, 42),(37, 21),(37, 59),(37, 18),(38, 15),(38, 51),(38, 14),(39, 52),(39, 24),(39, 25),(39, 28),(40, 10),(40, 47),(41, 19),(41, 33),(41, 34),(41, 16),(42, 37),(42, 35),(42, 55),(42, 25),(43, 49),(43, 31),(44, 4),(44, 36),(44, 2),(44, 16),(45, 32),(45, 20),(45, 2),(45, 16),(46, 32),(46, 64),(46, 55),(46, 25),(47, 26),(47, 29),(47, 40),(47, 7),(48, 29),(48, 21),(48, 59),(49, 61),(49, 43),(49, 56),(50, 52),(50, 23),(50, 53),(50, 17),(51, 38),(51, 20),(51, 11),(51, 3),(52, 39),(52, 24),(52, 50),(52, 13),(53, 24),(53, 50),(53, 17),(54, 60),(54, 6),(54, 11),(54, 56),(55, 0),(55, 42),(55, 46),(55, 64),(56, 49),(56, 1),(56, 54),(56, 31),(57, 33),(57, 34),(57, 65),(58, 27),(58, 0),(58, 7),(58, 30),(59, 37),(59, 26),(59, 29),(59, 48),(60, 13),(60, 61),(60, 54),(60, 28),(61, 60),(61, 49),(61, 22),(62, 4),(62, 36),(62, 12),(62, 30),(63, 19),(63, 5),(63, 12),(64, 27),(64, 46),(64, 2),(64, 55),(65, 14),(65, 34),(65, 57),]
            dual=VGroup(
                *[Line([x[ee[0]],y[ee[0]],0],[x[ee[1]],y[ee[1]],0]) for ee in e],
                # *[Circle(0.005,color=WHITE).set_fill("#9999ff",opacity=1).move_to([x[i],y[i],0]) for i in range(len(x))]
            ).move_to(3*RIGHT+DOWN).set_color(RED).stretch_to_fit_height(4).stretch_to_fit_width(4)
            dual_text=Tex("Rand.\\ Tetravalent").next_to(dual,UP).set_color(RED)
            self.play(FadeIn(primal_text),FadeIn(dual_text),*[Write(p) for p in primal],*[Write(d) for d in dual])
            self.wait()
            self.play(FadeOut(primal_text),FadeOut(dual_text),*[Unwrite(p) for p in primal],*[Unwrite(d) for d in dual])
            self.wait()


        self.play(Transform(subheading,Tex("Other codes").move_to(subheading)))
        self.wait()


        DIAG=np.array([0.5,np.sqrt(3)/2,0])

        Tup=Group(
            Polygon(ORIGIN,DIAG,DIAG+RIGHT,2*RIGHT,color=RED,stroke_width=1).set_fill(opacity=1),
            Polygon(3*RIGHT,2*RIGHT,DIAG+RIGHT,2*DIAG+RIGHT,color=BLUE,stroke_width=1).set_fill(opacity=1),
            Polygon(DIAG,3*DIAG,2*DIAG+RIGHT,DIAG+RIGHT,color=GREEN,stroke_width=1).set_fill(opacity=1),
        )
        Lup=Group(
            Line(DIAG,DIAG+RIGHT,color=WHITE),
            Line(2*RIGHT,DIAG+RIGHT,color=WHITE),
            Line(RIGHT+2*DIAG,DIAG+RIGHT,color=WHITE),
            Line(ORIGIN,DIAG,color=WHITE),
            Line(3*DIAG,2*DIAG+RIGHT,color=WHITE),
        )
        Tdown=Tup.copy().rotate(-60*DEGREES).align_to(Tup,UP).align_to(Tup.get_top(),LEFT).flip()
        Tdown[0].set_color(GREEN)
        Tdown[2].set_color(RED)
        Ldown=Lup.copy().rotate(-60*DEGREES).align_to(Lup,UP).align_to(Lup.get_top(),LEFT).flip().shift(RIGHT/2)

        Ncc=4
        colourcode=Group()
        for x in range(Ncc):
            for y in range(Ncc):
                if x+y<Ncc:
                    for g in Tup.copy().shift(3*x*RIGHT+3*y*DIAG):
                        colourcode.add(g)
        for x in range(Ncc-1):
            for y in range(Ncc-1):
                if x+y<Ncc-1:
                    for g in Tdown.copy().shift(3*x*RIGHT+3*y*DIAG):
                        colourcode.add(g)
        for x in range(Ncc):
            for y in range(Ncc):
                if x+y<Ncc:
                    for g in Lup.copy().shift(3*x*RIGHT+3*y*DIAG):
                        colourcode.add(g)
        for x in range(Ncc-1):
            for y in range(Ncc-1):
                if x+y<Ncc-1:
                    for g in Ldown.copy().shift(3*x*RIGHT+3*y*DIAG):
                        colourcode.add(g)
        colourcode.move_to(0.5*DOWN+3*LEFT).height=3.5#.stretch_to_fit_height(4).stretch_to_fit_width(4)
        colourcode.add(Tex("Colour Code").next_to(colourcode,DOWN).scale(0.75))

        ssc_cell=Group(
            Polygon(UP,ORIGIN,RIGHT,color=WHITE).set_fill(RED,opacity=1),
            Polygon(2*RIGHT+2*UP,2*RIGHT+UP,RIGHT+2*UP,color=WHITE).set_fill(RED,opacity=1),
            Polygon(UP,2*UP,2*UP+RIGHT,color=WHITE).set_fill(BLUE,opacity=1),
            Polygon(RIGHT,2*RIGHT,2*RIGHT+UP,color=WHITE).set_fill(BLUE,opacity=1),
        )

        Nssc=4
        ssc=Group()
        for x in range(Nssc):
            for y in range(Nssc):
                for g in ssc_cell.copy().move_to(2*x*RIGHT+2*y*UP):
                    ssc.add(g)
        ssc.move_to(0.5*DOWN+3*RIGHT).height=3.5#.stretch_to_fit_height(4).stretch_to_fit_width(4)
        ssc.add(Tex("Subsystem Surface Code").next_to(ssc,DOWN).scale(0.75))

        self.play(*[Write(cc) for cc in colourcode[:-1]], FadeIn(colourcode[-1]))
        self.wait()

        self.play(*[Write(s) for s in ssc[:-1]], FadeIn(ssc[-1]))
        self.wait()

        self.play(
            FadeOut(heading),
            FadeOut(subheading),
            FadeOut(colourcode),
            FadeOut(ssc),
        )
        self.wait()

class Results(Scene):
    def construct(self):
        heading = toc[5].copy().move_to(ORIGIN).scale(1.5).to_corner(UP)
        self.play(FadeIn(toc))
        self.wait()
        self.play(FadeOut(toc), ReplacementTransform(toc[5],heading))
        self.wait()

        rows=VGroup(
            Tex(r"~","Observed","Upper bound","Observed","Upper bound","Observed","Upper bound"),

            # Tex(r"\textbf{Subsystem SC}",r"\phantom{derp}",r"\phantom{derp}",r"\phantom{derp}",r"\phantom{derp}",r"\phantom{derp}",r"\phantom{derp}"),
            Tex(r"\textbf{Surface code (reg.)}","~","~","~","~","~","~"),
            Tex(r"\qquad Square","10.917(5)\\%","10.9187\\%","10.917(5)\\%","10.9187\\%","18.81(3)\\%","18.9(3)\\%"),
            Tex(r"\qquad Tri./Hex.","16.341(7)\\%","16.4015\\%","6.748(5)\\%","6.7407\\%","13.81(7)\\%","?"),
            Tex(r"\qquad Kag./Rho.","9.875(5)\\%","?","11.910(6)\\%","?","18.09(4)\\%","?"),
            Tex(r"\qquad T.H./Asa.","4.297(7)\\%","?","20.701(13)\\%","?","9.07(8)\\%","?"),

            # Tex(r"\textbf{Subsystem SC}",r"\phantom{derp}",r"\phantom{derp}",r"\phantom{derp}",r"\phantom{derp}",r"\phantom{derp}",r"\phantom{derp}"),
            Tex(r"\textbf{Surface code (irr.)}","~","~","~","~","~","~"),
            Tex(r"\qquad Rand.\ Tri.","17.128(15)\\%","?","6.237(9)\\%","?","12.85(3)\\%","?"),
            Tex(r"\qquad Rand.\ Quad.","12.195(12)\\%","?","9.715(11)\\%","?","18.05(3)\\%","?"),

            Tex(r"\textbf{Subsystem SC}","~","~","~","~","~","~"),
            Tex(r"\qquad Square","6.705(13)\\%","6.7407\\%","6.705(13)\\%","6.7407\\%","11.23(3)\\%","?"),

            Tex(r"\textbf{Colour code}","~","~","~","~","~","~"),
            Tex(r"\qquad Hexagonal","10.910(5)\\%","10.9(2)\\%","10.910(5)\\%","10.9(2)\\%","18.68(3)\\%","18.9(3)\\%"),
        )

        X=7
        Y=13


        cols=VGroup(*[VGroup() for _ in range(X)])
        for x in range(X):
            for y in range(Y):
                cols[x].add(rows[y][x].move_to(.75*y*DOWN))
        cols.arrange(RIGHT,buff=0.5)

        for y in range(1,Y):
            cols[0][y].align_to(cols[0][0],2*LEFT)
        for y in [1,6,9,11]:
            cols[0][y].shift(LEFT)

        cols[0].shift(2*LEFT)

        rows[1:6].shift(0.2*DOWN)
        rows[6:9].shift(0.4*DOWN)
        rows[9:11].shift(0.6*DOWN)
        rows[11:].shift(0.8*DOWN)

        cols[1:3].shift(0.5*RIGHT)
        cols[3:5].shift(1.5*RIGHT)
        cols[5:7].shift(3.0*RIGHT)
        cols[7:9].shift(4.5*RIGHT)


        table=VGroup(rows,VGroup(),VGroup()).scale(0.5)

        l=table.get_left()[0]
        r=table.get_right()[0]
        y=rows[1].get_top()[1]+0.1
        table[1].add(Line([l,y,0],[r,y,0],stroke_width=2))
        y=rows[6].get_top()[1]+0.1
        table[1].add(Line([l,y,0],[r,y,0],stroke_width=2))
        y=rows[9].get_top()[1]+0.1
        table[1].add(Line([l,y,0],[r,y,0],stroke_width=2))
        y=rows[11].get_top()[1]+0.1
        table[1].add(Line([l,y,0],[r,y,0],stroke_width=2))

        table[2].add(Tex(r"\textbf{Bit-flip}").scale(0.5).next_to(cols[1:3],UP))
        table[2].add(Tex(r"\textbf{Phase-flip}").scale(0.5).next_to(cols[3:5],UP))
        table[2].add(Tex(r"\textbf{Depolarising}").scale(0.5).next_to(cols[5:7],UP))
        # y=rows[0].get_top()[1]+0.1
        # table.add(Line([l,y,0],[r,y,0],stroke_width=2))

        y=table.get_top()[1]+0.2
        table[1].add(Line([l,y,0],[r,y,0],stroke_width=5))
        y=table.get_bottom()[1]-0.2
        table[1].add(Line([l,y,0],[r,y,0],stroke_width=5))

        l=cols[1].get_left()[0]
        r=cols[2].get_right()[0]
        y=rows[0].get_top()[1]+0.1
        table[1].add(Line([l,y,0],[r,y,0],stroke_width=2))

        l=cols[3].get_left()[0]
        r=cols[4].get_right()[0]
        y=rows[0].get_top()[1]+0.1
        table[1].add(Line([l,y,0],[r,y,0],stroke_width=2))

        l=cols[5].get_left()[0]
        r=cols[6].get_right()[0]
        y=rows[0].get_top()[1]+0.1
        table[1].add(Line([l,y,0],[r,y,0],stroke_width=2))


        codes=cols[0].set_color(WHITE)
        bitflip=VGroup(table[2][0],cols[1:3]).set_color(BLUE)
        phaseflip=VGroup(table[2][1],cols[3:5]).set_color(RED)
        depolarising=VGroup(table[2][2],cols[5:7]).set_color(YELLOW)

        table.scale(0.9).move_to(DOWN/2)

        # self.add(table)
        # self.wait()

        contents=VGroup();
        for x in range(X):
            for y in range(Y):
                contents.add(rows[y][x])
        for t in table[1]:
            contents.add(t)
        for t in table[2]:
            contents.add(t)

        # self.play(Write(contents))
        self.play(*[Write(c) for c in contents])
        self.wait()

        # self.play(Indicate(cols[0],color=WHITE))
        self.play(*[Indicate(c,color=WHITE) for c in cols[0]])
        self.wait()

        # self.play(Indicate(rows[1:6],color=WHITE))
        self.play(*[Indicate(rr,color=WHITE) for r in rows[1:6] for rr in r])
        self.wait()

        # self.play(Indicate(rows[6:9],color=WHITE))
        self.play(*[Indicate(rr,color=WHITE) for r in rows[6:9] for rr in r])
        self.wait()

        # self.play(Indicate(rows[9:11],color=WHITE))
        self.play(*[Indicate(rr,color=WHITE) for r in rows[9:11] for rr in r])
        self.wait()

        # self.play(Indicate(rows[11:],color=WHITE))
        self.play(*[Indicate(rr,color=WHITE) for r in rows[11:] for rr in r])
        self.wait()

        # self.play(Indicate(bitflip,color=WHITE))
        # self.wait()
        # self.play(Indicate(phaseflip,color=WHITE))
        # self.wait()
        # self.play(Indicate(depolarising,color=WHITE))
        # self.wait()
        for i in range(3):
            self.play(
                Indicate(table[2][i],color=WHITE),
                *[Indicate(c,color=WHITE) for c in cols[2*i+1]],
                *[Indicate(c,color=WHITE) for c in cols[2*i+2]],
            )
            self.wait()

        # self.play(
        #     Indicate(cols[1],color=WHITE),
        #     Indicate(cols[3],color=WHITE),
        #     Indicate(cols[5],color=WHITE),
        # )
        self.play(
            *[Indicate(c,color=WHITE) for c in cols[1]],
            *[Indicate(c,color=WHITE) for c in cols[3]],
            *[Indicate(c,color=WHITE) for c in cols[5]],

        )
        self.wait()

        # self.play(
        #     Indicate(cols[2],color=WHITE),
        #     Indicate(cols[4],color=WHITE),
        #     Indicate(cols[6],color=WHITE),
        # )
        self.play(
            *[Indicate(c,color=WHITE) for c in cols[2]],
            *[Indicate(c,color=WHITE) for c in cols[4]],
            *[Indicate(c,color=WHITE) for c in cols[6]],

        )
        self.wait()

        self.play(FadeOut(table))





        t1=Tex("Zero-rate hashing bound:",color=YELLOW).shift(3*UP/2)
        t2=MathTex(r"h(\tau_X)+h(\tau_Z)\leq 1").shift(3*UP/4).set_color(YELLOW)
        t3=Tex("We compare ","our results", " to:","Fujii et.al.",r"\texttt{arXiv:1202.2743}\qquad\texttt{doi:d5sb}").scale(0.75).set_color(YELLOW)
        t3[1].set_color_by_gradient(RED,GREEN)
        t3[3:].set_color(BLUE)
        t3[0:3].next_to(t2,DOWN,buff=1.5)
        t3[3].next_to(t3[0:3],DOWN)
        t3[4].scale(0.75).next_to(t3[3],DOWN)

        ax=Axes(
            x_range=[3,24,1],
            y_range=[3,24,1],
            x_length=5,
            y_length=5,
            axis_config={
                "include_tip": False,
                "include_numbers": True,
                "numbers_to_exclude": [r for r in range(3,25) if np.mod(r,5)!=0]
            },
        ).shift(0.5*DOWN+3.5*RIGHT)
        for x in range(22):
            if np.mod(x,5)!=2:
                ax[0][1][x].set_stroke(width=0)
                ax[1][1][x].set_stroke(width=0)



        x=[3.3000000000000003,3.4000000000000004,3.5000000000000004,3.5999999999999996,3.6999999999999997,3.8,3.9,4.0,4.1000000000000005,4.2,4.3,4.3999999999999995,4.5,4.6,4.7,4.8,4.9,5.0,5.1,5.2,5.3,5.4,5.5,5.6000000000000005,5.7,5.800000000000001,5.8999999999999995,6.0,6.1,6.2,6.3,6.4,6.5,6.6000000000000005,6.7,6.800000000000001,6.9,7.000000000000001,7.1,7.199999999999999,7.3,7.3999999999999995,7.5,7.6,7.7,7.8,7.9,8.0,8.1,8.200000000000001,8.3,8.4,8.5,8.6,8.7,8.799999999999999,8.9,9.0,9.1,9.2,9.3,9.4,9.5,9.6,9.700000000000001,9.8,9.9,10.0,10.100000000000001,10.2,10.299999999999999,10.4,10.5,10.6,10.7,10.8,10.9,11.0,11.1,11.200000000000001,11.3,11.4,11.5,11.600000000000001,11.700000000000001,11.799999999999999,11.899999999999999,12.0,12.1,12.2,12.3,12.4,12.5,12.6,12.7,12.8,12.9,13.0,13.100000000000001,13.200000000000001,13.3,13.4,13.5,13.600000000000001,13.700000000000001,13.8,13.900000000000002,14.000000000000002,14.099999999999998,14.2,14.299999999999999,14.399999999999999,14.499999999999998,14.6,14.7,14.799999999999999,14.899999999999999,15.0,15.1,15.2,15.299999999999999,15.4,15.5,15.6,15.7,15.8,15.9,16.0,16.1,16.2,16.3,16.400000000000002,16.5,16.6,16.7,16.8,16.900000000000002,17.0,17.1,17.2,17.299999999999997,17.4,17.5,17.599999999999998,17.7,17.8,17.9,18.0,18.099999999999998,18.2,18.3,18.4,18.5,18.6,18.7,18.8,18.9,19.0,19.1,19.2,19.3,19.400000000000002,19.5,19.6,19.7,19.8,19.900000000000002,20.0,20.1,20.200000000000003,20.3,20.4,20.5,20.599999999999998,20.7,20.8,20.9,21.0,21.099999999999998,21.2,21.3,21.4,21.5,21.6,21.7,21.8,21.9,22.0,22.1,22.2,22.3,22.400000000000002,22.5,22.6,22.7,22.8,22.900000000000002,23.0,23.1,23.200000000000003,23.3,23.400000000000002,23.5,23.599999999999998,23.7,23.799999999999997,23.9,24.0,]
        y=[23.7457275390625,23.4588623046875,23.1781005859375,22.9034423828125,22.6348876953125,22.3724365234375,22.1160888671875,21.8658447265625,21.6156005859375,21.3775634765625,21.1395263671875,20.9075927734375,20.6756591796875,20.4498291015625,20.2301025390625,20.0103759765625,19.7967529296875,19.5892333984375,19.3817138671875,19.1802978515625,18.9788818359375,18.7774658203125,18.5882568359375,18.3929443359375,18.2098388671875,18.0206298828125,17.8375244140625,17.6605224609375,17.4835205078125,17.3065185546875,17.1356201171875,16.9647216796875,16.7938232421875,16.6290283203125,16.4703369140625,16.3055419921875,16.1468505859375,15.9881591796875,15.8355712890625,15.6829833984375,15.5303955078125,15.3839111328125,15.2374267578125,15.0909423828125,14.9444580078125,14.8040771484375,14.6636962890625,14.5233154296875,14.3890380859375,14.2547607421875,14.1204833984375,13.9862060546875,13.8580322265625,13.7237548828125,13.5955810546875,13.4735107421875,13.3453369140625,13.2232666015625,13.1011962890625,12.9791259765625,12.8631591796875,12.7410888671875,12.6251220703125,12.5091552734375,12.3931884765625,12.2833251953125,12.1673583984375,12.0574951171875,11.9476318359375,11.8377685546875,11.7279052734375,11.6241455078125,11.5203857421875,11.4166259765625,11.3128662109375,11.2091064453125,11.1053466796875,11.0076904296875,10.9039306640625,10.8062744140625,10.7086181640625,10.6109619140625,10.5194091796875,10.4217529296875,10.3302001953125,10.2325439453125,10.1409912109375,10.0494384765625,9.9639892578125,9.8724365234375,9.7808837890625,9.6954345703125,9.6099853515625,9.5184326171875,9.4329833984375,9.3536376953125,9.2681884765625,9.1827392578125,9.1033935546875,9.0179443359375,8.9385986328125,8.8592529296875,8.7799072265625,8.7005615234375,8.6212158203125,8.5418701171875,8.4686279296875,8.3892822265625,8.3160400390625,8.2366943359375,8.1634521484375,8.0902099609375,8.0169677734375,7.9437255859375,7.8765869140625,7.8033447265625,7.7301025390625,7.6629638671875,7.5897216796875,7.5225830078125,7.4554443359375,7.3883056640625,7.3211669921875,7.2540283203125,7.1868896484375,7.1258544921875,7.0587158203125,6.9915771484375,6.9305419921875,6.8695068359375,6.8023681640625,6.7413330078125,6.6802978515625,6.6192626953125,6.5582275390625,6.4971923828125,6.4361572265625,6.3812255859375,6.3201904296875,6.2591552734375,6.2042236328125,6.1492919921875,6.0882568359375,6.0333251953125,5.9783935546875,5.9234619140625,5.8685302734375,5.8135986328125,5.7586669921875,5.7037353515625,5.6488037109375,5.5999755859375,5.5450439453125,5.4901123046875,5.4412841796875,5.3924560546875,5.3375244140625,5.2886962890625,5.2398681640625,5.1910400390625,5.1422119140625,5.0933837890625,5.0445556640625,4.9957275390625,4.9468994140625,4.8980712890625,4.8492431640625,4.8065185546875,4.7576904296875,4.7149658203125,4.6661376953125,4.6234130859375,4.5806884765625,4.5318603515625,4.4891357421875,4.4464111328125,4.4036865234375,4.3609619140625,4.3182373046875,4.2755126953125,4.2327880859375,4.1900634765625,4.1473388671875,4.1046142578125,4.0679931640625,4.0252685546875,3.9886474609375,3.9459228515625,3.9093017578125,3.8665771484375,3.8299560546875,3.7933349609375,3.7506103515625,3.7139892578125,3.6773681640625,3.6407470703125,3.6041259765625,3.5675048828125,3.5308837890625,3.4942626953125,3.4576416015625,3.4210205078125,3.3843994140625,3.3477783203125,3.3172607421875,3.2806396484375,3.2440185546875,3.2135009765625,]
        hashing_bound = ax.get_line_graph(
            x_values = x,
            y_values = y,
            vertex_dot_radius=0,
            line_color=WHITE,
            stroke_width = 1,
        )



        # # Square
        # mx=10.3; tx=10.917; dtx=0.005;
        # mz=10.3; tz=10.917; dtz=0.005;
        # # Triangular/Hexagonal
        # mx=15.9; tx=16.341; dtx=0.007;
        # mz=6.5;  tz=6.748;  dtz=0.005;
        # # Kagoma/Rhombille
        # mx=9.5;  tx=9.875;  dtz=0.005;
        # mz=11.6; tz=11.910; dtx=0.006;
        # # Trihexa/Asanoha
        # mz=20.5; tz=20.701; dtz=0.013;
        # mx=4.1;  tx=4.297;  dtx=0.007;
        # # Random tri/vor
        # tx=17.128; dtx=0.015;
        # tz=6.237;  dtz=0.009;
        # # Random quad/tetra
        # tx=12.195; dtx=0.012;
        # tz=9.715;  dtz=0.011;

        MWPM = ax.get_line_graph(
            x_values = [10.3,15.9,9.5,20.5,6.5,11.6,4.1,18],
            y_values = [10.3,6.5,11.6,4.1,15.9,9.5,20.5,24],
            vertex_dot_style=dict(stroke_width=1,  fill_color=BLUE),
            stroke_width = 0,
        )

        TN_reg = ax.get_line_graph(
            x_values = [10.917,16.341,9.875,20.701,6.748,11.910,4.297,18],
            y_values = [10.917,6.748,11.910,4.297,16.341,9.875,20.701,22],
            vertex_dot_style=dict(stroke_width=1,  fill_color=RED),
            stroke_width = 0,
        )

        TN_irr = ax.get_line_graph(
            x_values = [17.128,12.195,6.237,9.715,18],
            y_values = [6.237,9.715,17.128,12.195,20],
            vertex_dot_style=dict(stroke_width=1,  fill_color=GREEN),
            stroke_width = 0,
        )

        axis_labels=MathTex(r"\tau_X~(\%)",r"\tau_Z~(\%)").scale(0.75)
        axis_labels[0].next_to(ax,DOWN)
        axis_labels[1].rotate(90*DEGREES).next_to(ax,LEFT)

        legend=Group(
            Tex("MWPM",color=BLUE).scale(0.5).next_to(ax.coords_to_point(18,24),RIGHT),
            Tex("TN (reg.)",color=RED).scale(0.5).next_to(ax.coords_to_point(18,22),RIGHT),
            Tex("TN (irr.)",color=GREEN).scale(0.5).next_to(ax.coords_to_point(18,20),RIGHT),
        )
        code_labels=Group(
            Tex("Square").scale(0.4).rotate(45*DEGREES).next_to(TN_reg['vertex_dots'][0],UR,buff=0.1),
            Tex("Triangular").scale(0.4).rotate(45*DEGREES).next_to(TN_reg['vertex_dots'][1],UR,buff=0.1),
            Tex("Kagome").scale(0.4).rotate(45*DEGREES).next_to(TN_reg['vertex_dots'][2],UR,buff=0.1),
            Tex("Asaonoha").scale(0.4).rotate(45*DEGREES).next_to(TN_reg['vertex_dots'][3],UR,buff=0.1),
            Tex("Hexagonal").scale(0.4).rotate(45*DEGREES).next_to(TN_reg['vertex_dots'][4],UR,buff=0.1),
            Tex("Rhombille").scale(0.4).rotate(45*DEGREES).next_to(TN_reg['vertex_dots'][5],UR,buff=0.1),
            Tex("Trunc.\ Hex.").scale(0.4).rotate(45*DEGREES).next_to(TN_reg['vertex_dots'][6],UR,buff=0.1),
            Tex("Rand.\ Triangulation").scale(0.4).rotate(45*DEGREES).next_to(TN_irr['vertex_dots'][0],UR,buff=0.1),
            Tex("Rand.\ Quadrangulation").scale(0.4).rotate(45*DEGREES).next_to(TN_irr['vertex_dots'][1],(UR+RIGHT)*.75+.35*DOWN+.25*DR,buff=0.1),
            Tex("Rand.\ Trivalent").scale(0.4).rotate(45*DEGREES).next_to(TN_irr['vertex_dots'][2],UR,buff=0.1),
            Tex("Rand.\ Tetravalent").scale(0.4).rotate(45*DEGREES).next_to(TN_irr['vertex_dots'][3],(UR+UP)*.75+.35*LEFT+.25*UL,buff=0.1),
        )

        self.play(FadeIn(t1))
        self.play(Write(t2))
        self.wait()

        self.play(t1.animate.shift(4*LEFT),t2.animate.shift(4*LEFT),FadeIn(t3.shift(4*LEFT)))
        self.play(FadeIn(ax),FadeIn(axis_labels))
        self.wait()

        self.play(FadeIn(hashing_bound))
        self.wait()

        self.play(FadeIn(MWPM),Write(legend[0]),*[Write(c) for c in code_labels[:7]])
        self.wait()

        self.play(FadeIn(TN_reg),Write(legend[1]))
        self.wait()

        self.play(FadeIn(TN_irr),Write(legend[2]),*[Write(c) for c in code_labels[7:]])
        self.wait()

        self.play(FadeOut(t3),FadeOut(t1),t2.animate.shift(1.25*UP))
        self.wait()

        X=3;
        Y=9
        rows=Group(
            Tex("~", "{MWPM}", "{TN}"),
            Tex("\\textbf{Regular}", "~", "~"),
            Tex("Square", "0.957", "0.9948(3)"),
            Tex("Tri./Hex.", "0.979", "0.9989(3)"),
            Tex("Kag./Rho.", "0.971", "0.9918(3)"),
            Tex("T.H./Asa.", "0.979", "0.9915(6)"),
            Tex("\\textbf{Irregular}", "~", "~"),
            Tex("Rand.Tri.", "?", "0.9974(7)"),
            Tex("Rand.Quad.", "?", "0.9948(7)"),
        )

        cols=Group(*[Group() for _ in range(X)])
        for x in range(X):
            for y in range(Y):
                cols[x].add(rows[y][x].move_to(.75*y*DOWN+0.5*rows[y][x].height*DOWN))
        cols.arrange(RIGHT,buff=0.5)

        for y in range(1,Y):
            cols[0][y].align_to(cols[0][0],2*LEFT)
        cols[0].shift(LEFT)
        for y in [1,6]:
            cols[0][y].shift(LEFT)

        cols[1][2:].set_color(BLUE)
        cols[2][2:6].set_color(RED)
        cols[2][6:].set_color(GREEN)
        cols.scale(0.5).next_to(t2,DOWN,buff=1.5)

        rows[0].shift(0.1*UP)
        rows[-3:].shift(0.1*DOWN)
        rows[0][-1].align_to(rows[0][-2],DOWN)

        table=Group()

        l=rows.get_left()[0]
        r=rows.get_right()[0]
        y=rows[1].get_top()[1]+0.1
        table.add(Line([l,y,0],[r,y,0],stroke_width=1))
        y=rows[6].get_top()[1]+0.1
        table.add(Line([l,y,0],[r,y,0],stroke_width=1))
        y=rows.get_bottom()[1]-0.1
        table.add(Line([l,y,0],[r,y,0],stroke_width=1))
        table.add(Tex("\\textbf{Entropy}").scale(0.5).next_to(cols[1:3],UP))
        y=table.get_top()[1]+0.1
        table.add(Line([l,y,0],[r,y,0],stroke_width=3))
        y=table.get_bottom()[1]-0.1
        table.add(Line([l,y,0],[r,y,0],stroke_width=3))
        l=cols[1].get_left()[0]
        r=cols[2].get_right()[0]
        y=table.get_bottom()[1]-0.1
        y=rows[0].get_top()[1]+0.1
        table.add(Line([l,y,0],[r,y,0],stroke_width=1))

        self.play(*[Write(t) for t in table], *[FadeIn(rr) for r in rows for rr in r])
        self.wait()

        # self.play(*[Indicate(x) for x in cols[1][2:]])
        # self.wait()
        #
        # self.play(*[Indicate(x) for x in cols[2][2:]])
        # self.wait()


        self.play(
            FadeOut(heading),
            FadeOut(t2),
            FadeOut(table),
            FadeOut(rows),
            FadeOut(ax),
            FadeOut(axis_labels),
            FadeOut(hashing_bound),
            FadeOut(MWPM),
            FadeOut(TN_reg),
            FadeOut(TN_irr),
            FadeOut(legend),
            FadeOut(code_labels),
        )

        self.wait()

class Conclusion(Scene):
    def construct(self):
        heading = toc[6].copy().move_to(ORIGIN).scale(1.5).to_corner(UP)
        self.play(FadeIn(toc))
        self.wait()
        self.play(FadeOut(toc), ReplacementTransform(toc[6],heading))
        self.wait()

        temp = TexTemplate()
        temp.add_to_preamble(r"\usepackage{marvosym} \usepackage{fontawesome}")

        email=Tex(r"\faEnvelope~~\texttt{me@christopherchubb.com}", tex_template=temp)
        website=Tex(r"\faLink~~\texttt{christopherchubb.com}", tex_template=temp)
        twitter=Tex(r"\faTwitter~~\texttt{@QuantumChubb}", tex_template=temp)


        summary=Tex("Tensor network decoding is highly\\\\","flexible"," and ","effective"," for 2D codes").scale(.75).move_to([-3.5,1.5,0])#.set_color(YELLOW)
        summary[1].set_color(BLUE)
        summary[3].set_color(GREEN)

        arxiv=Tex(r"\texttt{\bfseries arXiv:2101.04125}").next_to(summary,DOWN,buff=.5)

        future=Tex(
            "Future directions: \\\\",
            "\\textbullet Measurement errors \\\\",
            "\\textbullet 3D, hyperbolic, LDPC \\\\",
            "\\textbullet Non-Pauli noise \\\\",
            "\\textbullet Optimise run-times \\\\",
        ).scale(.75).arrange(DOWN,aligned_edge=LEFT).move_to([-3.75,-2,0])
        future[0].shift(LEFT/2)

        socials=VGroup(email,website,twitter).arrange(DOWN).scale(0.75).move_to([4,1,0]).align_to(summary,UP)

        self.play(Write(arxiv),Write(summary))
        self.wait()
        self.play(Write(future))
        self.wait()
        self.play(Write(socials))
        self.wait()
