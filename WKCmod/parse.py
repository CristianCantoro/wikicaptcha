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

# ----- global variables -----
from install import WIKICAPTCHA

# ----- service modules -----
import argparse
import logging

logger = logging.getLogger('wikicaptcha.parse')

def parsecli(appname, desc, vers, epi):
  
  #logger.debug("argv: %s %s %s %s" %(appname, desc, vers, epi))

  parser = argparse.ArgumentParser(description=desc, prog=appname, epilog=epi,\
  formatter_class=argparse.RawDescriptionHelpFormatter)

  VERSIONTEXT='***** %(prog)s VERSION: ' + ' ' + vers + ' ***** - ' + epi

  parser.add_argument('-v', '--version', action='version', version=VERSIONTEXT)

  parser.add_argument('infile', help='The input file')  

  parser.add_argument('-p', '--page', help='The number of the first page to process')  

  parser.add_argument('--debug', action='store_true', help='Turn on debug messages')  
  args = parser.parse_args()
  
  if args.page is None:
    args.page = 1

  logger.debug("args.__dict__: %s" %args.__dict__)

  dizcli=dict([(name, args.__dict__[name]) for name in args.__dict__.keys() if args.__dict__[name] != None])

  logger.debug("dizcli: %s" %dizcli)
  return dizcli

def parse():
  
  appname = WIKICAPTCHA['APPNAME']
  desc = WIKICAPTCHA['DESCRIPTION']
  vers = WIKICAPTCHA['VERSION']
  epi = WIKICAPTCHA['EPILOG']

  dizcli = parsecli(appname, desc, vers, epi)

  logger.debug("dizcli: %s" %dizcli)
 
  return dizcli
