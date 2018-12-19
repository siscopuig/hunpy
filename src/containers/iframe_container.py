from html_element import HtmlElement


class IframeContainer(HtmlElement):


	def __init__(self, parent=None):

		HtmlElement.__init__(self, parent)


	def __str__(self):

		tab = self.level * '\t'

		string = (
			'\n'
			'{t}Frame: 		  {level} : {hash}\n'
			'{t} id:          {id}\n'
			'{t} name:        {name}\n'
			'{t} src:         {src}\n'
			'{t} title:       {title}\n'
			'{t} style:       {style}\n'
			'{t} size:        {size}\n'
			'{t} location:    {location}\n'
			'{t} anchor_imgs: {anchor_imgs}\n'
			'{t} img_srcs:    {img_srcs}\n'
			'{t} onclicks:    {clicks}\n'
		).format(
			level=self.level, hash=self.hashref,
			id=self.id,
			name=self.name,
			src=self.src,
			title=self.title,
			style=self.style,
			size=self.size,
			location=self.location,
			anchor_imgs=self.anchor_imgs,
			img_srcs=self.img_srcs,
			clicks=self.onclicks, t=tab)

		# Include sub-frames.
		# return string + '\n' + ''.join([str(frame) for frame in self.iframes])

		# Includes nested frames
		for iframe in self.iframes:
			string + '\n' + ''.join(str(iframe))
		return string


