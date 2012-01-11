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

# ----- service modules -----
import numpy as np
import Image
import os
import logging

logger = logging.getLogger('wikicaptcha.unclear')

# ----- SQLAlchemy -----
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.dialects.mysql import LONGBLOB

Base = declarative_base()
# Mapping outline:
# http://www.sqlalchemy.org/docs/orm/tutorial.html
# Note: coords are WxH+X+Y
class unclear_word(Base):
  __tablename__ = 'unclear_words'
  
  wId = Column('wID', Integer, primary_key=True)
  book = Column('book', Integer, nullable=False)
  page = Column('page', Integer, nullable=False)
  column = Column('column', Integer, nullable=True)
  par = Column('par', Integer, nullable=True)
  line = Column('line', Integer, nullable=True)
  w = Column('w', Integer, nullable=False)
  h = Column('h', Integer, nullable=False)
  x = Column('x', Integer, nullable=False)
  y = Column('y', Integer, nullable=False)
  image = Column('image', LONGBLOB, nullable=True)
   
  def __init__(self,book, page, coords, word, column=None, par=None, line=None):
    self.book = book
    self.page = page
    self.word = word
    
    self.column = column
    self.par = par
    self.line = line
    
    self.x=coords[0]
    self.y=coords[1]
    self.w=coords[2]-coords[0]
    self.h=coords[3]-coords[1]

  def __repr__(self):
    return "Unclear_Word(book:%s, page:%s, word:%s, x:%s, y:%s, w:%s, h:%s)" \
    %(self.book, self.page, self.word, self.x, self.y, self.w, self.h)

  def get_book(self):
    return self.book
    
  def set_image(self, blob):
    self.image = blob
    
  def get_image(self):
    return self.image

  def get_coords():
    coords = [self.x, self.y, self.x + self.w, self.y + self.h]
