import os
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase import pdfmetrics, ttfonts

from foodgram.settings import MEDIA_ROOT


def create_pdf(buffer, content):
    path = os.path.join(MEDIA_ROOT, 'fonts/freesansbold.ttf')
    canvas = Canvas(buffer)
    pdfmetrics.registerFont(ttfonts.TTFont('FreeSans', path))
    canvas.setFont('FreeSans', 32)
    canvas.drawString(50, 50, content)
    canvas.showPage()
    canvas.save()
    return canvas

