#! /usr/bin/python
# Copyright 2015 Balasankar C <balasankarc@autistici.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

import re
import urllib
import os
import argparse
import sys

parser = argparse.ArgumentParser(description='Download commistrip images',
                                 formatter_class=lambda prog:
                                 argparse.HelpFormatter(
                                     prog, max_help_position=7))
parser.add_argument("language", help="Specify the language - en or fr")
parser.add_argument("outputdir", help="Specify the output directory")
parser.add_argument("-v", "--verbosity",
                    help="Print download url", action="store_true")
parser.add_argument("-ps", "--pagestart", help="Specify starting page number")
parser.add_argument("-pe", "--pageend", help="Sprcify ending page number")
args = parser.parse_args()
if args.language not in ["en", "fr"]:
    print "Language should be either en or fr"
    sys.exit()
baseurl = "http://www.commitstrip.com/" + args.language + "/page/"
pagestart = 1
pageend = 100
if args.pagestart:
    pagestart = int(args.pagestart)
if args.pageend:
    pageend = int(args.pageend)
if not os.path.exists(args.outputdir):
    os.mkdir(args.outputdir)
for pagecount in range(pagestart, pageend+1):
    page = urllib.urlopen(baseurl + str(pagecount))
    pagecontenthtml = page.read()
    page.close()
    imageline = re.findall(
        '<img class=".* size-full.*>', pagecontenthtml)
    if len(imageline) == 0:
        imageline = re.findall('<p><img.*>', pagecontenthtml)
    resultline = imageline[0]
    srcurl = re.findall('src=".*?"', resultline)
    imageurl = str(srcurl[0][5:-1])
    indexpos = imageurl[::-1].index('/')
    filename = imageurl[-indexpos:]
    if os.path.isfile(args.outputdir + "/" + filename):
        continue
    if args.verbosity:
        print "Page #" + str(pagecount) + "     : " + imageurl
    urllib.urlretrieve(
        imageurl,
        filename=args.outputdir + "/" + filename)
