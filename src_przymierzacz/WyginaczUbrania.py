from FunkcjeUbraniowe import *
from FunkcjePomocnicze import *
import cv2.cv as cv
import numpy as np

class WyginaczUbrania(FunkcjeUbraniowe, FunkcjePomocnicze):
	def __init__(self, punkty_ubrania, krawedzie_ciala,punkty_ciala, pkt_ubr_przed_trans, luz):
		self.luz =luz
		self.przesuniecia  = []
		self.przesunieciaCV,self.przesunieciaLV,self.przesunieciaRV =[],[],[]
		#rozdzielam punkty w zaleznosci w ktora strone sie zweza (w minus czy w plus)
		#na minus
		self.ujm_rozszerz = ['bark_L','talia_L','biodro_L','lokiec_L_L','lokiec_R_L','pas_L','kolano_L_L','kolano_R_L',
		'piszczel_L_L','piszczel_R_L','nogawka_L_L','nogawka_R_L']		
		#na plus
		self.dod_rozszerz = ['bark_R','talia_R','biodro_R','lokiec_R_R','lokiec_L_R','pas_R','kolano_L_R','kolano_R_R',
		'piszczel_L_R','piszczel_R_R','nogawka_L_R','nogawka_R_R']
		
		self.ujm_rozszerz_pion =['kolnierz_L','kolnierz_R']
		self.dod_rozszerz_pion =['nogawka_L_L','nogawka_L_R','nogawka_R_L','nogawka_R_R']
		
		for pu in punkty_ubrania:
			if pu=='kolnierz_L':
				#vp = self.get_vector(punkty_ubrania[pu],self.sredni_punkt(punkty_ciala['neck']['UL'],punkty_ciala['neck']['DL']))
				#self.przesuniecia.append([pkt_ubr_przed_trans[pu],vp])
				self.przesuniecia.append([punkty_ubrania[pu], self.sredni_punkt(punkty_ciala['neck']['UL'],punkty_ciala['neck']['DL'])])
			elif pu=='kolnierz_R':
				#vp = self.get_vector(punkty_ubrania[pu],self.sredni_punkt(punkty_ciala['neck']['UR'],punkty_ciala['neck']['DR']))
				#self.przesuniecia.append([pkt_ubr_przed_trans[pu],vp])
				self.przesuniecia.append([punkty_ubrania[pu], self.sredni_punkt(punkty_ciala['neck']['UR'],punkty_ciala['neck']['DR'])])				
			elif pu=='bark_L':
				#vp = self.get_vector(punkty_ubrania[pu],punkty_ciala['sholder']['L'])
				self.przesuniecia.append([punkty_ubrania[pu],punkty_ciala['sholder']['L']])
			elif pu=='bark_R':
				#vp = self.get_vector(punkty_ubrania[pu],punkty_ciala['sholder']['R'])
				self.przesuniecia.append([punkty_ubrania[pu],punkty_ciala['sholder']['R']])
			elif pu=='pacha_L':
				#vp = self.get_vector(punkty_ubrania[pu],punkty_ciala['armpit']['L'])
				self.przesuniecia.append([punkty_ubrania[pu],punkty_ciala['armpit']['L']])
			elif pu=='pacha_R':
				#vp = self.get_vector(punkty_ubrania[pu],punkty_ciala['armpit']['R'])
				self.przesuniecia.append([punkty_ubrania[pu],punkty_ciala['armpit']['R']])
			elif pu=='talia_L':
				pt = self.find_best_brink_point(punkty_ubrania[pu],krawedzie_ciala['corpse_brink']['L'],'y')
				#vp = self.get_vector(punkty_ubrania[pu],pt)
				self.przesuniecia.append([punkty_ubrania[pu],pt])
			elif pu=='talia_R':
				pt = self.find_best_brink_point(punkty_ubrania[pu],krawedzie_ciala['corpse_brink']['R'],'y')
				#vp = self.get_vector(punkty_ubrania[pu],pt)
				self.przesuniecia.append([punkty_ubrania[pu],pt])
			elif pu=='biodro_L':
				pt = self.find_best_brink_point(punkty_ubrania[pu],krawedzie_ciala['loin_brink']['L'],'y')
				#vp = self.get_vector(punkty_ubrania[pu],pt)
				self.przesuniecia.append([punkty_ubrania[pu],pt])
			elif pu=='biodro_R':
				pt = self.find_best_brink_point(punkty_ubrania[pu],krawedzie_ciala['loin_brink']['R'],'y')
				#vp = self.get_vector(punkty_ubrania[pu],pt)
				self.przesuniecia.append([punkty_ubrania[pu],pt])
			elif pu=='lokiec_L_L':
				pt = self.find_best_brink_point(punkty_ubrania[pu],krawedzie_ciala['arm_brink']['L']['outside'],'x')
				#vp = self.get_vector(punkty_ubrania[pu],pt)
				#vp = [vp[0],0]
				self.przesuniecia.append([punkty_ubrania[pu],pt])
			elif pu=='lokiec_L_R':
				pt = self.find_best_brink_point(punkty_ubrania[pu],krawedzie_ciala['arm_brink']['L']['inside'],'x')
				#vp = self.get_vector(punkty_ubrania[pu],pt)
				#vp = [vp[0],0]
				self.przesuniecia.append([punkty_ubrania[pu],pt])
			elif pu=='lokiec_R_L':
				pt = self.find_best_brink_point(punkty_ubrania[pu],krawedzie_ciala['arm_brink']['R']['inside'],'x')
				#vp = self.get_vector(punkty_ubrania[pu],pt)
				#vp = self.get_vector(punkty_ubrania[pu],punkty_ciala['elbow']['R']['inside'])
				#vp = self.luzuj_wektor(pu,vp)
				#vp = [vp[0],0]
				self.przesuniecia.append([punkty_ubrania[pu],pt])
			elif pu=='lokiec_R_R':
				pt = self.find_best_brink_point(punkty_ubrania[pu],krawedzie_ciala['arm_brink']['R']['outside'],'x')
				#vp = self.get_vector(punkty_ubrania[pu],pt)
				#vp = [vp[0],0]
				self.przesuniecia.append([punkty_ubrania[pu],pt])
			elif pu=='rekaw_L_L':
				pt = punkty_ciala['wrist']['L']['outside']
				#vp = self.get_vector(punkty_ubrania[pu],punkty_ciala['wrist']['L']['outside'])
				#pt = self.find_best_brink_point(punkty_ubrania[pu],krawedzie_ciala['arm_brink']['L']['outside'],'y')
				self.przesuniecia.append([punkty_ubrania[pu],pt])
			elif pu=='rekaw_L_R':
				pt = punkty_ciala['wrist']['L']['inside']
				#vp = self.get_vector(punkty_ubrania[pu],punkty_ciala['wrist']['L']['inside'])
				#pt = self.find_best_brink_point(punkty_ubrania[pu],krawedzie_ciala['arm_brink']['L']['inside'],'y')
				self.przesuniecia.append([punkty_ubrania[pu],pt])
			elif pu=='rekaw_R_L':
				pt = punkty_ciala['wrist']['R']['inside']
				#vp = self.get_vector(punkty_ubrania[pu],punkty_ciala['wrist']['R']['inside'])
				#pt = self.find_best_brink_point(punkty_ubrania[pu],krawedzie_ciala['arm_brink']['R']['inside'],'y')
				#vp = self.get_vector(punkty_ubrania[pu],pt)
				#self.przesunieciaRV.append([pkt_ubr_przed_trans[pu],vp])
				self.przesuniecia.append([punkty_ubrania[pu],pt])
			elif pu=='rekaw_R_R':
				pt = punkty_ciala['wrist']['R']['outside']
				#vp = self.get_vector(punkty_ubrania[pu],punkty_ciala['wrist']['R']['outside'])
				#pt = self.find_best_brink_point(punkty_ubrania[pu],krawedzie_ciala['arm_brink']['R']['outside'],'y')
				#vp = self.get_vector(punkty_ubrania[pu],pt)
				#self.przesunieciaRV.append([pkt_ubr_przed_trans[pu],vp])
				self.przesuniecia.append([punkty_ubrania[pu],pt])
				
			elif pu=='kolano_L_L':
				#vp = self.get_vector(punkty_ubrania[pu],punkty_ciala['knee']['L']['outside'])
				pt = self.find_best_brink_point(punkty_ubrania[pu],krawedzie_ciala['legs_brink']['L']['outside'],'y')
				#vp = self.get_vector(punkty_ubrania[pu],pt)
				#vp = self.luzuj_wektor(pu,vp)
				self.przesuniecia.append([punkty_ubrania[pu],pt])
			elif pu=='kolano_L_R':
				#vp = self.get_vector(punkty_ubrania[pu],punkty_ciala['knee']['L']['inside'])
				pt = self.find_best_brink_point(punkty_ubrania[pu],krawedzie_ciala['legs_brink']['L']['inside'],'y')
				#vp = self.get_vector(punkty_ubrania[pu],pt)
				#vp = self.luzuj_wektor(pu,vp)
				self.przesuniecia.append([punkty_ubrania[pu],pt])
			elif pu=='kolano_R_L':
				#vp = self.get_vector(punkty_ubrania[pu],punkty_ciala['knee']['R']['inside'])
				pt = self.find_best_brink_point(punkty_ubrania[pu],krawedzie_ciala['legs_brink']['R']['inside'],'y')
				#vp = self.get_vector(punkty_ubrania[pu],pt)
				#vp = self.luzuj_wektor(pu,vp)
				self.przesuniecia.append([punkty_ubrania[pu],pt])
			elif pu=='kolano_R_R':
				#vp = self.get_vector(punkty_ubrania[pu],punkty_ciala['knee']['R']['outside'])
				pt = self.find_best_brink_point(punkty_ubrania[pu],krawedzie_ciala['legs_brink']['R']['outside'],'y')
				#vp = self.get_vector(punkty_ubrania[pu],pt)
				#vp = self.luzuj_wektor(pu,vp)
				self.przesuniecia.append([punkty_ubrania[pu],pt])
			elif pu=='nogawka_L_L':
				#vp = self.get_vector(punkty_ubrania[pu],punkty_ciala['ankle']['L']['outside'])
				pt = self.find_best_brink_point(punkty_ubrania[pu],krawedzie_ciala['legs_brink']['L']['outside'],'y')
				#vp = self.get_vector(punkty_ubrania[pu],pt)
				#vp = self.luzuj_wektor(pu,vp)
				#print pu ,vp
				self.przesuniecia.append([punkty_ubrania[pu],pt])
				#self.przesunieciaLV.append([pkt_ubr_przed_trans[pu],vp])
			elif pu=='nogawka_L_R':
				#vp = self.get_vector(punkty_ubrania[pu],punkty_ciala['ankle']['L']['inside'])
				pt = self.find_best_brink_point(punkty_ubrania[pu],krawedzie_ciala['legs_brink']['L']['inside'],'y')
				#vp = self.get_vector(punkty_ubrania[pu],pt)
				#vp = self.luzuj_wektor(pu,vp)
				self.przesuniecia.append([punkty_ubrania[pu],pt])
				#self.przesunieciaLV.append([pkt_ubr_przed_trans[pu],vp])
			elif pu=='nogawka_R_L':
				#vp = self.get_vector(punkty_ubrania[pu],punkty_ciala['ankle']['R']['inside'])
				pt = self.find_best_brink_point(punkty_ubrania[pu],krawedzie_ciala['legs_brink']['R']['inside'],'y')
				#vp = self.get_vector(punkty_ubrania[pu],pt)
				self.przesuniecia.append([punkty_ubrania[pu],pt])
				#self.przesunieciaRV.append([pkt_ubr_przed_trans[pu],vp])
			elif pu=='nogawka_R_R':
				#vp = self.get_vector(punkty_ubrania[pu],punkty_ciala['ankle']['R']['outside'])
				pt = self.find_best_brink_point(punkty_ubrania[pu],krawedzie_ciala['legs_brink']['R']['outside'],'y')
				#vp = self.get_vector(punkty_ubrania[pu],pt)
				#vp = self.luzuj_wektor(pu,vp)
				self.przesuniecia.append([punkty_ubrania[pu],pt])
				#self.przesunieciaRV.append([pkt_ubr_przed_trans[pu],vp])
				
			elif pu=='piszczel_L_L':
				#vp = self.get_vector(punkty_ubrania[pu],punkty_ciala['crossbone']['L']['outside'])
				pt = self.find_best_brink_point(punkty_ubrania[pu],krawedzie_ciala['legs_brink']['L']['outside'],'y')
				#vp = self.get_vector(punkty_ubrania[pu],pt)
				#print pu , vp
				#vp = self.luzuj_wektor(pu,vp)
				self.przesuniecia.append([punkty_ubrania[pu],pt])
			elif pu=='piszczel_L_R':
				#vp = self.get_vector(punkty_ubrania[pu],punkty_ciala['crossbone']['L']['inside'])
				pt = self.find_best_brink_point(punkty_ubrania[pu],krawedzie_ciala['legs_brink']['L']['inside'],'y')
				#vp = self.get_vector(punkty_ubrania[pu],pt)
				#print pu , vp
				#vp = self.luzuj_wektor(pu,vp)
				self.przesuniecia.append([punkty_ubrania[pu],pt])
			elif pu=='piszczel_R_L':
				#vp = self.get_vector(punkty_ubrania[pu],punkty_ciala['crossbone']['R']['inside'])
				pt = self.find_best_brink_point(punkty_ubrania[pu],krawedzie_ciala['legs_brink']['R']['inside'],'y')
				#vp = self.get_vector(punkty_ubrania[pu],pt)
				#print pu , vp
				#vp = self.luzuj_wektor(pu,vp)
				self.przesuniecia.append([punkty_ubrania[pu],pt])
			elif pu=='piszczel_R_R':
				#vp = self.get_vector(punkty_ubrania[pu],punkty_ciala['crossbone']['R']['outside'])
				pt = self.find_best_brink_point(punkty_ubrania[pu],krawedzie_ciala['legs_brink']['R']['outside'],'y')
				#vp = self.get_vector(punkty_ubrania[pu],pt)
				#print pu , vp
				#vp = self.luzuj_wektor(pu,vp)
				self.przesuniecia.append([punkty_ubrania[pu],pt])
				
			elif pu=='pas_L':
				#vp = self.get_vector(punkty_ubrania[pu],punkty_ciala['waist']['L'])
				pt = self.find_best_brink_point(punkty_ubrania[pu],krawedzie_ciala['loin_brink']['L'],'y')
				#vp = self.luzuj_wektor(pu,self.get_vector(punkty_ubrania[pu],pt))
				#vp = self.get_vector(punkty_ubrania[pu],pt)
				#vp = [vp[0],0]
				self.przesuniecia.append([punkty_ubrania[pu],pt])
				#self.przesunieciaL.append([pkt_ubr_przed_trans[pu],vp])
			elif pu=='pas_R':
				#vp = self.get_vector(punkty_ubrania[pu],punkty_ciala['waist']['R'])
				pt = self.find_best_brink_point(punkty_ubrania[pu],krawedzie_ciala['loin_brink']['R'],'y')
				#vp = self.luzuj_wektor(pu,self.get_vector(punkty_ubrania[pu],pt))
				#vp = self.get_vector(punkty_ubrania[pu],pt)
				#print pu , vp , self.get_vector(punkty_ubrania[pu],pt)
				#vp = [vp[0],0]
				self.przesuniecia.append([punkty_ubrania[pu],pt])
				#self.przesunieciaC.append([pkt_ubr_przed_trans[pu],vp])
			elif pu=='krocze':
				vp = self.get_vector(punkty_ubrania[pu],self.sredni_punkt(punkty_ciala['groin']['L'],punkty_ciala['groin']['R']))
				#pt = self.find_best_brink_point(punkty_ubrania[pu],krawedzie_ciala['corpse_brink']['L'],'y')
				#vp = self.luzuj_wektor(pu,self.get_vector(punkty_ubrania[pu],pt))
				self.przesuniecia.append([punkty_ubrania[pu],pt])
			else:
				pass

	def wygnij_ubranie(self, imgC,imgL=None,imgR=None):
		#il =2
		stddevmult = 1.2
		mult =5.5
		for przes in self.przesuniecia:
			self.wygnij_gaussowsko2(imgC,przes[0],przes[1],stddevmult,mult)
		

		"""
		if imgL:
			for przes in self.przesunieciaL:
				p0, pk = przes[0] , [przes[0][0]+przes[1][0], przes[0][1]+przes[1][1]]
				self.wygnij_gaussowsko_poziomo(imgL,p0,pk,przes[1], il, abs(2.5*przes[1][0]))
			for przes in self.przesunieciaLV:
				p0, pk = przes[0] , [przes[0][0]+przes[1][0], przes[0][1]+przes[1][1]]
				self.wygnij_gaussowsko_pionowo(imgL,p0,pk,przes[1], il, 3*abs(przes[1][0]))
		if imgR:
			for przes in self.przesunieciaR:
				p0, pk = przes[0] , [przes[0][0]+przes[1][0], przes[0][1]+przes[1][1]]
				self.wygnij_gaussowsko_poziomo(imgR,p0,pk,przes[1], il, abs(2.5*przes[1][0]))
			for przes in self.przesunieciaRV:
				p0, pk = przes[0] , [przes[0][0]+przes[1][0], przes[0][1]+przes[1][1]]
				self.wygnij_gaussowsko2_pionowo(imgR,p0,pk,przes[1], il, 3*abs(przes[1][0]))
		"""
	def get_vector(self,p0,pk):
		v = [pk[0]-p0[0],pk[1]-p0[1]]
		return v
			
	def iloczyn_skalarny(self,v1, v2):
		return v1[0]*v2[0]+v1[1]*v2[1]
	
	def wygnij_gaussowsko2(self, img_url, p0, pk,stddevmult,mult):
		out = cv.LoadImage(img_url)
		img = cv.LoadImage(img_url)
		vw = self.get_vector(p0,pk)
		diffX = diffY = max(abs(vw[0]),abs(vw[1]))
		center = pk
		P0,PK=[0,0],[0,0]
		P0[0],P0[1] = center[0]-int(mult*diffX), center[1]-int(mult*diffY)   
		PK[0],PK[1] = center[0]+int(mult*diffX),center[1]+int(mult*diffY)
		xmin,xmax,ymin,ymax = min(P0[0],PK[0]),max(P0[0],PK[0]),min(P0[1],PK[1]),max(P0[1],PK[1])
	
		if xmin<0: xmin=0
		if ymin<0: ymin=0
		if xmax>img.width: xmax=img.width-1 
		if ymax>img.height: ymax=img.height-1
	
		roi = img[xmin:xmax , ymin:ymax]
		#center = (center[0]-xmin, center[1]-ymin)
		center = ((xmax-xmin)/2, (ymax-ymin)/2)
		center0 = (center[0]+xmin, center[1]+ymin)
		urltemp = 'test/dupachuj.jpg'
		cv.SaveImage(urltemp,roi)
		if vw[0]!=0:
			tan = vw[1]/float(vw[0])
			angle=math.atan(tan)
		else:
			abs_angle = math.pi/2.0
			if vw[1]>0:
				angle=abs_angle
			elif vw[1]<0:
				angle=-abs_angle
			else: 
				angle = 0
		sin_cos = [math.sin(angle), math.cos(angle)]
		roi_obrocone_url = self.obroc_zdjecie(urltemp, angle, center)
	
		#wyginanie gausowskie
		#	okreslam polozenie p0 i pk po obrocie w ukladzie ROI
		p0M = self.obroc_punkt_zmien_uklad(p0, angle, center,(xmin,ymin))
		pkM = self.obroc_punkt_zmien_uklad(pk, angle, center,(xmin,ymin))
		#	licze wektor p0->pk i wyginam poziomo gausowsko
		self.wygnij_gaussowsko_poziomo(urltemp, p0M,pkM,stddevmult)
		#ponowne obrocenie - do punktu poczatkowego
		roi_obrocone_url = self.obroc_zdjecie(urltemp, -angle, center)
		#przyciecie by nie bylo widac czarnego
		h , w = (ymax-ymin), (xmax-xmin)
		cos =  math.cos(math.degrees(angle))
		#cos =  0.5*math.sqrt(2)
		y02= int(h/2.0 - h/2.0*cos)
		x02= int(w/2.0 - w/2.0*cos)
		yk2= int(y02  +  h*cos)
		xk2= int(x02  +  w*cos)
		if x02<0:x02=0
		if y02<0:y02=0
		if x02>xk2:
			temp = x02
			x02,xk2=xk2,temp
		if y02>yk2:
			temp = y02
			y02,yk2=yk2,temp
		roi2 =cv.LoadImage(roi_obrocone_url)
		roi2= roi2[x02:xk2,y02:yk2]
		cv.SaveImage(urltemp, roi2)

		#roi2 =cv.LoadImage(roi_obrocone_url)
		self.wklej_zdjecie(img_url, roi_obrocone_url, center0)
	
	def obroc_punkt_zmien_uklad(self, p0, angle, center,(xmin,ymin)):
		sin_cos= [math.sin(-angle),math.cos(-angle)]
		p0M= [p0[0]-xmin-center[0],p0[1]-ymin-center[1]]
		p0M=self.rotate_vector(p0M,sin_cos[0],sin_cos[1])
		p0M= [int(p0M[0]+center[0]),int(p0M[1]+center[1])]
		return p0M

	def obroc_zdjecie(self, url,angle,  center):#parameter angel in degrees
		image = cv2.imread(url)
		height = image.shape[0]
		width = image.shape[1]
		image_center = (width/2, height/2)#rotation center
		rot_mat = cv2.getRotationMatrix2D(center,math.degrees(angle), 1)
		result = cv2.warpAffine(image, rot_mat, (width, height), flags=cv2.INTER_LINEAR)
		cv2.imwrite(url,result)
		return url
		
	def normalizeVector(self, vector):
		veclen = self.count_diagonal_length(vector,[0,0])
		if veclen>0:
			vector = [vector[0]/float(veclen),vector[1]/float(veclen)]
		return vector
	
	def count_diagonal_length(self, p1,p2):
		return math.sqrt((p1[0]-p2[0])**2 +(p1[1]-p2[1])**2)
	
	def rotate_vector(self,vector,sinBeta,cosBeta):
		x0,y0 = vector[0],vector[1]
		x = x0*cosBeta -y0*sinBeta
		y = x0*sinBeta +y0*cosBeta
		return [x,y]

	def wygnij_gaussowsko_poziomo(self,img_url, p0, pk,stddevmult):# ,il=4, mltpl=2.5):
		vw= [pk[0]-p0[0],pk[0]-p0[0]]
		#stddev = abs(vw[0]/2.9)
		stddev = max(abs(vw[0]),abs(vw[1]))*stddevmult
		#stddev = 200.0
		il=4
		out = cv.LoadImage(img_url)
		img = cv.LoadImage(img_url)
		if stddev<0.1: 
			return 0
		xmin, xmax = int(p0[0]-il*stddev) , int(pk[0]+il*stddev)
		ymin, ymax = int(p0[1]-il*stddev) , int(pk[1]+il*stddev)
		xmax, xmin = max(xmax,xmin), min(xmax,xmin)
		ymax, ymin = max(ymax,ymin), min(ymax,ymin)
		if xmin<0:xmin=0
		if xmax>=img.width-1:xmax= img.width-1
		if ymin<0:ymin=0
		if ymax>=img.height-1:ymax= img.height-1
	
		if xmin<0: xmin=0
		if ymin<0: ymin=0
		if xmax>img.width: xmax=img.width-1
		if ymax>img.height: ymax=img.height-1
	
		dymax = il*vw[1]
		il3 = 1/(1/(stddev*math.sqrt(2*math.pi)) *math.exp(0))
		for x in range(xmin,xmax):
			#licze roznice x miedzy punktem do przesuniecia i punktem docelowym glownym
			dx0 = pk[0]-x
			dx02 = dx0**2
			for y in range(ymin, ymax):
				#licze roznice wysokosci miedzy punktem do przesuniecia i punktem docelowym glownym
				dy0 = (pk[1]-y)
				dx = il3*vw[0]*(1/(stddev*math.sqrt(2*math.pi)) *math.exp((-(dy0**2+dx02)/2.0)/(2*stddev**2) ))
				pKon = (x+int(dx),y)
				if pKon[0]< img.width-1 and pKon[1]< img.height-1 and pKon[0]>0 and pKon[1]>0:
					cv.Set2D(out,pKon[1],pKon[0],cv.Get2D(img,y,x))
					cv.Set2D(out,pKon[1],pKon[0]+1,cv.Get2D(img,y,x))
					cv.Set2D(out,pKon[1],pKon[0]-1,cv.Get2D(img,y,x))
		cv.SaveImage(img_url,out)	
	
	def wklej_zdjecie(self, background_url, image_url, center):
		image = cv2.imread(image_url)
		print image.shape
		[w,h]= image.shape[:2]

		if w%2: #jesli dzieli  nieparzyste
			Sx= center[0]-w/2-1
		else:
			Sx= center[0]-w/2
			
		if h%2:#jesli dzieli nieparzyste
			Sy= center[1]-h/2-1
		else:
			Sy= center[1]-h/2
		
		background= cv2.imread(background_url)
		try:
			background[Sx:Sx+w ,Sy:Sy+h] = image
			cv2.imwrite(background_url,background)
		except:
			pass

	"""
	def wygnij_ubranie(self, imgC,imgL=None,imgR=None):
		il =2
		for przes in self.przesunieciaC:
			p0, pk = przes[0] , [przes[0][0]+przes[1][0], przes[0][1]+przes[1][1]]
			self.wygnij_gaussowsko_poziomo(imgC,p0,pk,przes[1], il, 5*abs(przes[1][0]))
		for przes in self.przesunieciaCV:
			p0, pk = przes[0] , [przes[0][0]+przes[1][0], przes[0][1]+przes[1][1]]
			self.wygnij_gaussowsko_pionowo(imgC,p0,pk,przes[1], il, 2*abs(przes[1][0]))
			
		if imgL:
			for przes in self.przesunieciaL:
				p0, pk = przes[0] , [przes[0][0]+przes[1][0], przes[0][1]+przes[1][1]]
				self.wygnij_gaussowsko_poziomo(imgL,p0,pk,przes[1], il, abs(2.5*przes[1][0]))
			for przes in self.przesunieciaLV:
				p0, pk = przes[0] , [przes[0][0]+przes[1][0], przes[0][1]+przes[1][1]]
				self.wygnij_gaussowsko_pionowo(imgL,p0,pk,przes[1], il, 3*abs(przes[1][0]))
		if imgR:
			for przes in self.przesunieciaR:
				p0, pk = przes[0] , [przes[0][0]+przes[1][0], przes[0][1]+przes[1][1]]
				self.wygnij_gaussowsko_poziomo(imgR,p0,pk,przes[1], il, abs(2.5*przes[1][0]))
			for przes in self.przesunieciaRV:
				p0, pk = przes[0] , [przes[0][0]+przes[1][0], przes[0][1]+przes[1][1]]
				self.wygnij_gaussowsko_pionowo(imgR,p0,pk,przes[1], il, 3*abs(przes[1][0]))

	def wygnij_gaussowsko_poziomo2(self,img_url, p0, pk,vw ,il, stddev0):
		if stddev0<=0:
			return 0
		out = cv.LoadImage(img_url)
		img = cv.LoadImage(img_url)
		
		if vw[0]>0:
			ax =[int(p0[0]-0.9*stddev0) , int(pk[0]+1.5*il*stddev0)]
		else:
			ax =[int(p0[0]-il*stddev0) , int(pk[0]+stddev0)]
		#ax =[int(p0[0]-3*vw[0]) , int(pk[0]+il*stddev0)]
		#ax =[int(p0[0]-il*stddev0) , int(pk[0]+vw[0])]
		#ax =[int(p0[0]-il*stddev0) , int(pk[0]+il*stddev0)]
		ay =[int(p0[1]-il*stddev0) , int(pk[1]+il*stddev0)]
		#ay =[int(p0[1]-il*abs(vw[0])) , int(pk[1]+il*abs(vw[0]))]
		xmin, xmax = min(ax), max(ax)
		ymin, ymax = min(ay) , max(ay)
		if xmin<0: xmin=0
		if ymin<0: ymin=0
		if xmax>=img.width: xmax=img.width-1
		if ymax>=img.height: ymax=img.height-1
	
		Dymax = 2*il*stddev0
		Dxmax = vw[0]+il*stddev0
		Dxmultip = 1/float(Dxmax)
		il3 = 1/(1/(stddev0*math.sqrt(2*math.pi)))
		#il3 =il3*il3
		for x in range(xmin,xmax):
			Dx = abs(p0[0]-x)
			#stddev = abs(1-abs(Dx/(Dxmax+0.001)))*stddev0
			stddev = stddev0*(1+Dx/float(Dxmax))
			for y in range(ymin, ymax):
				#licze roznice wysokosci miedzy punktem do przesuniecia i punktem docelowym glownym
				Dy = (y-p0[1])
				#powinno byc rowniez zalezne od Dx 
				dx = il3*vw[0]*( (1/(stddev*math.sqrt(2*math.pi))) *math.exp((-Dy**2)/(2*stddev**2)) ) #*(1/(stddev*math.sqrt(2*math.pi)) *math.exp((-Dx**2)/(2*stddev**2)))
				#pKon = (x+int(dx),y)
				pKon = (x-int(dx),y)
				if pKon[0]< img.width and pKon[1]< img.height and pKon[0]>-1 and pKon[1]>-1:
					#cv.Set2D(out,int(pKon[1]),int(pKon[0]),cv.Get2D(img,y,x))
					cv.Set2D(out,y,x,cv.Get2D(img,int(pKon[1]),int(pKon[0])))	
		cv.SaveImage(img_url,out)
		
	def wygnij_gaussowsko_poziomo(self,img_url, p0, pk,vw ,il, stddev):
		out = cv.LoadImage(img_url)
		img = cv.LoadImage(img_url)
		if stddev<0.1: 
			return 0
		xmin, xmax = int(p0[0]-il*stddev) , int(pk[0]+il*stddev)
		#xmin, xmax = p0[0]-il*int(stddev) , pk[0]+il*int(stddev)
		ymin, ymax = int(p0[1]-il*stddev) , int(pk[1]+il*stddev)
		#ymin, ymax = p0[1]-il*int(stddev) , pk[1]+il*int(stddev)
		xmax, xmin = max(xmax,xmin), min(xmax,xmin)
		ymax, ymin = max(ymax,ymin), min(ymax,ymin)
	
		if xmin<0: xmin=0
		if ymin<0: ymin=0
		if xmax>img.width: xmax=img.width-1
		if ymax>img.height: ymax=img.height-1
	
		dymax = il*vw[1]
		#il2 = 1/(1/(stddev*math.sqrt(2*math.pi)) *math.exp((-dymax**2)/(2*stddev**2) ))
		il3 = 1/(1/(stddev*math.sqrt(2*math.pi)) *math.exp(0))
		for x in range(xmin,xmax):
			#licze roznice x miedzy punktem do przesuniecia i punktem docelowym glownym
			dx0 = pk[0]-x
			dy = il3*vw[1]*(1/(stddev*math.sqrt(2*math.pi)) *math.exp((-dx0**2)/(2*stddev**2) ))
			for y in range(ymin, ymax):
				#licze roznice wysokosci miedzy punktem do przesuniecia i punktem docelowym glownym
				dy0 = (pk[1]-y)
				dx = il3*vw[0]*(1/(stddev*math.sqrt(2*math.pi)) *math.exp((-dy0**2)/(2*stddev**2) ))
				pKon = (x+int(dx),y+int(dy))
				if pKon[0]< img.width and pKon[1]< img.height and pKon[0]>-1 and pKon[1]>-1:
					cv.Set2D(out,pKon[1],pKon[0],cv.Get2D(img,y,x))
		cv.SaveImage(img_url,out)
			
	def wygnij_gaussowsko_pionowo(self,img_url, p0, pk,vw ,il, stddev0):
		if stddev0<=0:
			return 0
		out = cv.LoadImage(img_url)
		img = cv.LoadImage(img_url)
		
		if vw[0]>0:
			ay =[int(p0[1]-stddev0) , int(pk[1]+1.5*il*stddev0)]
		else:
			ay =[int(p0[1]-1.5*il*stddev0) , int(pk[1]+stddev0)]
		ax =[int(p0[0]-il*stddev0) , int(pk[0]+il*stddev0)]
		xmin, xmax = min(ax), max(ax)
		ymin, ymax = min(ay) , max(ay)
		if xmin<0: xmin=0
		if ymin<0: ymin=0
		if xmax>=img.width: xmax=img.width-1
		if ymax>=img.height: ymax=img.height-1
	
		Dxmax = 2*il*stddev0
		Dymax = vw[0]+il*stddev0
		Dymultip = 1/float(Dxmax)
		il3 = 1/(1/(stddev0*math.sqrt(2*math.pi)))
		for y in range(ymin,ymax):
			Dy = abs(p0[1]-y)
			stddev = stddev0*(1+Dy/float(Dymax))
			for x in range(xmin, xmax):
				#licze roznice wysokosci miedzy punktem do przesuniecia i punktem docelowym glownym
				Dx = (x-p0[0])
				#powinno byc rowniez zalezne od Dx 
				dy = il3*vw[1]*( (1/(stddev*math.sqrt(2*math.pi))) *math.exp((-Dx**2)/(2*stddev**2)) )
				pKon = (x,y-int(dy))
				if pKon[0]< img.width and pKon[1]< img.height and pKon[0]>-1 and pKon[1]>-1:
					cv.Set2D(out,y,x,cv.Get2D(img,int(pKon[1]),int(pKon[0])))	
		cv.SaveImage(img_url,out) 
	
	def luzuj_wektor3(self,nazwa_punktu, wektor, kierunek ='x' ):
		return wektor
		
	def luzuj_wektor2(self,nazwa_punktu, wektor ):
		luz = 1*self.luz
		if nazwa_punktu in self.ujm_rozszerz: #czyli lewa strona
			if wektor[0]>0: #zwezanie
				wektor = [int((1-luz)*wektor[0]),wektor[1]]
			else: 
				wektor = [int((1+luz)*wektor[0]),wektor[1]]
				
		if nazwa_punktu in self.dod_rozszerz: #czyli prawa strona
			if wektor[0]>0: #czyli rozszerz
				wektor = [int((1+luz)*wektor[0]),wektor[1]]
			else: 
				wektor = [int((1-luz)*wektor[0]),wektor[1]]
		return wektor
		
	def luzuj_wektor(self,nazwa_punktu, wektor ,kierunek='x' ):
		if kierunek =='x':
			luz =[self.luz, 0]
			ujm_rozsz = self.ujm_rozszerz
			dod_rozsz = self.dod_rozszerz
		else:
			luz =[0,3*self.luz]
			ujm_rozsz = self.ujm_rozszerz_pion
			dod_rozsz = self.dod_rozszerz_pion
			
		if nazwa_punktu in ujm_rozsz: #czyli lewa strona
			if wektor[1]>0: #zwezanie
				wektor = [int((1-luz[0])*wektor[0]),int((1-luz[1])*wektor[1])]
			else: 
				wektor = [int((1+luz[0])*wektor[0]),int((1-luz[1])*wektor[1])]
				
		if nazwa_punktu in dod_rozsz: #czyli prawa strona
			if wektor[1]>0: #czyli rozszerz
				wektor = [int((1+luz[0])*wektor[0]),int((1-luz[1])*wektor[1])]
			else: 
				wektor = [int((1-luz[0])*wektor[0]),int((1-luz[1])*wektor[1])]
		return wektor
	"""
