import requests
import argparse
import json
import csv
import unicodedata

class spotifyApp():
	def __init__(self):
		self.accessToken = ""
		self.client_id = '8a14ebc91cf34265b1acbfb777b946ab'
		self.client_secret = 'fe7ad45553294aff829b4a101f059fb5'
		self.scope = 'playlist-modify-public playlist-modify-private playlist-read-collaborative'
		self.refresh_token =  'AQAsQJRqXNVHkMsfAtvKciUg8LuinmLEi92NnDXDk2ePwsIJMc14Qci6Lhk7F-oAXOkOIcTnSJOOdMumR4yOMLVX8IbmRCzxIKZJ7jgytLwxAaEfYcY6pZMURNfCINJfwxs'
		self.excelheader = [
							'Year',
							'Artist',
							'Album',
							'Url',
							'Popularity'
							]

	def get_access_token(self):
		url = 'https://accounts.spotify.com/api/token'
		payload = {
		'grant_type': 'refresh_token',
		'refresh_token': self.refresh_token
		}
		auth = (self.client_id, self.client_secret)
		token = requests.post(url, data=payload, auth=auth).json()
		self.accessToken = token['access_token']
		return

	def getData(self,year, quantify, outputpath):
		csvfile = open(outputpath, 'w', newline='\n', encoding="utf-8-sig")#utf-8-sig, utf8
		writer = csv.DictWriter(csvfile, delimiter=",", fieldnames=self.excelheader)
		writer.writeheader()
		for i in range(0, quantify, 50):
			self.get_access_token()
			print('-------------{}'.format(i))
			headers = {'Origin': 'https://open.spotify.com',
						'Accept-Encoding': 'gzip, deflate, br',
						'Accept-Language': 'en',
						'Authorization': 'Bearer ' + self.accessToken,
						'Accept': 'application/json',
						# 'Referer': 'https://open.spotify.com/search/albums/year^%^3A1980',
						'Authority': 'api.spotify.com',
						'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}

			response = requests.get('https://api.spotify.com/v1/search?query=year%3A{}&type=album&include_external=audio&market=US&offset={}&limit=50'.format(year, i), headers=headers).json()
			
			try:
				data = response['albums']
			except:
				print(response)
				continue

			for album in response['albums']['items']:

				output = {
						'Year':'',
						'Artist':'',
						'Album':'',
						'Url':'',
						'Popularity':''
				}

				varyear = year
				try:
					varartist = album['artists'][0]['name']
				except:
					varartist = ""

				try:
					varalbum = album['name']
				except:
					varalbum = ""

				try:
					varurl = album['external_urls']['spotify']
				except:
					varurl = ""

				try:
					varhref = album['href']

					#get Popularity
					pheaders = {'Origin': 'https://open.spotify.com',
								'Accept-Encoding': 'gzip, deflate, br',
								'Accept-Language': 'en',
								'Authorization': 'Bearer ' + self.accessToken,
								'Accept': 'application/json',
								'Referer': 'https://open.spotify.com/search/albums/year^%^3A1980',
								'Authority': 'api.spotify.com',
								'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
					presponse = requests.get(varhref, headers=headers).json()
					
					try:
						varpopularity = presponse['popularity']
					except:
						varpopularity = 0
				except:
					varpopularity = 0

				print("Year:{}, Artist:{}, Album:{}, Url:{}, Popularity:{}".format(varyear, varartist, varalbum, varurl,varpopularity))

				# write the data to excel
				output['Year'] = varyear
				output['Artist'] = varartist
				output['Album'] = varalbum
				output['Url'] = varurl
				output['Popularity'] = varpopularity

				writer.writerow(output)

		csvfile.close()


def startProcess():
	parser = argparse.ArgumentParser()
	parser.add_argument("-y", "--year", default=1980, type=int)
	parser.add_argument("-q", "--quantify", default=100, type=int)
	parser.add_argument("-o", "--outputpath", default='output.csv', type=str)
	args = parser.parse_args()
	app = spotifyApp()
	app.getData(args.year, args.quantify, args.outputpath)

if __name__=="__main__":
	startProcess()
	print("------------finish------------")