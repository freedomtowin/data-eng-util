def get_stock_prices_v2(self):
		
	sym = self.get_symbol()
	params = {'interval':'30m','includePrePost':False,'events':"div,splits",'range':'5d'}
	proxy=None
	base_url = 'https://query2.finance.yahoo.com'
	user_agent_headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

	# Getting data from json
	url = "{}/v8/finance/chart/{}".format(base_url, sym)
	data = requests.get(
		url=url,
		params=params,
		proxies=proxy,
		headers=user_agent_headers
	)

	tmp = pd.DataFrame()

	chart = json.loads(data.content)['chart']['result'][0]

	chart['meta']['symbol']

	_time = chart['timestamp']

	quote = chart['indicators']['quote'][0]
	_low = quote['low']
	_high = quote['high']
	_open = quote['low']
	_close = quote['close']
	_volume = quote['volume']


	tmp['time'] = pd.to_datetime(_time, unit="s")
	tmp['low'] = _low
	tmp['high'] = _high
	tmp['open'] = _open
	tmp['close'] = _close
	tmp['volume'] = _volume


	tmp = tmp[((tmp.time.dt.minute==0)|(tmp.time.dt.minute==30)).values].copy()
	tmp.time = tmp.time.apply(lambda x: x.replace(minute=0, second=0))
	tmp=tmp.groupby(['time']).agg({'open':'mean','high':'mean','low':'mean','close':'mean','volume':'sum'}).reset_index()
	tmp['time'] = tmp['time'].apply(lambda x: datetime.datetime.strftime(x,"%Y-%m-%d %H:%M:%S"))
	tmp['sym'] = sym.lower()
	
	tmp['source'] = 'alpha_vantage_key'
	
	return tmp
	