#! /usr/bin/python
# -*- coding: UTF-8 -*-

# See AUTHORS file for further information
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
# If not, see <http://www.gnu.org/licenses/>.

# ----- code from djvu-dump-text.py ----- 
# Modified from
# https://bitbucket.org/jwilk/python-djvulibre/src/f67a7b205cf5/examples/djvu-dump-text
# Copyright © 2008, 2010 Jakub Wilk <jwilk@jwilk.net>, released under GPL v2

# ----- service modules -----
import os
import djvu.decode

# ----- END service modules -----

from unclear import unclear_word

def _get_text(sexpr, level=0):
    txt=''
    if (isinstance(sexpr, djvu.sexpr.ListExpression) and len(sexpr) !=0):
        txt = ''
        for child in sexpr[5:]:
            txt = txt + _get_text(child, level + 1)
        return txt
    else:
        txt = str(sexpr)
        txt = txt.strip('"') + ' '
        return  txt

def _get_word(sexpr, level=0):
    wl = []
    if (isinstance(sexpr, djvu.sexpr.ListExpression) and len(sexpr) !=0):
        if str(sexpr[0].value) == 'word':
          wl.append(sexpr)
          return wl
        for child in sexpr[5:]:
            res = _get_word(child, level + 1)
            if res is not None:
              wl.extend(res)
        return wl

def _slice(x, start, end):
  return [int(x[i]) for i in range(start, end+1)]

from devel import info
class context(djvu.decode.Context):

    def __init__(self, infile):
      self.infile = infile
      self.document = self.new_document(djvu.decode.FileURI(self.infile))
      self.document.decoding_job.wait()
      self.pages = len(self.document.pages)
      
    def _handle_message(self, message):
      if isinstance(message, djvu.decode.ErrorMessage):
        print >> sys.stderr, message
        sys.exit(1)

    def get_pages(self):
      return self.pages

    def get_text(self):
      text = []
      for page in self.document.pages:
        text.append(_get_text(page.text.sexpr))
      return text

    def get_page_text(self, pageno):
      page = self.document.pages[pageno]
      return _get_text(page.text.sexpr)

    def get_wordlist_page(self, pageno):
      page = self.document.pages[pageno]
      sexpr = page.text.sexpr
      wl = []
      if (isinstance(sexpr, djvu.sexpr.ListExpression) and len(sexpr) !=0):
        wl = _get_word(sexpr)
      return wl

    def _process(self):
      i=0
      print self.document.pages
      for page in self.document.pages:
        #info(page)
        print "-"*15, "\n"
        print page.n
        print page.get_info()
        print page
        print page.text.sexpr
        text = _get_text(page.text.sexpr)
        print text
        if i > 5:
          break
        i=i+1
      return text

class wikidjvu():
  
  def __init__(self, infile):
       self.context = context(infile)
       
       (path, name) = os.path.split(infile)
       self.infile = infile
       self.path = path
       self.name = name
       self.pages = self.context.get_pages()

  def _check_pageno(self, pageno):
    if not (isinstance(pageno, int) and pageno >= 0):
      raise IOError
    return pageno - 1

  def _process(self):
    return self.context._process()

  def get_pages(self):
    return self.pages

  def info(self):
    pass

  def get_text(self):
    return self.context.get_text()

  def get_wordlist_page(self, pageno):
    pageno = self._check_pageno(pageno)
    return self.context.get_wordlist_page(pageno)

  def get_page_text(self,pageno):
    pageno = self._check_pageno(pageno)
    if pageno == -1:
      return ' '.join(self.context.get_text())
    else:
      return self.context.get_page_text(pageno)

  def define_cond():
    # --- recognise in some way. ----
    #for i in somecondition:
    pass

  def recognise(self, reco_cond):
    #unclist = []
    pass

  def unclear_page(self, pageno, reco_cond):
    pageno = _check_pageno(pageno)
    wl = self.get_page(pageno)
    unclist = []
    return

  def unclear_page_caret(self, pageno):
    pageno = self._check_pageno(pageno)
    wl = self.get_wordlist_page(pageno)
    for wc in wl:
      w = str(wc[-1])
      unclist = []
      if "^" in w:
        coord = _slice(wc,1,4)
        uw = unclear_word(pageno, coord, w)
        unclist.append(uw)
    return unclist

  def unclear_caret(self):
    unclist = []
    for pn in range(1, self.pages):
      wl = self.get_wordlist_page(pn)
      for wc in wl:
        w = str(wc[-1])
        if "^" in w:
          if len(wc) != 6:
            raise IOError
          coord = _slice(wc,1,4)
          uw = unclear_word(pn, coord, w)
          unclist.append(uw)
    return unclist
