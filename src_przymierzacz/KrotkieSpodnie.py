from FunkcjeUbraniowe import *
class KrotkieSpodnie(FunkcjeUbraniowe):
	"""
	{'krocze': '(188,302)', 'pas_R': '(334,87)', 'nogawka_R_R': '(354,357)', 'nogawka_L_L': '(18,360)', 
	'nogawka_L_R': '(182,355)', 'pas_L': '(45,89)', 'nogawka_R_L': '(200,349)'}
	"""
	
	def __init__(self, body_points, brinks, url):
		self.get_cloath_points(url)
		self.srodek_ukladu_key = 'pas_L'
		self.punkt_odniesienia = body_points['waist']['L'] 
		
		szer_pasa = self.count_diagonal_length(body_points['waist']['L'] ,body_points['waist']['R'] )
		szer_spodni = self.ubranie['pas_R'][0]-self.ubranie['pas_L'][0]
		
		self.skala = self.count_scale(szer_pasa,szer_spodni)
		print "Spodnica SKALA ", self.skala
		ACx = abs(body_points["waist"]["R"][0]-body_points["waist"]["L"][0])
		BCy = abs(body_points["waist"]["R"][1]-body_points["waist"]["L"][1])
		self.count_rotation_sin_and_cos(szer_pasa, BCy , ACx)
		self.transformuj_punkty_ubrania()
		
