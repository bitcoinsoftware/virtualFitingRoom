import ast, math
import cv2.cv as cv
import cv2
import numpy as np
from FunkcjePomocnicze import *
class FunkcjeUbraniowe(FunkcjePomocnicze):
	def __init__(self):
		pass
		
	def get_cloath_points(self, url):
		self.url = url
		self.poprawione_punkty={}
		self.constantPointsKeys =[]
		self.brinkPointsKeys	=[]
		self.punktyStale,self.cechy_ubrania, self.punktyRuchome={},{},{}
		wartosci =  ast.literal_eval(open(url+".txt").read()) #otrzymuje tablice tupli
		for katka in wartosci:
			if katka[0].find('otherKeys#')>-1:
				self.cechy_ubrania[katka[0].replace('otherKeys#','')]=katka[1]
			elif katka[0].find('brinkKeys')>-1: 
				self.punktyRuchome[katka[0].replace('brinkKeys#','')]=katka[1]
			elif katka[0].find('pointKeys')>-1:
				self.punktyStale[katka[0].replace('pointKeys#','')]= katka[1]
				
		self.brinkPointKeys = self.punktyRuchome.keys()
		self.constantPointKeys = self.punktyStale.keys()
				
		self.punktyUbrania = {}
		self.punktyUbrania.update(self.punktyRuchome)
		self.punktyUbrania.update(self.punktyStale)

		try:bioder = self.punktyUbrania['loin#L'][0]-self.punktyUbrania['loin#R'][0]
		except: bioder = 0
		try:talii = self.punktyUbrania['corpse#L'][0]-self.punktyUbrania['corpse#R'][0]
		except: talii = 0
		try:pach = self.punktyUbrania['armpit#L'][0]-self.punktyUbrania['armpit#R'][0]
		except: pach = 0
		try:barkow = self.punktyUbrania['sholder#L'][0]-self.punktyUbrania['sholder#R'][0]
		except: barkow = 0
		try:kolnierza = self.punktyUbrania['neck#L'][0]-self.punktyUbrania['neck#R'][0]
		except: kolnierza=0
		
		self.szerokosc = {'bioder':bioder,'talii':talii,'pach':pach,'barkow':barkow,'kolnierza':kolnierza}
					
	def licz_zakrycia_ciala(self, body_object):
		try:szyi = self.cechy_ubrania['neckCover']*body_object.lenghts['neck']		; 
		except: szyi=0
		try: talii= self.cechy_ubrania['waistCover']*body_object.lenghts['waist']	; 
		except: talii=0
		try: bioder=self.cechy_ubrania['loinCover']*body_object.lenghts['loin']	; 
		except: bioder=0
		try: nog = self.cechy_ubrania['legCover']*body_object.lenghts['legs']		; 
		except: nog=0
		try: reki_L = self.cechy_ubrania['handCover']*body_object.lenghts['hand_L']	; 
		except: reki_L=0
		try: reki_R = self.cechy_ubrania['handCover']*body_object.lenghts['hand_R']	; 
		except: reki_R=0
		try: tulowia = self.cechy_ubrania['corpseCover']*body_object.lenghts['corpse']	; 
		except: tulowia=0
		
		self.zakrycie = {'szyi':szyi,'talii':talii,'bioder':bioder,
		'nog':nog,'reki_L':reki_L,'reki_R':reki_R,'tulowia':tulowia}
		self.suma_zakrycia = szyi+talii+bioder+nog+tulowia
		
	def find_best_brink_point(self,pt,brink,direction="x"):
		if direction=="x":
			index=0
		else:
			index=1
		best = brink[0]
		dist = abs(pt[index]-best[index])
		for b in brink:
			if abs(pt[index]-b[index])<dist:
				dist=abs(pt[index]-b[index])
				best = b
		return best 
	

	def transformuj_srodek_ukladu_ubraniowego(self):
		self.srodek_ukladu = self.rotate_vector(self.srodek_ukladu)
		self.srodek_ukladu = self.skaluj(self.srodek_ukladu)
			
	def get_scale(self, body_w,body_h,szerokosc_ubrania,wysokosc_ubrania):
		sx = body_w/float(szerokosc_ubrania)
		sy = body_h/float(wysokosc_ubrania)
		return [sx,sy]
	
	def skaluj(self,point,skala):
		return (skala[0]*point[0],skala[1]*point[1])
		
	def skaluj_punkty_ubrania(self,klucze=None , skala=None):
		if not klucze:
			klucze = self.punktyUbrania.keys()
		if not skala:
			skala = self.skala
		for key in klucze:
			self.punktyUbrania[key] = self.skaluj(self.punktyUbrania[key],skala)
			
	def obroc_punkty_ubrania(self,sin,cos,punkt_odniesienia,klucze=[]):
		if len(klucze)==0:
			klucze = self.punktyUbrania.keys()
		for key in klucze:
			vector = [self.punktyUbrania[key][0]-punkt_odniesienia[0], self.punktyUbrania[key][1]-punkt_odniesienia[1]]
			vector2 = self.rotate_vector(vector, sin,cos)
			self.punktyUbrania[key] = [vector2[0]+punkt_odniesienia[0], vector2[1]+punkt_odniesienia[1]]
		

			
	def skaluj_zdjecie(self, url,scale=None):
		if not scale:
			scale = self.skala
		frame = cv.LoadImage(url)
		cv.Threshold(frame, frame, 254,0, cv.CV_THRESH_TOZERO_INV)
		cv.Threshold(frame, frame, 1,254, cv.CV_THRESH_TOZERO)
		ht, wt = frame.height, frame.width
		nht,nwt = int(ht*scale[1]), int(wt*scale[0])
		out = cv.CreateImage((nwt,nht), 8, 3)
		cv.Resize(frame,out)
		filename = 'test/'+url.split('/')[-1]
		cv.SaveImage(filename,out)
		return filename
		
	def skaluj_zdjecie_i_przesun_o_wektor(self,url, Scale,P0,dictionary, dictKeys):

		frame = cv.LoadImage(url)
		cv.SetZero(frame)
		splited_url = url.split('.')
		splited_url[0]+='TEMP'
		bgUrl = '.'.join(splited_url)
		cv.SaveImage(bgUrl,frame)
		url = self.skaluj_zdjecie(url, Scale)
		scaledFrame = cv2.imread(url)
		bgFrame = cv2.imread(bgUrl)
		w = bgFrame.shape[1]
		h =bgFrame.shape[0]
		
		x0Prim=int(Scale[0]*P0[0])
		y0Prim=int(Scale[1]*P0[1])
		wPrim=scaledFrame.shape[1]
		hPrim=scaledFrame.shape[0]
		
		if Scale[0]>1 and Scale[1]<=1:
			bgFrame[P0[1]-y0Prim:P0[1]-y0Prim+hPrim,0: ] = scaledFrame[0:,
			x0Prim-P0[0]:x0Prim-P0[0]+w]
			
		elif Scale[0]<=1 and Scale[1]<=1:
			bgFrame[P0[1]-y0Prim:P0[1]-y0Prim+hPrim, P0[0]-x0Prim:P0[0]-x0Prim+wPrim] =scaledFrame
		WekPrzes= [P0[0]-x0Prim,P0[1]-y0Prim]
		
		cv2.imwrite(url,bgFrame)
		for key in dictKeys:
			dictionary[key]= [dictionary[key][0]*Scale[0]+WekPrzes[0],dictionary[key][1]*Scale[1]+WekPrzes[1]]
		return dictionary
		
		
	def rotateImageAroundCenter(self, url,angel,  center):#parameter angel in degrees
		image = cv2.imread(url)
		height = image.shape[0]
		width = image.shape[1]
		rot_mat = cv2.getRotationMatrix2D(center,math.degrees(angel), 1)
		result = cv2.warpAffine(image, rot_mat, (width, height), flags=cv2.INTER_LINEAR)
		cv2.imwrite(url,result)
		
		
	def find_rotation_sin_and_cos(self, startvect, finalvect):
		startvectNorm = self.normalizeVector(startvect)
		fianlvectNorm = self.normalizeVector(finalvect)
		diffvect = [fianlvectNorm[0] - startvectNorm[0],fianlvectNorm[1] - startvectNorm[1]]
		vectlen = self.count_diagonal_length(diffvect, [0,0])
		sin,cos =0,1
		if vectlen>0:
			sin =diffvect[0]/vectlen
			cos =diffvect[1]/vectlen
		return sin,cos
		
	def count_start_and_stop_points(self,  body_point,cloath_point,cloath_frame,body_frame):
		sx = int(body_point[0]-cloath_point[0])
		sy = int(body_point[1]-cloath_point[1])
		if sx<0: sx=0
		if sy<0: sy=0
		start_point =[sx,sy]
		stx =int(start_point[0]+cloath_frame.width-1)
		sty =int(start_point[1]+cloath_frame.height-1)
		if stx>=body_frame.width: stx=body_frame.width-1
		if sty>=body_frame.height: stx=body_frame.height-1
		stop_point =[stx,sty]
		return start_point, stop_point
		
	def paste_cloath(self, cloath_url, body_url, out_url):
		self.transformuj_srodek_ukladu_ubraniowego()
		#cloath_frame, body_frame = cv.LoadImageM(cloath_url), cv.LoadImageM(body_url)
		cloath_frame, body_frame = cv.LoadImage(cloath_url), cv.LoadImageM(body_url)
		zero_point,end_point= self.count_start_and_stop_points(self.punkt_odniesienia, self.srodek_ukladu,cloath_frame, body_frame)
		ix,iy=0,0
		
		stoper =0
		for x in range(zero_point[0],end_point[0]):
			iy=0
			for y in range(zero_point[1],end_point[1]):
				try:
					#if sum(cv.Get2D(cloath_frame,iy,ix))>0:
					if cv.Get2D(cloath_frame,iy,ix)[4]>0 or sum(cv.Get2D(cloath_frame,iy,ix))>0:
						cv.Set2D(body_frame, y, x,cv.Get2D(cloath_frame,iy,ix))
				except:
					#print "iy , ix ", iy,ix
					stoper = 1
					break
				iy+=1
			ix+=1
			if stoper: break
		cv.SaveImage(out_url,body_frame)
		
	def get_smallest_rectangle(self,pointDictionary, keys,image_size, scale=1.4):
		Xses , Yses =[],[]
		for key in keys:
			Xses.append(pointDictionary[key][0])
			Yses.append(pointDictionary[key][1])
		maxX , minX = max(Xses), min(Xses)  
		maxY , minY = max(Yses), min(Yses)
		if scale!=1:
			width = maxX-minX
			height= maxY-minY
			
			extensionX,extensionY  = (scale- 1)*width/2, (scale-1)*height/2
			maxX+=extensionX ; minX-=extensionX
			maxY+=extensionY ; minY-=extensionY
			if minX<0: minX=0
			if maxX>=image_size[0]:maxX=image_size[0]-1
			if minY<0: minY=0
			if maxY>=image_size[1]:maxY=image_size[1]-1
		#print "NAJMNIEJSZY KWADRACIK ", [[minX,minY],[maxX,maxY]]
		return [[minY,minX],[maxY,maxX]]
		
	def get_stretched_element(self,image_url,pointDictionary, keys, alfa,stretchScale):
		originalImage = cv2.imread(image_url)
		rectangle = self.get_smallest_rectangle(pointDictionary, keys, originalImage.shape)
		roiImage = originalImage[rectangle[0][0]:rectangle[1][0],rectangle[0][1]:rectangle[1][1]]
		roiImage = self.rotateImage(roiImage, alfa)
		cv2.imwrite(image_url, roiImage)
		
		self.skaluj_zdjecie(image_url, stretchScale)
		roiImageScaled = cv2.imread(image_url)
		roiImageScaled = self.rotateImage(roiImageScaled, -alfa)
		#wklejam przeskalowane zdjecie
		center = [(rectangle[0][0]+rectangle[1][0])/2, (rectangle[0][1]+rectangle[1][1])/2]
		originalImageModified = self.pasteImage2(originalImage,roiImageScaled,[int(center[0]),int(center[1])])
		
		cv2.imwrite(image_url,originalImageModified)
		
		
	def pasteImage2(self, background, image, center):
		c_img = (image.shape[0]/2,image.shape[1]/2)
		h= image.shape[1]
		w= image.shape[0]
		Dxp = Dxm = w/2
		Dyp = Dym = h/2
		maxDxp = abs(w - center[0])
		maxDxm = center[0]
		maxDyp = abs(h -center[1])
		maxDym = center[1]
		if Dxp > maxDxp: Dxp = maxDxp
		if Dxm > maxDxm: Dxm = maxDxm
		if Dyp > maxDyp: Dyp = maxDyp
		if Dym > maxDym: Dym = maxDym
		hBg = background.shape[1]
		wBg = background.shape[0]
		
		background[center[0]-Dxm:center[0]+Dxp , center[1]-Dym:center[1]+Dyp] = image[c_img[0]-Dxm:c_img[0]+Dxp , c_img[1]-Dym:c_img[1]+Dyp]
		#print 'background[',center[0]-Dxm,':',center[0]+Dxp,' , ',center[1]-Dym,':',center[1]+Dyp,'] = image[',c_img[0]-Dxm,':',c_img[0]+Dxp,' , ',c_img[1]-Dym,':',c_img[1]+Dyp,']'
		return background
		
