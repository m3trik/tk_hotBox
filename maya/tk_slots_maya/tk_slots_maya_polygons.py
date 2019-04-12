import maya.mel as mel
import pymel.core as pm

import os.path

from tk_slots_maya_init import Init





class Polygons(Init):
	def __init__(self, *args, **kwargs):
		super(Polygons, self).__init__(*args, **kwargs)




	def chk002(self):
		'''
		Un-Crease

		'''
		if self.hotBox.ui.chk002.isChecked():
			self.hotBox.ui.s003.setValue(0) #crease value
			self.hotBox.ui.s004.setValue(180) #normal angle
			self.setButtons(self.hotBox.ui, unchecked='chk003')
		else:
			self.hotBox.ui.s003.setValue(7.5) #crease value
			self.hotBox.ui.s004.setValue(30) #normal angle

	def chk003(self):
		'''
		Crease: Max

		'''
		if self.hotBox.ui.chk003.isChecked():
			self.hotBox.ui.s003.setValue(10) #crease value
			self.hotBox.ui.s004.setValue(30) #normal angle
			self.setButtons(self.hotBox.ui, unchecked='chk002')
		else:
			self.hotBox.ui.s003.setValue(7.5) #crease value
			self.hotBox.ui.s004.setValue(60) #normal angle

	def chk006(self):
		'''
		Merge: All

		'''
		if self.hotBox.ui.chk006.isChecked():
			self.hotBox.ui.s002.setSingleStep(.01)
		else:
			self.hotBox.ui.s002.setSingleStep(.5)

	def chk008(self):
		'''
		Split U

		'''
		self.setButtons(self.hotBox.ui, unchecked='chk010')

	def chk009(self):
		'''
		Split V

		'''
		self.setButtons(self.hotBox.ui, unchecked='chk010')

	def chk010(self):
		'''
		Tris

		'''
		self.setButtons(self.hotBox.ui, unchecked='chk008,chk009')

	def chk011(self):
		'''
		Crease: Auto

		'''
		if self.hotBox.ui.chk011.isChecked():
			self.setButtons(self.hotBox.ui, enabled='s005,s006')
		else:
			self.setButtons(self.hotBox.ui, disabled='s005,s006')


	def b000(self):
		'''
		Merge Vertex Options

		'''
		mel.eval('PolyMergeOptions;')

	def b001(self):
		'''
		Fill Holes

		'''
		mel.eval('FillHole;')

	def b002(self):
		'''
		Separate

		'''
		mel.eval('SeparatePolygon;')

	def b003(self):
		'''
		Combine

		'''
		# pm.polyUnite( 'plg1', 'plg2', 'plg3', name='result' ) #for future reference. if more functionality is needed use polyUnite
		if self.hotBox.ui.chk000.isChecked():
			mel.eval('bt_mergeCombineMeshes;')
		else:
			mel.eval('CombinePolygons;')

	def b004(self):
		'''
		

		'''
		pass
		
	def b005(self):
		'''
		Bridge

		'''
		mel.eval('polyBridgeEdge -divisions 0;')

	def b006(self):
		'''
		Extrude

		'''
		mel.eval('PolyExtrude;')

	def b007(self):
		'''
		Bevel Chamfer

		'''
		width = float(self.hotBox.ui.s000.value())
		chamfer = True
		pm.polyBevel3 (fraction=width, offsetAsFraction=1, autoFit=1, depth=1, mitering=0, 
			miterAlong=0, chamfer=chamfer, segments=1, worldSpace=1, smoothingAngle=30, subdivideNgons=1,
			mergeVertices=1, mergeVertexTolerance=0.0001, miteringAngle=180, angleTolerance=180, ch=0)

	def b008(self):
		'''
		

		'''
		pass

	def b009(self):
		'''
		Collapse Component

		'''
		mel.eval('PolygonCollapse;')

	def b010(self):
		'''
		Extract Curve

		'''
		# mel.eval('CreateCurveFromPoly;')
		pm.polyToCurve (form=2, degree=3, conformToSmoothMeshPreview=True) #degree: 1=linear,2= ,3=cubic,5= ,7=

	def b011(self):
		'''
		Extract Curve Options

		'''
		mel.eval('CreateCurveFromPolyOptions;')

	def b012(self):
		'''
		Multi-Cut Tool

		'''
		mel.eval('dR_multiCutTool;')

	def b013(self):
		'''
		Combine Polygon Options

		'''
		mel.eval('CombinePolygonsOptions;')

	def b014(self):
		'''
		 Bevel Options

		'''
		mel.eval('BevelPolygonOptions;')

	def b015(self):
		'''
		Delete Edgeloop

		'''
		mel.eval("bt_polyDeleteEdgeLoopTool;")

	def b016(self):
		'''
		Inset Face Region

		'''
		offset = float(self.hotBox.ui.s001.value())
		pm.polyExtrudeFacet (keepFacesTogether=1, pvx=0, pvy=40.55638003, pvz=33.53797107, divisions=1, twist=0, taper=1, offset=offset, thickness=0, smoothingAngle=30)

	def b017(self):
		'''
		Bridge Options

		'''
		mel.eval("BridgeEdgeOptions;")

	def b018(self):
		'''
		Extrude Options

		'''
		mel.eval("PolyExtrudeOptions;")

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
		Connect Border Edges

		'''
		mel.eval("performPolyConnectBorders 0;")

	def b022(self):
		'''
		Attach

		'''
		mel.eval("dR_connectTool;")

	def b023(self):
		'''
		Boolean

		'''
		mel.eval("PolygonBooleanUnion;")

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
		

		'''
		pass

	def b028(self):
		'''
		Quad Draw

		'''
		mel.eval("dR_quadDrawTool;")

	def b029(self):
		'''
		Divide Facet

		'''
		dv=u=v=0
		if self.hotBox.ui.chk008.isChecked(): #Split U
			u=2
		if self.hotBox.ui.chk009.isChecked(): #Split V
			v=2

		mode = 0 #The subdivision mode. 0=quads, 1=triangles
		subdMethod = 1 #subdivision type: 0=exponential(traditional subdivision) 1=linear(number of faces per edge grows linearly)
		if self.hotBox.ui.chk010.isChecked(): #tris
			mode=dv=1
			subdMethod=0
		if all([self.hotBox.ui.chk008.isChecked(), self.hotBox.ui.chk009.isChecked()]): #subdivide once into quads
			dv=1
			subdMethod=0
			u=v=0
		#perform operation
		selectedFaces = pm.filterExpand (pm.ls(sl=1), selectionMask=34, expand=1)
		if selectedFaces:
			for face in selectedFaces: #when performing polySubdivideFacet on multiple faces, adjacent subdivided faces will make the next face an n-gon and therefore not able to be subdivided. 
				pm.polySubdivideFacet (face, divisions=0, divisionsU=2, divisionsV=2, mode=0, subdMethod=1)
		else:
			print '# Warning: No faces selected. #'

	def b030(self):
		'''
		

		'''
		pass

	def b031(self):
		'''
		

		'''
		pass

	def b032(self):
		'''
		Poke

		'''
		mel.eval("PokePolygon;")

	def b033(self):
		'''
		Poke Options

		'''
		mel.eval("PokePolygonOptions;")

	def b034(self):
		'''
		Wedge

		'''
		mel.eval("WedgePolygon;")

	def b035(self):
		'''
		Wedge Options

		'''
		mel.eval("WedgePolygonOptions;")

	def b036(self):
		'''
		

		'''
		pass

	def b037(self):
		'''
		

		'''
		pass

	def b038(self):
		'''
		Assign Invisible

		'''
		mel.eval("polyHole -assignHole 1;")

	def b039(self):
		'''
		Assign Invisible Options

		'''
		mel.eval("PolyAssignSubdivHoleOptions;")

	def b040(self):
		'''
		Merge All

		'''
		floatXYZ = float(self.hotBox.ui.s002.value())
		mergeAll = self.hotBox.ui.chk006.isChecked()

		selection = pm.ls(selection=1, objectsOnly=1)

		if len(selection)<1:
			print "// Warning: No object selected. Must select an object or component"
			return

		if mergeAll:
			for obj in selection:
				# get number of vertices
				count = pm.polyEvaluate(obj, vertex=1)
				vertices = str(obj) + ".vtx [0:" + str(count) + "]" # mel expression: select -r geometry.vtx[0:1135];
				pm.polyMergeVertex(vertices, distance=floatXYZ, alwaysMergeTwoVertices=False, constructionHistory=False)

			#return to original state
			pm.select(clear=1)
			for obj in selection:
				pm.select(obj, add=1)
		else:
			if pm.filterExpand(selectionMask=31): #returns True if selectionMask=vertices
				pm.polyMergeVertex(distance=floatXYZ, alwaysMergeTwoVertices=True, constructionHistory=True)
			else: #if selection type =edges or facets:
				mel.eval("MergeToCenter;")

	def b041(self):
		'''
		

		'''
		pass

	def b042(self):
		'''
		

		'''
		pass

	def b043(self):
		'''
		Target Weld

		'''
		mel.eval("dR_targetWeldTool;")

		#max method:
		# for obj in rt.selection:
		# 	vertexNum = [i.index for i in obj.selectedVerts]
		# 	target = rt.polyOp.getVert(obj, index[-1])
			
		# 	for vNum in vertexNum:
		# 		rt.polyop.weldVerts (obj, vertexNum[0], vNum, target)

	def b044(self):
		'''
		Detach

		'''
		vertexMask = pm.selectType (query=True, vertex=True)
		edgeMask = pm.selectType (query=True, edge=True)
		facetMask = pm.selectType (query=True, facet=True)

		if vertexMask:
			mel.eval("polySplitVertex()")

		if facetMask:
			maskVertex = pm.selectType (query=True, vertex=True)
			if maskVertex:
				mel.eval("DetachComponent;")
			else:
				selFace = pm.ls (ni=1, sl=1)
				selObj = pm.ls (objectsOnly=1, noIntermediate=1, sl=1) #to errorcheck if more than 1 obj selected

				if len(selFace) < 1:
					print "// Warning: Nothing selected. //"
					return
				if len(selObj) > 1:
					print "// Warning: Only components from a single object can be extracted. //"
					return
				else:
					pm.undoInfo (openChunk=1)
					sel = str(selFace[0]).split(".") #creates ex. ['polyShape', 'f[553]']
					print sel
					extractedObject = "extracted_"+sel[0]
					pm.duplicate (sel[0], name=extractedObject)
					if self.hotBox.ui.chk007.isChecked(): #delete original
						pm.delete (selFace)

					allFace = [] #populate a list of all faces in the duplicated object
					numFaces = pm.polyEvaluate(extractedObject, face=1)
					num=0
					for _ in range(numFaces):
						allFace.append(extractedObject+".f["+str(num)+"]")
						num+=1

					extFace = [] #faces to keep
					for face in selFace:
						fNum = str(face.split(".")[0]) #ex. f[4]
						extFace.append(extractedObject+"."+fNum)

					delFace = [x for x in allFace if x not in extFace] #all faces not in extFace
					pm.delete (delFace)

					pm.select (extractedObject)
					pm.xform (cpc=1) #center pivot
					pm.undoInfo (closeChunk=1)
					return extractedObject

	def b045(self):
		'''
		Re-Order Vertices

		'''
		symmetryOn = pm.symmetricModelling(query=True, symmetry=True) #query symmetry state
		if symmetryOn:
			pm.symmetricModelling(symmetry=False)
		mel.eval("setPolygonDisplaySettings(\"vertIDs\");") #set vertex id on
		mel.eval("doBakeNonDefHistory( 1, {\"pre\"});") #history must be deleted
		mel.eval("performPolyReorderVertex;") #start vertex reorder ctx

	def b046(self):
		'''
		Split

		'''
		vertexMask = pm.selectType (query=True, vertex=True)
		edgeMask = pm.selectType (query=True, edge=True)
		facetMask = pm.selectType (query=True, facet=True)

		if facetMask:
			mel.eval("performPolyPoke 1;")

		if edgeMask:
			mel.eval("polySubdivideEdge -ws 0 -s 0 -dv 1 -ch 0;")

		if vertexMask:
			mel.eval("polyChamferVtx 0 0.25 0;")

	def b047(self):
		'''
		Insert Edgeloop

		'''
		mel.eval("SplitEdgeRingTool;")

	def b048(self):
		'''
		Collapse Edgering

		'''
		mel.eval("bt_polyCollapseEdgeRingTool;")

	def b049(self):
		'''
		Slide Edge Tool

		'''
		mel.eval("SlideEdgeTool;")

	def b050(self):
		'''
		Spin Edge

		'''
		mel.eval("bt_polySpinEdgeTool;")

	def b051(self):
		'''
		Offset Edgeloop

		'''
		mel.eval("performPolyDuplicateEdge 0;")

	def b052(self):
		'''
		Offset Edgeloop Options

		'''
		mel.eval("DuplicateEdgesOptions;")

	def b053(self):
		'''
		Edit Edge Flow

		'''
		mel.eval("PolyEditEdgeFlow;")

	def b054(self):
		'''
		Edit Edge Flow Options

		'''
		mel.eval("PolyEditEdgeFlowOptions;")

	def b055(self):
		'''
		Crease

		'''
		creaseAmount = float(self.hotBox.ui.s003.value())
		normalAngle = int(self.hotBox.ui.s004.value()) 

		if self.hotBox.ui.chk011.isChecked(): #crease: Auto
			angleLow = int(self.hotBox.ui.s005.value()) 
			angleHigh = int(self.hotBox.ui.s006.value()) 

			mel.eval("PolySelectConvert 2;") #convert selection to edges
			contraint = pm.polySelectConstraint( mode=3, type=0x8000, angle=True, anglebound=(angleLow, angleHigh) ) # to get edges with angle between two degrees. mode=3 (All and Next) type=0x8000 (edge). 

		operation = 0 #Crease selected components
		pm.polySoftEdge (angle=0, constructionHistory=0) #Harden edge normal
		if self.hotBox.ui.chk002.isChecked():
			objectMode = pm.selectMode (query=True, object=True)
			if objectMode: #if in object mode,
				operation = 2 #2-Remove all crease values from mesh
			else:
				operation = 1 #1-Remove crease from sel components
				pm.polySoftEdge (angle=180, constructionHistory=0) #soften edge normal

		if self.hotBox.ui.chk004.isChecked(): #crease vertex point
			pm.polyCrease (value=creaseAmount, vertexValue=creaseAmount, createHistory=True, operation=operation)
		else:
			pm.polyCrease (value=creaseAmount, createHistory=True, operation=operation) #PolyCreaseTool;

		if self.hotBox.ui.chk005.isChecked(): #adjust normal angle
			pm.polySoftEdge (angle=normalAngle)

		if self.hotBox.ui.chk011.isChecked(): #crease: Auto
			pm.polySelectConstraint( angle=False ) # turn off angle constraint

	def b056(self):
		'''
		

		'''
		pass

	def b057(self):
		'''
		Trifill

		'''
		pm.undoInfo (openChunk=True)
		selectTypeEdge = pm.filterExpand(selectionMask=32) #returns True if selectionMask=Edges

		symmetryOn = pm.symmetricModelling(query=True, symmetry=True) #query symmetry state
		if symmetryOn:
			axis = pm.symmetricModelling(query=True, axis=True) #query the symmetry axis and assign which vertex point position in list to query later in order to filter and perform an operation on them seperately 
			if axis == "x":
				axisInt = 0
			if axis == "y":
				axisInt = 1
			if axis == "z":
				axisInt = 2

		if (selectTypeEdge): #if selection is polygon edges, convert to vertices.
			mel.eval("PolySelectConvert 3;")

		selected = pm.ls (selection=True, flatten=True) #now that the selection is converted, get selected vertices
		if (len(selected)>0): #check to see if there is anything selected
			object_ = selected[0].split('.vtx')[0] #strip .vtx from the vertex name to get the object (shape) name
		else:
			print "// Warning: Nothing Selected. You must select two edges that share a vertex or at least three vertices. //"

		shadingEngines = pm.listConnections(object_, type="shadingEngine") #get the connected "shadingEngines"
		materials = pm.ls(pm.listConnections(shadingEngines), materials=True) #list the connected materials (shaders)

		vertexList = []
		vertexListNeg = []
		for vertex in selected:
			vertexPosition =  pm.pointPosition(vertex)
			if symmetryOn:
				if vertexPosition[axisInt]<0: #if symmetry on, seperate negative vertices on which ever axis is being used
					vertexListNeg.append(vertexPosition)
				else:
					vertexList.append(vertexPosition)
			else:
				vertexList.append(vertexPosition)

		def createFacetAndUnite(vertices):
			tempTriangle = "___fillTemp___" #create a polygon face using the list of vertex points and give it a temp name
			pm.polyCreateFacet (point=vertices, texture=1, name=tempTriangle) #0-None; 1-Normalize; 2-Unitize

			if (self.hotBox.ui.chk001.isChecked()):
				pm.polyNormal(tempTriangle, normalMode=4) #3-reverse and cut, 4-reverse and propagate

			pm.select(tempTriangle, add=True) #select and assign material from main object
			pm.hyperShade(assign=materials[0])
			pm.select(tempTriangle, clear=True)

			tempObject = "___objTemp___" #combine with main mesh, assigning a temp name so that the original name can be freed up and the object can then be renamed to the original name
			pm.polyUnite (object_, tempTriangle, constructionHistory=False, name=tempObject)
			pm.rename (tempObject, object_)

		if symmetryOn:
			createFacetAndUnite(vertexList)
			createFacetAndUnite(vertexListNeg)
		else:
			createFacetAndUnite(vertexList)

		pm.hilite (object_, replace=True)

		if (selectTypeEdge): #if original selection was edges, convert back to edges.
			mel.eval("PolySelectConvert 2;")
			pm.selectType(edge=True)
		pm.undoInfo (closeChunk=True)

	def b058(self):
		'''
		

		'''
		pass

	def b059(self):
		'''
		Crease Editor

		'''
		from maya.app.general import creaseSetEditor
		creaseSetEditor.showCreaseSetEditor()

	def b060(self):
		'''
		

		'''
		pass


#module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------
#b008, b010, b011, b019, b024-27, b058, b059, b060