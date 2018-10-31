


class Advert:


	def __init__(self):

		self.uid = None
		self.src = None
		self.width = None
		self.height = None
		self.advertiser = None
		self.landing = None
		self.finfo = None
		self.datetime = None
		self.is_iframe = None


	def __str__(self):

		tab = '\t'

		string = (
			'\n'
			'{t} Advert: 	  \n'
			'{t} uid:         {uid}\n'
			'{t} src:         {src}\n'
			'{t} width:       {width}\n'
			'{t} height:      {height}\n'
			'{t} advertiser:  {advertiser}\n'
			'{t} landing: 	  {landing}\n'
			'{t} finfo:	      {finfo}\n'
			'{t} datetime:    {datetime}\n'
			'{t} is iframe:   {is_iframe}\n'
		).format(
			uid=self.uid,
			src=self.src,
			width=self.width,
			height=self.height,
			advertiser=self.advertiser,
			landing=self.landing,
			finfo=self.finfo,
			datetime=self.datetime,
			is_iframe=self.is_iframe, t=tab)

		return string






