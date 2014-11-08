import cv2.cv as cv
import itertools
from BodyBrinks import *
from FunkcjePomocnicze import *
#from Biustonosz import *

class Body(FunkcjePomocnicze):
	
	def __init__(self,f_center_f_rect, out_borders_url ):
		face_center,face_rect = f_center_f_rect[0],f_center_f_rect[1]
		center =self.count_matrix_center(out_borders_url)
		
		ht= self.find_head_top(face_center,face_rect,out_borders_url)
		n = self.find_neck(face_center, face_rect,out_borders_url) # OK
		e = self.find_ears(face_rect, n["neck"],ht["head_top"],out_borders_url)
		fh =self.find_forhead(face_rect, ht['head_top'], e,out_borders_url)
		g = self.find_groin(face_center,face_rect,n["neck"], out_borders_url) #OK
		f=self.find_feet(g["groin"], out_borders_url)  #OK
		aswl = self.find_armpit_hands_sholders_waist_and_loin(face_center,g["groin"], out_borders_url)
				
		self.body = {"head_top":ht["head_top"],"groin":g['groin'], "armpit":aswl['armpit'],
		'hand':aswl['hand'],"sholder":aswl['sholder'],"waist":aswl['waist'],"neck":n["neck"],
		"feet":f["feet"],"loin":aswl['loin'],'ear':e,'forhead':fh}
				
		bb = BodyBrinks(out_borders_url,self.body)
		sholder_brink = bb.find_sholders_brink()
		neck_brink = bb.find_neck_brink()
		head_brink = bb.find_head_brink()
		hands_brink = bb.find_hands_brink()
		legs_brink = bb.find_legs_brink()
		corpse_brink = bb.find_corpse_brink()
		groin_brink = bb.find_groin_brink()
		loin_brink = bb.find_loin_brink()
		
		self.brinks ={}
		self.brinks.update(sholder_brink)
		self.brinks.update(neck_brink)
		self.brinks.update(head_brink)
		self.brinks.update(hands_brink)
		self.brinks.update(legs_brink)
		self.brinks.update(corpse_brink)
		self.brinks.update(groin_brink)
		self.brinks.update(loin_brink)
		
		#knees_ankles_crossbones = self.find_knee_ankle_crossbones(legs_brink['legs_brink'])
		knees_ankles_crossbones = self.find_knee_ankle_crossbones(legs_brink['leg'])
		#elbows_wrists=self.find_elbow_wrist(hands_brink['arm_brink'])
		elbows_wrists=self.find_elbow_wrist(hands_brink['arm'])
		#wings = self.find_wings(sholder_brink['sholder_brink'])
		wings = self.find_wings(sholder_brink['sholder'])
		
		self.body['knee']  = knees_ankles_crossbones['knee']
		self.body['ankle']  = knees_ankles_crossbones['ankle']
		self.body['crossbone']  = knees_ankles_crossbones['crossbone']
		self.body['elbow'] = elbows_wrists['elbow']
		self.body['wrist'] = elbows_wrists['wrist']
		self.body['wing'] = wings['wing']
		self.count_angles_vectors_lengths()
		
	def count_angles_vectors_lengths(self):
		#wysokosc talii ,bioder, korpusu, szyi
		sza = self.body['neck']
		tal = self.body['loin']
		pas = self.body['waist']
		grn = self.body['groin']
		neck_height = sza['DL'][1]-sza['UL'][1]+sza['DR'][1]-sza['UL'][1]
		loin_height= (grn['L'][1]+grn['R'][1]- tal['L'][1]-tal['R'][1])/2.0
		waist_height = (tal['L'][1]+tal['R'][1] - pas['L'][1]-pas['R'][1])/2.0
		neck_height =(self.body['neck']['DL'][1] -self.body['neck']['UL'][1])
		legs_height = (self.body['feet']['L'][1] + self.body['feet']['R'][1])/2.0 -(self.body['groin']['L'][1] + self.body['groin']['R'][1])/2.0
		corpse_height =(pas['L'][1]-sza['DL'][1]+pas['R'][1]-sza['DR'][1])/2.0

		#szerokosci
		neck_width = (sza['DL'][0]-sza['DR'][0]+sza['UL'][0]-sza['UR'][0])/2.0
		waist_width = pas['L'][0] -pas['R'][0]
		print "szerokosc pasa" , waist_width
		loin_width  = tal['L'][0] -tal['R'][0]
		groin_width = grn['L'][0] -grn['R'][0]

		#sholder alfa
		sholder_width = self.count_diagonal_length(self.body['sholder']['L'],self.body['sholder']['R'])
		ACx = self.body["sholder"]["L"][0]-self.body["sholder"]["R"][0]
		BCy = self.body["sholder"]["L"][1]-self.body["sholder"]["R"][1]
		sholder_alfa = self.count_rotation_sin_and_cos(sholder_width, ACx , BCy)
	
		#armpit alfa
		armpit_width = self.count_diagonal_length(self.body['armpit']['L'],self.body['armpit']['R'])
		ACx = self.body["armpit"]["L"][0]-self.body["armpit"]["R"][0]
		BCy = self.body["armpit"]["L"][1]-self.body["armpit"]["R"][1]
		armpit_alfa = self.count_rotation_sin_and_cos(armpit_width , ACx, BCy)
		
		#loin alfa
		loin_width = self.count_diagonal_length(tal['R'],tal['L'])
		ACx = tal['L'][0]-tal['R'][0]
		BCy = tal['L'][1]-tal['R'][1]
		loin_alfa = self.count_rotation_sin_and_cos(loin_width,ACx,BCy)
		print "KAT BIODER", loin_alfa
		
		#Left hand alfa
		base = self.sredni_punkt(self.body['armpit']['L'] , self.body['sholder']['L'])
		#base = self.body['sholder']['L']
		wrist = self.sredni_punkt(self.body["wrist"]["L"]["inside"], self.body["wrist"]["L"]["outside"])
		#hand_l_length = self.count_diagonal_length(self.body['wrist']['L']["inside"],self.body['armpit']['L'])
		hand_l_length = self.count_diagonal_length(wrist,base)
		ACx = wrist[0]-base[0]
		#BCy = self.body["wrist"]["L"]["inside"][1]-self.body["armpit"]["L"][1]
		BCy = wrist[1]-base[1]
		left_hand_alfa = self.count_rotation_sin_and_cos(hand_l_length, BCy , ACx)
		#hand_start = self.sredni_punkt(self.body['armpit']['L'],self.body['sholder']['L'])
		#left_hand_vector = self.count_vector(hand_start,self.body['wrist']['L']['inside'])
		left_hand_vector = self.count_vector(base,wrist)
		print 'Kat lewej reki', math.degrees(left_hand_alfa[0]), ACx , BCy
	
		#right hand alfa
		base = self.sredni_punkt(self.body['armpit']['R'] , self.body['sholder']['R'])
		#base = self.body['sholder']['R']
		wrist = self.sredni_punkt(self.body["wrist"]["R"]["inside"], self.body["wrist"]["R"]["outside"])
		#hand_r_length = self.count_diagonal_length(self.body['wrist']['R']['inside'],self.body['armpit']['R'])
		hand_r_length = self.count_diagonal_length(wrist,base)
		#ACx = self.body["wrist"]["R"]["inside"][0]-self.body["armpit"]["R"][0]
		ACx = wrist[0]-base[0]
		#BCy = self.body["wrist"]["R"]["inside"][1]-self.body["armpit"]["R"][1]
		BCy = wrist[1]-base[1]
		right_hand_alfa = self.count_rotation_sin_and_cos(hand_r_length, BCy , ACx)
		#hand_start = self.sredni_punkt(self.body['armpit']['R'],self.body['sholder']['R'])
		#right_hand_vector = self.count_vector(hand_start,self.body['wrist']['R']['inside'])
		right_hand_vector = self.count_vector(base,wrist)
		
		#print 'Kat prawej reki', math.degrees(right_hand_alfa[0]) , ACx , BCy
		
		#right leg alfa
		dlugosc_prawej_nogi = self.count_diagonal_length(self.body['feet']['R'],self.body['groin']['R'])
		ACx = self.body["feet"]["R"][0]-self.body["groin"]["R"][0]
		BCy = self.body["feet"]["R"][1]-self.body["groin"]["R"][1]
		right_leg_alfa = self.count_rotation_sin_and_cos(dlugosc_prawej_nogi, BCy , ACx)
		right_leg_vector = self.count_vector(self.body['groin']['R'],self.body['feet']['R'])
		
		#left leg alfa
		dlugosc_lewej_nogi = self.count_diagonal_length(self.body['feet']['L'],self.body['groin']['L'])
		ACx = self.body["feet"]["L"][0]-self.body["groin"]["L"][0]
		BCy = self.body["feet"]["L"][1]-self.body["groin"]["L"][1]
		left_leg_alfa = self.count_rotation_sin_and_cos(dlugosc_lewej_nogi, BCy , ACx)
		left_leg_vector = self.count_vector(self.body['groin']['L'],self.body['feet']['L'])
		
		#przypisanie
		self.angles={'sholder':sholder_alfa , 'armpit':armpit_alfa,'loin':loin_alfa,'left_hand':left_hand_alfa,
		'right_hand':right_hand_alfa,'left_leg':left_leg_alfa,'right_leg':right_leg_alfa}
		
		self.vectors={'left_hand':left_hand_vector,'right_hand':right_hand_vector,'left_leg':left_leg_vector,
		'right_leg':right_leg_vector}
		
		self.lenghts={'neck':neck_height,'loin':loin_height,'waist':waist_height,'legs':legs_height,
		'hand_L':hand_l_length,'hand_R':hand_r_length,'corpse':corpse_height}
		
		self.widths ={'neck':neck_width,'sholder':sholder_width,'armpit':armpit_width,
		'waist':waist_width,'loin':loin_width,'groin':groin_width}
		
	def count_vector(self,p0, pK):
		vector = [pK[0]-p0[0],pK[1]-p0[1]]
		return vector
		
	def find_eye_position(self, image,  roi):
		nested1 = cv.Load("haarcascades/haarcascade_eye.xml")
		nested3 = cv.Load("haarcascades/haarcascade_mcs_lefteye.xml")
		nested3_2 = cv.Load("haarcascades/haarcascade_righteye_2splits.xml")
		nested4 = cv.Load("haarcascades/haarcascade_mcs_righteye.xml")
        
		gray = cv.CreateImage((image.width,image.height), 8, 1)
		# convert color input image to grayscale
		cv.CvtColor(image, gray, cv.CV_BGR2GRAY)
		cv.EqualizeHist(gray, gray)
		y1, y2 , x1, x2 =  roi[1], roi[1]+roi[3], roi[0], roi[0]+roi[2]
		imroi = gray[y1:y2, x1:x2]
		vis_roi = image[y1:y2, x1:x2]
		min_eye_size = (10,10)
		subrects1 = self.detect(imroi, nested1,1.2,min_eye_size) #eye
		subrects3 = self.detect(imroi, nested3,1.2,min_eye_size) #lefteye
		subrects4 = self.detect(imroi, nested4,1.2,min_eye_size) #mcs righteye
		subrects3_2=self.detect(imroi, nested3_2,1.2,min_eye_size) #righteye
        
		centers ,right_eye_centers,left_eye_centers=[],[],[]
		face_center =((x2+x1)/2 , (y2+y1)/2 )
		#print "FACE CENTER", face_center
		subrects=[]
		srcts = [subrects1,subrects3,subrects3_2,subrects4]
		i=0
		for sr in srcts:
			for s in sr:
				subrects.append(s)	
		for subrect in subrects:
			centers.append(self.count_middle(subrect))
		for center in centers:
			if center[1]+y1<face_center[1]:
				if center[0]+x1<face_center[0]:
					right_eye_centers.append(center)
				else:
					left_eye_centers.append(center)
		x_sum, y_sum ,i=0,0,0
		#print "right eye centers" ,right_eye_centers , "left eye centers", left_eye_centers
		for center in right_eye_centers:
			i+=1
			color = (0,0,255)
			x_sum, y_sum = x_sum+center[0] , y_sum+center[1]
		if i>0:
			rcenter= (x1+x_sum/i ,y1+y_sum/i)
		x_sum, y_sum,i =0,0,0
		for center in left_eye_centers:
			i+=1
			color = (255,0,0)
			x_sum, y_sum = x_sum+center[0] , y_sum+center[1]
		if i>0:
			lcenter = (x1+x_sum/i ,y1+y_sum/i)
		if len(left_eye_centers) and len(right_eye_centers):
			return  [lcenter,  rcenter],face_center
		return []
    
	def find_neck_position(self,face_rect, eyes_pos):
		left_eye_x , right_eye_x = eyes_pos[0][0],eyes_pos[1][0]
		lower_border_y = face_rect[1]+face_rect[3]
		res =[(left_eye_x,lower_border_y  )  ,(right_eye_x, lower_border_y)]
		return res

	def find_face(self,path):
		img = cv.LoadImage(path)
		cascade0 = cv.Load("haarcascades/haarcascade_frontalface_default.xml")
		cascade1 = cv.Load("haarcascades/haarcascade_frontalface_alt.xml")
		cascade2 = cv.Load("haarcascades/haarcascade_frontalface_alt2.xml")
		cascades=[cascade0,  cascade1, cascade2]
		min_size = (38, 38)
		image_scale = 1.2
		haar_scale = 1.4
		min_neighbors = 4
		haar_flags = 0
		# allocate temporary images
		gray = cv.CreateImage((img.width,img.height), 8, 1)
		small_img_height = cv.Round (img.height / image_scale)
		small_img_width = cv.Round (img.width / image_scale)
		small_img = cv.CreateImage((cv.Round(img.width / image_scale),small_img_height), 8, 1)
		# convert color input image to grayscale
		cv.CvtColor(img, gray, cv.CV_BGR2GRAY)
		# scale input image for faster processing
		cv.Resize(gray, small_img, cv.CV_INTER_LINEAR)
		cv.EqualizeHist(small_img, small_img)
       
		faces = cv.HaarDetectObjects(small_img, cascades[0], cv.CreateMemStorage(0),haar_scale, min_neighbors, haar_flags, min_size)
		if len(faces)==0: faces = cv.HaarDetectObjects(small_img, cascades[1], cv.CreateMemStorage(0),haar_scale, min_neighbors, haar_flags, min_size)
		if len(faces)==0: faces = cv.HaarDetectObjects(small_img, cascades[2], cv.CreateMemStorage(0),haar_scale, min_neighbors, haar_flags, min_size)
		min_face_cert=0
		face_centers = []
		if faces:
			#print "TWARZE" ,faces
			for ((x, y, w, h), n) in faces:
				if n>min_face_cert:
					x2 , y2, w2 , h2 = self.make_the_rectangle_bigger(x, y, w, h, 1.7,1.5,  small_img_height,small_img_width, image_scale)
					#eye_position, face_center = self.find_eye_position(img ,(x2, y2, w2, h2))
					face_center = [x2+w2/2 , y2+h2/2]
					#print eye_position[0]
					return face_center, (x2, y2, w2, h2)
					
	def find_skin_RGB_color_range(self, img_path, face_rect, face_center,variation):
		frame = cv.LoadImageM(img_path)
		w, h = face_rect[2]/6 , face_rect[3]/6
		x0,y0 = face_center[0]- w , face_center[1]-h
		w2,h2 = 2*w , 2*h
		roi = frame[y0+h2:y0+2*h2 , x0:x0+w2]
		avg = cv.AvgSdv(roi)[0]
		min = (int(avg[0]*(1-variation)),int(avg[1]*(1-variation)),int(avg[2]*(1-variation)),int(avg[3]*(1-variation)))
		max = (int(avg[0]*(1+variation)),int(avg[1]*(1+variation)),int(avg[2]*(1+variation)),int(avg[3]*(1+variation)))
		avg_range = [min, max]
		return avg_range
	
	def find_feet(self,groin, border_img_path):
		frame = cv.LoadImageM(border_img_path)
		xk,yk = frame.width-1, frame.height-1
		fL,fR = (0,0),(0,0)
		fLsList, fRsList= [],[]
		flag_break=[0,0]
		fslist_len=5
		groinL=(groin["L"][0],groin["L"][1])
		groinR=(groin["R"][0],groin["R"][1])
		for y in range(yk, groinL[1],-1):
			fLs, fRs = [],[]
			#appenduje 
			for x in range(1,xk):
				if cv.Get2D(frame, y,x)[0]>0 and cv.Get2D(frame, y,x-1)[0]<1 and x<groinR[0]:
					fRs.append((x,y))
				if cv.Get2D(frame, y,x)[0]>0 and cv.Get2D(frame, y,x-1)[0]<1 and x>=groinL[0]:
					fLs.append((x,y))
		
			if len(fRs)==2 and len(fRsList)<fslist_len:
				fR=((fRs[0][0]+fRs[1][0])/2, fRs[0][1])
				fRsList.append(fR)
			if len(fRs)==1 and len(fRsList)<fslist_len:
				fR=(fRs[0][0], fRs[0][1])
				fRsList.append(fR)
				if len(fRsList)==fslist_len:
					flag_break[0]=1
			if len(fLs)==2 and len(fLsList)<fslist_len:
				fL=((fLs[0][0]+fLs[1][0])/2, fLs[0][1])
				fLsList.append(fL)
			if len(fLs)==1 and len(fLsList)<fslist_len:
				fL=(fLs[0][0], fLs[0][1])
				fLsList.append(fL)
				if len(fLsList)==fslist_len:
					flag_break[1]=1
			if flag_break[0] and flag_break[1]: break
	
		if len(fRsList)==fslist_len  and len(fLsList)==fslist_len:
			sXL,sYL,sXR,sYR =0,0,0,0
			for i in range(fslist_len):
				sXL , sYL = sXL+fLsList[i][0] , sYL+fLsList[i][1]
				sXR , sYR = sXR+fRsList[i][0] , sYR+fRsList[i][1]
			fL = (sXL/fslist_len,sYL/fslist_len)
			fR = (sXR/fslist_len,sYR/fslist_len)
		else:
			fL,fR = (0,0),(0,0)

		return {"feet":{"L":fL,"R":fR}}
				
	def find_armpit_hands_sholders_waist_and_loin(self,face_center, krocze, img_path):
		frame = cv.LoadImageM(img_path)
		y_max = frame.height-1
		x_k2 = frame.width -1
		x_k1 = face_center[0]
		y0, yk = face_center[1], krocze["R"][1] + (y_max-krocze["R"][1])/6
		wylapane_potrojneR=[]
		wylapane_R_dlonie=[]
		wylapane_potrojneL=[]
		wylapane_L_dlonie=[]
		margin=10
		catched_am=10
		
		#sprawdzam prawa polowe
		for y in range(y0, yk):
			gr=[]
			for x in range(0, x_k1-1-margin):
				#sprawdz ilosc granic
				if cv.Get2D(frame, y,x)[0] and cv.Get2D(frame, y,x+1)[0]<1:
					gr.append((x,y))
			if len(gr)==3 and len(wylapane_potrojneR)<catched_am: #przestaje zgarniac gdy jest 10
				wylapane_potrojneR.append(gr)
			if len(gr)==3 or len(gr)==4:
				wylapane_R_dlonie.append(gr)
			#if len(wylapane_potrojneL)==catched_am:
				#break
				
		#sprawdzam lewa polowe
		for y in range(y0, yk):
			gr=[]
			for x in range(x_k1+margin, x_k2-1):
				#sprawdz ilosc granic
				if cv.Get2D(frame, y,x)[0] and cv.Get2D(frame, y,x+1)[0]<1:
					gr.append((x,y))
			if len(gr)==3 and len(wylapane_potrojneL)<catched_am:
				wylapane_potrojneL.append(gr)
			if len(gr)==3 or len(gr)==4:
				wylapane_L_dlonie.append(gr)
			#if len(wylapane_potrojneR)==catched_am:
				#break
			
		#PACHY
		xsum, ysum = 0,0
		for pt in wylapane_potrojneR:
			xsum, ysum = xsum+pt[2][0] , ysum+pt[2][1]   # bo z wylapanych potrojnych dlatego index 2
		xsrR, ysrR = xsum/catched_am , ysum/catched_am
		xsum, ysum = 0,0
		for pt in wylapane_potrojneL:
			xsum, ysum = xsum+pt[0][0] , ysum+pt[0][1]   # bo z wylapanych potrojnych dlatego index 2
		xsrL, ysrL = xsum/catched_am , ysum/catched_am
		#DLONIE
		wylapane_R_dlonie = wylapane_R_dlonie[len(wylapane_R_dlonie)-catched_am:]
		wylapane_L_dlonie = wylapane_L_dlonie[len(wylapane_L_dlonie)-catched_am:]

		xsum, ysum = 0,0
		for pt in wylapane_R_dlonie:
			xsum, ysum = xsum+pt[0][0] , ysum+pt[0][1]   # bo z wylapanych potrojnych dlatego index 
		xsrRdlon, ysrRdlon = xsum/catched_am , ysum/catched_am
		xsum, ysum = 0,0
		for pt in wylapane_L_dlonie:
			xsum, ysum = xsum+pt[2][0] , ysum+pt[2][1]   # bo z wylapanych potrojnych dlatego index 
		xsrLdlon, ysrLdlon = xsum/catched_am , ysum/catched_am
		###
		waistR, waistL = self.find_waist(frame, (ysrR, ysrL), krocze)
		loinR , loinL = self.find_loin(frame, (ysrR, ysrL) , krocze)
		armR, armL = self.find_sholders(frame, [(xsrR,ysrR), (xsrL, ysrL)], face_center[1])
		return {"armpit":{"R":(xsrR, ysrR),'L':(xsrL,ysrL)},"hand":{"R": (xsrRdlon, ysrRdlon),"L":(xsrLdlon, ysrLdlon)},
		"sholder":{"R":armR,"L":armL}, "waist":{"R":waistR,"L":waistL},"loin":{"L":loinL,"R":loinR}}
		
	def find_elbow_wrist(self, hand_brinks):
		hb_lo , hb_li = hand_brinks["L"]['outside'],hand_brinks['L']['inside']
		hb_ro , hb_ri = hand_brinks['R']['outside'],hand_brinks['R']['inside']
		
		hb_loPT = ((2*hb_lo[0][0]+hb_lo[-1][0])/3,(2*hb_lo[0][1]+hb_lo[-1][1])/3)
		hb_liPT = ((2*hb_li[0][0]+hb_li[-1][0])/3,(2*hb_li[0][1]+hb_li[-1][1])/3)
		hb_roPT = ((2*hb_ro[0][0]+hb_ro[-1][0])/3,(2*hb_ro[0][1]+hb_ro[-1][1])/3)
		hb_riPT = ((2*hb_ri[0][0]+hb_ri[-1][0])/3,(2*hb_ri[0][1]+hb_ri[-1][1])/3)
		
		EL_lo =self.find_best_brink_point(hb_loPT,hb_lo,'y')
		EL_li =self.find_best_brink_point(hb_liPT,hb_li,'y')
		EL_ro =self.find_best_brink_point(hb_roPT,hb_ro,'y')
		EL_ri =self.find_best_brink_point(hb_riPT,hb_ri,'y')
		
		hb_loPT = ((hb_lo[0][0]+5*hb_lo[-1][0])/6,(hb_lo[0][1]+5*hb_lo[-1][1])/6)
		hb_liPT = ((hb_li[0][0]+5*hb_li[-1][0])/6,(hb_li[0][1]+5*hb_li[-1][1])/6)
		hb_roPT = ((hb_ro[0][0]+5*hb_ro[-1][0])/6,(hb_ro[0][1]+5*hb_ro[-1][1])/6)
		hb_riPT = ((hb_ri[0][0]+5*hb_ri[-1][0])/6,(hb_ri[0][1]+5*hb_ri[-1][1])/6)
		
		WR_lo =self.find_best_brink_point(hb_loPT,hb_lo,'y')
		WR_li =self.find_best_brink_point(hb_liPT,hb_li,'y')
		WR_ro =self.find_best_brink_point(hb_roPT,hb_ro,'y')
		WR_ri =self.find_best_brink_point(hb_riPT,hb_ri,'y')
		
		return {'elbow':{'L':{'inside':EL_li,'outside':EL_lo},'R':{'inside':EL_ri,'outside':EL_ro}},
				'wrist':{'L':{'inside':WR_li,'outside':WR_lo},'R':{'inside':WR_ri,'outside':WR_ro}}}
	
	def find_knee_ankle_crossbones(self, legs_brinks):
		hb_lo , hb_li = legs_brinks["L"]['outside'],legs_brinks['L']['inside']
		hb_ro , hb_ri = legs_brinks['R']['outside'],legs_brinks['R']['inside']
		
		hb_loPT = ((hb_lo[0][0]+hb_lo[-1][0])/2,(hb_lo[0][1]+hb_lo[-1][1])/2)
		hb_liPT = ((hb_li[0][0]+hb_li[-1][0])/2,(hb_li[0][1]+hb_li[-1][1])/2)
		hb_roPT = ((hb_ro[0][0]+hb_ro[-1][0])/2,(hb_ro[0][1]+hb_ro[-1][1])/2)
		hb_riPT = ((hb_ri[0][0]+hb_ri[-1][0])/2,(hb_ri[0][1]+hb_ri[-1][1])/2)
		
		KN_lo =self.find_best_brink_point(hb_loPT,hb_lo,'y')
		KN_li =self.find_best_brink_point(hb_liPT,hb_li,'y')
		KN_ro =self.find_best_brink_point(hb_roPT,hb_ro,'y')
		KN_ri =self.find_best_brink_point(hb_riPT,hb_ri,'y')
		
		hb_loPT = ((hb_lo[0][0]+7*hb_lo[-1][0])/8,(hb_lo[0][1]+7*hb_lo[-1][1])/8)
		hb_liPT = ((hb_li[0][0]+7*hb_li[-1][0])/8,(hb_li[0][1]+7*hb_li[-1][1])/8)
		hb_roPT = ((hb_ro[0][0]+7*hb_ro[-1][0])/8,(hb_ro[0][1]+7*hb_ro[-1][1])/8)
		hb_riPT = ((hb_ri[0][0]+7*hb_ri[-1][0])/8,(hb_ri[0][1]+7*hb_ri[-1][1])/8)
		
		AN_lo =self.find_best_brink_point(hb_loPT,hb_lo,'y')
		AN_li =self.find_best_brink_point(hb_liPT,hb_li,'y')
		AN_ro =self.find_best_brink_point(hb_roPT,hb_ro,'y')
		AN_ri =self.find_best_brink_point(hb_riPT,hb_ri,'y')
		
		hb_loPT = ((hb_lo[0][0]+13*hb_lo[-1][0])/16,(hb_lo[0][1]+13*hb_lo[-1][1])/16)
		hb_liPT = ((hb_li[0][0]+13*hb_li[-1][0])/16,(hb_li[0][1]+13*hb_li[-1][1])/16)
		hb_roPT = ((hb_ro[0][0]+13*hb_ro[-1][0])/16,(hb_ro[0][1]+13*hb_ro[-1][1])/16)
		hb_riPT = ((hb_ri[0][0]+13*hb_ri[-1][0])/16,(hb_ri[0][1]+13*hb_ri[-1][1])/16)
		
		CR_lo =self.find_best_brink_point(hb_loPT,hb_lo,'y')
		CR_li =self.find_best_brink_point(hb_liPT,hb_li,'y')
		CR_ro =self.find_best_brink_point(hb_roPT,hb_ro,'y')
		CR_ri =self.find_best_brink_point(hb_riPT,hb_ri,'y')
		
		return {'knee':{'L':{'inside':KN_li,'outside':KN_lo},'R':{'inside':KN_ri,'outside':KN_ro}},
				'ankle':{'L':{'inside':AN_li,'outside':AN_lo},'R':{'inside':AN_ri,'outside':AN_ro}},
				'crossbone':{'L':{'inside':CR_li,'outside':CR_lo},'R':{'inside':CR_ri,'outside':CR_ro} }}
		
	def find_wings(self, sholder_brinks):
		hb_l , hb_r = sholder_brinks["L"],sholder_brinks['R']
		hb_lm = ((hb_l[0][0]+hb_l[-1][0])/2,(hb_l[0][1]+hb_l[-1][1])/2)
		hb_rm = ((hb_r[0][0]+hb_r[-1][0])/2,(hb_r[0][1]+hb_r[-1][1])/2)
		SL_r =self.find_best_brink_point(hb_rm,hb_r,'x')
		SL_l =self.find_best_brink_point(hb_lm,hb_l,'x')
		
		return {'wing':{'L':SL_l,'R':SL_r}}
		
	def find_loin(self, frame, y_armpits, krocze):
		[ysrL, ysrR] = y_armpits
		krX = (krocze["L"][0] + krocze["R"][0])/2
		#loinY = int((krocze[1]+((ysrR+ysrL)/2.0))/2.0) # int((krocze[1]- (ysrR+ysrL)/2.0)/5.0) + krocze[1]
		loinY =krocze["L"][1] - int((krocze["L"][1]- (ysrR+ysrL)/1.5)/4.0) 
		for x in range(krX, frame.width-1):
			if cv.Get2D(frame, loinY,x)[0] and cv.Get2D(frame, loinY,x+1)[0]<1:
				loinR =(x,loinY)
				break
		for x in range(krX, 1,-1):
			if cv.Get2D(frame, loinY,x)[0] and cv.Get2D(frame, loinY,x-1)[0]<1:
				loinL =(x,loinY)
				break
		if loinL and loinR:
			return loinL, loinR
		else:
			return None, None
	
	def find_groin(self,face_center,face_rect,neck,img_path):
		frame = cv.LoadImageM(img_path)
		face_center_x=face_center[0]
		y_max = frame.height-1
		x_max = frame.width
		pt0 = (face_center_x-x_max/16, y_max)
		x_k = face_center_x+x_max/16
		y_list,point_list=[],[]
		if x_k>=frame.width:
			x_k= frame.width -1
		# ide od dolu w gore i zapisuje wszystkie biale pkty
		for x in range(pt0[0],x_k):
			for y in range(y_max, 0,-2):
				#print cv.Get2D(frame,y,x)
				if cv.Get2D(frame,y,x)[0]>0:
					break
			y_list.append(y)
			point_list.append((x,y))
		suma =sum(y_list)
		srednia = int(suma/float(len(y_list)))
	
		y_list.sort()
		y_list = y_list
		i=0
		big_y_list=[]
		#biore tylko 3 pkt
		for y in y_list:
			if y> srednia/3:
				big_y_list.append(y)
				i+=1
			if i==3:
				break
		
		proper_x_list=[]
		for point in point_list:
			if point[1] in big_y_list:
				proper_x_list.append(point[0])
		suma_x=sum(proper_x_list)
		srednia_x = int(suma_x/float(len(proper_x_list)))
		suma_y = sum(big_y_list)
		srednia_y=int(suma_y/float(len(big_y_list)))
		rozsuniecie = face_rect[2]/8
		krocze_R = (srednia_x-rozsuniecie,srednia_y)
		krocze_L = (srednia_x+rozsuniecie,srednia_y)
		return {"groin":{"L":krocze_L,"R":krocze_R}}		
	
	def find_neck(self,face_center, face_rect,border_img_path):
		frame = cv.LoadImageM(border_img_path)
		ymin=0
		x0,y0,xk,yk = face_rect[0],face_center[1],face_center[0]+face_rect[2]/2, face_center[1]+face_rect[3]/2
		d = face_rect[2]
		ds=[]
		for y in range(y0, yk):
			dL, dR = face_rect[2]/2,face_rect[2]/2
			for x in range(x0, xk):
				if x< face_center[0]:  # dla lewej polowki
					if cv.Get2D(frame, y,x)[0]>0 :
						dL = face_center[0]- x
						
				if x>face_center[0]: #dla prawej polowki
					if cv.Get2D(frame, y,x)[0]>0 :
						dR = x- face_center[0]
			d2 =dL+dR
			ds.append(d2)
			if d > d2:
				d= d2
				y_min=y
		d_av = sum(ds)/(yk-y0)
		i=y_min-y0
		y_max=y_min
		for y in range(y_min,yk):
			if ds[i]<=d_av:
				cv.Circle(frame , (face_center[0],y),5, (0,255, 0, 0), 4)
				y_max = y
			i+=1
		x_y_max , x_y_min =[],[]
		for x in range(x0,xk-1):
			if cv.Get2D(frame, y_min,x)[0]>0 and cv.Get2D(frame, y_min,x+1)[0]<1:
				#cv.Circle(frame , (x,y_min),5, (0,0, 255, 0), 4)
				x_y_min.append(x)
			if cv.Get2D(frame, y_max,x)[0]>0 and cv.Get2D(frame, y_max,x+1)[0]<1:
				#cv.Circle(frame , (x,y_max),5, (0,0, 255, 0), 4)
				x_y_max.append(x)
		p0u, pku = (x_y_min[0],y_min), (x_y_min[1],y_min)
		p0d, pkd = (x_y_max[0],y_max), (x_y_max[1],y_max)
	
		return {"neck":{"UR":p0u, "UL":pku, "DR":p0d,"DL":pkd}}
			
	#szukam najnizszego miejsca w ktorym znajduje sie 6 lub 8 krawedzi
	def find_hands(self,groin, feet,armpits, border_img_path):
		frame = cv.LoadImageM(border_img_path)
		x0,y0 = 0, armpits["L"][1]
		xk,yk =frame.width, (feet["R"][1]+groin[1])/2
		xL, xR = None, None
		y_max = None
		for y in range(y0,yk):
			i=0
			xses=[]
			for x in range(x0,xk):
				if cv.Get2D(frame, y,x)[0]>0 and cv.Get2D(frame, y,x+1)[0]<1:
					i+=1
					xses.append(x)
			if i in [6,8]:
				y_max = y
				xL, xR = xses[0], xses[len(xses)-1]
		cv.Circle(frame , (xL,y_max),5, (255,0, 0, 0), 4)
		cv.Circle(frame , (xR,y_max),5, (255,0, 0, 0), 4)
		#cv.SaveImage("TEST4.jpg", frame)
		return {"hand":{"L":(xL,y_max),"R":(xR,y_max)}}
	
	def find_sholders(self,frame,armpits, y_head):
		arms=[]
		for armpit in armpits:
			for y in range( armpit[1]-armpit[1]/24,y_head+3,-1):  #pierwsze odjecie zapobiega wylapaniu pachy
				if cv.Get2D(frame, y,armpit[0])[0] and cv.Get2D(frame, y-1,armpit[0])[0]<1 and cv.Get2D(frame, y-2,armpit[0])[0]<1 :
					arms.append(( armpit[0],y))
		if len(arms)>=2:
			ayL = (arms[0][1]+armpits[0][1])/2
			ayR = (arms[1][1]+armpits[1][1])/2
			ayLx, ayRx =None, None
			for x in range(0, frame.width):
				if cv.Get2D(frame, ayL,x)[0]>0 and cv.Get2D(frame, ayL,x-1)[0]<1 and ayLx==None:
					ayLx=x ; i=1
				if cv.Get2D(frame, ayR,x)[0]>0 and cv.Get2D(frame, ayR,x-1)[0]<1:
					ayRx=x
			return (ayLx,ayL) , (ayRx,ayR)
		return None , None
	
	def find_waist(self,frame, y_armpits, krocze):
		[ysrL, ysrR] = y_armpits
		waistY = int((krocze["L"][1]+((ysrR+ysrL)/2.0))/2.0)
		talia_pts=[]
		for x in range(0, frame.width-1):
			if cv.Get2D(frame, waistY,x)[0] and cv.Get2D(frame, waistY,x+1)[0]<1:
				talia_pts.append((x,waistY))
		if len(talia_pts)>=6:
			return talia_pts[2] , talia_pts[3]
		return None,None

	def find_head_top(self,face_center, face_rect,border_img_path):
		frame =cv.LoadImageM(border_img_path)
		for y in range(face_rect[1], face_rect[1]+face_rect[3]):
			t_x,t_y = 0,0
			top_pts=[]
			for x in range(face_rect[0], face_rect[0]+face_rect[2]):
				if cv.Get2D(frame, y,x)[0]:
					top_pts.append((x,y))
			if len(top_pts)>=2:
				t_x = (top_pts[0][0]+top_pts[1][0])/2
				t_y = (top_pts[0][1]+top_pts[1][1])/2
				break
		return {"head_top":(t_x,t_y)}
		
	def find_ears(self,face_rect, neck, head_top,border_img_path):
		frame =cv.LoadImageM(border_img_path)
		obszar_sprawdzania = face_rect[2]/4
		pt_stop = head_top
		
		#prawe ucho
		pt_start = neck['UR']
		xes =[]
		start_x = x_min = pt_start[0]
		y_min = pt_start[1]
		for y in range(pt_start[1],pt_stop[1],-1):
			xst =start_x-obszar_sprawdzania
			xsp =start_x+obszar_sprawdzania
			if xst <0:xst=face_rect[0]
			if xsp>frame.width: xsp=face_rect[0]+face_rect[2]
			for x in range(xst, xsp):
				if cv.Get2D(frame, y,x)[0]:
					if x<x_min:
						x_min = x
						y_min = y
					start_x = x
					break
			y-=1
			
		#teraz lewe ucho
		pt_start = neck['UL']
		xes =[]
		start_x = x_max = pt_start[0]
		y_max = pt_start[1]
		for y in range(pt_start[1],pt_stop[1],-1):
			xst =start_x-obszar_sprawdzania
			xsp =start_x+obszar_sprawdzania
			if xst <0:xst=face_rect[0]
			if xsp>frame.width: xsp=pt_start[1]
			for x in range(xst, xsp):
				if cv.Get2D(frame, y,x)[0]:
					if x>x_max:
						x_max = x
						y_max = y
					start_x = x
					break
			y-=1
			
		return {"R":(x_min,y_min),"L":(x_max,y_max)}
		
	def find_forhead(self, face_rect, head_top, ears,border_img_path):
		frame =cv.LoadImageM(border_img_path)
		start_L= ((ears['L'][0]+head_top[0])/2, (ears['L'][1]+head_top[1])/2)
		start_R= ((ears['R'][0]+head_top[0])/2, (ears['R'][1]+head_top[1])/2)
		obszar_sprawdzania = face_rect[2]/6
		for y in range(start_L[1]-3, start_L[1]+3):
			
			for x in range (start_L[0]-obszar_sprawdzania ,start_L[0]+obszar_sprawdzania):
				if cv.Get2D(frame, y,x)[0]:
					forhead_L= (x,y)
					break
			for x in range(start_R[0]-obszar_sprawdzania, start_R[0]+obszar_sprawdzania):
				if cv.Get2D(frame,y,x)[0]:
					forhead_R= (x,y)
					break
		return {'L':forhead_L, 'R':forhead_R}
			
	def mean(self,list):
		return sum(list)/len(list)
	
