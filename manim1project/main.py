from manim import *
from magnifyingGlass import MagnifyingGlass
class DefaultTemplate(MovingCameraScene):
    def construct(self):

        self.play(self.camera.frame.animate.scale(1.2).move_to(DOWN))
        self.squares = [[Square().move_to([2*k-n, -2*n+2,0]) for k in range(8)] for n in range(8)]
        numbers = [[0 for _ in range(8)] for _ in range(8)]
        squareNumbers = [[None for _ in range(8)] for _ in range(8)]
        group = VGroup()
        for n in range(8):
            for k in range(n + 1):
                square = self.squares[n][k]
                numbers[n][k] = self.sumNumbers(n, k, numbers)
                square_number = Text(str(numbers[n][k]))
                square_number.move_to(square.get_center())
                squareNumbers[n][k] = square_number
                group.add(square)

        for n in range(4):
            for k in range(n + 1):
                square = self.squares[n][k]
                square_number = squareNumbers[n][k]
                self.play(Create(square), run_time=1/(1+n))

        self.wait(1)

        self.play(Create(squareNumbers[0][0]))

        magnifying_glass = MagnifyingGlass()
        magnifying_glass.move_to(LEFT * 5 + UP * 2)
        self.play(Create(magnifying_glass))


        for n in range(1, 4):
            for k in range(n + 1):
                square = self.squares[n][k]
                self.play(magnifying_glass.animate.move_to(square.get_center()))
                square_number = squareNumbers[n][k]
                source = VGroup()
                leftArrow = Arrow(start=square.get_center(), end=square.get_center() + LEFT + UP + UP, color=RED)
                rightArrow = Arrow(start=square.get_center(), end=square.get_center() + RIGHT + UP + UP, color=RED)
                if k > 0:
                    leftArrow.color = GREEN
                    source.add(squareNumbers[n - 1][k - 1].copy())
                if k < n:
                    rightArrow.color = GREEN
                    source.add(squareNumbers[n - 1][k].copy())
                self.play(Create(leftArrow), run_time=0.2)
                self.play(Create(rightArrow), run_time=0.2)
                target = square_number
                self.play(Transform(source, target), rightArrow.animate.fade(1), leftArrow.animate.fade(1))
                self.remove(rightArrow, leftArrow)

        self.play(self.camera.frame.animate.scale(2).move_to(DOWN * 4.5), magnifying_glass.animate.fade(1))
        self.remove(magnifying_glass)

        numberAdds = []
        for n in range(4, 8):
            rowCreate = []
            numberAdd = []
            for k in range(n + 1):
                square = self.squares[n][k]
                square_number = squareNumbers[n][k]
                source = VGroup()
                if k > 0:
                    source.add(squareNumbers[n-1][k-1].copy())
                if k < n:
                    source.add(squareNumbers[n-1][k].copy())
                rowCreate.append(Create(square))
                numberAdd.append(Transform(source, square_number))
            self.play(*rowCreate, run_time=0.5)
            numberAdds.append(numberAdd)

        self.play(*numberAdds[0])
        self.play(*numberAdds[1])
        self.play(*numberAdds[2])
        self.play(*numberAdds[3])

        self.wait(2)

        # Show how many ways there are to reach the top from square 4,2
        questionText = Text("How many ways to\nget to the top?", color = YELLOW, line_spacing = 1, font=BOLD)
        questionText.move_to(UP * 3 + LEFT * 7)
        self.play(Create(questionText))

        # TODO: Maybe show each of the 3,3 squares first, reuse those sections?
        self.offsets = []
        self.offsets.append(RIGHT * 10)
        self.offsets.append(RIGHT * 8)
        self.offsets.append(RIGHT * 6)
        self.offsets.append(LEFT * 6)
        self.offsets.append(LEFT * 8)
        self.offsets.append(LEFT * 10)
        self.path = []
        self.allPaths = VGroup()
        leftArrow = Arrow(start = self.squares[4][2].get_center(), end = self.squares[3][1].get_center())
        leftArrow.set_opacity(0)
        self.path.append(leftArrow)

        magnifying_glass = MagnifyingGlass()
        magnifying_glass.move_to(self.squares[3][1].get_center())
        self.play(Create(magnifying_glass))
        self.speed = 1
        self.drawRoutes(3, 1)

        self.play(magnifying_glass.animate.move_to(self.squares[3][2].get_center()))

        self.path.remove(leftArrow)
        rightArrow = Arrow(start = self.squares[4][2].get_center(), end = self.squares[3][2].get_center())
        rightArrow.set_opacity(0)
        self.path.append(rightArrow)
        self.drawRoutes(3, 2)
        self.path.remove(rightArrow)

        self.offsets.append(RIGHT * 10)
        self.offsets.append(RIGHT * 8)
        self.offsets.append(RIGHT * 6)
        self.offsets.append(LEFT * 6)
        self.offsets.append(LEFT * 8)
        self.offsets.append(LEFT * 10)
        self.speed = 2
        self.play(magnifying_glass.animate.move_to(self.squares[4][2].get_center()))
        self.drawRoutes(4, 2)

        self.wait(2)
        self.play(magnifying_glass.animate.fade(1))
        self.remove(magnifying_glass)

        self.play(self.allPaths.animate.fade(1))
        self.remove(self.allPaths)

        names = ["Rafi", "Hilton", "Halle", "Hannah", "Jonah", "Dwayne", "Yuan"]
        self.nameTexts = []
        for i in range(7):
            name = Text(names[i], color = BLUE)
            name.move_to(self.squares[i+1][0].get_center() + LEFT * 2, aligned_edge=RIGHT)
            self.nameTexts.append(name)
            self.play(Create(name), run_time=0.3)

        questionText2 = Text("How many ways of\nchoosing 2 people from 7?", color = YELLOW, line_spacing = 1, font=BOLD)
        questionText2.move_to(UP * 3 + LEFT * 7)
        self.play(Transform(questionText, questionText2), run_time=1)
        magnifying_glass = MagnifyingGlass()
        magnifying_glass.move_to(LEFT * 8)
        self.play(Create(magnifying_glass))
        self.play(magnifying_glass.animate.move_to(self.squares[7][2].get_center()))
        line = Line(start = self.squares[7][2].get_center(), end = self.squares[7][0].get_center(), color = YELLOW)
        brace = Brace(line, color = YELLOW)
        brace.shift(DOWN /2)
        braceText = Text("Distance 2", color = YELLOW)
        braceText.next_to(brace, direction=DOWN)
        self.play(Create(brace), Create(braceText), run_time=1)

        demoPath = []
        for i in range(7):
            demoPath.append(Arrow(start = self.squares[7-i][2].get_center(), end = self.squares[7-i-1][2].get_center(), color=BLUE))
            self.play(Create(demoPath[i]), run_time=0.5)

        topline = Line(start = self.squares[0][0].get_center(), end = self.squares[0][2].get_center(), color = YELLOW)
        topbrace = Brace(topline, color = YELLOW)
        brace.shift(DOWN/2)
        braceText = Text("Distance 2", color = YELLOW)
        braceText.next_to(topbrace, direction=DOWN)
        self.play(Create(topbrace), Create(braceText), run_time=1)

        # Shift the top 2 arrows to the left
        # Swivel the 3rd top arrow to the left and make it green
        # Change the distance brace and text
        # Change the color of the 3rd top name to green

        left2Text = Text("Each route needs\nto go left 2 times", color = YELLOW, line_spacing=1)
        left2Text.move_to(UP * 3 + RIGHT * 7)
        self.play(Create(left2Text), run_time=1)

        mutations = []
        leftidx1 = 2
        leftidx2 = 4
        demoPath2 = demoPath.copy()
        for i in range(7-leftidx1, 7):
            demoPath2[i] = demoPath[i].copy()
            demoPath2[i].shift(LEFT * 2)
            mutations.append(Transform(demoPath[i], demoPath2[i]))

        demoPath2[7-leftidx1-1] = Arrow(start = self.squares[leftidx1+1][2].get_center(), end = self.squares[leftidx1][1].get_center(), color=GREEN, stroke_width=10)
        mutations.append(Transform(demoPath[7-leftidx1-1], demoPath2[7-leftidx1-1]))

        line2 = Line(start = self.squares[0][0].get_center(), end = self.squares[0][1].get_center(), color = YELLOW)
        brace2 = Brace(line2, color = YELLOW)
        brace2Text = Text("Distance 1", color = YELLOW)
        brace2Text.next_to(brace2, direction=DOWN)

        newname1 = self.nameTexts[leftidx1].copy()
        newname1.color = GREEN
        newname1.set_stroke(width=5)
        mutations.append(Transform(self.nameTexts[leftidx1], newname1))
        oval1 = Ellipse(width = newname1.width + 0.5, height = newname1.height + 0.5, color = RED)
        oval1.move_to(newname1.get_center())
        mutations.append(Transform(topbrace, brace2))
        mutations.append(Transform(braceText, brace2Text))

        self.play(*mutations, run_time=2)
        mutations = []

        left2Text2 = Text("The rows we turn left\nare chosen people", color = YELLOW, line_spacing=1)
        left2Text2.move_to(RIGHT * 7)
        self.play(Create(left2Text2))
        self.play(Create(oval1))

        demoPath2 = demoPath.copy()
        for i in range(7-leftidx2, 7):
            demoPath2[i] = demoPath[i].copy()
            demoPath2[i].shift(LEFT * 2)
            mutations.append(Transform(demoPath[i], demoPath2[i]))

        demoPath2[7-leftidx2-1] = Arrow(start = self.squares[leftidx2+1][2].get_center(), end = self.squares[leftidx2][1].get_center(), color=GREEN, stroke_width=10)
        mutations.append(Transform(demoPath[7-leftidx2-1], demoPath2[7-leftidx2-1]))

        newname2 = self.nameTexts[leftidx2].copy()
        newname2.color = GREEN
        newname2.set_stroke(width=5)
        mutations.append(Transform(self.nameTexts[leftidx2], newname2))
        oval2 = Ellipse(width = newname2.width + 0.5, height = newname2.height + 0.5, color = RED)
        oval2.move_to(newname2.get_center())
        mutations.append(Transform(topbrace, brace2))
        mutations.append(topbrace.animate.fade(1))
        mutations.append(braceText.animate.fade(1))

        self.play(*mutations, run_time=2)
        self.play(Create(oval2))
        self.wait(2)

        for i in range(7):
            self.nameTexts[i].set_color(BLUE)
            self.nameTexts[i].set_stroke(width=0)

        fades = []
        fades.append(oval1.animate.fade(1))
        fades.append(oval2.animate.fade(1))
        fades.append(left2Text.animate.fade(1))
        fades.append(left2Text2.animate.fade(1))
        for i in range(7):
            fades.append(demoPath[i].animate.fade(1))
        self.play(*fades, run_time=1)
        self.remove(oval1)
        self.remove(oval2)
        self.remove(*demoPath)
        self.remove(left2Text)
        self.remove(left2Text2)

        self.pickedNames = []
        self.offsets = []
        for i in range(7):
            for j in range(3):
                self.offsets.append(RIGHT * (2.5* j +7) + UP * (i) * 1.5 + 5 * DOWN)

        self.wait(1)
        self.speed = 1
        self.drawRoutesWithNames(7, 2)
        self.wait(1)

    def magnifyingGlass(self):
        lens = Circle(radius = 0.8, color = BLUE)
        lens.move_to(LEFT * 5 + UP * 2)
        lens.set_stroke(width=10)
        handle = Rectangle(height = 0.2, width=1.5, color=GOLD, fill_opacity=1)
        handle.set_stroke(width=4)
        handle.rotate(-PI/4)
        handle.next_to(lens, direction=DR, buff=-0.3)
        lens.set_fill(WHITE, opacity=0.1)
        magnifiying_glass = VGroup(lens, handle)
        return magnifiying_glass

    def sumNumbers(s, n, k, numbers):
        if n == k:
            return 1
        if k == 0:
            return 1
        return numbers[n-1][k-1] + numbers[n-1][k]
    
    def drawRoutes(self, n, k):
        if n == 0:
            thispath = []
            for i in self.path:
                thispath.append(i.copy())            
            pathGroup = VGroup(*thispath)
            self.play(pathGroup.animate.move_to(self.offsets.pop()).scale(0.5), run_time=1.0/self.speed)
            self.allPaths.add(pathGroup)
            return
        if k > 0:
            leftArrow = Arrow(start = self.squares[n][k].get_center(), end = self.squares[n-1][k-1].get_center(), color = GREEN)
            self.play(Create(leftArrow), run_time=0.2/self.speed)
            self.path.append(leftArrow)
            self.drawRoutes(n-1, k-1)
            self.path.remove(leftArrow)
            self.play(leftArrow.animate.fade(1), run_time=0.2/self.speed)
            self.remove(leftArrow)
        if k < n:
            rightArrow = Arrow(start = self.squares[n][k].get_center(), end = self.squares[n-1][k].get_center(), color = GREEN)
            self.play(Create(rightArrow), run_time=0.2/self.speed)
            self.path.append(rightArrow)
            self.drawRoutes(n-1, k)
            self.path.remove(rightArrow)
            self.play(rightArrow.animate.fade(1), run_time=0.2/self.speed)
            self.remove(rightArrow)

    def drawRoutesWithNames(self, n, k):
        if n == 0:
            thisnames = []
            thisnamestargets = []
            moves = []
            for name in self.pickedNames:
                thisnames.append(name.copy())
                target = name.copy()
                target.color = ORANGE
                target.set_stroke(width=1)
                thisnamestargets.append(target)
            offset = self.offsets.pop()
            namesOutline = Rectangle(height=1, width=2, color=YELLOW)
            namesOutline.move_to(offset)
            nameTargetGroup = VGroup(*thisnamestargets).scale(0.5).arrange(DOWN, buff = 0.2)
            nameTargetGroup.move_to(offset)

            for i in range(len(self.pickedNames)):
                moves.append(Transform(thisnames[i],thisnamestargets[i]))
            self.play(*moves, Create(namesOutline), run_time=1.0/self.speed)
            self.speed = self.speed + 1
            return
        if k > 0:
            leftArrow = Arrow(start = self.squares[n][k].get_center(), end = self.squares[n-1][k-1].get_center(), color = GREEN, stroke_width=10)
            name = self.nameTexts[n-1]
            name.set_color(GREEN)
            name.set_stroke(width=5)
            self.pickedNames.append(name)
            self.play(Create(leftArrow), run_time=0.5/self.speed)
            self.path.append(leftArrow)
            self.drawRoutesWithNames(n-1, k-1)
            self.path.remove(leftArrow)
            self.remove(leftArrow)
            name.set_color(BLUE)
            name.set_stroke(width=0)
            self.pickedNames.remove(name)
        if k < n:
            rightArrow = Arrow(start = self.squares[n][k].get_center(), end = self.squares[n-1][k].get_center(), color = BLUE)
            self.play(Create(rightArrow), run_time=0.5/self.speed)
            self.path.append(rightArrow)
            self.drawRoutesWithNames(n-1, k)
            self.path.remove(rightArrow)
            self.remove(rightArrow)
