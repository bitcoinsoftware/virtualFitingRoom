import cv2.cv as cv
import itertools
from tkFileDialog import askopenfilename
from Body import *
from BodyBrinks import *
from Borders import *
from FunkcjeSprawdzajace import *
from FunkcjePomocnicze import *
from Biustonosz import *
from Pants  import*
from Skirt  import*
from DressNoSleve import *
from trousersLong  import*
from trousersShort  import*
#from Sukienka  import*
from Coat  import*
from Jacket import*
from Top  import*

class pozycjoner2( FunkcjeSprawdzajace, FunkcjePomocnicze):
	
	def find_if_there_is_a_face(self,path):
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
					
	def find_border_amount_array(self,img, face_center_x):
		width,height = img.width, img.height
		max_steps_right = width - face_center_x
		y=0
		borders_amount_right =[]
		borders_amount_left =[]
		for y in range(height):
			#jade w prawo
			x= face_center_x
			border_amount=0
			while x<width:
				if abs(cv.Get2D(img, y,x)[0]-cv.Get2D(img,y,x-1)[0])>0:
					border_amount+=1
				x+=1
			borders_amount_right.append(border_amount)
			#znowu na srodek
			x= face_center_x
			border_amount=0
			#a teraz w druga strone - lewo
			while x>0:
				if abs(cv.Get2D(img, y,x)[0]-cv.Get2D(img,y,x+1)[0])>0:
					border_amount+=1
				x-=1
			borders_amount_left.append(border_amount)
		borders_amount =[]
		for i in range(height):
			borders_amount.append(borders_amount_left[i]+ borders_amount_right[i])
		return borders_amount
	
	def get_only_body_borders(self,img , start_point,direction_to_find_start=-1,vertical=0):
		#zaczynam od start pointa , ide w lewo  i szukam pierwszego bialego piksela
		tablica_konturow=[]
		x ,y= start_point[0], start_point[1]
		border_x = 0
		if vertical==0:  #jesli na boki ma isc
			while x >2 and x<img.width-1:
				c_x , c_xm1 ,c_xm2, c_xm3  = cv.Get2D(img, y,x)[0],cv.Get2D(img, y,x-1)[0],cv.Get2D(img, y,x-2)[0],cv.Get2D(img, y,x-3)[0]
				if c_x + c_xm3 <1 and  c_xm1 + c_xm2>255:  #to znaczy ze trafilem w bialy pasek
					border_x = x+direction_to_find_start
					break
				x+=direction_to_find_start
			x =border_x
		else: #jesli od krocza ma isc
			x ,y= start_point[0], start_point[1]
			border_y=0
			while y >2 and y <img.height-1:
				c_y, c_ym1, c_ym2, c_ym3 = cv.Get2D(img, y,x)[0],cv.Get2D(img, y-1,x)[0],cv.Get2D(img, y-2,x)[0],cv.Get2D(img, y-3,x)[0]
				if c_y+c_ym3 < 1 and c_ym1 + c_ym2>255:
					border_y = y +direction_to_find_start
					break
				y=y+direction_to_find_start
			y =border_y
				
		res_matrix = cv.CreateImage((img.width,img.height), 8,1)
		for i in range(res_matrix.width):
			for j in range(res_matrix.height):
				cv.Set2D(res_matrix,j,i,(0,0,0,0))
			
				
		#cv.SaveImage("Argument_wejsciowy.jpg",img)
		#cv.SaveImage("Czysta_macierz.jpg",res_matrix)
		print "start border found" , (border_x, y)
		
		x0,y0 =prev_x, prev_y= x, y 
		#zaczynam wedrowke po konturze
		cv.Set2D(res_matrix,y,x,255)
		i=0
		indeks_niepowodzen,dyst,flaga_parzystosci, = 0,2,0
		while 1:
			i+=1		
			
			if x-dyst>=0 and x-dyst<img.width and y>=0 and y<img.height and cv.Get2D(img,y,x-dyst)[0]>0 and cv.Get2D(res_matrix,y,x-dyst)[0]<1:
				x = x-dyst; cv.Set2D(res_matrix,y,x,(255,0,0,0)); 
				cv.Set2D(res_matrix,(prev_y+y)/2,(prev_x+x)/2,(255,0,0,0));indeks_niepowodzen=0
			elif x-dyst>=0 and x-dyst<img.width and y-dyst>=0 and y-dyst<img.height and cv.Get2D(img,y-dyst,x-dyst)[0]>0 and cv.Get2D(res_matrix,y-dyst,x-dyst)[0]<1:
				x,y = x-dyst,y-dyst; cv.Set2D(res_matrix,y,x,(255,0,0,0));
				cv.Set2D(res_matrix,(prev_y+y)/2,(prev_x+x)/2,(255,0,0,0));indeks_niepowodzen=0
			elif x-dyst>=0 and x-dyst<img.width and y+dyst>=0 and y+dyst<img.height and cv.Get2D(img,y+dyst,x-dyst)[0]>0 and cv.Get2D(res_matrix,y+dyst,x-dyst)[0]<1:
				x,y = x-dyst,y+dyst; cv.Set2D(res_matrix,y,x,(255,0,0,0));
				cv.Set2D(res_matrix,(prev_y+y)/2,(prev_x+x)/2,(255,0,0,0));indeks_niepowodzen=0
			#x =x
			elif x>=0 and x<img.width and y-dyst>=0 and y-dyst<img.height and cv.Get2D(img,y-dyst,x)[0]>0 and cv.Get2D(res_matrix,y-dyst,x)[0]<1:
				y = y-dyst; cv.Set2D(res_matrix,y,x,(255,0,0,0));
				cv.Set2D(res_matrix,(prev_y+y)/2,(prev_x+x)/2,(255,0,0,0));indeks_niepowodzen=0
			elif x>=0 and x<img.width and y+dyst>=0 and y+dyst<img.height and cv.Get2D(img,y+dyst,x)[0]>0 and cv.Get2D(res_matrix,y+dyst,x)[0]<1:
				y = y+dyst; cv.Set2D(res_matrix,y,x,(255,0,0,0));
				cv.Set2D(res_matrix,(prev_y+y)/2,(prev_x+x)/2,(255,0,0,0));indeks_niepowodzen=0
			#x+1
			elif x+dyst>=0 and x+dyst<img.width and y-dyst>=0 and y-dyst<img.height and cv.Get2D(img,y-dyst,x+dyst)[0]>0 and cv.Get2D(res_matrix,y-dyst,x+dyst)[0]<1:
				x,y=x+dyst,y-dyst; cv.Set2D(res_matrix,y,x,(255,0,0,0));
				cv.Set2D(res_matrix,(prev_y+y)/2,(prev_x+x)/2,(255,0,0,0));indeks_niepowodzen=0
			elif x+dyst>=0 and x+dyst<img.width and y>=0 and y<img.height and cv.Get2D(img,y,x+dyst)[0]>0 and cv.Get2D(res_matrix,y,x+dyst)[0]<1:
				x = x+dyst; cv.Set2D(res_matrix,y,x,(255,0,0,0));
				cv.Set2D(res_matrix,(prev_y+y)/2,(prev_x+x)/2,(255,0,0,0));indeks_niepowodzen=0
			elif x+dyst>=0 and x+dyst<img.width and y+dyst>=0 and y+dyst<img.height and cv.Get2D(img,y+dyst,x+dyst)[0]>0 and cv.Get2D(res_matrix,y+dyst,x+dyst)[0]<1:
				x,y=x+dyst,y+dyst; cv.Set2D(res_matrix,y,x,(255,0,0,0));
				cv.Set2D(res_matrix,(prev_y+y)/2,(prev_x+x)/2,(255,0,0,0));indeks_niepowodzen=0
			else:
				#tu bedzie funkcja co jak szukacz sie zgubi, to szuka czy jest jakis bialy punkt w kwadracie x_zgubiony, y_zgubiony, co jeszcze nie byl tam		
				indeks_niepowodzen+=1
				dyst+=1
				if dyst==3 and flaga_parzystosci==0:
					x,y=x0,y0
					indeks_niepowodzen,dyst=0,2
					flaga_parzystosci =1
				elif flaga_parzystosci==1 and indeks_niepowodzen==3:
					indeks_niepowodzen,dyst,flaga_parzystosci=0,2,0
					print "lost way ", x,y
					x,y= self.find_lost_way(x,y,5,5,img,res_matrix)
					print "found way ",x,y
					if x==None: 
						break
			tablica_konturow.append([(prev_y+y)/2,(prev_x+x)/2])
			tablica_konturow.append([y,x])
			prev_x, prev_y = x,y
		#print tablica_konturow
		#Czysta_macierz
		cv.SaveImage("Dane_wyjsciowe.pgm",res_matrix)
		return res_matrix , tablica_konturow
		
	def find_lost_way(self,x,y, dx,dy,img,res_matrix):
		#print "FIND" ,res_matrix.height,res_matrix.width,img.height,img.width
		x0,y0,xk,yk = x-dx,y-dy,x+dx,y+dy
		for x in range(x0,xk):
			for y in range(y0,yk):
				if x>0 and y>0 and y<res_matrix.height and x<res_matrix.width: #jesli nie wykraczam poza obraz
					#print x,y
					if cv.Get2D(res_matrix, y,x)[0]<1 and cv.Get2D(img, y,x)[0]>1:  #jesli jeszcze nie wszedlem na ten piksel i jest bialy
						cv.Set2D(res_matrix,y,x,(255,0,0,0))
						return x,y
		return None ,None
			

		
	def detect(self,img, cascade,scaleFactor=1.3, minsize=(30,30)):
		rects = cv.HaarDetectObjects(img, cascade, cv.CreateMemStorage(0),scaleFactor, 4, cv.CV_HAAR_SCALE_IMAGE, minsize)
		if len(rects) == 0:
			return []
		rectss=[]
		for rect in rects:
			rectss.append(rect[0])
		return rectss

	def substract_body_from_background(self,img_path, bg_path):
		frame = cv.LoadImageM(img_path)
		bg = cv.LoadImageM(bg_path)
		#returns frame - bg
		cv.AbsDiff(frame,bg,frame)
		#zmieniam glebie
		gray = cv.CreateImage((frame.width,frame.height), 8, 1)
		grayM1 = cv.CreateImage((frame.width,frame.height), 8, frame.channels)
		cv.ConvertScale(frame,grayM1)
		cv.CvtColor(grayM1, gray, cv.CV_BGR2GRAY)
		gray = self.prepare_photo(gray)
		
		gray0 = cv.CreateImage((frame.width,frame.height), 8, 1)
		gray1 = cv.CreateImage((frame.width,frame.height), 8, 1)
		gray2 = cv.CreateImage((frame.width,frame.height), 8, 1)
		#print frame.channels

		#rozmazuje i proguje
		cv.Smooth(gray, gray1,cv.CV_BILATERAL,3)
		cv.Threshold(gray1,gray,35,255,cv.CV_THRESH_BINARY)
		cv.Smooth(gray, gray,cv.CV_BLUR,7)
		cv.Threshold(gray,gray,70,255,cv.CV_THRESH_BINARY)
		
		#kopiuje za wczsu
		cv.Copy(gray,gray0)
		
		#w dywergenceje w poziomie

		cv.Flip(gray ,gray2,1)
		gray3 = cv.CreateImage((frame.width,frame.height), 32, 1)
		gray4 = cv.CreateImage((frame.width,frame.height), 32, 1)
		cv.Sobel(gray, gray3, 1,0,1) 
		cv.Sobel(gray2, gray4, 1,0,1)
		cv.Flip(gray3,gray3,1)
		gray8bit0 = cv.CreateImage((frame.width,frame.height), 8, 1)
		gray8bit1 = cv.CreateImage((frame.width,frame.height), 8, 1)
		cv.ConvertScale(gray3,gray8bit0)
		cv.ConvertScale(gray4,gray8bit1)
		cv.Add(gray8bit0, gray8bit1, gray1)
		
		#dywergence w pionie
		cv.Flip(gray ,gray2,0)
		cv.Sobel(gray2, gray3,0,1,1)
		cv.Sobel(gray,  gray4,0,1,1)
		cv.Flip(gray3,gray3,0)
		cv.ConvertScale(gray3,gray8bit0)
		cv.ConvertScale(gray4,gray8bit1)
		cv.Add(gray8bit0, gray8bit1, gray2) 
		
		cv.Flip(gray2, gray2,1)
		#suma pionowej i poziomej dywergencji
		cv.Add(gray2,gray1,gray)
		cv.Flip(gray,gray,1)
		#zwraca pelna postac, kontury
		return gray0,gray	
	
	def make_background(self,frame, bg_path):
		bg = cv.CreateImage((frame.width,frame.height), 8, 4)
		color = cv.Get2D(frame,0,0)
		for i in range(frame.width):
			for j in range(frame.height):
				cv.Set2D(bg,j,i,color)
		cv.SaveImage(bg_path, bg)
		
		
	def aktualizuj_punkty_na_podstawie_krawedzi(self, krawedz, klucze):
		#krawedz=krawedz[key]
		if klucze[0] in ['L','R']:
			xL, ptL, xR, ptR=krawedz[0][0], krawedz[0], krawedz[0][0],krawedz[0]
			sumY=i=0
			for pt in krawedz:
				sumY += pt[1]
				if pt[0]<xL:
					xL=pt[0]
					ptL=pt
				if pt[0]>xR:
					xR=pt[0]
					ptR=pt	
				i+=1
			avY=sumY/i
			ptL = (xL, avY)
			ptR = (xR, avY)
			return {'L':ptL,'R':ptR}		
		elif klucze[0] in ['U','D']:
			yU, ptU, yD, ptD=krawedz[0][1], krawedz[0], krawedz[0][1],krawedz[0]
			for pt in krawedz:
				if pt[1]<yU:
					yU=pt[1]
					ptU=pt
				if pt[1]>yD:
					yD=pt[1]
					ptD=pt
			return {'U':ptU, 'D':ptD}
		
	
	def extract_only_borders(self, tresholded_frame, out_borders_url, center):
		body_borders,tk1 = self.get_only_body_borders(tresholded_frame, start_point = center, 
		direction_to_find_start=-1,)# start z lewej
		
		bb8bit = cv.CreateImage((body_borders.width,body_borders.height), 8, 1)
		cv.ConvertScale(body_borders,bb8bit)
		
		body_borders2,tk2 = self.get_only_body_borders(tresholded_frame, start_point = center, 
		direction_to_find_start=1)# start z prawej
		
		bb8bit2 = cv.CreateImage((body_borders.width,body_borders.height), 8, 1)
		cv.ConvertScale(body_borders2,bb8bit2)
		
		cv.Add(bb8bit2,bb8bit,body_borders)
		
		body_borders2,tk2 = self.get_only_body_borders(tresholded_frame, start_point = center,
		 direction_to_find_start=-1,vertical=1)# start z krocza do gory
		cv.ConvertScale(body_borders2,bb8bit)
		cv.Add(bb8bit,body_borders,body_borders)

		body_borders2,tk2 = self.get_only_body_borders(tresholded_frame, start_point = center,
		 direction_to_find_start=1,vertical=1)# start z krocza do dolu
		
		cv.ConvertScale(body_borders2,bb8bit)
		cv.Add(body_borders,bb8bit,body_borders)
		
		#to samo na flipped
		cv.Flip(tresholded_frame,tresholded_frame,1)
		body_borders2,tk2 = self.get_only_body_borders(tresholded_frame, start_point = center, direction_to_find_start=-1)
		cv.Flip(body_borders2,body_borders2,1)
		cv.ConvertScale(body_borders2,bb8bit)
		cv.Add(body_borders,bb8bit,body_borders)
		
		body_borders2,tk2 = self.get_only_body_borders(tresholded_frame, start_point = center, direction_to_find_start=1)
		cv.Flip(body_borders2,body_borders2,1)
		cv.ConvertScale(body_borders2,bb8bit)
		cv.Add(body_borders,bb8bit,body_borders)
		cv.SaveImage(out_borders_url, body_borders)
		
	def run_analysis(self,img_path, bg_path):
		face = self.find_if_there_is_a_face(img_path)
		if face[0]:
			#img_path2 = self.prepare_photo(img_path)
			#print img_path2
			face_center = face[0]
			#print "face center  ",face_center , "######", face
			out_bdr_url = 'test/brdrs.png'
			out_prprd_url = 'test/prepared_photo.png'
			borders = Borders(img_path, bg_path, out_bdr_url,out_prprd_url, face_center)
			borders.get_only_body( 'test/cialo.jpg')
			#body =  Body(img_path)
			body = Body(face, out_bdr_url)
			
			"""
			url = "/home/gimbo/Desktop/koniu/ubrania/plaszcze/hmprod0.png/hmprod0.png"
			#url = "/home/gimbo/Desktop/koniu/ubrania/plaszcze/hmprod1.png/hmprod1.png"
			plaszcz =Plaszcz(body,url)
			o_url = "test/plaszcz.jpg"
			plaszcz.paste_cloath("input2.jpg",o_url)	
			
			#url = "/home/gimbo/Desktop/koniu/ubrania/top/krotki_rekaw/hmprod5.png/hmprod5.png"		
			#url = "/home/gimbo/Desktop/koniu/ubrania/top/krotki_rekaw/hmprod4.png/hmprod4.png"		
			#url = "/home/gimbo/Desktop/koniu/ubrania/top/krotki_rekaw/hmprod3.png/hmprod3.png"		
			url = "/home/gimbo/Desktop/koniu/ubrania/top/krotki_rekaw/hmprod1.png/hmprod1.png"		
			top =Top(body,url)
			o_url = "test/top.jpg"
			top.paste_cloath("input2.jpg",o_url)
			
			url = "/home/gimbo/Desktop/koniu/ubrania/spodnica/hmprod.png/hmprod.png"
			spodnica = Spodnica(body, url)
			o_url = "test/spodnica.png"
			spodnica.paste_cloath("input.jpg",o_url)
			
			"""
			"""
			#body = Body(img_path)
			body = Body(f_center_f_rect, photo_url, out_borders_url = "TEST24.pgm" )
			out_bdr_url = "test/testujeBORDERS.png"
			out_borders_url = "TEST24.pgm"
			"""
			"""
			#TODO Skalowanie rekawow
 		
			url = "/home/gimbo/Desktop/koniu/ubrania/spodnie/dlugie/hmprod1.png/hmprod1.png"
			spodnie = Spodnie(body,url)
			o_url = "test/spodenki.jpg"
			spodnie.paste_cloath("input.jpg",o_url)
			
			url = "/home/gimbo/Desktop/koniu/ubrania/kurtki/hmprod2.png/hmprod2.png"
			spodnie = Kurtka(body,url)
			o_url = "test/kurtka.jpg"
			spodnie.paste_cloath("input.jpg",o_url)
			"""
			
		else:
			print "nie wykryto twarzy "
		
if __name__ == "__main__":
	a = pozycjoner2()
	path = "input2.jpg"
	bg_path = "bg.jpg"
	a.run_analysis(path,bg_path)    
