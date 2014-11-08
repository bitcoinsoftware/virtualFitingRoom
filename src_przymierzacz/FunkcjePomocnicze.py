import cv2.cv as cv
import cv2
import math
class FunkcjePomocnicze:
	
	def find_best_brink_point(self,pt,brink,direction="x"):
		if direction=="x" or direction=="y":
			if direction=="x":
				index=0
			elif direction=="y":
				index=1
		
			best = brink[0]
			dist = abs(pt[index]-best[index])
			for b in brink:
				if abs(pt[index]-b[index])<dist:
					dist=abs(pt[index]-b[index])
					best = b
		elif direction =="r":
			best = brink[0]
			dist = self.count_diagonal_length(pt ,best)
			for b in brink:
				tempDist = self.count_diagonal_length(pt,b)
				if tempDist<dist:
					dist = tempDist
					best = b 
		return best 
	
	def get_filename_and_folder_from_url(self, url, sep='/'):
		x= url.split(sep)
		return x[-1] , sep.join(x[:-1])
		
	def make_the_rectangle_bigger(self, x0,  y0, w,  h,  h2h0, w2w0, img_height,img_width, image_scale):
		h2 = int(h2h0*h)
		w2 = int(w2w0*w)
		y02 = y0 - int((h2h0-1)*h/2.0)
		x02 = x0 - int((w2w0-1)*w/2.0)
		if y02<0: y02=0
		if x02<0: x02=0
		if y02+h2 >=img_height: y02 = img_height -1
		if x02+w2 >=img_width: x02 = img_width -1
		x02 ,  y02 ,  w2,  h2 = int(x02 * image_scale),  int(y02 * image_scale), int(w2 * image_scale),  int(h2 * image_scale)
		return x02,  y02,  w2 ,  h2
		
	def sredni_punkt(self, p1,p2):
		x = int(p1[0]+p2[0])/2
		y = int(p2[1]+p2[1])/2
		return [x,y]
		
	def count_rotation_sin_and_cos(self,przeciwprostokatna,BCy,ACx):
		if przeciwprostokatna >0:
			cosAlfa = BCy/przeciwprostokatna
			sinAlfa = ACx/przeciwprostokatna
			#print "count_rotation_sin_and_cos" , cosAlfa**2 + sinAlfa**2
			alfa = math.asin(sinAlfa)
		else:
			sinAlfa =0
			cosAlfa =1
			alfa= 0
		return [alfa ,sinAlfa,cosAlfa]
		
	def count_matrix_center(self,matrix_url):
		matrix = cv.LoadImageM(matrix_url)
		return (matrix.width/2 , matrix.height/2)
		
	def count_diagonal_length(self, p1,p2):
		return math.sqrt((p1[0]-p2[0])**2 +(p1[1]-p2[1])**2)
		
	def rotate_vector(self, vector,sinBeta,cosBeta):
		x0,y0 = vector[0],vector[1]
		x = x0*cosBeta -y0*sinBeta
		y = x0*sinBeta +y0*cosBeta
		return [x,y]
		
	def rotatePointChangeCoordSystem(self, p0, angle, center,(xmin,ymin)):
		sin_cos= [math.sin(-angle),math.cos(-angle)]
		p0M= [p0[0]-xmin-center[0],p0[1]-ymin-center[1]]
		p0M=self.rotate_vector(p0M,sin_cos[0],sin_cos[1])
		p0M= [int(p0M[0]+center[0]),int(p0M[1]+center[1])]
		return p0M

	def get_vector(self, p0,pk):
		v = [pk[0]-p0[0],pk[1]-p0[1]]
		return v
		
	def getScalarProduct(self, v1, v2):
		return v1[0]*v2[0]+v1[1]*v2[1]
		
	def count_diagonal_length(self, p1,p2):
		return math.sqrt((p1[0]-p2[0])**2 +(p1[1]-p2[1])**2)
		
	def normalizeVector(self, vector):
		veclen = self.count_diagonal_length(vector,[0,0])
		if veclen>0:
			vector = [vector[0]/float(veclen),vector[1]/float(veclen)]
		return vector
		
	def rotateImage(self, image, angle, center = None):
		if center ==None:
			center = (image.shape[0]/2, image.shape[1]/2)
		height = image.shape[0]
		width = image.shape[1]
		rot_mat = cv2.getRotationMatrix2D(center,angle,1.0)
		result = cv2.warpAffine(image, rot_mat, (width, height),flags=cv2.INTER_LINEAR)
		return result
		
	def pasteImage(self, background, image, center):
		h= image.shape[1]
		w= image.shape[0]
		Sx= center[0]-w/2
		if Sx<0:Sx=0
		Sy= center[1]-h/2
		if Sy<0:Sy=0
		background[Sx:Sx+w , Sy:Sy+h] = image
		return background
	
	def make_linear_array(self,multi_array_dict ):
		normalItems =multi_array_dict.items()
		ReadyNitTupl=[]
		while normalItems !=[]:
			for item in normalItems:
				#if the item is not a dictionary
				if type(item[1])==type({}):
					normalItems = filter(lambda x: x!=item, normalItems) #usuwam element bedacy slownikiem
					items = self.make_tuples_from_dict(item)
					for it in items:
						normalItems.append(it)
				else:
					ReadyNitTupl.append(item)
				normalItems = filter(lambda x: x!=item, normalItems) #usuwam element nie bedacy slownikiem
		return ReadyNitTupl 
        
	def make_tuples_from_dict(self, tuple_with_dict, divider='#'):
		basickey = tuple_with_dict[0]
		items = tuple_with_dict[1].items()
		ret_array=[]
		for it in items:
			tot_key = basickey+divider+it[0]
			tup = (tot_key,  it[1])
			ret_array.append(tup)
		return ret_array
		
	def transformuj_punkty_liniowego_slownika(self, srodek_nowego_ukladu,plus_czy_minus, slownik,lista_kluczy=None):
		if lista_kluczy==None:
			lista_kluczy = slownik.keys()
		for key in lista_kluczy:
			typ_elementu = type(slownik[key][0])
			if typ_elementu==type(1.1) or typ_elementu==type(1) :
				slownik[key] = self.przyjmij_inny_uklad_wspolrzednych(slownik[key],srodek_nowego_ukladu,plus_czy_minus)
			elif typ_elementu==type([]) or typ_elementu==type([]):
				for i in range(len(slownik[key])):
					slownik[key][i] = self.przyjmij_inny_uklad_wspolrzednych(slownik[key][i],srodek_nowego_ukladu,plus_czy_minus)
		return slownik
		
	def przyjmij_inny_uklad_wspolrzednych(self, point, srodek_nowego_ukl,pORm):
		return (point[0]+srodek_nowego_ukl[0]*pORm ,point[1]+srodek_nowego_ukl[1]*pORm)
		
	#ponizsza funkcja nie jest uzywana ale szkoda ja wyrzucac :)
	def bgr2hsv(self,bgr):
		[blu,grn,red] = bgr
		x = min(min(red, grn), blu)
		val = max(max(red, grn), blu)
		if (x == val):
			hue=0
			sat=0
		else:
			if red == x:
				f = grn-blu
			else:
				if grn == x:
					f = blu-red
				else:
					f = red-grn
			if red == x:
				i = 3
			else:
				if grn == x:
					i = 5
				else:
					i = 1
			hue = ((i-f/(val-x))*60)%360
			sat = ((val-x)/val)
		return [hue,sat,val]
