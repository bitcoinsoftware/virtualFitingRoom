import cv2.cv as cv
class BodyBrinks:
	def __init__(self,inUrl,body_points):
		#pass
		self.f = cv.LoadImageM(inUrl)
		self.bp = body_points
		self.w , self.h = self.f.width, self.f.height

	def _find_brink(self,start_point, stop_point,obszar_sprawdzania,kierunek_przecinania,strona,strictness="permissive"):
		wektor = (stop_point[0]-start_point[0], stop_point[1]-start_point[1])
		if wektor[0]:
			a= wektor[1]/float(wektor[0])
		else: a = 2
		kreska =[]
		if abs(a)>1:
			if wektor[1]:
				a = wektor[0]/float(wektor[1])
			for i in range(min(wektor[1],0),max(wektor[1],0)):
				kreska.append((start_point[0]+int(a*i),start_point[1]+i))		
		else:
			for i in range(min(wektor[0],0),max(wektor[0],0)):
				kreska.append((start_point[0]+i,start_point[1]+int(a*i)))
		last_difference =0
		brink =[]
		amount,i = len(kreska),0
		for point in kreska:
			licznik=0
			if kierunek_przecinania:
				y0 =point[1]-obszar_sprawdzania/2+int(last_difference*i/float(amount))
				yk =point[1]+obszar_sprawdzania/2+int(last_difference*i/float(amount))
				if y0<0: y0=0
				if yk>self.f.height: yk=self.f.height
				diff_min = obszar_sprawdzania/2
				best_point = point
				for y in range(y0,yk):
					if cv.Get2D(self.f, y,point[0])[0]:
						diff = abs(y-(point[1]+last_difference))
						licznik+=1
						if diff< diff_min:
							best_point = (point[0],y)
				if strictness=="permissive":
					brink.append(best_point)
				elif strictness=="strict" and licznik>0:
					brink.append(best_point)
				last_difference = best_point[1]-point[1]	
			else:
				if strona=="L":
					x0 = point[0]-2*obszar_sprawdzania/3 +int(last_difference*i/float(amount))
					xk = point[0]+obszar_sprawdzania/3 +int(last_difference*i/float(amount))
				elif strona=="R":
					x0 = point[0]-obszar_sprawdzania/3 +int(last_difference*i/float(amount))
					xk = point[0]+2*obszar_sprawdzania/3 +int(last_difference*i/float(amount))
				else:
					x0 = point[0]-obszar_sprawdzania/2 +int(last_difference*i/float(amount))
					xk = point[0]+obszar_sprawdzania/2 +int(last_difference*i/float(amount))
				if x0<0: x0=0
				if xk>self.f.width: xk=self.f.width
				diff_min = obszar_sprawdzania/2
				best_point = point
				for x in range(x0,xk):
					if cv.Get2D(self.f, point[1],x)[0]:
						diff = abs(x-(point[0]+last_difference))
						licznik+=1
						if diff <diff_min:
							best_point = (x,point[1])
				if strictness=="permissive":
					brink.append(best_point)
				elif strictness=="strict" and licznik>0:
					brink.append(best_point)
				last_difference = best_point[0]-point[0]
			i+=1
		return brink
			
	def find_head_brink(self):
		neck_UL = self.bp['neck']['UL']
		neck_UR = self.bp['neck']['UR']
		ear_L , ear_R = self.bp['ear']['L'],self.bp['ear']['R']
		forhead_L,forhead_R = self.bp['forhead']['L'],self.bp['forhead']['R']
		ht = self.bp['head_top']
		obszar_sprawdzania = abs(neck_UL[0]-neck_UR[0])/2
		
		#left_brinks
		neck_ear_b_L = self._find_brink(neck_UL,ear_L,obszar_sprawdzania,0,"L")
		ear_forhead_b_L = self._find_brink(forhead_L,ear_L,obszar_sprawdzania,0,"L")
		forhead_top_b_L = self._find_brink(ht,forhead_L,obszar_sprawdzania,1,"L")
		
		#right brinks
		neck_ear_b_R = self._find_brink(neck_UR,ear_R,obszar_sprawdzania,0,"R")
		ear_forhead_b_R = self._find_brink(forhead_R,ear_R,obszar_sprawdzania,0,"R")
		forhead_top_b_R = self._find_brink(ht,forhead_R,obszar_sprawdzania,1,"R")
		"""
		for point in neck_ear_b_R:
			cv.Circle(self.f , point,5, (40,255, 128, 0), 4)
		for point in ear_forhead_b_R:
			cv.Circle(self.f , point,5, (128,255, 40, 0), 4)
		for point in forhead_top_b_R:
			cv.Circle(self.f , point,5, (128,40, 40, 0), 4)
		cv.SaveImage("glowa.jpg", self.f)
		"""
		return {"face":{"L":neck_ear_b_L,"R":neck_ear_b_R,},"forhead":{"L":ear_forhead_b_L ,"R":ear_forhead_b_R},
		"head_top":{"L":forhead_top_b_L,"R":forhead_top_b_R}}
		
	def find_neck_brink(self):
		start_point_L,start_point_R = self.bp['neck']['UL'] , self.bp['neck']['UR']
		stop_point_L , stop_point_R = self.bp['neck']['DL'], self.bp['neck']['DR']
		wektor_L = (stop_point_L[0]-start_point_L[0], stop_point_L[1]-start_point_L[1])
		wektor_R = (stop_point_R[0]-start_point_R[0], stop_point_R[1]-start_point_R[1])
		aL , aR = wektor_L[1]/float(wektor_L[0]) , wektor_R[1]/float(wektor_R[0])
		obszar_sprawdzania = abs(start_point_L[0]-self.bp['head_top'][0])
		
		kreska_L,kreska_R =[],[]
		for i in range(wektor_L[0],0,-1):
			kreska_L.append((start_point_L[0]+i,start_point_L[1]+int(aL*i)))
		for i in range(wektor_R[0],-1):
			kreska_R.append((start_point_R[0]+i,start_point_R[1]+int(aR*i)))
		return {"neck":{"R":kreska_R,"L":kreska_L,"UR":kreska_R,"UL":kreska_L,"DR":kreska_R,"DL":kreska_L}}
		
	def find_sholders_brink(self):
		start_point_L,start_point_R = self.bp['neck']['DL'] , self.bp['neck']['DR']
		stop_point_L , stop_point_R = self.bp['sholder']['L'], self.bp['sholder']['R']
		obszar_sprawdzania = abs(start_point_L[0]-self.bp['head_top'][0])
		
		sholder_R_brink = self._find_brink(start_point_R, stop_point_R, obszar_sprawdzania,1,"R")
		sholder_L_brink = self._find_brink(start_point_L, stop_point_L, obszar_sprawdzania,1,"L")
		return {"sholder":{"R":sholder_R_brink , "L":sholder_L_brink}}
			
	def find_groin_brink(self):
		groin_L = self.bp["groin"]['L']
		groin_R = self.bp["groin"]['R']
		obszar_sprawdzania = abs(groin_L[0]-groin_R[0])/2
		groin_brink = self._find_brink(groin_L, groin_R, obszar_sprawdzania,1,"N","strict")
		
		return {"groin":groin_brink}
		
	def find_legs_brink(self):
		feet_L = self.bp['feet']['L']
		feet_R = self.bp['feet']['R']
		groin = self.bp['groin']
		loin_L = self.bp['loin']['L']
		loin_R = self.bp['loin']['R']
		obszar_sprawdzania = abs(loin_L[0]-loin_R[0])/6
		
		brink_L_L = self._find_brink(loin_L, feet_L,obszar_sprawdzania,0,"L")
		brink_L_R = self._find_brink(groin["L"], feet_L,obszar_sprawdzania,0,"N")
		brink_R_R = self._find_brink(loin_R, feet_R,obszar_sprawdzania,0,"R")
		brink_R_L = self._find_brink(groin["R"], feet_R,obszar_sprawdzania,0,"N")
		return {"leg":{"L":{"outside":brink_L_L,"inside":brink_L_R},"R":{"outside":brink_R_R,"inside":brink_R_L}}}
		
	def find_loin_brink(self):
		waist_L=self.bp['waist']['L']
		waist_R=self.bp['waist']['R']
		loin_R=self.bp['loin']['R']
		loin_L=self.bp['loin']['L']
		obszar_sprawdzania= (loin_L[0]-loin_R[0])/6
		brink_L = self._find_brink(waist_L, loin_L,obszar_sprawdzania,0,"L")
		brink_R = self._find_brink(waist_R, loin_R,obszar_sprawdzania,0,"R")
		"""
		for point in brink_L:
			cv.Circle(self.f , point,5, (0,0,255, 0), 4)
		for point in brink_R:
			cv.Circle(self.f , point,5, (128,128,128, 0), 4)
		cv.SaveImage("biodra.jpg", self.f)
		"""
		return {"loin":{"L":brink_L,"R":brink_R}}
		
	def find_hands_brink(self):
		hand_L = self.bp['hand']['L']
		hand_R = self.bp['hand']['R']
		sholder_L=self.bp['sholder']['L']
		sholder_R=self.bp['sholder']['R']
		armpit_L=self.bp['armpit']['L']
		armpit_R=self.bp['armpit']['R']
		neck_UL = self.bp['neck']['UL']
		neck_UR = self.bp['neck']['UR']
		obszar_sprawdzania = abs(neck_UL[0]-neck_UR[0])/2
	
		brink_L_L = self._find_brink(sholder_L, hand_L,obszar_sprawdzania,0,"L")
		brink_L_R = self._find_brink(armpit_L, hand_L,obszar_sprawdzania,0,"N")
		brink_R_R = self._find_brink(sholder_R, hand_R,obszar_sprawdzania,0,"R")
		brink_R_L = self._find_brink(armpit_R, hand_R,obszar_sprawdzania,0,"N")
		
		return {"arm":{"L":{"outside":brink_L_L,"inside":brink_L_R},"R":{"outside":brink_R_R,"inside":brink_R_L}}}
	
	"""
	{'feet': {'R': (375, 1092), 'L': (227, 1096)}, 'loin': {'R': (459, 504), 'L': (252, 504)}, 'waist': {'R': (436, 434), 'L': (274, 434)},
	'sholder': {'R': (493, 256), 'L': (229, 237)}, 'armpit': {'R': (436, 311), 'L': (284, 284)}, 'ears': {'R': (428, 78), 'L': (310, 99)}, 
	'head_top': (363, 23), 'neck': {'UL': (337, 158), 'DL': (327, 183), 'DR': (414, 183), 'UR': (403, 158)}, 'groin': (341, 572), 
	'hand': {'R': (513, 593), 'L': (210, 573)}}
	"""
	def find_corpse_brink(self):
		armpit_L=self.bp['armpit']['L']
		armpit_R=self.bp['armpit']['R']
		waist_L =self.bp['waist']['L']
		waist_R =self.bp['waist']['R']
		obszar_sprawdzania = abs(armpit_L[0]-armpit_R[0])/6
		brink_L = self._find_brink(armpit_L, waist_L,obszar_sprawdzania,0,"R")
		brink_R = self._find_brink(armpit_R, waist_R,obszar_sprawdzania,0,"L")

		return {"corpse":{"L":brink_L,"R":brink_R}}
	
	
