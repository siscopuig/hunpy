# -*- coding: utf-8 -*-

from hunpy.containers.image_container import ImageContainer


class Image(ImageContainer):

	def __init__(self):

		ImageContainer.__init__(self)

		self.src = None
		self.onclick = None
		self.style = None
		self.a_href = None
		self.a_onclick = None
		self.a_style = None


	def __str__(self):

		string = 'Image container:\n' + ImageContainer.__str__(self) + (
			' src:            {img_src}\n'
			' onclick:        {img_onclick}\n'
			' image style:    {img_style}\n'
			' anchor href: 	  {a_href}\n'
			' anchor onclick: {a_onclick}\n'
			' anchor style:   {a_style}\n'
		).format(
			img_src=self.src,
			img_onclick=self.onclick,
			img_style=self.style,
			a_href=self.a_href,
			a_onclick=self.a_onclick,
			a_style=self.a_style
		)

		return string