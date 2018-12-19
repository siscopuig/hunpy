from enum import Enum


class AdvertState(Enum):

	NEW = 0
	EXISTING = 1


class Advert:


	def __init__(self):

		self.id = None
		self.uid = None
		self.src = None
		self.size = None
		self.advertiser = None
		self.landing = None
		self.finfo = None
		self.location = None
		self.state = None
		self.isframe = None
		self.instances = 1



	def __str__(self):

		tab = '\t'

		string = (
			'\n'
			'{t} Advert: 	  \n'
			'{t} uid:         {uid}\n'
			'{t} src:         {src}\n'
			'{t} size:        {size}\n'
			'{t} advertiser:  {advertiser}\n'
			'{t} landing: 	  {landing}\n'
			'{t} finfo:	      {finfo}\n'
			'{t} datetime:	  {datetime}\n'
			'{t} location:	  {location}\n'
			'{t} datetime:    {datetime}\n'
			'{t} isframe:     {isframe}\n'
			'{t} instances:	  {instances}\n'

		).format(
			uid=self.uid,
			src=self.src,
			size=self.size,
			advertiser=self.advertiser,
			landing=self.landing,
			finfo=self.finfo,
			isframe=self.isframe,
			t=tab
		)

		return string






