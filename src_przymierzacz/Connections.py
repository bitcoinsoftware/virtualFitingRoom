from PyQt4 import QtCore, QtGui
from Connections import *
from pozycjoner2 import *
import pickle
class Connections:
	def connect(self):
		print "connect"
		QtCore.QObject.connect(self.pushButton,QtCore.SIGNAL('clicked()'),self.wyodrebnij_kontury)
		QtCore.QObject.connect(self.pushButton_5,QtCore.SIGNAL('clicked()'),self.wyswietl_argumenty)
		QtCore.QObject.connect(self.pushButton_2,QtCore.SIGNAL('clicked()'),self.rozpoznaj_czesci_ciala)
		QtCore.QObject.connect(self.pushButton_3,QtCore.SIGNAL('clicked()'),self.przymierz_ubranie)
		QtCore.QObject.connect(self.pushButton_4,QtCore.SIGNAL('clicked()'),self.wyodrebnij_postac)
        
		self.kurlcomborequester.setText("../postacie/woman0/input.jpg")
		self.kurlcomborequester_2.setText("../postacie/woman0/bg.jpg")
		#self.kurlcomborequester_3.setText("/home/gimbo/Desktop/koniu/ubrania/top/krotki_rekaw/hmprod5.png/hmprod5.png")
		self.kurlcomborequester_3.setText("../ubrania/plaszcze/hmprod4.png")
		#self.kurlcomborequester_3.setText("../ubrania/sukienka/bez_rekawu/hmprod.png/hmprod.png")
		self.kurlcomborequester_4.setText("../postacie/woman0/body.pickle")
		self.bd=None
        
	def wyswietl_argumenty(self):
		url = self.kurlcomborequester.text()
		urlbg =self.kurlcomborequester_2.text()
		self.display_photo(url,  self.graphicsView)
		self.display_photo(urlbg,  self.graphicsView_4)
        
	def wyodrebnij_kontury(self):
		url = str(self.kurlcomborequester.text())
		urlbg =str(self.kurlcomborequester_2.text())
		self.pzcr = pozycjoner2()
		self.face = self.pzcr.find_if_there_is_a_face(url)
		if self.face[0]:
			face_center = self.face[0]
			self.out_bdr_url = 'test/brdrs.png'
			self.out_prprd_url = 'test/prepared_photo.png'
			borders = Borders(url, urlbg, self.out_bdr_url ,self.out_prprd_url, face_center)
			self.display_photo(self.out_bdr_url,  self.graphicsView_2)
			self.display_photo(self.out_prprd_url ,  self.graphicsView_3)
        
	def wyodrebnij_postac(self):
		url = str(self.kurlcomborequester.text())
		urlbg =str(self.kurlcomborequester_2.text())
		self.pzcr = pozycjoner2()
		self.face = self.pzcr.find_if_there_is_a_face(url)
		if self.face[0]:
			face_center = self.face[0]
			self.out_bdr_url = 'test/brdrs.png'
			self.out_prprd_url = 'test/prepared_photo.png'
			borders = Borders(url, urlbg, self.out_bdr_url ,self.out_prprd_url, face_center)
			u_out='test/wyodrebnione.jpg'
			urlout = borders.get_only_body(u_out)
		self.display_photo(urlout  ,  self.graphicsView_3)

	def przymierz_ubranie(self):
		print "przymierz_ubranie"
		if self.bd==None:
			self.bd = pickle.loads(open(str(self.kurlcomborequester_4.text())).read())
		cloath_url = str(self.kurlcomborequester_3.text())
		o_url = "test/o_url.jpg"
		if cloath_url.find('trousersLong')>-1:
			print 'trousersLong' , cloath_url.find('trousersLong')
			spodnie = trousersLong(self.bd,cloath_url)
			spodnie.paste_cloath(str(self.kurlcomborequester.text()),o_url)
		if cloath_url.find('trousersShort')>-1:
			spodnie = trousersShort(self.bd,cloath_url)
			spodnie.paste_cloath(str(self.kurlcomborequester.text()),o_url)
		elif cloath_url.find('coat')>-1:
			plaszcz =Coat(self.bd,cloath_url)
			plaszcz.paste_cloath(str(self.kurlcomborequester.text()),o_url)
			#self.pzcr.rysuj_slownik_punktow(o_url, plaszcz.punktyUbrania, o_url)
		elif cloath_url.find('pants')>-1:
			pants = Pants(self.bd,cloath_url)
			pants.paste_cloath(str(self.kurlcomborequester.text()),o_url)
		elif cloath_url.find('skirt')>-1:
			print "SPODNICA"
			spodnica = Skirt(self.bd,cloath_url)
			spodnica.paste_cloath(str(self.kurlcomborequester.text()),o_url)
		elif cloath_url.find('topX')>-1:
			top =Top(self.bd,cloath_url)
			top.paste_cloath(str(self.kurlcomborequester.text()),o_url)
		elif cloath_url.find('biustonosze')>-1:
			pass
		elif cloath_url.find('jacket')>-1:
			jacket = Jacket(self.bd,cloath_url)
			jacket.paste_cloath(str(self.kurlcomborequester.text()),o_url)
		elif cloath_url.find('dressNoSleeve')>-1:
			print "dressNoSleeve"
			dress = DressNoSleve(self.bd, cloath_url)
			dress.paste_cloath(str(self.kurlcomborequester.text()),o_url)
		else:
			print "ELSE"
        
		self.display_photo(o_url,  self.graphicsView_2)
		self.display_photo(cloath_url,  self.graphicsView_3)
        
	def rozpoznaj_czesci_ciala(self):
		self.bd = Body(self.face,  self.out_bdr_url)
		outUrl = 'test/body_parts.png'
		self.pzcr.rysuj_punkty_ciala(str(self.kurlcomborequester.text()), self.bd.body, outUrl)
		self.display_photo(outUrl,  self.graphicsView_2)
		f = open('test/body.pickle','w')
		f.write(pickle.dumps(self.bd))
		f.close()
    
	def display_photo(self, url, graphicsView):
		self.graphic_scene = QGraphicsScene2((1),graphicsView)
		graphicsView.setScene(self.graphic_scene)
		qpixmap = QtGui.QPixmap(url)
		self.graphic_scene.set_display_widget(graphicsView,qpixmap.width(),qpixmap.height())
		print url	
		size = graphicsView.size()
		self.width,  self.height = size.width(),  size.height()
		#Jesli zdjecie mniejsze od rozmiarow display
		if qpixmap.width()<self.width:
			self.graphic_scene.x_move = (self.width- qpixmap.width())/2
		if qpixmap.height()<self.height:
			self.graphic_scene.y_move = (self.height- qpixmap.height())/2
		#Jesli zdjecie wieksze od rozmiarow display
		if qpixmap.width()>self.width:
			print "PRZESKALOWANE"
			self.graphic_scene.skala_zdjecia = self.width/float(qpixmap.width())
			item =QtGui.QGraphicsPixmapItem(QtGui.QPixmap(url).scaledToWidth(self.width))
			self.qpixmap_width = int(qpixmap.width()*self.graphic_scene.skala_zdjecia)
			self.qpixmap_height = int(qpixmap.height()*self.graphic_scene.skala_zdjecia) 
			if self.qpixmap_height<self.height:
				self.graphic_scene.y_move = (self.height- self.qpixmap_height)/2         
		else:
			item =QtGui.QGraphicsPixmapItem(QtGui.QPixmap(url))        
		self.graphic_scene.addItem(item)
		graphicsView.show()


