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

# ----- module imports -----
from WKCmod import wikidjvu
from WKCmod.parse import parse
from WKCmod.install import WIKICAPTCHA

# ----- global variables definition -----
APPNAME = WIKICAPTCHA['APPNAME']
BASE_DIR = WIKICAPTCHA['BASE_DIR']
CURR_DIR = WIKICAPTCHA['CURR_DIR']

# -----  logging -----
import logging

LOGLEVELS = { logging.CRITICAL: 'CRITICAL',
              logging.ERROR: 'ERROR',
              logging.WARNING: 'WARNING',
              logging.INFO: 'INFO',
              logging.DEBUG: 'DEBUG'}

# --- NullHandler ---
class NullHandler(logging.Handler):
    def emit(self, record):
        pass
# --- END NullHandles

# --- logger formatter ---
LOGFORMAT_STDOUT = { logging.DEBUG: \
         '%(module)s:%(lineno)-4s - %(levelname)-4s: %(message)s',
         logging.INFO: '%(levelname)-8s: %(message)s',
         logging.WARNING: '%(levelname)-8s: %(message)s',
         logging.ERROR: '%(levelname)-8s: %(message)s',
         logging.CRITICAL: '%(levelname)-8s: %(message)s'
       }
# --- END logger formatter ---

# --- root logger ---
rootlogger = logging.getLogger()
rootlogger.setLevel(logging.DEBUG)

lvl_config_logger = logging.DEBUG
#lvl_config_logger = logging.INFO

console = logging.StreamHandler()
console.setLevel(lvl_config_logger)
formatter = logging.Formatter('%(levelname)-8s: %(message)s')
console.setFormatter(formatter)
rootlogger.addHandler(console)

logger = logging.getLogger('wikicaptcha')
# --- END root logger ---

# ----- END logging -----

# ----- SQLAlchemy -----
import sqlalchemy as sqlalc

# ----- END SQLAlchemy -----

# ----- option parsing -----
dizcli = parse()

page = dizcli['page']
debug = dizcli['debug']

lvl = logging.WARNING
if debug:
  lvl = logging.DEBUG
  formatter = logging.Formatter(LOGFORMAT_STDOUT[lvl])
  console.setFormatter(formatter)
  console.setLevel(lvl)
else:
  h = NullHandler()
  console.setLevel(lvl)
  rootlogger.addHandler(h)

logger = logging.getLogger(APPNAME)
logger.info("Log level set to: %s" %LOGLEVELS.get(lvl))

djvuinfile_name = dizcli['infile']
djvuinfile = os.path.normpath(os.path.join(CURR_DIR, djvuinfile_name))
logger.info("Input file: %s" %djvuinfile)

# ----- END option parsing ----

# --- create engine object (SQLAlchemy) -----
# dialect+driver://user:password@host/dbname[?key=value..]
dbuser = 'pywikicaptcha'
dbpass = 'pywiki'
dbhost = 'localhost'
dbname = 'captcha'

dbconfig = 'mysql://%s:%s@%s/%s'%(dbuser, dbpass, dbhost, dbname)
dbengine = sqlalc.create_engine(dbconfig)
dbengine.echo = True
# --- END create engine object (SQLAlchemy) -----

metadata = sqlalc.MetaData(dbengine)

# ----- creating tables -----
# *** import schemas ***
from WKCmod import data

data.wkdjv_table_schema(metadata)
data.uws_table_schema(metadata)

try:
  metadata.create_all()
  logger.info("Tables created!")
except Exception as e:
  logger.error("Exception: %s" %e)
# ----- END creating tables -----

rootsession = sqlalc.orm.sessionmaker(bind=dbengine)

booksession = rootsession()

# Djvu file object
#infile, title, author, edition, year, ISBN)
title ='Horse-shoes and horse-shoeing'
author ='George Fleming'
edition = '1st'
year = '1869'
ISBN ='ABCD'
djvf = wikidjvu.Wikidjvu(djvuinfile, title, author, edition, year, ISBN)

booksession.add(djvf)
booksession.commit()

# get the list of the words contained in page 2
wl = djvf.get_wordlist_page(2)

# print a list of unclear words (containing a caret ^)
ul = djvf.unclear_caret()
print ul[1]



for uw in ul:
  print uw
  # produce a TIFF image of the second unclear word
  tiffoutfile_name = "test/out.tiff"
  tiffoutfile = os.path.normpath(os.path.join(CURR_DIR, tiffoutfile_name))
  if tiffoutfile is None:
      tiffoutfile='someuniquerandomname.tiff'
  dirname = os.path.dirname(tiffoutfile)
  filename, fileext = os.path.splitext(os.path.basename(tiffoutfile))
  logger.info("dirname: %s, filename: %s, fileext: %s" %(dirname, filename, fileext))

  # produce TIFF file, note segment option is WxH+X+Y
  command="ddjvu %s -page=%s -format=tiff -segment %sx%s+%s+%s %s" %(djvf.infile, uw.page, uw.w, uw.h, uw.x, uw.y, tiffoutfile)
  #print command
  os.system(command)
    
  jpgoutfile = os.path.join(dirname, filename + ".jpg")
  logger.info("jpgoutfile: %s" %jpgoutfile)
  command="convert %s %s" %(tiffoutfile, jpgoutfile)
  #print command
  os.system(command)
  
  blob = open(jpgoutfile, 'rb').read()
  uw.set_image(blob)
  
  booksession.add(uw)

booksession.commit()
booksession.close()


