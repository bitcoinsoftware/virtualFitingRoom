import cv2.cv as cv

class FunkcjeSprawdzajace:
	
	def rysuj_slownik_punktow(self,inUrl,dictionary,outUrl, color=(0,255,0,0)):
		f = cv.LoadImageM(inUrl)
		keys = dictionary.keys()
		for key in keys:
			pt = (int(dictionary[key][0]), int(dictionary[key][1]) )
			#print pt
			cv.Circle(f , pt,3, color, 2)
			#cv.PutText(f, key, pt, cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, 1, 2, 0, 0, 0), (150,0,0, 0))
		cv.SaveImage(outUrl, f)
		
	def rysuj_tablice_punktow(self,inUrl,array,outUrl):
		pass
		f = cv.LoadImageM(inUrl)
		for pt in array:
			pt = (int(pt[0]),int(pt[1]))
			cv.Circle(f,pt,3,(0,255,0,0),2)
		cv.SaveImage(outUrl, f)
	
	def rysuj_punkty_ciala(self,inUrl, body, outUrl):
		#frame = cv.LoadImageM("TEST22.pgm")
		frame = cv.LoadImageM(inUrl)
		cv.Circle(frame , body["groin"]["L"],5, (0,0, 255, 0), 4)
		cv.Circle(frame , body["groin"]["R"],5, (0,0, 255, 0), 4)
		cv.Circle(frame , body["head_top"],5, (255,0, 0, 0), 4)
		cv.Circle(frame , body["armpit"]["L"],5, (255,0, 0, 0), 4)
		cv.Circle(frame , body["armpit"]["R"],5, (255,0, 0, 0), 4)
		cv.Circle(frame , body["hand"]["L"],5, (255,0, 0, 0), 4)
		cv.Circle(frame , body["hand"]["R"],5, (255,0, 0, 0), 4)
		
		cv.Circle(frame , body["forhead"]["L"],5, (255,0, 0, 0), 4)
		cv.Circle(frame , body["forhead"]["R"],5, (255,0, 0, 0), 4)
		
		if body["sholder"]["L"]:
			cv.Circle(frame , body["sholder"]["L"],5, (255,0, 0, 0), 4)
			cv.Circle(frame , body["sholder"]["R"],5, (255,0, 0, 0), 4)
		
		cv.Circle(frame , body["waist"]["L"],5, (255,0, 0, 0), 4)
		cv.Circle(frame , body["waist"]["R"],5, (255,0, 0, 0), 4)
		#print "LOIN",body["loin"]["L"]
		cv.Circle(frame , body["loin"]["L"],5, (255,0, 0, 0), 4)
		cv.Circle(frame , body["loin"]["R"],5, (255,0, 0, 0), 4)
		cv.Circle(frame , body["neck"]["UL"],5, (255,0, 0, 0), 4)
		cv.Circle(frame , body["neck"]["UR"],5, (255,0, 0, 0), 4)
		cv.Circle(frame , body["neck"]["DL"],5, (255,0, 0, 0), 4)
		cv.Circle(frame , body["neck"]["DR"],5, (255,0, 0, 0), 4)
		cv.Circle(frame , body["feet"]["L"],5, (255,0, 0, 0), 4)
		cv.Circle(frame , body["feet"]["R"],5, (255,0, 0, 0), 4)
		cv.Circle(frame , body["wing"]["L"],5, (255,0, 0, 0), 4)
		cv.Circle(frame , body["wing"]["R"],5, (255,0, 0, 0), 4)
		cv.Circle(frame , body["knee"]["L"]['inside'],5, (0,0, 255, 0), 4)
		cv.Circle(frame , body["knee"]["L"]['outside'],5, (0,60,0, 0), 4)
		cv.Circle(frame , body["knee"]["R"]['inside'],5, (128,0, 60, 0), 4)
		cv.Circle(frame , body["knee"]["R"]['outside'],5, (60,60, 60, 0), 4)
		
		cv.Circle(frame , body["crossbone"]["L"]['inside'],5, (0,0, 255, 0), 4)
		cv.Circle(frame , body["crossbone"]["L"]['outside'],5, (0,60,0, 0), 4)
		cv.Circle(frame , body["crossbone"]["R"]['inside'],5, (128,0, 60, 0), 4)
		cv.Circle(frame , body["crossbone"]["R"]['outside'],5, (60,60, 60, 0), 4)
		
		cv.Circle(frame , body["ankle"]["L"]['inside'],5, (0,0, 255, 0), 4)
		cv.Circle(frame , body["ankle"]["L"]['outside'],5, (0,60,0, 0), 4)
		cv.Circle(frame , body["ankle"]["R"]['inside'],5, (128,0, 60, 0), 4)
		cv.Circle(frame , body["ankle"]["R"]['outside'],5, (60,60, 60, 0), 4)
		
		cv.Circle(frame , body["elbow"]["L"]['inside'],5, (128,0, 0, 0), 4)
		cv.Circle(frame , body["elbow"]["L"]['outside'],5, (128,128, 0, 0), 4)
		cv.Circle(frame , body["elbow"]["R"]['inside'],5, (128,128, 128, 0), 4)
		cv.Circle(frame , body["elbow"]["R"]['outside'],5, (128,0, 128, 0), 4)
		
		cv.Circle(frame , body["wrist"]["L"]['inside'],10, (0,0, 128, 0), 4)
		cv.Circle(frame , body["wrist"]["L"]['outside'],5, (0,128, 128, 0), 4)
		cv.Circle(frame , body["wrist"]["R"]['inside'],10, (255,0,255, 0), 4)
		cv.Circle(frame , body["wrist"]["R"]['outside'],5, (70,0, 70, 0), 4)
		cv.SaveImage(outUrl, frame)
		
	def rysuj_krawedzie(self,inUrl,brinks,outUrl):
		frame = cv.LoadImageM(inUrl)
		#pojedyncze
		for point in brinks['groin_brink']:
			cv.Circle(frame , point,3, (60,60,60, 0), 2)
		#podwojne
		for point in brinks['head_top_brink']['L']:
			cv.Circle(frame , point,3, (0,255,255, 0), 2)
		for point in brinks['head_top_brink']['R']:
			cv.Circle(frame , point,3, (255,255,0, 0), 2)	
		for point in brinks['forhead_brink']['L']:
			cv.Circle(frame , point,3, (0,255,0, 0), 2)
		for point in brinks['forhead_brink']['R']:
			cv.Circle(frame , point,3, (0,255,0, 0), 2)	
		for point in brinks['face_brink']['L']:
			cv.Circle(frame , point,3, (255,0,0, 0), 2)
		for point in brinks['face_brink']['R']:
			cv.Circle(frame , point,3, (255,0,0, 0), 2)
		for point in brinks['neck_brink']['L']:
			cv.Circle(frame , point,3, (0,0,255, 0), 2)
		for point in brinks['neck_brink']['R']:
			cv.Circle(frame , point,3, (0,0,255, 0), 2)	
		for point in brinks['sholder_brink']['L']:
			cv.Circle(frame , point,3, (128,0,128, 0), 2)
		for point in brinks['sholder_brink']['R']:
			cv.Circle(frame , point,3, (128,0,128, 0), 2)
		for point in brinks['corpse_brink']['L']:
			cv.Circle(frame , point,3, (0,0,255, 0), 2)
		for point in brinks['corpse_brink']['R']:
			cv.Circle(frame , point,3, (0,0,255, 0), 2)
		for point in brinks['loin_brink']['L']:
			cv.Circle(frame , point,3, (255,0,0, 0), 2)
		for point in brinks['loin_brink']['R']:
			cv.Circle(frame , point,3, (255,0,0, 0), 2)
		#poczworne
		for point in brinks['legs_brink']['L']['outside']:
			cv.Circle(frame , point,3, (0,255,255, 0), 2)
		for point in brinks['legs_brink']['R']['outside']:
			cv.Circle(frame , point,3, (255,255,0, 0), 2)
		for point in brinks['legs_brink']['L']['inside']:
			cv.Circle(frame , point,3, (60,60,60, 0), 2)
		for point in brinks['legs_brink']['R']['inside']:
			cv.Circle(frame , point,3, (128,128,128, 0), 2)		
			
		for point in brinks['arm_brink']['L']['outside']:
			cv.Circle(frame , point,3, (0,170,170, 0), 2)
		for point in brinks['arm_brink']['R']['outside']:
			cv.Circle(frame , point,3, (170,170,0, 0), 2)
		for point in brinks['arm_brink']['L']['inside']:
			cv.Circle(frame , point,3, (90,190,90, 0), 2)
		for point in brinks['arm_brink']['R']['inside']:
			cv.Circle(frame , point,3, (100,100,100, 0), 2)	
			
		cv.SaveImage(outUrl, frame)
		
	
		
