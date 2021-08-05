from manim import *

import os
import shutil

config.video_dir= "./video_slides"
config.flush_cache = True
config.disable_caching = True
class SlideScene(Scene):
    breaks=[0]
    video_slides_dir="./video_slides"
    def setup(self):
        super(SlideScene, self).setup()
        self.breaks=[0]

    def slide_break(self,t=0.5):
        self.breaks+=[self.renderer.time+t/2]
        self.wait(t)

    def save_times(self):
        self.breaks+=[self.renderer.time]
        out=""
        dirname=os.path.dirname(self.renderer.file_writer.movie_file_path)
        for i in range(len(self.breaks)-1):
            out+=f"<p class=\"fragment\" type='video' time_start={self.breaks[i]} time_end={self.breaks[i+1]}></p>\n"
        with open("%s/%s.txt"%(dirname,type(self).__name__),'w') as f:
            f.write(out)

    def copy_files(self):
        if self.video_slides_dir !=None:
            dirname=os.path.dirname(self.renderer.file_writer.movie_file_path)
            slide_name = type(self).__name__
            if not os.path.exists(self.video_slides_dir):
                os.makedirs(self.video_slides_dir)
            shutil.copy2(os.path.join(dirname,"%s.mp4"%slide_name), self.video_slides_dir)
            shutil.copy2(os.path.join(dirname,"%s.txt"%slide_name), self.video_slides_dir)

    def tear_down(self):
        super(SlideScene, self).tear_down()
        self.save_times()

    def print_end_message(self):
        super(SlideScene, self).print_end_message()
        self.copy_files()


class Title(SlideScene):
    def construct(self):
        title = Tex(r"\bfseries\textsc{Title}").scale(1.25).shift(2.5*UP)
        arxiv = Tex(r"\bfseries\texttt{arXiv:????.?????}").scale(.75).shift(1.5*UP)
        name = Tex("Christopher T.\ Chubb")
        ethz=SVGMobject("ethz_logo_white.svg").scale(1/3).next_to(1.5*DOWN,LEFT,buff=2.5)
        udes=SVGMobject("Université_de_Sherbrooke_(logo).svg").scale(1/3).next_to(1.5*DOWN,RIGHT,buff=2.5)

        self.add(title,arxiv,name,ethz,udes)

        self.play(*[FadeOut(x) for x in [title,arxiv,name,ethz,udes]],run_time=0.5)
        self.wait(0.5)
        
class ExampleSlide(SlideScene):
    def construct(self):
        circle = Circle(radius=1, color=BLUE)
        dot = Dot()
        dot2 = dot.copy().shift(RIGHT)
        self.add(dot)

        line = Line([3, 0, 0], [5, 0, 0])
        self.add(line)

        self.play(GrowFromCenter(circle))
        self.slide_break()
        self.play(Transform(dot, dot2))
        self.slide_break()
        self.play(MoveAlongPath(dot, circle), run_time=2, rate_func=linear)
        self.slide_break()
        self.play(Rotating(dot, about_point=[2, 0, 0]), run_time=1.5)
        self.wait()

