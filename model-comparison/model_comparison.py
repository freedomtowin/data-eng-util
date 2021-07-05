class model_loader():

	def __init__(self,model_folder):
		self.model_folder = model_folder
		self.get_coef()
		
	def get_coef(self):
		#load txt file
		self.coef = np.loadtxt(self.model_folder+'/filename.txt')
		
		#load tensorflow model
		export_path_sm = self.model_folder+"./mobilenet_final/001"
		self.reloaded_sm = tf.saved_model.load(export_path_sm)
		
	def predict(self,X):
		#example
		return reloaded_sm(tf.cast(X[np.newaxis, ...],tf.float32)).numpy()


class fast_frugal():

	def __init__(self,model_folder):
		self.model_folder = model_folder
		
	def my_import(self):
		name = self.model_folder.replace('/','.')+'.fast_frugal_ensembler'
		mod = __import__(name, fromlist=['fast_frugal_ensembler'])
		klass = getattr(mod, 'fast_frugal_ensembler')
		return kclass
        
        
 model = model_loader('model/v1')
 
 rule_coef = json.load(open('model/v1/rule_ceof.json','r'))
 rmap = fast_frugal('model/v1').my_import(rule_coef)
 
 
 
 