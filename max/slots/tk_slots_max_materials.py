from tk_slots_max_init import *

from widgets.qLabel_ import QLabel_

import os.path



class Materials(Init):
	def __init__(self, *args, **kwargs):
		super(Materials, self).__init__(*args, **kwargs)

		self.currentMaterial=None
		self.materials=None
		self.randomMat=None


	# def cmb001(self, index=None):
	# 	'''
	# 	Editors
	# 	'''
	# 	cmb = self.parentUi.cmb001

	# 	files = ['Material Editor']
	# 	contents = cmb.addItems_(files, ' ')

	# 	if index is None:
	# 		index = cmb.currentIndex()
	# 	if index!=0:
	# 		if index==contents.index('Material Editor'):
	# 			maxEval('max mtledit')
	# 		cmb.setCurrentIndex(0)


	def cmb002(self, index=None):
		'''
		Material list

		args:
			index (int) = parameter on activated, currentIndexChanged, and highlighted signals.
		'''
		cmb = self.parentUi.cmb002

		if not cmb.initialized:
			cmb.addToContext(QLabel_(), setText='Open in Editor', setObjectName='lbl000', setToolTip='Open material in editor.')
			cmb.addToContext(QLabel_(), setText='Rename', setObjectName='lbl001', setToolTip='Rename material')
			cmb.addToContext(QLabel_(), setText='Delete', setObjectName='lbl002', setToolTip='Delete the current material.')
			cmb.addToContext(QLabel_(), setText='Delete All Unused Materials', setObjectName='lbl003', setToolTip='Delete All unused materials.')
			cmb.addToContext(QLabel_(), setText='Refresh', setObjectName='cmb002', setToolTip='Refresh materials list')

		if cmb.lineEdit():
			self.renameMaterial()
			return

		try:
			sceneMaterials = self.parentUi.tb001.chk000.isChecked()
			idMapMaterials = self.parentUi.tb001.chk001.isChecked()
		except: #if the toolbox hasn't been built yet: default to sceneMaterials
			sceneMaterials = True

		if sceneMaterials:
			materials=[] #get any scene material that does not start with 'Material'
			for mat in rt.sceneMaterials:
				try:
					if rt.getNumSubMtls(mat): #if material is a submaterial; search submaterials
						for i in range(1, rt.getNumSubMtls(mat)+1):
							subMat = rt.getSubMtl(mat, i)
							if subMat and not subMat.name.startswith('Material'):
								materials.append(subMat)
					elif not mat.name.startswith('Material'):
						materials.append(mat)

				except RuntimeError:
					pass

		elif idMapMaterials:
			materials=[] #get any scene material that startswith 'matID'
			for mat in rt.sceneMaterials:
				if rt.getNumSubMtls(mat): #if material is a submaterial; search submaterials
					for i in range(1, rt.getNumSubMtls(mat)+1):
						subMat = rt.getSubMtl(mat, i)
						if subMat.name.startswith('matID'):
							materials.append(subMat)
				elif mat.name.startswith('matID'):
					materials.append(mat)

		mats = sorted([mat for mat in set(materials)])
		matNames = [mat.name for mat in mats]
		contents = cmb.addItems_(matNames)

		#create and set icons with color swatch
		for i in range(len(mats)): #create icons with color swatch
			r = int(mats[i].diffuse.r) #convert from float value
			g = int(mats[i].diffuse.g)
			b = int(mats[i].diffuse.b)
			pixmap = QtGui.QPixmap(100,100)
			pixmap.fill(QtGui.QColor.fromRgb(r, g, b))
			cmb.setItemIcon(i, QtGui.QIcon(pixmap))

		if index is None:
			index = cmb.currentIndex()

		self.materials = {name:mats[i] for i, name in enumerate(matNames)} #add mat objects to materials dictionary. 'mat name'=key, <mat object>=value
		self.currentMaterial = mats[index] if len(mats)>index and index>=0 else None #store material


	def tb000(self, state=None):
		'''
		Select By Material Id
		'''
		tb = self.currentUi.tb000
		if state=='setMenu':
			tb.add('QRadioButton', setText='Shell', setObjectName='chk005', setToolTip='Select entire shell.')
			tb.add('QRadioButton', setText='Invert', setObjectName='chk006', setToolTip='Invert Selection.')
			return

		shell = tb.chk005.isChecked() #Select by material: shell
		invert = tb.chk006.isChecked() #Select by material: invert

		if not rt.getNumSubMtls(self.currentMaterial): #if not a multimaterial
			mat = self.currentMaterial
		else:
			return '# Error: No valid stored material. If material is a multimaterial, select a submaterial. #'

		sel = rt.selection
		if not sel: #if not selection; use all scene geometry
			sel = rt.geometry

		for obj in sel:
			if shell: #set to base object level
				rt.modPanel.setCurrentObject(obj.baseObject)
			else: #set object level to face
				self.setSubObjectLevel(4)
			m = obj.material
			multimaterial = rt.getNumSubMtls(m)

			same=[] #list of faces with the same material
			other=[] #list of all other faces

			faces = list(range(1, obj.faces.count))
			for f in faces:
				if multimaterial:
					id = obj.GetFaceMaterial(f) #Returns the material ID of the specified face.
					m = rt.getSubMtl(m, id) #get the material using the matID index

				if m==mat:
					if shell: #append obj to same and break loop
						same.append(obj)
						break
					else: #append face ID to same
						same.append(f)
				else:
					if shell: #append obj to other and break loop
						other.append(obj)
						break
					else: #append face ID to other
						other.append(f)

			if shell:
				if invert:
					(rt.select(i) for i in other)
				else:
					(rt.select(i) for i in same)
			else:
				if invert:
					rt.polyop.setFaceSelection(obj, other) #select the faces
				else:
					rt.polyop.setFaceSelection(obj, same) #select the faces
			# print same
			# print other


	def tb001(self, state=None):
		'''
		Stored Material Options
		'''
		tb = self.currentUi.tb001
		if state=='setMenu':
			tb.add('QRadioButton', setText='All Scene Materials', setObjectName='chk000', setChecked=True, setToolTip='List all scene materials.') #Material mode: Stored Materials
			tb.add('QRadioButton', setText='ID Map Materials', setObjectName='chk001', setToolTip='List ID map materials.') #Material mode: ID Map Materials

			self.connect_([tb.chk000, tb.chk001], 'toggled', [self.cmb002, self.tb001])
			return

		if tb.chk000.isChecked():
			self.parentUi.group000.setTitle(tb.chk000.text())
		elif tb.chk001.isChecked():
			self.parentUi.group000.setTitle(tb.chk001.text())


	def tb002(self, state=None):
		'''
		Assign Material
		'''
		tb = self.currentUi.tb002
		if state=='setMenu':
			tb.add('QRadioButton', setText='Current Material', setObjectName='chk007', setChecked=True, setToolTip='Re-Assign the current stored material.')
			tb.add('QRadioButton', setText='New Random Material', setObjectName='chk008', setToolTip='Assign a new random ID material.')
			return


		if tb.chk008.isChecked(): #Assign New random mat ID
			import random

			selection = rt.selection

			if selection:
				prefix = 'matID'
				rgb = [random.randint(0, 255) for _ in range(3)] #generate a list containing 3 values between 0-255

				#format name
				name = '_'.join([prefix, str(rgb[0]), str(rgb[1]), str(rgb[2])])
				#create shader
				mat = rt.StandardMaterial()
		 		mat.name = name
				mat.diffuse = rt.color(rgb[0], rgb[1], rgb[2])

				for obj in selection:
					obj.material = mat

				#delete previous shader
				if self.randomMat:
					self.randomMat = None #replace with standard material

				self.randomMat = mat

				if self.parentUi.tb001.chk001.isChecked():
					self.cmb002() #refresh the combobox
				else:
					self.parentUi.tb001.chk001.setChecked(True) #set combobox to ID map mode. toggling the checkbox refreshes the combobox.
				self.parentUi.cmb002.setCurrent_(name) #set the combobox index to the new mat #self.cmb002.setCurrentIndex(self.cmb002.findText(name))
			else:
				return '# Error: No valid object/s selected. #'

		elif tb.chk007.isChecked(): #Assign current mat
			name = self.parentUi.cmb002.currentText()
			mat = self.materials[name]

			for obj in rt.selection:
				if rt.getNumSubMtls(mat): #if multimaterial
					mat.materialList.count = mat.numsubs+1 #add slot to multimaterial
					mat.materialList[-1] = material #assign new material to slot
				else:
					obj.material = mat

			rt.redrawViews()


	def lbl000(self):
		'''
		Open material in editor
		'''
		if self.parentUi.tb001.chk001.isChecked(): #ID map mode
			try:
				mat = self.materials[self.parentUi.cmb002.currentText()] #get object from string key
			except:
				return '# Error: No stored material or no valid object selected. #'
		else: #Stored material mode
			if not self.currentMaterial: #get material from selected scene object
				if rt.selection:
					self.currentMaterial = rt.selection[0].material
				else:
					return '# Error: No stored material or no valid object selected. #'
			mat = self.currentMaterial

		#open the slate material editor
		if not rt.SME.isOpen():
			rt.SME.open()

		#create a temp view in the material editor
		if rt.SME.GetViewByName('temp'):
			rt.SME.DeleteView(rt.SME.GetViewByName('temp'), False)
		index = rt.SME.CreateView('temp')
		view = rt.SME.GetView(index)

		#show node and corresponding parameter rollout
		node = view.CreateNode(mat, rt.point2(0, 0))
		rt.SME.SetMtlInParamEditor(mat)

		rt.redrawViews()


	def renameMaterial(self):
		'''
		Rename Material
		'''
		cmb = self.parentUi.cmb002 #scene materials
		newMatName = cmb.currentText()

		if self.currentMaterial and self.currentMaterial.name!=newMatName:
			if self.parentUi.tb001.chk001.isChecked(): #Rename ID map Material
				prefix = 'matID_'
				if not newMatName.startswith(prefix):
					newMatName = prefix+newMatName

			cmb.setItemText(cmb.currentIndex(), newMatName)
			try:
				self.currentMaterial.name = newMatName
			except RuntimeError as error:
				cmb.setItemText(cmb.currentIndex(), str(error.strip('\n')))

		#re-enable widgets
		self.lbl001(setEditable=False)


	def lbl001(self, setEditable=True):
		'''
		Rename Material: Set cmb002 as editable and disable widgets.
		'''
		if setEditable:
			self.parentUi.cmb002.setEditable(True)
			# self.parentUi.cmb002.lineEdit().returnPressed.connect(self.renameMaterial)
			self.toggleWidgets(self.parentUi, setDisabled='b002,lbl000,tb000,tb002')
		else:
			self.parentUi.cmb002.setEditable(False)
			self.toggleWidgets(self.parentUi, setEnabled='b002,lbl000,tb000,tb002')


	def lbl002(self):
		'''
		Delete Material
		'''
		mat = self.currentMaterial
		mat = rt.Standard(name="Default Material") #replace with standard material

		self.currentMaterial = None

		index = self.parentUi.cmb002.currentIndex()
		self.parentUi.cmb002.setItemText(index, mat.name) #self.parentUi.cmb002.removeItem(index)


	def lbl003(self):
		'''
		Delete Unused Materials
		'''
		defaultMaterial = rt.Standard(name='Default Material')
		
		for mat in rt.sceneMaterials:
			nodes = rt.refs().dependentnodes(mat) 
			if nodes.count==0:
				rt.replaceinstances(mat, defaultMaterial)
				
			rt.gc()
			rt.freeSceneBitmaps()


	def b002(self):
		'''
		Store Material: Store the Currently Selected Material
		'''
		try: 
			obj = rt.selection[0]
		except:
			return '# Error: Nothing selected. #'

		mat = obj.material #get material from selection

		if rt.subObjectLevel == 4: #if face selection check for multimaterial
			if rt.getNumSubMtls(mat): #if multimaterial; use selected face to get material ID
				f = rt.bitArrayToArray(rt.getFaceSelection(obj))[0] #get selected faces
				id_ = obj.GetFaceMaterial(f) #Returns the material ID of the specified face.
				mat = rt.getSubMtl(mat, id_) #get material from mat ID

		self.currentMaterial = mat #store material
		self.parentUi.tb001.chk000.setChecked(True) #put combobox in current material mode
		self.cmb002() #refresh the combobox









