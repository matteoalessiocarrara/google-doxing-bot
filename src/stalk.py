#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  Copyright 2016 Matteo Alessio Carrara <sw.matteoac@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.

from sys import argv, stdout
import re

import requests
import colorama
from bs4 import BeautifulSoup as bs


# TODO Spostare in repo separato, può sempre fare comodo
def google_search(query, pages=1):
	stdout.write("Scaricando i risultati... 0\r")
	stdout.flush()
	
	user_agent = "Opera/9.80 (Android; Opera Mini/7.6.35766/35.5706; U; it) Presto/2.8.119 Version/11.10"
	res = requests.get("https://google.com/search", params={"q": query}, headers={'User-Agent': user_agent})
	
	results_list = []
	next_page = ""
	for i in range(pages):
		if next_page != "":
			res = requests.get(next_page)
		for result in bs(res.text, "html.parser").find("div", attrs={"id": "ires"}).find("ol").findAll("div", attrs={"class": "g"}):
			tmp = {}
			
			# Immagini proposte
			if result.find("img") != None:
				continue
			
			try:
				tmp["href"] = "https://google.com" + result.h3.a.get("href")
				tmp["title"] = result.h3.a.text
				tmp["description"] = result.div.span.text
			except:
				print (result)
				pass
			
			results_list.append(tmp)
			stdout.write("Scaricando i risultati... " + str(len(results_list)) + "\r")
			stdout.flush()
		try:
			next_page = "https://google.com/" + bs(res.text, "html.parser").find("div", attrs={"id": "foot"}).table.findAll("td")[-1].a.get("href")
		except:
			break
			
	stdout.write("\n")
	return results_list


def find_info_email(bsobj):
	ret = ""
	r = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
	
	try:
		for s in bsobj.body(text=True):
			for ss in str(s).split(" "):
				if r.match(ss) != None:
					ret += r.match(ss).group() + " "
	except:
		pass
		
	return ret


def find_info(url):
	ret = []
	res = requests.get(url)
	bsobj = bs(res.text, "html.parser")
	
	if find_info_email(bsobj) != "":
		ret.append({"name": "email", "value": find_info_email(bsobj)})
	
	return ret


colorama.init()

	
if len(argv) != 1 + 2:
	exit("Uso: stalk.py query pagine_di_google_da_scaricare")

	
query = argv[1]
pages = int(argv[2])
res = google_search(query, pages)

print ("")
for page in res:
	stdout.write(colorama.Fore.YELLOW + page["title"] + "\r")
	stdout.flush()
	
	info_found = find_info(page["href"])
	if info_found == []:
		stdout.write(colorama.Fore.RED + page["title"] + "\n")
	else:
		stdout.write(colorama.Fore.GREEN + page["title"] + "\n")

	stdout.write(colorama.Fore.RESET)
	
	stdout.write(page["description"] + "\n")
	stdout.write(colorama.Style.DIM + page["href"] + "\n\n")
	stdout.write(colorama.Style.RESET_ALL)
	
	if info_found != []:
		
		
		for info in info_found:
			stdout.write(colorama.Style.BRIGHT + info["name"] + colorama.Style.RESET_ALL + ": " + info["value"] + "\n\n")



