import requests
from lxml import etree
from io import StringIO
import subprocess
import re
import os
import json


PASSWORD = ''
EMAIL = ''
DIRECTORY = '.../egghead/downloads/'
TOP_DIRECTORY = '.../egghead/'

def writeFile(lista):
    with open('courses.json', mode='w') as f:
        return json.dump(lista, f, ensure_ascii=False)


def loadFile():
    with open('courses.json', mode='r') as f:
        return json.load(f)


def main():
	result = requests.get('https://egghead.io/courses')
	parser = etree.HTMLParser()
	tree   = etree.parse(StringIO(result.text), parser)
	languages = tree.xpath('//div[@class="technology-set"]')

	database = loadFile()

	for language in languages:
		name_obj = re.match(r'technology-(.*)', language.xpath('@id')[0])
		name = name_obj.group(1)

		if not os.path.exists(DIRECTORY + '{}'.format(name)):
			os.makedirs(DIRECTORY + '{}'.format(name), 0777)

		os.chdir(DIRECTORY + '{}'.format(name))

		courses_db = []
		if name in database:
			courses_db = database[name]
		courses = language.xpath('.//div[@class="card-content"]/a/@href')

		for course in courses:
			if course not in courses_db:
				str_obj = re.match(r'https://egghead.io/courses/(.*)', course)
				folder = 'egghead - ' + str_obj.group(1)
				print(str_obj.group(1))
				os.makedirs(folder, 0777)
				os.chdir(folder)
				subprocess.check_call('egghead-downloader -e {0} -p {1} -c {2}'.format(EMAIL, PASSWORD, course), shell=True)
				os.chdir(DIRECTORY + '{}'.format(name))
				courses_db.append(course)

		database[name] = courses_db

	os.chdir(TOP_DIRECTORY)

	writeFile(database)


if __name__ == '__main__':
	main()
