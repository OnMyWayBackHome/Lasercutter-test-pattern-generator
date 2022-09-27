from HersheyFonts import HersheyFonts
import svgwrite

dwg = svgwrite.drawing.Drawing(
    "tmphershey.svg", 
    size=('500', '100'),
    profile='full')

thefont = HersheyFonts()
thefont.load_default_font()
factor = 40

scale_factor = float(factor) / (thefont.render_options['bottom_line'] - thefont.render_options['cap_line'])
thefont.render_options.scaley = scale_factor
thefont.render_options.scalex = scale_factor
thefont.render_options.yofs = 50 #thefont.render_options['bottom_line'] * scale_factor
thefont.render_options.xofs = 20

for (x1, y1), (x2, y2) in thefont.lines_for_text('Hello'):
    dwg.add(dwg.line((x1, y1), (x2 ,y2), stroke='blue', fill='none'))

dwg.save()