import maya.mel as mel
import pymel.core as pm

import os.path

from tk_slots_maya_init import Init





class Edit(Init):
	def __init__(self, *args, **kwargs):
		super(Edit, self).__init__(*args, **kwargs)


		self.ui = self.sb.getUi('edit')




	def cmb000(self):
		'''
		Editors
		'''
		cmb = self.ui.cmb000
		
		files = ['Cleanup', 'Transfer: Attribute Values', 'Transfer: Shading Sets']
		contents = self.comboBox (cmb, files, '::')

		index = cmb.currentIndex()
		if index!=0:
			if index==contents.index('Cleanup'):
				mel.eval('CleanupPolygonOptions;')
			if index==contents.index('Transfer: Attribute Values'):
				mel.eval('TransferAttributeValuesOptions;')
				# mel.eval('performTransferAttributes 1;') #Transfer Attributes Options
			if index==contents.index('Transfer: Shading Sets'):
				mel.eval('performTransferShadingSets 1;')
			cmb.setCurrentIndex(0)


	def b000(self):
		'''
		Mesh Cleanup
		'''
		repair = self.ui.chk004.isChecked() #auto repair errors


		#Select components for cleanup from all visible geometry in the scene
		scene = pm.ls (visible=1, geometry=1)
		[pm.select (geometry, add=1) for geometry in scene]
		if repair: #auto repair errors
			mel.eval(r'polyCleanupArgList 4 { "0","1","1","0","1","0","1","0","0","1e-005","1","0.0001","0","1e-005","0","1","1","0" };')
		else:
			mel.eval(r'polyCleanupArgList 3 { "0","2","1","0","1","0","0","0","0","1e-005","1","1e-005","0","1e-005","0","1","1" };')

		if self.ui.chk002.isChecked(): #N-Sided Faces
			if repair: #Maya Bonus Tools: Convert N-Sided Faces To Quads
				mel.eval('bt_polyNSidedToQuad;')
			else: #Find And Select N-Gons
				#Change to Component mode to retain object highlighting for better visibility
				pm.changeSelectMode (component=1)
				#Change to Face Component Mode
				pm.selectType (smp=0, sme=1, smf=0, smu=0, pv=0, pe=1, pf=0, puv=0)
				#Select Object/s and Run Script to highlight N-Gons
				pm.polySelectConstraint (mode=3, type=0x0008, size=3)
				pm.polySelectConstraint (disable=1)
				#Populate an in-view message
				nGons = pm.polyEvaluate (faceComponent=1)
				self.viewPortMessage("<hl>"+str(nGons[0])+"</hl> N-Gon(s) found.")


	def b001(self):
		'''

		'''
		pass


	def b006(self):
		'''
		Delete History
		'''
		all_ = self.ui.chk018.isChecked()
		unusedNodes = self.ui.chk019.isChecked()
		deformers = self.ui.chk020.isChecked()
		objects = pm.ls (selection=1)
		if all_:
			objects = pm.ls (typ="mesh")

		for obj in objects:
			try:
				if all_:
					pm.delete (obj, constructionHistory=1)
				else:
					pm.bakePartialHistory (obj, prePostDeformers=1)
			except:
				pass
		if unusedNodes:
			mel.eval('hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes");')

		#display viewPort messages
		if all_:
			if deformers:
				self.viewPortMessage("delete <hl>all</hl> history.")
			else:
				self.viewPortMessage("delete <hl>all non-deformer</hl> history.")
		else:
			if deformers:
				self.viewPortMessage("delete history on "+str(objects))
			else:
				self.viewPortMessage("delete <hl>non-deformer</hl> history on "+str(objects))


	def b007(self):
		'''
		Delete 
		'''
		selectionMask = pm.selectMode (query=True, component=True)
		maskVertex = pm.selectType (query=True, vertex=True)
		maskEdge = pm.selectType (query=True, edge=True)
		maskFacet = pm.selectType (query=True, facet=True)

		objects = pm.ls(sl=1)
		
		for obj in objects:
			if pm.objectType(obj, isType='joint'):
				pm.removeJoint(obj) #remove joints

			elif pm.objectType(obj, isType='mesh'): 
				if all([selectionMask==1, maskEdge==1]):
					pm.polyDelEdge(cleanVertices=True) #delete edges

				elif all([selectionMask==1, maskVertex==1]):
					pm.polyDelVertex() #delete vertices

				else: #all([selectionMask==1, maskFacet==1]):
					pm.delete(obj) #delete faces\mesh objects
		
		self.viewPortMessage('Delete <hl>'+str(objects)+'</hl>.')


	def b009(self):
		'''
		Crease Set Transfer: Transform Node
		'''
		if self.ui.b043.isChecked():
			newObject = str(pm.ls(selection=1)) #ex. [nt.Transform(u'pSphere1')]

			index1 = newObject.find("u")
			index2 = newObject.find(")")
			newObject = newObject[index1+1:index2].strip("'") #ex. pSphere1

			if newObject != "[":
				self.ui.b043.setText(newObject)
			else:
				self.ui.b043.setText("must select obj first")
				self.setButtons(self.ui, unchecked='b043')
			if self.ui.b042.isChecked():
				self.setButtons(self.ui, enable='b052')
		else:
			self.ui.b043.setText("Object")


	def b010(self):
		'''
		Crease Set Transfer: Crease Set
		'''
		if self.ui.b042.isChecked():
			creaseSet = str(pm.ls(selection=1)) #ex. [nt.CreaseSet(u'creaseSet1')]

			index1 = creaseSet.find("u")
			index2 = creaseSet.find(")")
			creaseSet = creaseSet[index1+1:index2].strip("'") #ex. creaseSet1

			if creaseSet != "[":
				self.ui.b042.setText(creaseSet)
			else:
				self.ui.b042.setText("must select set first")
				self.setButtons(self.ui, unchecked='b042')
			if self.ui.b043.isChecked():
				self.setButtons(self.ui, enable='b052')
		else:
			self.ui.b042.setText("Crease Set")


	def b011(self):
		'''
		Transfer Crease Edges
		'''
		# an updated version of this is in the maya python projects folder
		# the use of separate buttons for donor and target mesh are obsolete
		# add pm.polySoftEdge (angle=0, constructionHistory=0); #harden edge, when applying crease
		
		creaseSet = str(self.ui.b042.text())
		newObject = str(self.ui.b043.text())

		sets = pm.sets (creaseSet, query=1)

		setArray = []
		for set_ in sets:
			name = str(set_)
			setArray.append(name)
		print setArray

		pm.undoInfo (openChunk=1)
		for set_ in setArray:
			oldObject = ''.join(set_.partition('.')[:1]) #ex. pSphereShape1 from pSphereShape1.e[260:299]
			pm.select (set_, replace=1)
			value = pm.polyCrease (query=1, value=1)[0]
			name = set_.replace(oldObject, newObject)
			pm.select (name, replace=1)
			pm.polyCrease (value=value, vertexValue=value, createHistory=True)
			# print "crease:", name
		pm.undoInfo (closeChunk=1)

		self.setButtons(self.ui, disable='b052', unchecked='b042')#,self.ui.b043])
		self.ui.b042.setText("Crease Set")
		# self.ui.b043.setText("Object")


	def b012(self):
		'''
		
		'''
		pass


	def b013(self):
		'''
		
		'''
		pass


	def b014(self):
		'''
		

		'''
		pass


	def b015(self):
		'''
		

		'''
		pass


	def b016(self):
		'''

		'''
		pass


	def b017(self):
		'''
		
		'''
		pass


	def b018(self):
		'''
		
		'''
		pass


	def b019(self):
		'''
		
		'''
		pass


	def b020(self):
		'''
		
		'''
		pass


	def b021(self):
		'''
		Tranfer Maps
		'''
		mel.eval('performSurfaceSampling 1;')


	def b022(self):
		'''
		Transfer Vertex Order
		'''
		mel.eval('TransferVertexOrder;')


	def b023(self):
		'''
		Transfer Attribute Values
		'''
		mel.eval('TransferAttributeValues;')


	def b024(self):
		'''

		'''
		pass


	def b025(self):
		'''

		'''
		pass


	def b026(self):
		'''
		
		'''
		pass


	def b027(self):
		'''
		Shading Sets
		'''
		mel.eval('performTransferShadingSets 0;')


	def b028(self):
		'''

		'''
		pass





#module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------
	# b008, b009, b011