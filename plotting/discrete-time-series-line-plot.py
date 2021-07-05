count=0
days = (df.date_col.max() - df.date_col.min()).days
vector = np.array([df.date_col.min()+datetime.timedelta(days=i) for i in range(days)])


tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),  
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),  
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),  
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),  
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]
             
  
# Rescale to values between 0 and 1 
for i in range(len(tableau20)):  
    r, g, b = tableau20[i]  
    tableau20[i] = (r / 255., g / 255., b / 255.)

plt.figure(figsize=(12, 9))  
  
ax = plt.subplot(111)  
ax.spines["top"].set_visible(False)  
ax.spines["right"].set_visible(False)  
#ax.spines["left"].set_visible(False)  
#ax.spines["bottom"].set_visible(False)  


ax.get_xaxis().tick_bottom()  
ax.get_yaxis().tick_left()  

plt.yticks(fontsize=14)    
plt.xticks(fontsize=14)  
plt.title('TEST',fontsize=14)

for item in df.feature_name.unique()[:20]:

	tmp  =[(df.date_col.min()+datetime.timedelta(days=i)).date() in df[df.feature_name==item].date_col.dt.date.values.flatten() for i in range(days)]

	mask = np.array(tmp)
	
	if np.sum(maask)<=2:
		continue
		
	plt.tick_params(axis='both',which='both',bottom='off', top='off', labelbottom='on', left='off',right='off',labelleft='on'_
	
	p = plt.plot(vector[mask>0],mask[mask>0]+count,'.',color=tableau20[count%20])
	
	plt.text(np.max(df.date_col),count+1, item.upper(), fontsize=16,color=tableau20[count%20])
	
	plt.xticks(rotation=70)
	
	count+=1
	
plt.show()
		
		
		
	