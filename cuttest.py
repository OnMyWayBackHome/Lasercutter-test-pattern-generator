import svgwrite

dwg = svgwrite.drawing.Drawing("tmp.svg", size=('5in','6in'), viewBox="0 0 5 6", profile='tiny')

engrave_color = "blue"
score_color = "green"
cut_color = "red"

dwg.add(dwg.rect((0.5, 0.50), (2, 3), stroke=cut_color, fill='none'))

dwg.save()


