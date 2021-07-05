class fast_frugal_ensembler():

	def __init__(self,rule_coef):
		self.rule_coef = rule_coef
		
	def mapper(self,df):
	
		rules = {
			'RULE_0': (df['FEATURE_0']>self.rule_coef['RULE_0']['FEATURE_0'])&(df['FEATURE_1']>self.rule_coef['RULE_0']['FEATURE_1']),
			'RULE_1': (df['FEATURE_0']>self.rule_coef['RULE_1']['FEATURE_0'])&(df['FEATURE_1']>self.rule_coef['RULE_1']['FEATURE_1'])
			}
			
		#postprocess rules
		return rules['RULE_0'],rules['RULE_1']