class QGraphicsScene2(QtGui.QGraphicsScene):
	def __init__(self,status, parent=None,TODO_pointer=None):
		self.status = status   # decyduje czy robic kolka czy kwadraty
		self.TODO = TODO_pointer
		super(QGraphicsScene2, self).__init__(parent)
        
	def set_display_widget(self, display, heigth, width):
		self.ROI = [-1,-1,-1,-1]
		self.heigth = heigth 
		self.width=width
		self.display = display
		self.pointsx=[]
		self.pointsy=[]
		self.x_move=0
		self.y_move=0
		self.skala_zdjecia=1.0
	
	def mouseReleaseEvent(self, event):
		button = event.button()
		#if self.active_listwidget=1:
		sk = self.skala_zdjecia
		if button == 1 and not self.status:
			point = self.display.mapFromGlobal(QtGui.QCursor.pos())
			print 'SIMPLE LEFT CLICK' , self.display.pos()
			self.pointsx.append((point.x()-self.x_move)) 
			self.pointsy.append((point.y()-self.y_move))
			#rysowanie kolek na granicach zaznaczenia
			self.addEllipse(point.x()-self.x_move,point.y()-self.y_move,6,6, QtCore.Qt.blue, QtGui.QBrush(QtCore.Qt.red))

			if len(self.pointsx)==2:
				self.pointsx=sorted(self.pointsx)
				self.pointsy=sorted(self.pointsy)
				rect_width = abs(self.pointsx[0]-self.pointsx[1])
				rect_heigth = abs(self.pointsy[0]-self.pointsy[1])
				self.addRect(self.pointsx[0],self.pointsy[0],rect_width, rect_heigth, QtCore.Qt.blue)
                
				self.ROI = [int(self.pointsx[0]/sk),int(self.pointsy[0]/sk),int(rect_width/sk), int(rect_heigth/sk)]
				i=0
				for wsp in self.ROI:
					if self.ROI[i] <0:
						self.ROI[i] =0
					i=i+1
               
				if (self.ROI[0]+self.ROI[2]) > self.width:
					self.ROI[2]=self.width-self.ROI[0]
				if (self.ROI[1]+self.ROI[3]) > self.heigth:
					self.ROI[3] = self.heigth - self.ROI[1]
				print self.ROI
                
			if len(self.pointsx)==3:
				item_list=self.items()
				ilosc_obiektow = len(item_list)
				for i in range(ilosc_obiektow-2):
					self.removeItem(self.items().pop(1))
				tempx=self.pointsx[2]
				tempy=self.pointsy[2]
				self.pointsx=[]
				self.pointsy=[]
				self.pointsx.append(tempx)
				self.pointsy.append(tempy)
                
		if button == 1 and self.status:  # jak zaznaczony radiobutt imbalance i subwidget aktywna
			point = self.display.mapFromGlobal(QtGui.QCursor.pos())
			self.addEllipse(point.x()-self.x_move,point.y()-self.y_move,6,6, QtCore.Qt.blue, QtGui.QBrush(QtCore.Qt.blue))
			#przekazuje wskaznik do funkcji i wywoluje ja z argumentami (point.x()-self.x_move,point.y()-self.y_move)
			self.TODO((point.x()-self.x_move),(point.y()-self.y_move))
	
	def mousePressEvent(self, event):
		button = event.button()
		if button == 1:
			print 'LEFT CLICK - DRAG'
		if button == 2:
			print 'RIGHT CLICK'
			item_list=self.items()
			ilosc_obiektow = len(item_list)
			for i in range(ilosc_obiektow-1):
				self.removeItem(self.items().pop(0))
			self.pointsx=[]
			self.pointsy=[]
