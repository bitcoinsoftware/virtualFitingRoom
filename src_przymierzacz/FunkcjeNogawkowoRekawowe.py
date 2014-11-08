import ast, math
import cv2.cv as cv
import cv2
from FunkcjeUbraniowe import *
class FunkcjeNogawkowoRekawowe(FunkcjeUbraniowe):

	def paste_cloath(self, body_url, out_url):
		body_frame = cv.LoadImageM(body_url)
		if self.Lparturl:
			Lpart_frame = cv.LoadImageM(self.Lparturl )
			body_frame = self.paste_part(Lpart_frame,body_frame)
		if self.Rparturl:
			Rpart_frame = cv.LoadImageM(self.Rparturl)
			body_frame = self.paste_part(Rpart_frame,body_frame)
		if self.centralurl:
			central_frame = cv.LoadImageM(self.centralurl)
			body_frame = self.paste_part(central_frame,body_frame)
		cv.SaveImage(out_url,body_frame)
		 
	def paste_part(self, cloath_frame, body_frame,):
		# self.punkt_odniesienia - cialo , self.srodek_ukladu - ubranie
		zero_point,end_point= self.count_start_and_stop_points(self.punkt_odniesienia_na_ciele, self.punkt_odniesienia_na_ubraniu,cloath_frame, body_frame)
		ix,iy=0,0
		stoper =0
		for x in range(zero_point[0],end_point[0]):
			iy=0
			for y in range(zero_point[1],end_point[1]):
				try:
					if sum(cv.Get2D(cloath_frame,iy,ix))>0:
						cv.Set2D(body_frame, y, x,cv.Get2D(cloath_frame,iy,ix))
				except:
					print "iy , ix ", iy,ix
					stoper = 1
					break
				iy+=1
			ix+=1
			if stoper: break
		return body_frame
			
	def change_url_by_pasting_filename(self, url, pasta):
		splitedname = url.split('/')
		filename=splitedname[-1]
		folder = '/'.join(splitedname[:-1])
		filename = pasta+filename
		url = folder+'/'+filename
		return [url , filename]

		
