import cv2.cv as cv
import cv2
import ast
import math
import numpy as np
from FunkcjeUbraniowe import *

class Biustonosz(FunkcjeUbraniowe):

	"""
	{'ramiaczko_L': '(67,52)', 'ramiaczko_dol_L': '(63,157)', 'pas_R': '(345,320)', 'gorny_pas_L': '(19,217)',
	'gorny_pas_R': '(361,227)', 'pas_L': '(28,320)', 'ramiaczko_dol_R': '(318,160)', 'ramiaczko_R': '(320,56)'}
	
	{'hand': {'R': (513, 593), 'L': (210, 573)}, 'feet': {'R': (399, 1092), 'L': (231, 1098)}, 
	'loin': {'R': (458, 502), 'L': (252, 502)}, 'sholder': {'R': (493, 256), 'L': (229, 237)}, 
	'neck': {'UL': (337, 158), 'DL': (327, 183), 'DR': (414, 183), 'UR': (403, 158)}, 
	'waist': {'R': (436, 433), 'L': (275, 433)}, 'forhead': {'R': (421, 61), 'L': (316, 63)}, 
	'armpit': {'R': (436, 311), 'L': (284, 284)}, 'head_top': (363, 23), 'groin': {'R': (364, 569), 'L': (324, 569)}, 
	'ears': {'R': (428, 78), 'L': (310, 99)}}	
	"""
	def __init__(self, body_points, brinks, url):
		self.get_cloath_points(url)
		self.body_points = body_points
		self.brinks = brinks
		
		#self.punkt_odniesienia=body_points['armpit']['L']
		#self.srodek_ukladu = self.ubranie['gorny_pas_L']
		
		self.srodek_ukladu = ((self.ubranie['gorny_pas_L'][0]+self.ubranie['gorny_pas_R'][0])/2.0,(self.ubranie['gorny_pas_L'][1]+self.ubranie['gorny_pas_R'][1])/2.0)
		print "Srodek ukladu przed transformacja", self.srodek_ukladu
		self.punkt_odniesienia = ((body_points['armpit']['L'][0]+body_points['armpit']['R'][0] )/2.0,(body_points['armpit']['L'][1]+body_points['armpit']['R'][1] )/2.0)

		szer_pach = self.count_diagonal_length(body_points['armpit']['R'], body_points['armpit']['L'])
		szer = self.count_diagonal_length(body_points['sholder']['R'], body_points['sholder']['L'])

		szer_biustonosza = (self.ubranie['gorny_pas_R'][0] -self.ubranie['gorny_pas_L'][0])

		wys_biustonosza = (self.ubranie['gorny_pas_L'][1]+self.ubranie['gorny_pas_R'][1])/2.0 -(
		self.ubranie['ramiaczko_L'][1]+self.ubranie['ramiaczko_R'][1])/2.0
		
		wysokosc_pachy_szyja = (body_points['armpit']['R'][1]+body_points['armpit']['L'][1])/2.0-(body_points['neck']['DL'][1]+body_points['neck']['DR'][1])/2.0
		self.skala = [self.count_scale(szer_pach, szer_biustonosza)  ,self.count_scale(wysokosc_pachy_szyja, wys_biustonosza)]
		print "BIUSTONOSZ SKALA ",self.skala
		#licze sinusy i cosinusy do macierzy obrotu
		self.count_rotation_sin_and_cos(szer,abs(body_points['sholder']['R'][1]-body_points['sholder']['L'][1]),abs(body_points['sholder']['R'][0]-body_points['sholder']['L'][0]))
		self.transformuj_punkty_ubrania()
		self.popraw_pas_biustonosza()
		self.popraw_koniec_ramiaczek()
		
	def popraw_koniec_ramiaczek(self):
		sl = self.brinks['sholder_brink']['L']
		sr = self.brinks['sholder_brink']['R']
		rl = self.ubranie['ramiaczko_L']
		rr = self.ubranie['ramiaczko_R']
		
		self.poprawione_punkty['ramiaczko_L'] = self.find_best_brink_point(rl,sl,'x')
		self.poprawione_punkty['ramiaczko_R'] = self.find_best_brink_point(rr,sr,'x')
		
	def popraw_pas_biustonosza(self):
		self.poprawione_punkty['gorny_pas_R']= self.body_points['armpit']['R']
		self.poprawione_punkty['pas_L'] = self.find_best_brink_point(self.ubranie['pas_L'],
											self.brinks['corpse_brink']['L'],'y')
		self.poprawione_punkty['pas_R'] = self.find_best_brink_point(self.ubranie['pas_R'],
											self.brinks['corpse_brink']['R'],'y')

		
		
		
		
	
