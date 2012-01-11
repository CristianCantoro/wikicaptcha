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

# ----- SQLAlchemy -----
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

def wkdjv_table_schema(metadata):
  wkdjv = Table('wikidjvu', metadata,
     Column('bID', Integer, primary_key=True),
     Column('title', String(1024)),
     Column('author', String(1024)),
     Column('edition', String(1024)),
     Column('year', String(1024)),
     Column('pages', String(1024)),
     Column('ISBN', String(1024)),
     Column('infile', String(2048)),
  )
  return wkdjv

from sqlalchemy.dialects.mysql import BLOB
# note: coords are WxH+X+Y
def uws_table_schema(metadata):
  uws = Table('unclear_words', metadata,
    Column('wID', Integer, primary_key=True),
    Column('book', Integer, ForeignKey('wikidjvu.bID')),
    Column('page', Integer, nullable=False),
    Column('column', Integer, nullable=True),
    Column('par', Integer, nullable=True),
    Column('line', Integer, nullable=True),
    Column('w', Integer, nullable=False),
    Column('h', Integer, nullable=False),
    Column('x', Integer, nullable=False),
    Column('y', Integer, nullable=False),
    Column('image', BLOB, nullable=False),
  )
  return uws

