from tk_slots_max_init import Init
maxEval = Init.maxEval

import os.path



class Rigging(Init):
	def __init__(self, *args, **kwargs):
		super(Rigging, self).__init__(*args, **kwargs)

		self.ui = self.sb.getUi('rigging')



	def cmb000(self, index=None):
		'''
		Editors
		'''
		cmb = self.ui.cmb000
		
		files = ['']
		contents = cmb.addItems_(files, ' ')

		if not index:
			index = cmb.currentIndex()
		if index!=0:
			if index==contents.index(''):
				pass
			cmb.setCurrentIndex(0)


	def b000(self):
		'''
		
		'''
		pass


	def b001(self):
		'''
		
		'''
		pass


	def b002(self):
		'''
		
		'''
		pass


	def b003(self):
		'''
		
		'''
		pass


	def b004(self):
		'''
		
		'''
		pass


	def b005(self):
		'''
		
		'''
		pass


	def b006(self):
		'''
		
		'''
		pass


	def b007(self):
		'''
		
		'''
		pass


	def b008(self):
		'''
		
		'''
		pass


	def b009(self):
		'''
		
		'''
		pass








#module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------