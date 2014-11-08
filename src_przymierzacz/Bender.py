import cv2.cv as cv
import cv2
import numpy as np
import math
from FunkcjePomocnicze import *
from FunkcjeUbraniowe import *

class Bender(FunkcjePomocnicze, FunkcjeUbraniowe):
	def __init__(self, stdevMult, mult,bodyObject, clothDict, clothDictBeforeTrans, brinkPointKeys, clothBasePoint,bodyBasePoint, treshold =1, divider='#'):
		self.stdevMult= stdevMult
		self.mult = mult
		self.divider = divider
		self.diff_treshold = treshold #minimal amount of pix when the cloth gets bended
		self.bodyPointsLinearDict = dict(self.make_linear_array(bodyObject.body))
		self.bodyBrinksLinearDict = dict(self.make_linear_array(bodyObject.brinks))
		self.brinkPointKeys = brinkPointKeys
		
		#musze przetrasformowac punkty i brinksy do ukladu ubrania
		"""
		self.bodyPointsLinearDict = self.transformuj_punkty_liniowego_slownika(bodyBasePoint ,-1,self.bodyPointsLinearDict)
		self.bodyPointsLinearDict = self.transformuj_punkty_liniowego_slownika(clothBasePoint, 1,self.bodyPointsLinearDict)
		
		self.bodyBrinksLinearDict = self.transformuj_punkty_liniowego_slownika(bodyBasePoint ,-1,self.bodyBrinksLinearDict)
		self.bodyBrinksLinearDict = self.transformuj_punkty_liniowego_slownika(clothBasePoint , 1,self.bodyBrinksLinearDict)
		"""
		self.clothTupleArray = clothDict.items()
		self.clothTupleArrayBeforeTrans = clothDictBeforeTrans.items()
		
	def manageBends(self, imageUrl, dictKeys=None):
		#load cruicial prameters
		self.out = cv2.imread(imageUrl)
		self.img = cv2.imread(imageUrl)
		self.imageUrl = imageUrl
		#przechodze po tablicy tupli z punktami ubrania
		i=0
		for clothTuple in self.clothTupleArray:
			clothTupleBeforeTrans = self.clothTupleArrayBeforeTrans[i]
			i+=1
			if dictKeys!=None:
				if clothTuple[0] not in dictKeys:
					continue
				else:
					pass
			splClTuplIndex = clothTuple[0].split(self.divider)
			paramList = [0,1,1]
			if clothTuple[0] in self.brinkPointKeys:
				paramList[0]=1
			if 'inside' in splClTuplIndex:
				paramList[1]=-1
			if 'L' in splClTuplIndex:
				paramList[2]=-1
			p0 = clothTuple[1]
			#p0 = (clothTuple[1][0]-self.basePoint[0], clothTuple[1][1] - self.basePoint[1])
			#if it's a movable point find the best place for it
			if paramList[0]:
				pk = self.find_best_brink_point(clothTuple[1], self.bodyBrinksLinearDict[clothTuple[0]], "r")
			else:
				pk = self.bodyPointsLinearDict[clothTuple[0]]
			#pk = (pk[0]-self.basePoint[0], pk[1] - self.basePoint[1])
			#if we the cloth should be shrinked, we decreese the shrinking vector, 
			#beacause it's more important to get the body covered than to get the 
			#cloth streached
			if (paramList[1]*paramList[2]<0):
				pk=self.sredni_punkt(p0, pk)
				
			vec = 	self.get_vector(p0 , pk)
			#vec = [vec[0],0]
			vec = [vec[0],0]
			p0BeforeTrans = clothTupleBeforeTrans[1] 
			pkBeforeTrans = (int(p0BeforeTrans[0]+vec[0]), int(p0BeforeTrans[1]+vec[1]))
				
			if abs(vec[0])>self.diff_treshold:
				print  "gaussian bend", splClTuplIndex ,vec[0], vec[1]
				try:
					self.img = self.gaussianBend(p0BeforeTrans, pkBeforeTrans)
					#cv2.circle(self.img, (int(p0[0]),int(p0[1])), 5,(255,0,0,0),4)
					cv2.circle(self.img, (int(p0BeforeTrans[0]),int(p0BeforeTrans[1])), 5,(255,0,0,0),4)
					#cv2.circle(self.img , tuple(pk),5, (0,0, 255, 0), 4)
					cv2.circle(self.img , tuple(pkBeforeTrans),5, (0,0, 255, 0), 4)
				except:
					print "this bend fucked up"
		cv2.imwrite(self.imageUrl , self.img)
				
	def gaussianBend(self, p0, pk):
		vw = self.get_vector(p0,pk)
		diffX = diffY = max(abs(vw[0]),abs(vw[1]))
		P0,PK=[0,0],[0,0]
		P0[0],P0[1] = pk[0]-int(self.mult*diffX), pk[1]-int(self.mult*diffY)   
		PK[0],PK[1] = pk[0]+int(self.mult*diffX), pk[1]+int(self.mult*diffY)
		xmin,xmax,ymin,ymax = min(P0[0],PK[0]),max(P0[0],PK[0]),min(P0[1],PK[1]),max(P0[1],PK[1])
		Dx = Dy = 0
		
		if xmin<0: 
			Dx= -xmin
			xmin=0
		elif xmax>	self.img.shape[1]:
			Dx= self.img.shape[1] - xmax
			xmax=self.img.shape[1]
		if ymin<0: 
			Dy= -ymin
			ymin=0
		elif ymax>self.img.shape[0]: 
			Dy= self.img.shape[0] - ymax
			ymax=self.img.shape[0]
			
		if Dx:
			ymin-=Dx/2
			ymax+=Dx/2
		if Dy: 
			xmin-=Dy/2
			xmax+=Dy/2
		#we take only the region of interest which best fits the element
		roi = self.img[ymin:ymax , xmin:xmax]
	
		center = ((ymax-ymin)/2, (xmax-xmin)/2)
		center0 = (center[1]+ymin, center[0]+xmin)
		
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
		#BYC MOZE BEDZIE TRZEBA ZROBIC NAJPIERW KOPIE
		roi_obrocone = self.rotateImage(roi, angle, center)
		

		
		#wyginanie gausowskie
		#	okreslam polozenie p0 i pk po obrocie w ukladzie ROI
		p0M = self.rotatePointChangeCoordSystem(p0, angle, center,(xmin,ymin))
		pkM = self.rotatePointChangeCoordSystem(pk, angle, center,(xmin,ymin))
		#	licze wektor p0->pk i wyginam poziomo gausowsko
		
		#	licze wektor p0->pk i wyginam poziomo gausowsko
		roi_obrocone_wygiete = self.horizontalGaussianBend(roi_obrocone, p0M,pkM,self.stdevMult)
		
		#ponowne obrocenie - do punktu poczatkowego
		roi_wygiete = self.rotateImage(roi_obrocone_wygiete, -angle, center)
		
		#przyciecie by nie bylo widac czarnego
		h , w = (ymax-ymin), (xmax-xmin)
		cos =  math.cos(math.degrees(angle))
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
		roi2= roi_wygiete[x02:xk2,y02:yk2]
		
		result = self.pasteImage(self.out, roi_wygiete, center0)
		return result
		
	def horizontalGaussianBend(self, img, p0, pk,stdevmult):
		vw= [pk[0]-p0[0],pk[0]-p0[0]]
		stddev = max(abs(vw[0]),abs(vw[1]))*stdevmult
		il=4
		out = img.copy()
		if stddev<0.1: 
			return 0
		xmin, xmax = int(p0[0]-il*stddev) , int(pk[0]+il*stddev)
		ymin, ymax = int(p0[1]-il*stddev) , int(pk[1]+il*stddev)
		xmax, xmin = max(xmax,xmin), min(xmax,xmin)
		ymax, ymin = max(ymax,ymin), min(ymax,ymin)
		if xmin<0:xmin=0
		if xmax>=img.shape[1]-1:xmax= img.shape[1]-1
		if ymin<0:ymin=0
		if ymax>=img.shape[0]-1:ymax= img.shape[0]-1
	
		if xmin<0: xmin=0
		if ymin<0: ymin=0
		if xmax>img.shape[1]: xmax=img.shape[1]-1
		if ymax>img.shape[0]: ymax=img.shape[0]-1
	
		dymax = il*vw[1]
		il3 = 1/(1/(stddev*math.sqrt(2*math.pi)) *math.exp(0))
		for x in np.arange(xmin,xmax):
			#licze roznice x miedzy punktem do przesuniecia i punktem docelowym glownym
			dx0 = pk[0]-x
			dx02 = dx0**2
			for y in np.arange(ymin, ymax):
				#licze roznice wysokosci miedzy punktem do przesuniecia i punktem docelowym glownym
				dy0 = (pk[1]-y)
				dx = il3*vw[0]*(1/(stddev*math.sqrt(2*math.pi)) *math.exp((-(dy0**2+dx02)/2.0)/(2*stddev**2) ))
				pKon = (x+int(dx),y)
				if pKon[0]< img.shape[1]-1 and pKon[1]< img.shape[0]-1 and pKon[0]>0 and pKon[1]>0:
					#cv.Set2D(out,pKon[1],pKon[0],cv.Get2D(img,y,x))
					out[pKon[1],pKon[0]  ] = img[y,x]
					out[pKon[1],pKon[0]+1] = img[y,x]
					out[pKon[1],pKon[0]-1] = img[y,x]
					#cv.Set2D(out,pKon[1],pKon[0]+1,cv.Get2D(img,y,x))
					#cv.Set2D(out,pKon[1],pKon[0]-1,cv.Get2D(img,y,x))
		#cv.SaveImage(img_url,out)
		return out	
		

