import math, copy
from FunkcjeNogawkowoRekawowe import *
from FunkcjePomocnicze import *
from Bender import *
class Skirt(FunkcjePomocnicze,FunkcjeNogawkowoRekawowe):
	
	def __init__(self,body_object, cloath_url):
		self.get_cloath_points(cloath_url)	
		self.licz_zakrycia_ciala(body_object)
		
		self.punkt_odniesienia_na_ciele = self.sredni_punkt(body_object.body['loin']['L'], body_object.body['loin']['R'])
		poprawka_wysokosci = 1* self.zakrycie['bioder']
		self.punkt_odniesienia_na_ciele[1]+=poprawka_wysokosci
		
		#dlugosc ubrania - self.suma_zakrycia
		body_h = self.suma_zakrycia
		#szerokosc ubrania 
		body_w = body_object.widths['loin']
		poprawka_szerokosci =  body_w*self.cechy_ubrania['loose']
		body_w+=poprawka_szerokosci
	
		#this treshold is used when the bending of the cloath is processed
		treshold = 5
		
		#skaluje
		self.skala =  self.get_scale(body_w,body_w,self.szerokosc['bioder'],self.szerokosc['bioder'])
		sep = '/'
		filename,folder = self.get_filename_and_folder_from_url(cloath_url,sep)
		self.Rparturl  = None
		#self.Lparturl  = folder+sep+'Lpart'  +filename
		self.Lparturl  = None
		self.centralurl= folder+sep+'central'+filename
		
		self.skaluj_punkty_ubrania()
		self.centralurl= self.skaluj_zdjecie(self.centralurl)
		
		#obracanie calego ubrania
		self.punkt_odniesienia_na_ubraniu = tuple(self.sredni_punkt(self.punktyUbrania['loin#L'],self.punktyUbrania['loin#R']))
		self.obroc_punkty_ubrania(body_object.angles['loin'][1],body_object.angles['loin'][2],self.punkt_odniesienia_na_ubraniu)		
		
		self.punktyUbrania_przed_transformacja = copy.deepcopy(self.punktyUbrania)
		self.punktyUbrania = self.transformuj_punkty_liniowego_slownika(self.punkt_odniesienia_na_ubraniu, -1,self.punktyUbrania)
		self.punktyUbrania = self.transformuj_punkty_liniowego_slownika(self.punkt_odniesienia_na_ciele,1,self.punktyUbrania)
		
		self.bender = Bender(1.01, 3.0, body_object, self.punktyUbrania,self.punktyUbrania_przed_transformacja, self.brinkPointKeys,
						self.punkt_odniesienia_na_ubraniu, self.punkt_odniesienia_na_ciele, treshold )
		self.bender.manageBends(self.centralurl)
		
		
		
