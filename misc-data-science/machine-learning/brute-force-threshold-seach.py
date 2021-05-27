#p: predicted, y: actual
def classification_metrics(p,y):
    tp = np.sum((p==1)&(y.flatten()==1))
    fp = np.sum((p==1)&(y.flatten()==0))
    tn = np.sum((p==0)&(y.flatten()==0))
    fn = np.sum((p==0)&(y.flatten()==1))
    acc = (tn+tp)/(tp+tn+fp+fn)
    return tp,fp,tn,fn,acc

#find optimal maximum threshold for where the false positives is equal to 0
def find_max_thres(p,y):
    threshold = 0
    for i in np.linspace(0,1,100):
        tp,fp,tn,fn,acc = classification_metrics(p>i,y.flatten())
        if fp==0:
            threshold=i-20/100
            break
    return threshold
    
#same idea as above, but with average value in a conditions instead of accuracy metrics.
def action_metric(cond,y):
    return y[cond].mean()

#find optimal maximum threshold for where the false positives is equal to 0
def find_max_thres(p,y):
    threshold = 0
    best = -100
    for i in np.linspace(0,p.max(),10):
        b = action_metric(p>i,y)
        if b>best:
            best=b
    return best