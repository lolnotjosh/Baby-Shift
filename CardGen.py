import pandas as pd
import pdfkit
import os
import numpy as np

from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.lib.colors import black, white

class System(self):
    def __init__(self):

        ### seting pdf and card size specs ###

        self.pdfW = 8.5
        self.pdfH = 11
        self.pdfPixW, self.pdfPixH = letter

        self.dpi = pdfPixW // pdfW

        self.cardW = 2.25
        self.cardH = 3.25
        self.cardPixW = cardW * self.dpi
        self.cardPixH = cardH * self.dpi

        self.leftmost = (self.pdfPixW - self.cardPixW * 3) // 2
        self.rightmost = self.pdfPixW - self.leftmost
        self.topmost = (self.pdfPixH - self.cardPixH * 3) // 2
        self.botmost = self.pdfPixH - self.botmost

        ### setting font specs ###

        self.font = 'Chakra Petch'

        self.nameFontSize = 18
        self.slotFontSize = 20
        self.descriptionFontSize = 11
        self.cdFontSize = 20


class Page(self):
    def __init__(self, df, ind):
        self.df = df

        fileName = f'Card_Sheet_{ind}.pdf'
        self.pdf = canvas.Canvas(fileName, letter)
    

    def drawCardGrid(self):
        for i in range(4):
            self.pdf.line(system.leftmost, system.topmost + system.cardPixH * i, system.rightmost, system.topmost + system.cardPixH * i)
            self.pdf.line(system.leftmost + system.cardPixW * i, system.topmost, system.leftmost + system.cardPixW * i, system/botmost)


class Card(self):
    def __init__(self):
        pass

if __name__ == '__main__':
    system = System()

    path = ''
    df = pd.read_csv(path)
    cut_df = df[['Name', 'Slot', 'Description', 'CD', 'Tags']].copy()

    for i, cd in enumerate(cut_df['CD']):
        if cd.isalpha():
            cut_df.loc[i, 'CD'] = 'X'
        else:
            cut_df.loc[i, 'CD'] = str(int(cd))
    
    for i, card in enumerate(cut_df['Name']):
        if i % 9 == 0:
            page_df = cut_df[i : i + 9]
            Page(page_df, i // 9)

            