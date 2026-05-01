'''
Feel free to mess around with the code here, all of it is preliminary and half of it doesn't work yet. I have to find a way
to be able to view PDFs in VSCode (they aren't naturally supported), but most of this stuff is good.
'''


### general ###

import pandas as pd
import pdfkit
import os
import numpy as np

### pdf specs ###

from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

### text specs ###

from reportlab.lib.colors import black, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import stringWidth


class System():
    def __init__(self):

        ### seting pdf and card size specs ###

        self.pdfW = 8.5
        self.pdfH = 11
        self.pdfPixW, self.pdfPixH = letter

        self.dpi = self.pdfPixW // self.pdfW

        self.cardW = 2.25
        self.cardH = 3.25
        self.cardPixW = self.cardW * self.dpi
        self.cardPixH = self.cardH * self.dpi

        ### defining bounds for cards for easier processing ###

        self.leftmost = (self.pdfPixW - self.cardPixW * 3) // 2
        self.rightmost = self.pdfPixW - self.leftmost
        self.topmost = (self.pdfPixH - self.cardPixH * 3) // 2
        self.botmost = self.pdfPixH - self.topmost

        ### setting font specs ###

        font_path = 'Chakra_Petch_Font_Family/Chakra Petch Regular 400.ttf'
        pdfmetrics.registerFont(TTFont('Chakra Petch', font_path))

        self.font = 'Chakra Petch'

        self.nameFontSize = 18
        self.slotFontSize = 20
        self.descriptionFontSize = 11
        self.cdFontSize = 20


class Page():
    def __init__(self, df, ind, pageType):
        self.df = df
        self.ind = ind
        self.pageType = pageType

        fileName = f'Card_Sheet_{ind}.pdf'
        self.pdf = canvas.Canvas(fileName, letter)
    

    def build(self):
        self.drawCardGrid()
        self.drawCards()


    def drawCardGrid(self):
        for i in range(4):
            self.pdf.line(system.leftmost, system.topmost + system.cardPixH * i, system.rightmost, system.topmost + system.cardPixH * i)
            self.pdf.line(system.leftmost + system.cardPixW * i, system.topmost, system.leftmost + system.cardPixW * i, system.botmost)


    def drawCards(self):
        for i in range(self.ind * 9, self.ind * 9 + 9):
            cardLeft = system.leftmost + system.cardPixW * (i // 3)
            cardTop = 0.5 * system.topmost + system.cardPixH * (3 - (i % 3))

            if self.pageType == 'ability':
                cardName = self.df['Name'].iloc[i]
                cardSlot = self.df['Slot'].iloc[i]
                cardDescription = self.df['Description'].iloc[i]
                cardCD = self.df['CD'].iloc[i]
                cardTags = self.df['Tags'].iloc[i]

            card = Card(self.pageType, cardLeft, cardTop)
            card.buildCard([cardName, cardSlot, cardDescription, cardCD, cardTags])
    
    
    def savePDF(self):
        self.pdf.save()


class Card():
    def __init__(self, cardType, x, y):
        self.cardType = cardType

        self.x = x
        self.y = y


    def buildCard(self, specs, isNecro=False):
        cardName, cardSlot, cardDescription, cardCD, cardTags = specs

        if self.cardType == 'ability':
            self.name(cardName)
            self.slot(cardSlot)

            if not isNecro:
                self.description(cardDescription)
                self.cd(cardCD)
            else:
                self.necro()

            self.tags(cardTags)


    def name(self, cardName):
        nameWidth = stringWidth(cardName, system.font, system.nameFontSize)
        scale = 100

        if nameWidth > 0.85 * system.cardPixW:
            scale = 0.85 * system.cardPixW * 100 / nameWidth

        nameObj = page.pdf.beginText()
        nameObj.setFont(system.font, system.nameFontSize)
        nameObj.setTextOrigin(self.x + 0.5 * (system.cardPixW - nameWidth * scale / 100), self.y)
        nameObj.setHorizScale(scale)
        nameObj.textOut(cardName)

        page.pdf.drawText(nameObj)
    

    def slot(self, cardSlot):
        slotWidth = stringWidth(cardSlot, system.font, system.slotFontSize)

        slotX = self.x + system.cardPixW // 8
        slotY = self.y - 0.82 * system.cardPixH

        slotObj = page.pdf.beginText()
        slotObj.setFont(system.font, system.slotFontSize)
        slotObj.setTextOrigin(slotX - 0.5 * slotWidth, slotY - 0.5 * slotWidth)
        slotObj.setHorizScale(100)
        slotObj.textOut(cardSlot)

        page.pdf.setFillColor(white)
        page.pdf.circle(slotX, slotY, system.cardPixW // 12, fill=1)
        page.pdf.setFillColor(black)
        page.pdf.drawText(slotObj)


    def description(self, cardDescription):
        descriptionObj = page.pdf.beginText()
        descriptionObj.setFont(system.font, system.descriptionFontSize)
        descriptionObj.setTextOrigin(self.x + 0.25 * system.cardPixW, self.y - 0.1 * system.cardPixH)
        descriptionObj.setHorizScale(100)

        lines = []
        line = ''

        for word in cardDescription:
            if line == '':
                line = word
            elif stringWidth(f'{line} {word}', system.font, system.descriptionFontSize) > 0.7 * system.cardPixW:
                lines.append(line)
                line = word
            else:
                line += f' {word}'
        lines.append(line)

        for line in lines:
            descriptionObj.textLine(line)

        page.pdf.drawText(descriptionObj)


    def cd(self, cardCD):
        cdWidth = stringWidth(cardCD, system.font, system.cdFontSize)

        cdX = self.x + int((7 / 8) * system.cardPixW)
        cdY = self.y - 0.82 * system.cardPixH

        cdObj = page.pdf.beginText()
        cdObj.setFont(system.font, system.cdFontSize)
        cdObj.setTextOrigin(cdX - 0.5 * cdWidth, cdY - 0.5 * cdWidth)
        cdObj.setHorizScale(100)
        cdObj.textOut(cardCD)

        page.pdf.setFillColor(white)
        page.pdf.circle(cdX, cdY, system.cardPixW // 12, fill=1)
        page.pdf.setFillColor(black)
        page.pdf.drawText(cdObj)


    def tags(self, cardTags):
        cardTags = cardTags.split(', ')

        for i, tag in enumerate(cardTags):
            tagWidth = system.cardPixW // 12 # with current setup, tagWidth = 13.0
            page.pdf.drawImage(f'symbols/{tag}_icon.png', self.x, self.y - tagWidth * i, width=tagWidth, height=tagWidth)


    def necro(self):

        ### separate handling for necromancy cards ###

        pass


if __name__ == '__main__':
    system = System()

    path = 'abilities.csv'
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
            page = Page(page_df, i // 9, 'ability')
            page.build()
            page.savePDF()
            