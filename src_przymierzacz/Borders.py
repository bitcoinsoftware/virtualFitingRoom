import cv2.cv as cv
import itertools
from FunkcjePomocnicze import *


class Borders:
	def __init__(self, img_path, bg_path, out_borders_url, prepared_photo_out_url,center):
		self.prepare_photo(img_path, prepared_photo_out_url)
		print "prepared photo zrobione"
		res, tresholded_frame =self.substract_body_from_background(img_path, bg_path,prepared_photo_out_url)
		print "subs zrobione"
		self.tresholded_frame = res
		self.extract_only_borders(tresholded_frame, out_borders_url, center)
		self.img_path = img_path
	def prepare_photo(self, img_path_or_frame, out_url):
		to_jest_str = type(img_path_or_frame)==type("dupa") 
		if to_jest_str:
			frame = cv.LoadImageM(img_path_or_frame)
		else:
			frame = img_path_or_frame
		w,h = frame.width, frame.height
		black =[0]*frame.channels
		h2,w2=h-1,w-1
		for x in range(w):
			cv.Set2D(frame,0,x,black)
			cv.Set2D(frame,1,x,black)
			cv.Set2D(frame,h2-1,x,black)
		for y in range(h):
			cv.Set2D(frame,y,0,black)
			cv.Set2D(frame,y,1,black)
			cv.Set2D(frame,y,w2,black)
			cv.Set2D(frame,y,w2-1,black)
		if to_jest_str:
			cv.SaveImage(out_url,frame)
			return url
		else:
			return frame
		
	def substract_body_from_background(self,img_path, bg_path,prepared_photo_out_url):
		frame = cv.LoadImageM(img_path)
		bg = cv.LoadImageM(bg_path)
		#returns frame - bg
		cv.AbsDiff(frame,bg,frame)
		#zmieniam glebie
		gray = cv.CreateImage((frame.width,frame.height), 8, 1)
		grayM1 = cv.CreateImage((frame.width,frame.height), 8, frame.channels)
		cv.ConvertScale(frame,grayM1)
		cv.CvtColor(grayM1, gray, cv.CV_BGR2GRAY)
		[gray,self.prepared_photo_url] = self.prepare_photo(gray,prepared_photo_out_url)
		
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
		self.bodybrds = body_borders
		cv.SaveImage(out_borders_url, body_borders)

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
		self.tablica_konturow = tablica_konturow
		#print tablica_konturow
		#Czysta_macierz
		cv.SaveImage("Dane_wyjsciowe.pgm",res_matrix)
		return res_matrix , tablica_konturow
		
	def get_only_body(self,out_url):
		tresh_body = self.tresholded_frame
		cv.SaveImage('test/tresholded.jpg',tresh_body)
		borders = self.bodybrds
		frame = cv.LoadImage(self.img_path)
		res_mat1 = cv.CreateImage((frame.width,frame.height), 8, 4)
		#zerowanie macierzy
		for i in range(res_mat1.width):
			for j in range(res_mat1.height):
				cv.Set2D(res_mat1,j,i,(0,0,0,0))
				
		for y in range(borders.height):
			flaga_parzystosci = 0
			for x in range(borders.width-2):
				if flaga_parzystosci==1: #wtedy kopiuj
					color = cv.Get2D(frame,y,x)
					cv.Set2D(res_mat1,y,x,color)
				if cv.Get2D(borders,y,x)[0]>1  and flaga_parzystosci==0: #kopiuj #and cv.Get2D(tresh_body,y,x)[0]>1
					flaga_parzystosci=1
				elif cv.Get2D(tresh_body,y,x)[0]<1  and cv.Get2D(tresh_body,y,x+1)[0]<1 and cv.Get2D(tresh_body,y,x+2)[0]<1 and flaga_parzystosci==1: #przestan kopiowac #and cv.Get2D(tresh_body,y,x)[0]<1
					flaga_parzystosci=0
		cv.SaveImage(out_url,res_mat1)
		return out_url
        """         
		for pt in self.tablica_konturow: # usuwanie konturow
			for x in range(pt[1]-2,pt[1]+2):
				if x>0 and x<res_mat1.width:
					cv.Set2D(res_mat1,pt[0],x,(0,0,0,0))
		"""

		
		
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

	def prepare_photo(self, img_path_or_frame, prepared_photo_url):
		to_jest_str = type(img_path_or_frame)==type("dupa") 
		if to_jest_str:
			frame = cv.LoadImageM(img_path_or_frame)
		else:
			frame = img_path_or_frame
			
		w,h = frame.width, frame.height
		black =[0]*frame.channels
		h2,w2=h-1,w-1
		for x in range(w):
			cv.Set2D(frame,0,x,black)
			cv.Set2D(frame,1,x,black)
			cv.Set2D(frame,h2-1,x,black)
		for y in range(h):
			cv.Set2D(frame,y,0,black)
			cv.Set2D(frame,y,1,black)
			cv.Set2D(frame,y,w2,black)
			cv.Set2D(frame,y,w2-1,black)
		#if to_jest_str:
		#	url = "test/przygotowane_zdjecie.jpg"
		cv.SaveImage(prepared_photo_url,frame)
		#return url
		#else:
		return [frame, prepared_photo_url]
