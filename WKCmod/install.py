#! /usr/bin/python
# -*- coding: UTF-8 -*-

# ----- system modules -----
import re
import os
import sys

# ----- service modules -----
import tuct
import logging

logger = logging.getLogger('wikicaptcha.install')

# ***** application (meta)data *****
APPNAME = 'wikicaptcha'

VERSION = '0.1'

BASE_DIR = os.path.dirname(os.path.normpath(os.path.realpath(sys.argv[0])))

CURR_DIR = os.path.abspath(os.path.normpath(os.getcwd()))

INSTALLED = None
if os.path.exists(os.path.join(BASE_DIR,'config/')):  
  logger.debug("Trovata directory di configurazione: %s" %os.path.join(BASE_DIR,'config/'))
  INSTALLED = False
else:
  #config_logger.info("Directory di configurazione '%s' non trovata" %os.path.join(BASE_DIR,'config/'))
  for directory in [sys.prefix, os.path.join(sys.prefix,'local/')]:
    logger.debug("Scanning directory: %s" %directory)
    sharedir = os.path.join(directory, 'share/')
    installed = os.path.join(sharedir, '%s/config' % APPNAME)
    if os.path.exists(installed):
      BASE_DIR = os.path.abspath(os.path.normpath(os.path.join(installed, '../')))
      INSTALLED = True

if INSTALLED == None: raise IOError("Non sono riuscito a trovare la cartella di configurazione di %s" %APPNAME)

logger.debug("BASE_DIR: %s" %BASE_DIR)
logger.debug("Installed: %s" %INSTALLED)
logger.debug("CURR_DIR: %s" %CURR_DIR)

WKCMOD_DIR = os.path.join(BASE_DIR, 'WKCmod')

DESCRIPTION="""wikicaptcha is a CAPTCHA implementation for Wikisource"""

EPILOG = """Copyright 2010 - Alex Brollo and Cristian Consonni (see AUTHORS file for details).
This program is free software; you may redistribute it under the terms of
the GNU General Public License version 3 or (at your option) any later version. 
This program has absolutely no warranty."""

WIKICAPTCHA = tuct.tuct(APPNAME = APPNAME,

    VERSION = VERSION,

    BASE_DIR = BASE_DIR,

    CURR_DIR = CURR_DIR,

    WKCMOD_DIR = WKCMOD_DIR,

    INSTALLED = INSTALLED,

    DESCRIPTION = DESCRIPTION,

    EPILOG = EPILOG 
           )

# ----- END application (meta)data -----
