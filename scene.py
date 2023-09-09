from manim import *
from math import gcd

# Вспомогательные функции
#------------------------------------
def gcd_ryada(lst):
    if len(lst) == 2:
        return gcd(lst[0], lst[1])
    return gcd(lst[0], gcd_ryada(lst[1:]))

def stolbik(matrix, number):
    return [matrix[i][number] for i in range(len(matrix))]

def nok(a, b):
    return a*b//gcd(a, b)
#------------------------------------

class Gaus(MovingCameraScene):
    def construct(self):

        def swap_rows(a, matrix, i, j):
            i, j = min(i, j), max(i, j)

            row1 = matrix.get_rows()[i]
            row2 = matrix.get_rows()[j]

            # Отрисовка стрелочек
            #---------------
            n = len(a)

            arrow1 = Arrow(start=ORIGIN, end=(LEFT * n / 10 * 3), max_tip_length_to_length_ratio=(0.1 * 10 ** 0.5 / n ** 0.5), stroke_width=(3 * n / 4.7))
            arrow1.next_to(matrix, RIGHT)
            arrow1.align_to(matrix.get_rows()[i], UP)

            arrow2 = Arrow(start=ORIGIN, end=(LEFT * n / 10 * 3), max_tip_length_to_length_ratio=(0.1 * 10 ** 0.5 / n ** 0.5), stroke_width=(3 * n / 4.7))
            arrow2.next_to(matrix, RIGHT)
            arrow2.align_to(matrix.get_rows()[j], DOWN)

            line = Line()
            line.put_start_and_end_on(arrow1.get_start(), arrow2.get_start())

            group = VGroup(arrow1, line, arrow2)

            self.play(Write(group))
            #---------------

            self.play(ApplyFunction(self.custom_paint(RED), row1), ApplyFunction(self.custom_paint(GREEN), row2))

            self.wait(0.5)

            self.play(FadeOut(row1, shift=(DOWN * 0.3)), FadeOut(row2, shift=(UP * 0.3)))

            a[i], a[j] = a[j], a[i]

            for elem, index in zip(row1, range(len(row1))):
                elem.set_value(a[i][index])
                elem.set_color(GREEN)

            for elem, index in zip(row2, range(len(row2))):
                elem.set_value(a[j][index])
                elem.set_color(RED)

            self.play(FadeIn(row1, shift=(UP * 0.3)), FadeIn(row2, shift=(DOWN * 0.3)))

            self.wait(0.5)

            m2 = DecimalMatrix(a, left_bracket="(", right_bracket=")", element_to_mobject_config={'num_decimal_places': 0})
            self.play(Transform(matrix, m2), Unwrite(group))

            return a


        def multiply_row(a, matrix, i, k, decimal=False):
            j = 0

            b = a[:]
            b[i] = [x * k for x in b[i]]

            m2 = DecimalMatrix(b, left_bracket="(", right_bracket=")", element_to_mobject_config={'num_decimal_places': 0})
            self.play(ApplyFunction(self.custom_width_of_matrix(width=m2.width), matrix))
            self.play(self.camera.frame.animate.set(width=matrix.width * 1.7).move_to(matrix))

            row = matrix.get_rows()[i]

            if decimal:
                if k == 1:
                    text = Tex("+", color=YELLOW)
                elif k == -1:
                    text = Tex("*(-1)", color=YELLOW)
                elif k < 0:
                    text = Tex("*(-1/" + str(-k) + ")", color=YELLOW)
                else:
                    text = Tex("*1/" + str(k), color=YELLOW)
            else:
                if k == 1:
                    text = Tex("+", color=YELLOW)
                elif k == -1:
                    text = Tex("*(-1)", color=YELLOW)
                elif k < 0:
                    text = Tex("*(" + str(k) + ")", color=YELLOW)
                else:
                    text = Tex("*" + str(k), color=YELLOW)

            text.next_to(matrix, RIGHT)
            text.align_to(row, UP)
            self.play(Write(text))

            for entry in row:
                self.play(Unwrite(entry))

                if decimal:
                    a[i][j] = int(a[i][j] // k)
                else:
                    a[i][j] = int(a[i][j] * k)
                m2 = DecimalMatrix(a, left_bracket="(", right_bracket=")", element_to_mobject_config={'num_decimal_places': 0})
                m2.get_rows()[i][j].set_fill("#1BFF00")

                self.play(Transform(matrix, m2))
                
                j += 1

                #print(entry.get_value())

            m2 = DecimalMatrix(a, left_bracket="(", right_bracket=")", element_to_mobject_config={'num_decimal_places': 0})
            self.play(Transform(matrix, m2))

            self.play(Unwrite(text))

            return a


        def multiply_row_and_plus(a, matrix, i, k, j, decimal=False):

            b = [row[:] for row in a]
            if decimal:
                for t in range(len(b[0])):
                    b[j][t] = b[i][t] // k + b[j][t]
            else:
                for t in range(len(b[0])):
                    b[j][t] = b[i][t] * k + b[j][t]
            m2 = DecimalMatrix(b, left_bracket="(", right_bracket=")", element_to_mobject_config={'num_decimal_places': 0})
            self.play(ApplyFunction(self.custom_width_of_matrix(width=m2.width), matrix))

            # Отрисовка стрелочек справа
            #---------------
            n = len(a)

            arrow1 = Arrow(start=ORIGIN, end=(RIGHT * n / 10 * 3), max_tip_length_to_length_ratio=(0.1 * 10 ** 0.5 / n ** 0.5), stroke_width=(3 * n / 4.7))
            arrow1.next_to(matrix, RIGHT)
            arrow1.align_to(matrix.get_rows()[i], UP)

            arrow2 = Arrow(start=ORIGIN, end=(LEFT * n / 10 * 3), max_tip_length_to_length_ratio=(0.1 * 10 ** 0.5 / n ** 0.5), stroke_width=(3 * n / 4.7))
            arrow2.next_to(matrix, RIGHT)
            arrow2.align_to(matrix.get_rows()[j], DOWN)

            line = Line()
            line.put_start_and_end_on(arrow1.get_end(), arrow2.get_start())

            if decimal:
                if k == 1:
                    text = Tex("+", color=YELLOW)
                elif k == -1:
                    text = Tex("*(-1)", color=YELLOW)
                elif k < 0:
                    text = Tex("*(-1/" + str(-k) + ")", color=YELLOW)
                else:
                    text = Tex("*1/" + str(k), color=YELLOW)
            else:
                if k == 1:
                    text = Tex("+", color=YELLOW)
                elif k == -1:
                    text = Tex("*(-1)", color=YELLOW)
                elif k < 0:
                    text = Tex("*(" + str(k) + ")", color=YELLOW)
                else:
                    text = Tex("*" + str(k), color=YELLOW)
            text.next_to(line, RIGHT * 0.3)

            group = VGroup(arrow1, line, arrow2, text)

            self.play(self.camera.frame.animate.set(width=matrix.width * 1.7 + group.width).move_to(matrix))

            self.play(Write(group))
            #---------------


            row = matrix.get_rows()[i].copy()
            row_cp = row.copy() # для красоты
            row.next_to(matrix, UP)
            row.set_fill("#1BFF00")


            if k != 1:
                # Отрисовка стрелочек слева
                #---------------
                arrow3 = Arrow(start=ORIGIN, end=(LEFT * n / 10 * 3), max_tip_length_to_length_ratio=(0.1 * 10 ** 0.5 / n ** 0.5), stroke_width=(3 * n / 4.7))
                arrow3.next_to(row, LEFT)

                arrow4 = Arrow(start=ORIGIN, end=(RIGHT * n / 10 * 3), max_tip_length_to_length_ratio=(0.1 * 10 ** 0.5 / n ** 0.5), stroke_width=(3 * n / 4.7))
                arrow4.next_to(row, LEFT)
                arrow4.align_to(matrix.get_rows()[j], DOWN)

                line1 = Line()
                line1.put_start_and_end_on(arrow4.get_start(), arrow3.get_end())

                text1 = Tex("+", color=YELLOW)
                text1.next_to(line1, LEFT * 0.3)

                group1 = VGroup(arrow3, line1, arrow4, text1)

                self.play(self.camera.frame.animate.set(width=matrix.width * 1.7 + group1.width + group.width).move_to(matrix))

                self.play(Write(row), FadeOut(row_cp, shift=UP))
                self.play(Write(group1))
                #---------------
            else:
                self.play(Write(row), FadeOut(row_cp, shift=UP))


            elems = []
            r = list(a[i])
            t = 0
            for elem in matrix.get_rows()[j]:

                if decimal:
                    a[j][t] = a[i][t] // k + a[j][t] # берём i-ую и j-ую строки, умножаем i-ую на 1/k и прибавляем к j-ой
                else:
                    a[j][t] = a[i][t] * k + a[j][t] # берём i-ую и j-ую строки, умножаем i-ую на k и прибавляем к j-ой

                rt = row[t].copy()
                if decimal:
                    rt.set_value(r[t] // k)
                else:
                    rt.set_value(r[t] * k)
                rt.set_fill("#00FF00")

                self.play(Transform(row[t], rt))

                self.wait(0.5)

                elem_cp = elem.copy()
                elem_cp.set_value(a[j][t])
                elem_cp.set_fill("#1BFF1B")
                elems.append(elem_cp)

                self.play(ReplacementTransform(row[t], elem_cp), FadeOut(elem, scale=0.0), run_time=1.5)

                elem.set_value(a[j][t])

                t += 1

            m2 = DecimalMatrix(a, left_bracket="(", right_bracket=")", element_to_mobject_config={'num_decimal_places': 0})
            self.play(Transform(matrix, m2), FadeOut(Group(*elems)))

            self.wait(0.5)

            if k != 1:
                self.play(Unwrite(group), self.camera.frame.animate.set(width=matrix.width * 1.7).move_to(matrix), Unwrite(group1))
            else:
                self.play(Unwrite(group), self.camera.frame.animate.set(width=matrix.width * 1.7).move_to(matrix))

            return a
            



        #a = [[2, 1, -1, 8], [-3, -1, 2, -11], [-2, 1, 2, -3]]
        #a = [[1, 2, -1, 7], [2, 4, -2, 17], [1, -1, 3, -1]]
        a = [[6, 8, -7, 2], [4, -2, 6, 0], [2, -1, 3, 1]]
        #a = [[1, 2, 3, 3], [3, 5, 7, 0], [1, 3, 4, 1]]
        #a = [[0, 0, 1, 3], [1, 0, 0, 5], [0, 1, 0, 1]]

        n = len(a)

        m1 = DecimalMatrix(a, left_bracket="(", right_bracket=")", element_to_mobject_config={'num_decimal_places': 0})

        self.play(self.camera.frame.animate.set(width=m1.width * 1.7).move_to(m1))
        self.play(Write(m1))


        # Прямой ход метода Гаусса
        for i in range(n):
            # Делим все строки по отдельности на их общий делитель (если он не равен 1)
            for j in range(n):
                stroka = a[j]
                x = gcd_ryada(stroka)
                if x != 1 and x != 0:
                    a = multiply_row(a, m1, j, x, decimal=True)

            # Меняем строчки таким образом, чтобы единичка(или -1) оказалась на главной диагонали (если такое возможно)
            # Если на главной диагонали появился 0, то пытаемся заменить его на любую другую строчку
            x = stolbik(a, i)
            if (1 in x[i+1:] or -1 in x[i+1:]) and x[i] != 1 and x[i] != -1:
                if 1 in x:
                    index = x.index(1)
                else:
                    index = x.index(-1)
                
                a = swap_rows(a, m1, index, i)

                if a[i][i] == -1:
                    a = multiply_row(a, m1, i, -1)
                    
            elif a[i][i] == 0:
                for j in range(i+1, n):
                    if a[j][i] != 0:
                        a = swap_rows(a, m1, j, i)
                        break

            # Делаем нули под элементом a[i][i]
            for j in range(i+1, n):
                if a[i][i] == 0 or a[j][i] == 0:
                    x = 0
                else:
                    x = nok(a[i][i], a[j][i])

                if a[i][i]==a[j][i]:
                    a = multiply_row_and_plus(a, m1, i, -1, j)
                elif a[i][i]==-a[j][i]:
                    a = multiply_row_and_plus(a, m1, i, 1, j) # Сложение строк
                elif x == a[j][i] and x != 0:
                    a = multiply_row_and_plus(a, m1, i, -(x//a[i][i]), j)
                elif x != 0:
                    x1, x2 = a[i][i], a[j][i]

                    a = multiply_row(a, m1, i, -(x//x1))
                    a = multiply_row(a, m1, j, x//x2)
                    a = multiply_row_and_plus(a, m1, i, 1, j) # Сложение строк
                    a = multiply_row(a, m1, i, -(x//x1), decimal=True) # Будем умножать на дробное, в данном случае на 1/(-(x//x1))


        """
        # Умножение одной строки на число и прибавление к другой
        # -------------
        a = multiply_row_and_plus(a, m1, 1, 5, 0)
        a = multiply_row_and_plus(a, m1, 2, 1, 3)
        a = multiply_row_and_plus(a, m1, 3, -1, 2)
        # -------------
        """

        """
        # Смена строк местами
        # -------------
        i = 0
        j = 2
        a = swap_rows(a, m1, i, j)
        a = swap_rows(a, m1, j, i)
        # -------------
        """
        
        """
        # Домножение строки на число
        # -------------
        a = multiply_row(a, m1, 2, 3)
        a = multiply_row(a, m1, 3, -1)
        # -------------
        """

        self.wait()

        # Вывод финальных титров
        c = Circle(fill_opacity=0.9, fill_color=ORANGE)
        c.scale(m1.width)
        c.set_color(BLACK)
        self.play(FadeIn(c, scale=0.0), run_time=3)

        t = Tex("Made by 3pknai from DistrIcTion", color=GOLD)
        t1 = Tex("https://github.com/3pknai/manim", color=GOLD)
        t.scale(c.width / 2)
        t1.scale(c.width / 2)
        t1.next_to(t, DOWN)
        self.play(Write(t), self.camera.frame.animate.set(width=t.width * 1.7).move_to(t), Write(t1))

        self.wait(3)


    def custom_paint(self, color):
        def custom_func(mob):
            mob.set_style(fill_color=color)
            return mob
        return custom_func

    def custom_width_of_matrix(self, width):
        def custom_func(mob):
            mob.set(width=width)
            return mob
        return custom_func