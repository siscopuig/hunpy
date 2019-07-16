# -*- coding: utf-8 -*-

class Captures:

    def __init__(self):

        self.type = None
        self.ext = None
        self.finfo = None
        self.src = None
        self.width = None
        self.height = None
        self.fname = None
        self.tmp_path = None
        self.dest_path = None
        self.tmp_filepath = None
        self.dest_filepath = None
        self.iframe_xpath = None
        self.state = None


    def __str__(self):
        tab = '\t'
        string = (
            '\n'
            '{t} Capture: 	   \n'
            '{t} type:         {type}\n'
            '{t} finfo:	       {finfo}\n'
            '{t} ext:	       {ext}\n'
            '{t} src:          {src}\n'
            '{t} width:        {width}\n'
            '{t} height:       {height}\n'
            '{t} fname: 	   {fname}\n'
            '{t} tmp_path:	   {tmp_path}\n'
            '{t} dest_path:    {dest_filepath}\n'
            '{t} iframe_xpath: {iframe_xpath}\n'
            '{t} state:	       {state}\n'
        ).format(
            type=self.type,
            ext=self.ext,
            finfo=self.finfo,
            src=self.src,
            width=self.width,
            height=self.height,
            fname=self.fname,
            tmp_path=self.tmp_path,
            dest_path=self.dest_path,
            tmp_filepath=self.tmp_filepath,
            dest_filepath=self.dest_filepath,
            iframe_xpath=self.iframe_xpath,
            state=self.state,
            t=tab
        )

        return string