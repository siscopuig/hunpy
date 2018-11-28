
from enum import Enum

class AdvertState(Enum):

	NEW = 0
	EXISTING = 1


class Advert:


	def __init__(self):

		self.id = None
		self.uid = None
		self.src = None
		self.width = None
		self.height = None
		self.advertiser = None
		self.landing = None
		self.finfo = None
		self.datetime = None
		self.location = None
		self.state = None
		self.isframe = 0
		self.instances = 1



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
			'{t} is frame:    {isframe}\n'

		).format(
			uid=self.uid,
			src=self.src,
			width=self.width,
			height=self.height,
			advertiser=self.advertiser,
			landing=self.landing,
			finfo=self.finfo,
			datetime=self.datetime,
			is_iframe=self.isframe, t=tab)

		return string






