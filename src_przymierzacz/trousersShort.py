import math, copy
from FunkcjeNogawkowoRekawowe import *
from FunkcjePomocnicze import *
from Bender import *
class trousersShort(FunkcjePomocnicze,FunkcjeNogawkowoRekawowe):
	
	def __init__(self,body_object, cloath_url):
		self.get_cloath_points(cloath_url)	
		self.licz_zakrycia_ciala(body_object)
		
		self.punkt_odniesienia_na_ciele = self.sredni_punkt(body_object.body['groin']['L'], body_object.body['groin']['R'])
		#poprawka_wysokosci = -1* self.zakrycie['szyi']
		#self.punkt_odniesienia_na_ciele[1]+=poprawka_wysokosci
		
		#dlugosc ubrania - self.suma_zakrycia
		body_h = self.suma_zakrycia
		#szerokosc ubrania 
		body_w = body_object.widths['loin']
		poprawka_szerokosci =  body_w*self.cechy_ubrania['loose']
		body_w+=poprawka_szerokosci
	
		#this treshold is used when the bending of the cloath is processed
		treshold = 5
		
		#skaluje
		#wysokosc_ubrania = self.punktyUbrania['ankle#L#outside'][1]-self.punktyUbrania['loin#R'][1]
		self.skala =  self.get_scale(body_w,body_w,self.szerokosc['bioder'],self.szerokosc['bioder'])
		sep = '/'
		filename,folder = self.get_filename_and_folder_from_url(cloath_url,sep)
		self.Rparturl  = None
		#self.Lparturl  = folder+sep+'Lpart'  +filename
		self.Lparturl  = None
		self.centralurl= folder+sep+'central'+filename
		
		self.skaluj_punkty_ubrania()
		#self.Lparturl=   self.skaluj_zdjecie(self.Lparturl)
		#self.Rparturl=   self.skaluj_zdjecie(self.Rparturl)
		self.centralurl= self.skaluj_zdjecie(self.centralurl)
		
		#obracanie calego ubrania
		self.punkt_odniesienia_na_ubraniu = self.punktyUbrania['groin']#tuple(self.sredni_punkt(self.punktyUbrania['loin#L'],self.punktyUbrania['loin#R']))
		self.obroc_punkty_ubrania(body_object.angles['loin'][1],body_object.angles['loin'][2],self.punkt_odniesienia_na_ubraniu)
		#self.rotateImageAroundCenter(self.Lparturl,-body_object.angles['loin'][0],self.punkt_odniesienia_na_ubraniu)
		#self.rotateImageAroundCenter(self.Rparturl,-body_object.angles['loin'][0],self.punkt_odniesienia_na_ubraniu)
		
		self.punktyUbrania_przed_transformacja = copy.deepcopy(self.punktyUbrania)
		self.punktyUbrania = self.transformuj_punkty_liniowego_slownika(self.punkt_odniesienia_na_ubraniu, -1,self.punktyUbrania)
		self.punktyUbrania = self.transformuj_punkty_liniowego_slownika(self.punkt_odniesienia_na_ciele,1,self.punktyUbrania)
		
		self.bender = Bender(1.01, 3.0, body_object, self.punktyUbrania,self.punktyUbrania_przed_transformacja, self.brinkPointKeys,
						self.punkt_odniesienia_na_ubraniu, self.punkt_odniesienia_na_ciele, treshold )
		#self.bender.manageBends(self.Rparturl, kluczeR)
		#self.bender.manageBends(self.Lparturl, kluczeL)
		self.bender.manageBends(self.centralurl)
		
		"""
		print "PRAWA NOGA "
		kluczeR = ['loin#R','leg#R#outside','leg#R#inside']
		#punkt_odniesienia = tuple(self.punktyUbrania['armpit#R'])
		punkt_odniesienia = self.punktyUbrania['groin']
		rekaw_R = self.sredni_punkt(self.punktyUbrania['ankle#R#inside'],self.punktyUbrania['ankle#R#outside'])
		dlugosc_rekawa = self.count_diagonal_length(punkt_odniesienia,rekaw_R)
		ACx = rekaw_R[0]-punkt_odniesienia[0]
		BCy = rekaw_R[1]-punkt_odniesienia[1]
		sleeve_scale = abs(body_object.lenghts['legs']/float(BCy))*self.cechy_ubrania['legCover']
		sleeve_scaleX =abs(float(body_object.vectors['right_leg'][0])/ACx)
		sleeve_scaleY =abs(float(body_object.vectors['right_leg'][1])/BCy)*self.cechy_ubrania['legCover']
		#RpartScale = [sleeve_scaleX,sleeve_scaleY]
		RpartScale = [sleeve_scaleY, sleeve_scaleY]
		kat_pol_rekawa = ay =  self.count_rotation_sin_and_cos(dlugosc_rekawa, BCy, ACx)
		#TRZEBA ZMIENIC ROZPOZNAWANIE CZESCI CIALA NA PRZECIWNA STRONE
		kat_pol_reki = ax = body_object.angles['right_leg']
		sinx, siny = ax[1],ay[1]
		cosx, cosy = ax[2],ay[2]
		#print "OBROT PRAWEGO RAMIENIA ", (sinx**2+ cosx**2)
		sinXminusY = sinx*cosy - siny*cosx
		cosXminusY = cosx*cosy + sinx*siny
		#print "OBROT PRAWEGO RAMIENIA ", (sinXminusY**2+ cosXminusY**2)
		kat_obrotu = math.asin(sinXminusY)
		self.rotateImageAroundCenter(self.Rparturl, kat_obrotu, tuple(punkt_odniesienia))
		
		self.obroc_punkty_ubrania(-sinXminusY,cosXminusY,punkt_odniesienia,kluczeR)

		#po obrocie trzeba zeskalowac rekaw podlug dlugosci reki
		punkt_srodka_reki= self.sredni_punkt(punkt_odniesienia, rekaw_R)
		self.punktyUbrania = self.skaluj_zdjecie_i_przesun_o_wektor(self.Rparturl, RpartScale, punkt_odniesienia , self.punktyUbrania, kluczeR)
		#poszerzanie rekawa
		self.get_stretched_element(self.Rparturl, self.punktyUbrania, kluczeR, body_object.angles['right_leg'][0],stretchScale)

		
		###########lewa nogawka

		print "LEWA NOGA "
		kluczeL = ['loin#L','leg#L#outside','leg#L#inside','ankle#L#inside','ankle#L#outside','knee#L#inside','knee#L#outside']
		#punkt_odniesienia = tuple(self.punktyUbrania['armpit#R'])
		punkt_odniesienia = self.punktyUbrania['groin']
		rekaw_R = self.sredni_punkt(self.punktyUbrania['ankle#L#inside'],self.punktyUbrania['ankle#L#outside'])
		dlugosc_rekawa = self.count_diagonal_length(punkt_odniesienia,rekaw_R)
		ACx = rekaw_R[0]-punkt_odniesienia[0]
		BCy = rekaw_R[1]-punkt_odniesienia[1]
		sleeve_scale = abs(body_object.lenghts['legs']/float(BCy))*self.cechy_ubrania['legCover']
		sleeve_scaleX =abs(float(body_object.vectors['left_leg'][0])/ACx)
		sleeve_scaleY =abs(float(body_object.vectors['left_leg'][1])/BCy)*self.cechy_ubrania['legCover']
		#RpartScale = [sleeve_scaleX,sleeve_scaleY]
		RpartScale = [sleeve_scaleY, sleeve_scaleY]
		kat_pol_rekawa = ay =  self.count_rotation_sin_and_cos(dlugosc_rekawa, BCy, ACx)
		#TRZEBA ZMIENIC ROZPOZNAWANIE CZESCI CIALA NA PRZECIWNA STRONE
		kat_pol_reki = ax = body_object.angles['left_leg']
		sinx, siny = ax[1],ay[1]
		cosx, cosy = ax[2],ay[2]
		#print "OBROT PRAWEGO RAMIENIA ", (sinx**2+ cosx**2)
		sinXminusY = sinx*cosy - siny*cosx
		cosXminusY = cosx*cosy + sinx*siny
		#print "OBROT PRAWEGO RAMIENIA ", (sinXminusY**2+ cosXminusY**2)
		kat_obrotu = math.asin(sinXminusY)
		self.rotateImageAroundCenter(self.Rparturl, kat_obrotu, tuple(punkt_odniesienia))
		
		self.obroc_punkty_ubrania(-sinXminusY,cosXminusY,punkt_odniesienia,kluczeR)

		#po obrocie trzeba zeskalowac rekaw podlug dlugosci reki
		punkt_srodka_reki= self.sredni_punkt(punkt_odniesienia, rekaw_R)
		self.punktyUbrania = self.skaluj_zdjecie_i_przesun_o_wektor(self.Lparturl, RpartScale, punkt_odniesienia , self.punktyUbrania, kluczeR)
		#poszerzanie rekawa
		self.get_stretched_element(self.Lparturl, self.punktyUbrania, kluczeL, body_object.angles['left_leg'][0],stretchScale)
		"""
		
		self.punktyUbrania_przed_transformacja = copy.deepcopy(self.punktyUbrania)
		self.punktyUbrania = self.transformuj_punkty_liniowego_slownika(self.punkt_odniesienia_na_ubraniu, -1,self.punktyUbrania)
		self.punktyUbrania = self.transformuj_punkty_liniowego_slownika(self.punkt_odniesienia_na_ciele,1,self.punktyUbrania)
		"""
		self.bender = Bender(1.01, 3.0, body_object, self.punktyUbrania,self.punktyUbrania_przed_transformacja, self.brinkPointKeys,
						self.punkt_odniesienia_na_ubraniu, self.punkt_odniesienia_na_ciele, treshold )
		self.bender.manageBends(self.Rparturl, kluczeR)
		self.bender.manageBends(self.Lparturl, kluczeL)
		"""
