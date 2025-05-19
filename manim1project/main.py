from manim import *
class DefaultTemplate(MovingCameraScene):
    def construct(self):

        self.play(self.camera.frame.animate.scale(1.2).move_to(DOWN))
        squares = [[Square() for _ in range(8)] for _ in range(8)]
        numbers = [[0 for _ in range(8)] for _ in range(8)]
        squareNumbers = [[Text for _ in range(8)] for _ in range(8)]
        group = VGroup()
        for n in range(8):
            for k in range(n + 1):
                square = squares[n][k]
                square.move_to([2* k - n, - 2 * n + 2, 0])
                numbers[n][k] = self.sumNumbers(n, k, numbers)
                square_number = Text(str(numbers[n][k]))
                square_number.move_to(square.get_center())
                squareNumbers[n][k] = square_number
                group.add(square)

        # Put all the squares in a group
        group2 = VGroup(*squares)

        for n in range(4):
            for k in range(n + 1):
                square = squares[n][k]
                square_number = squareNumbers[n][k]
                self.play(Create(square), run_time=1/(1+n))

        self.wait(1)

        self.play(Create(squareNumbers[0][0]))

        lens = Circle(radius = 0.8, color = BLUE)
        lens.move_to(LEFT * 5 + UP * 2)
        lens.set_stroke(width=10)
        handle = Rectangle(height = 0.2, width=1.5, color=GOLD, fill_opacity=1)
        handle.set_stroke(width=4)
        handle.rotate(-PI/4)
        handle.next_to(lens, direction=DR, buff=-0.3)
        lens.set_fill(WHITE, opacity=0.1)
        magnifiying_glass = VGroup(lens, handle)
        self.play(Create(magnifiying_glass))
        offset = magnifiying_glass.get_center() - lens.get_center()

        for n in range(1, 4):
            for k in range(n + 1):
                square = squares[n][k]
                self.play(magnifiying_glass.animate.move_to(square.get_center() + offset))
                square_number = squareNumbers[n][k]
                source = VGroup()
                leftArrow = Arrow(start = square.get_center(), end = square.get_center() + LEFT + UP + UP, color = RED)
                rightArrow = Arrow(start = square.get_center(), end = square.get_center() + RIGHT + UP + UP, color = RED)
                if k > 0:
                    leftArrow.color = GREEN
                    source.add(squareNumbers[n-1][k-1].copy())
                if k < n:
                    rightArrow.color = GREEN
                    source.add(squareNumbers[n-1][k].copy())
                self.play(Create(leftArrow), run_time=0.2)
                self.play(Create(rightArrow), run_time=0.2)
                target = square_number
                self.play(Transform(source, target), rightArrow.animate.fade(1), leftArrow.animate.fade(1))

        self.play(self.camera.frame.animate.scale(2).move_to(DOWN * 4.5), magnifiying_glass.animate.fade(1))

        numberAdds = []
        for n in range(4, 8):
            rowCreate = []
            numberAdd = []
            for k in range(n + 1):
                square = squares[n][k]
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
        offsets = []
        offsets.append(RIGHT * 10)
        offsets.append(RIGHT * 8)
        offsets.append(RIGHT * 6)
        offsets.append(LEFT * 6)
        offsets.append(LEFT * 8)
        offsets.append(LEFT * 10)
        path = []
        allPaths = VGroup()
        self.drawRoutes(4, 2, squares, path, offsets, allPaths)

        self.wait(2)

        self.play(allPaths.animate.fade(1))

        names = ["Michaela", "Haley", "Hilton", "LongName", "E", "F", "G"]
        nameTexts = []
        for i in range(7):
            name = Text(names[i], color = BLUE)
            name.move_to(squares[i+1][0].get_center() + LEFT * 2, aligned_edge=RIGHT)
            nameTexts.append(name)
            self.play(Create(name), run_time=0.3)

        line = Line(start = squares[7][2].get_center(), end = squares[7][0].get_center(), color = YELLOW)
        brace = Brace(line, color = YELLOW)
        brace.shift(DOWN /2)
        self.play(Create(brace))

        pickedNames = []
        offsets = []
        for i in range(7):
            for j in range(3):
                offsets.append(RIGHT * (2* j +6) + UP * (i) + 3 * DOWN)

        self.drawRoutesWithNames(7, 2, squares, path, offsets, allPaths, nameTexts, pickedNames)

    def sumNumbers(s, n, k, numbers):
        if n == k:
            return 1
        if k == 0:
            return 1
        return numbers[n-1][k-1] + numbers[n-1][k]
    
    def drawRoutes(self, n, k, squares, path, offsets, allPaths):
        if n == 0:
            thispath = []
            for i in path:
                thispath.append(i.copy())            
            pathGroup = VGroup(*thispath)
            self.play(pathGroup.animate.move_to(offsets.pop()).scale(0.5))
            allPaths.add(pathGroup)
            return
        if k > 0:
            leftArrow = Arrow(start = squares[n][k].get_center(), end = squares[n-1][k-1].get_center(), color = GREEN)
            self.play(Create(leftArrow), run_time=0.2)
            path.append(leftArrow)
            self.drawRoutes(n-1, k-1, squares, path, offsets, allPaths)
            path.remove(leftArrow)
            self.play(leftArrow.animate.fade(1), run_time=0.2)
        if k < n:
            rightArrow = Arrow(start = squares[n][k].get_center(), end = squares[n-1][k].get_center(), color = GREEN)
            self.play(Create(rightArrow), run_time=0.2)
            path.append(rightArrow)
            self.drawRoutes(n-1, k, squares, path, offsets, allPaths)
            path.remove(rightArrow)
            self.play(rightArrow.animate.fade(1), run_time=0.2)

    def drawRoutesWithNames(self, n, k, squares, path, offsets, allPaths, nameTexts, pickedNames):
        if n == 0:
            thisnames = []
            thisnamestargets = []
            moves = []
            for name in pickedNames:
                thisnames.append(name.copy())
                target = name.copy()
                target.color = ORANGE
                thisnamestargets.append(target)
            offset = offsets.pop()
            namesOutline = Rectangle(height=1, width=2, color=YELLOW)
            namesOutline.move_to(offset)
            nameTargetGroup = VGroup(*thisnamestargets).scale(0.5).arrange(DOWN, buff = 0.2)
            nameTargetGroup.move_to(offset)

            for i in range(len(pickedNames)):
                moves.append(Transform(thisnames[i],thisnamestargets[i]))
            self.play(*moves, Create(namesOutline), run_time=0.5)
            return
        if k > 0:
            leftArrow = Arrow(start = squares[n][k].get_center(), end = squares[n-1][k-1].get_center(), color = GREEN, stroke_width=3)
            name = nameTexts[n-1]
            name.set_color(GREEN)
            pickedNames.append(name)
            self.play(Create(leftArrow), run_time=0.05)
            path.append(leftArrow)
            self.drawRoutesWithNames(n-1, k-1, squares, path, offsets, allPaths, nameTexts, pickedNames)
            path.remove(leftArrow)
            self.remove(leftArrow)
            name.set_color(BLUE)
            pickedNames.remove(name)
        if k < n:
            rightArrow = Arrow(start = squares[n][k].get_center(), end = squares[n-1][k].get_center(), color = GREEN)
            self.play(Create(rightArrow), run_time=0.05)
            path.append(rightArrow)
            self.drawRoutesWithNames(n-1, k, squares, path, offsets, allPaths, nameTexts, pickedNames)
            path.remove(rightArrow)
            self.remove(rightArrow)
