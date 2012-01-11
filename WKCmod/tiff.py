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

# ----- general imports -----
import os
import sys

# ----- logging module -----
import logging

# ----- service modules -----
import numpy as np
import Image


logger = logging.getLogger('wikicaptcha.tiff')

class image_extractor():

    def __init__(self, djvufile):
      self.

    extract_tiff(self, unclist, djvufile, pageno)
        for coord in lista:
        
        w=str(eval(coord[2])-eval(coord[0]))
        h=str(eval(coord[3])-eval(coord[1]))
        x=coord[0]
        y=coord[1]
    return
    
    #http://bytes.com/topic/python/answers/444058-batch-tiff-jpeg-conversion-script
    def tiff2jpeg(self):
      outfile = os.path.splitext(os.path.join(root,f))[0] + ".jpg"
      try:
        im = Image.open(os.path.join(root,f))
        print "Generating jpeg for %s" %f
        im.thumbnail(im.size)
        im.save(outfile, "JPEG", quality=90)
      except Exception, e:
      print e

    #http://www.sqlalchemy.org/trac/wiki/UsageRecipes/StoringImages
    def img2array():
      return np.asarray(Image.open('myfile.jpg'),dtype='uint8')