#module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------


# deprecated


# elif storedMaterial:
# 	mat = self.currentMaterial
# 	if not mat:
# 		cmb.addItems_(['Stored Material: None'])
# 		return

# 	matName = mat.name
	
# 	subMaterials = [rt.getSubMtl(mat, i) for i in range(1, rt.getNumSubMtls(mat)+1)] #get the material using the matID index. modify index range for index starting at 1.
# 	subMatNames = [s.name for s in subMaterials if s is not None]
	
# 	contents = cmb.addItems_(subMatNames, matName)

# 	if index is None:
# 		index = cmb.currentIndex()
# 	if index!=0:
# 		self.currentMaterial = subMaterials[index-1]
# 	else:
# 		self.currentMaterial = mat



	# def cmb000(self, index=None):
	# 	'''
	# 	Existing Materials
	# 	'''
	# 	cmb = self.parentUi.cmb000

	# 	self.parentUi.tb001.chk001.setChecked(False) #put combobox cmb002 in stored material mode.

	# 	# materials = [mat for mat in rt.sceneMaterials if 'Multimaterial' not in mat.name and 'BlendMtl' not in mat.name and not mat.name.startswith('Material')]
	# 	materials=[] #get any scene material that doesnt startswith 'Material'
	# 	for mat in rt.sceneMaterials:
	# 		try:
	# 			if rt.getNumSubMtls(mat): #if material is a submaterial; search submaterials
	# 				for i in range(1, rt.getNumSubMtls(mat)+1):
	# 					subMat = rt.getSubMtl(mat, i)
	# 					if subMat and not subMat.name.startswith('Material'):
	# 						materials.append(subMat)
	# 			elif not mat.name.startswith('Material'):
	# 				materials.append(mat)

	# 		except RuntimeError:
	# 			pass

	# 	materialNames = sorted([mat.name for mat in materials])
		
	# 	contents = cmb.addItems_(materialNames, 'Scene Materials:')

	# 	if index is None:
	# 		index = cmb.currentIndex()
	# 	if index!=0:
	# 		mat = [m for m in materials if m.name==contents[index]][0]

	# 		self.currentMaterial = mat #store material
	# 		self.cmb002() #refresh combobox

	# 		cmb.setCurrentIndex(0)

