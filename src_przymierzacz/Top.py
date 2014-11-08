import math, copy
from FunkcjeNogawkowoRekawowe import *
from FunkcjePomocnicze import *
from WyginaczUbrania import *
class Top(FunkcjeNogawkowoRekawowe, FunkcjePomocnicze):

	def __init__(self,body_object, cloath_url):
		self.get_cloath_points(cloath_url)	
		self.licz_zakrycia_ciala(body_object)
		
		self.punkt_odniesienia_na_ciele = self.sredni_punkt(body_object.body['neck']['DL'], body_object.body['neck']['DR'])
		poprawka_wysokosci = -1* self.zakrycie['szyi']
		self.punkt_odniesienia_na_ciele[1]+=poprawka_wysokosci
		
		#dlugosc ubrania - self.suma_zakrycia
		body_h = self.suma_zakrycia
		#szerokosc ubrania -
		#body_w = body_object.widths['armpit']
		body_w = body_object.widths['sholder']
		poprawka_szerokosci =  body_w*self.cechy_ubrania['luz']
		body_w+=poprawka_szerokosci
		
		#skaluje
		wysokosc_ubrania = self.ubranie['koniec_M'][1]-self.ubranie['kolnierz_L'][1]
		print "szerokosci" ,body_w,body_h,  self.szerokosc['talii'],wysokosc_ubrania
		#self.skala =  self.get_scale(body_w,body_h,self.szerokosc['pach'],wysokosc_ubrania)
		self.skala =  self.get_scale(body_w,body_h,self.szerokosc['barkow'],wysokosc_ubrania)
		print self.skala, cloath_url
		sep = '/'
		filename,folder = self.get_filename_and_folder_from_url(cloath_url,sep)
		self.centralurl= folder+sep+'central'+filename
		self.Lparturl =None
		self.Rparturl =None
		
		self.skaluj_punkty_ubrania()
		self.centralurl= self.skaluj_zdjecie(self.centralurl)
		
		self.punkt_odniesienia_na_ubraniu = tuple(self.sredni_punkt(self.ubranie['kolnierz_L'],self.ubranie['kolnierz_R']))

		#obracanie calego ubrania
		self.obroc_punkty_ubrania(body_object.angles['sholder'][1],body_object.angles['sholder'][2],self.punkt_odniesienia_na_ubraniu)
		self.obroc_zdjecie(self.centralurl,-body_object.angles['sholder'][0],self.punkt_odniesienia_na_ubraniu)

		self.punkty_ubrania_przed_transformacja = copy.deepcopy(self.ubranie)
		self.transformuj_punkty_ubrania(self.punkt_odniesienia_na_ubraniu, -1,self.ubranie)
		self.transformuj_punkty_ubrania(self.punkt_odniesienia_na_ciele,1,self.ubranie)
		
		#wu = WyginaczUbrania( self.ubranie,body_object.brinks,body_object.body,self.punkty_ubrania_przed_transformacja,self.cechy_ubrania['luz'])
		#wu.wygnij_ubranie(self.centralurl)
		"""
		self.get_cloath_points(url)
		self.body_points = body_points
		self.brinks = brinks
		#self.srodek_ukladu_key = 'pacha_L'
		#self.punkt_odniesienia = body_points['armpit']['L'] 
		self.wektor_reki_L = [self.body_points['hand']['L'][0]-self.body_points['armpit']['L'][0], self.body_points['hand']['L'][1]-self.body_points['armpit']['L'][1]]
		self.wektor_reki_R = [self.body_points['hand']['R'][0]-self.body_points['armpit']['R'][0], self.body_points['hand']['R'][1]-self.body_points['armpit']['R'][1]]

		
		#self.srodek_ukladu = ((self.ubranie['pacha_L'][0]+self.ubranie['pacha_R'][0])/2.0,(self.ubranie['pacha_L'][1]+self.ubranie['pacha_R'][1])/2.0)
		#self.punkt_odniesienia = ((body_points['armpit']['L'][0]+body_points['armpit']['R'][0] )/2.0,(body_points['armpit']['L'][1]+body_points['armpit']['R'][1] )/2.0)
		
		self.srodek_ukladu = ((self.ubranie['kolnierz_L'][0]+self.ubranie['kolnierz_R'][0])/2.0,(self.ubranie['kolnierz_L'][1]+self.ubranie['kolnierz_R'][1])/2.0)
		self.punkt_odniesienia = ((body_points['neck']['DL'][0]+body_points['neck']['DR'][0] )/2.0,(body_points['neck']['DL'][1]+body_points['neck']['DR'][1] )/2.0)
		przesuniecie_do_gory = self.cechy_ubrania['zakrycieSzyi']*(body_points['neck']['DL'][1] -body_points['neck']['UL'][1])
		self.punkt_odniesienia= (self.punkt_odniesienia[0],self.punkt_odniesienia[1]-przesuniecie_do_gory)

		dlugosc_nog = (body_points['feet']['L'][1] + body_points['feet']['R'][1])/2.0 -(body_points['groin']['L'][1] + body_points['groin']['R'][1])/2.0
		wysokosc_bioder = (body_points['groin']['L'][1] + body_points['groin']['R'][1])/2.0 - (body_points['loin']['L'][1] + body_points['loin']['R'][1])/2.0
		wysokosc_talii = (body_points['loin']['L'][1] + body_points['loin']['R'][1])/2.0 - (body_points['waist']['L'][1] + body_points['waist']['R'][1])/2.0
		wysokosc_korpusu = (body_points['waist']['L'][1] + body_points['waist']['R'][1])/2.0 - (body_points['neck']['DL'][1] + body_points['neck']['DR'][1])/2.0
		pozadana_dlugosc = dlugosc_nog*self.cechy_ubrania['zakrycieNog']+ wysokosc_bioder*self.cechy_ubrania['zakrycieBioder'] + wysokosc_talii*self.cechy_ubrania['zakrycieTalii'] + wysokosc_korpusu

		dlug_topu = (self.ubranie['koniec_L'][1]+self.ubranie['koniec_R'][1])/2.0 - (self.ubranie['kolnierz_L'][1]+self.ubranie['kolnierz_R'][1])/2.0

		szer_topu = self.ubranie['pacha_R'][0]-self.ubranie['pacha_L'][0]
		szer_pach = self.count_diagonal_length(body_points['armpit']['R'],body_points['armpit']['L'])
		
		szer_barkow = self.count_diagonal_length(body_points['sholder']['R'],body_points['sholder']['L'])
		
		self.skala = [self.count_scale(szer_pach,szer_topu),self.count_scale(pozadana_dlugosc,dlug_topu)]
		print "Top SKALA ", self.skala
		ACx = abs(body_points["sholder"]["R"][0]-body_points["sholder"]["L"][0])
		BCy = abs(body_points["sholder"]["R"][1]-body_points["sholder"]["L"][1])
		self.count_rotation_sin_and_cos(szer_barkow, BCy , ACx)
		self.transformuj_punkty_ubrania()
		self.popraw_pachy()
		self.popraw_rekawy()
		self.popraw_kolnierz()
		self.popraw_barki()
		"""
	def popraw_pachy(self):
		#wektor_pacha_bark_L = self.get_vector(self.ubranie['pacha_L'],self.ubranie['bark_L'])
		#wektor_pacha_bark_R = self.get_vector(self.ubranie['pacha_R'],self.ubranie['bark_R'])
		#luz =self.cechy_ubrania['luz']
		#przes_L = [wektor_pacha_bark_L[0]*luz/2.0,-1*wektor_pacha_bark_L[1]*luz]
		#przes_R = [wektor_pacha_bark_R[0]*luz/2.0,-1*wektor_pacha_bark_R[1]*luz]
		#print przes_L , przes_R
		self.ubranie['pacha_L'] = self.find_best_brink_point(self.ubranie['pacha_L'],self.brinks['corpse_brink']['L'],'y')
		self.ubranie['pacha_R'] = self.find_best_brink_point(self.ubranie['pacha_R'],self.brinks['corpse_brink']['R'],'y')
		#self.ubranie['pacha_L']=(self.ubranie['pacha_L'][0]+przes_L[0],self.ubranie['pacha_L'][1]+przes_L[1])
		#self.ubranie['pacha_R']=(self.ubranie['pacha_R'][0]+przes_R[0],self.ubranie['pacha_R'][1]+przes_R[1])
		
	def popraw_rekawy(self):
		punkt_zaczepienia_L = self.body_points['armpit']['L']
		punkt_zaczepienia_R = self.body_points['armpit']['R']
		
		wektor_rekawu_L = [(self.ubranie['rekaw_L_R'][0]-self.ubranie['pacha_L'][0]),(self.ubranie['rekaw_L_R'][1]-self.ubranie['pacha_L'][1])]
		wektor_rekawu_R = [(self.ubranie['rekaw_R_L'][0]-self.ubranie['pacha_R'][0]),(self.ubranie['rekaw_R_L'][1]-self.ubranie['pacha_R'][1])]
		
		alfa_0L = self.find_alfa_angle(wektor_rekawu_L)
		alfa_0R = self.find_alfa_angle(wektor_rekawu_R)
		alfa_KL = self.find_alfa_angle(self.wektor_reki_L)
		alfa_KR = self.find_alfa_angle(self.wektor_reki_R)
		
		sin_L, cos_L =  math.sin(alfa_0L-alfa_KL),math.cos(alfa_0L-alfa_KL)
		sin_R, cos_R =  math.sin(alfa_0R-alfa_KR),math.cos(alfa_0R-alfa_KR)
		skalowanie_wektora = self.cechy_ubrania['zakrycieRak']
		self.poprawione_punkty['rekaw_L_L'] = self.rotate_and_fit(self.ubranie['rekaw_L_L'], punkt_zaczepienia_L, sin_L,cos_L,skalowanie_wektora)
		self.poprawione_punkty['rekaw_L_R'] = self.rotate_and_fit(self.ubranie['rekaw_L_R'], punkt_zaczepienia_L, sin_L,cos_L,skalowanie_wektora)
		
		self.poprawione_punkty['rekaw_R_R'] = self.rotate_and_fit(self.ubranie['rekaw_R_R'], punkt_zaczepienia_R, sin_R,cos_R,skalowanie_wektora)
		self.poprawione_punkty['rekaw_R_L'] = self.rotate_and_fit(self.ubranie['rekaw_R_L'], punkt_zaczepienia_R, sin_R,cos_R,skalowanie_wektora)
				
		self.poprawione_punkty['rekaw_R_R'] =self.find_best_brink_point(self.poprawione_punkty['rekaw_R_R'],
											self.brinks['arm_brink']['R']['outside'],'y')
											
		self.poprawione_punkty['rekaw_R_L'] =self.find_best_brink_point(self.poprawione_punkty['rekaw_R_L'],
											self.brinks['arm_brink']['R']['inside'],'y')
											
		self.poprawione_punkty['rekaw_L_L'] =self.find_best_brink_point(self.poprawione_punkty['rekaw_L_L'],
											self.brinks['arm_brink']['L']['outside'],'y')
											
		self.poprawione_punkty['rekaw_L_R'] =self.find_best_brink_point(self.poprawione_punkty['rekaw_L_R'],
											self.brinks['arm_brink']['L']['inside'],'y')				
								
											
	def popraw_kolnierz(self):
		self.poprawione_punkty['kolnierz_R'] =self.find_best_brink_point(self.ubranie['kolnierz_R'],
											self.brinks['neck_brink']['R']+self.brinks['sholder_brink']['R'],'y')
		self.poprawione_punkty['kolnierz_L'] =self.find_best_brink_point(self.ubranie['kolnierz_L'],
											self.brinks['neck_brink']['L']+self.brinks['sholder_brink']['L'],'y')
	
	def popraw_barki(self):
		self.poprawione_punkty['bark_R'] =self.find_best_brink_point(self.ubranie['bark_R'],
											self.brinks['arm_brink']['R']['outside']+self.brinks['sholder_brink']['R'],'y')
		self.poprawione_punkty['bark_L'] =self.find_best_brink_point(self.ubranie['bark_L'],
											self.brinks['arm_brink']['L']['outside']+self.brinks['sholder_brink']['L'],'y')
