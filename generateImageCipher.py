from PIL import Image, ImageDraw
import binascii
import struct
import math
from random import *

width = 320
height = 240
center = (width / 2, height / 2)

braille = {
	'a' : [1,0,0,0,0,0],
	'b' : [1,0,1,0,0,0],
	'c' : [1,1,0,0,0,0],
	'd' : [1,1,0,1,0,0],
	'e' : [1,0,0,1,0,0],
	'f' : [1,1,1,0,0,0],
	'g' : [1,1,1,1,0,0],
	'h' : [1,0,1,1,0,0],
	'i' : [0,1,1,0,0,0],
	'j' : [0,1,1,1,0,0],
	'k' : [1,0,0,0,1,0],
	'l' : [1,0,1,0,1,0],
	'm' : [1,1,0,0,1,0],
	'n' : [1,1,0,1,1,0],
	'o' : [1,0,0,1,1,0],
	'p' : [1,1,1,0,1,0],
	'q' : [1,1,1,1,1,0],
	'r' : [1,0,1,1,1,0],
	's' : [0,1,1,0,1,0],
	't' : [0,1,1,1,1,0],
	'u' : [1,0,0,0,1,1],
	'v' : [1,0,1,0,1,1],
	'w' : [0,1,1,1,0,1],
	'x' : [1,1,0,0,1,1],
	'y' : [1,1,0,1,1,1],
	'z' : [1,0,0,1,1,1]
}

def letterToBraille(letter):
	if len(letter) == 1:
		return braille[letter.lower()]

def convertWordToBraille(word):
	converted_word = []
	for letter in word:
		converted_word.append(letterToBraille(letter))
	return converted_word

def mapWordToBrailleLocations(word, center):
	braille_word = convertWordToBraille(word)
	word_length = len(braille_word)
	dots = []
	for i in range(word_length):
		letter_center = int(float(center[0]) * 2.0 * (float(i) + 0.5) / float(word_length))
		dots.append((letter_center, braille_word[i]))
	return dots

def printDots(im, draw, dots, center):
	dot_size = 4
	gap_size = 2
	bbox_size = (dot_size) * 2 + gap_size

	for s in dots:
		w = s[0]
		h = center[1]
		for i in range(len(s[1])):
			if s[1][i] == 1:
				x = w + bbox_size * (float(i % 2) - 0.5)
				y = h + bbox_size * (int(i / 2) - 1)
				draw.ellipse((x - dot_size/2, y - dot_size/2, x + dot_size/2, y + dot_size/2), fill=(255,0,0), outline=(255,0,0))

def drawStatic(im, width, height)
	for i in range(0, width, width/8):
		m = randint(1, 100)
		for k in range(i, i + width/8):
			for j in range(0, height/8):
				r = randint(1, 100)
				im.putpixel((k,j), ((r+m)%100,m,r,255))
			for j in range(height*7/8, height):
				r = randint(1, 100)
				im.putpixel((k,j), ((r+m)%100,r,m,255))


im = Image.new("RGBA", (width, height), (0, 0, 0))
draw = ImageDraw.Draw(im)

dots = mapWordToBrailleLocations("testing", center)
printDots(im, draw, dots, center)
drawStatic(im, width, height)

im.save("loremipsum.png", "PNG")
