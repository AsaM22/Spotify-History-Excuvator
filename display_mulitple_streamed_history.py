import json
from collections import Counter
import glob


###################### CHANGE THIS NUMBER FROM (0-2) ######################
METHOD = 2
# 0: Artist 		(Most played artist)
# 1: Track/Artist 	(Track then Artist)
# 2: Artist/Tarck	(Artist then Track)



def main():

	# Folder path with streaming history files in it
	folder_path = "/Users/asa/Desktop/Code/SpotifyDisplayer"

	# Creates a list to append all the songs to
	myList = list()

	# Finds the total number of StreamingHistory files
	file_count = len(glob.glob1(folder_path, "StreamingHistory*.json"))


	# Loops through the amout of files you have (example: 4 loops)
	for count in range(file_count):

		# Changes file path
		_file_path = f"{folder_path}/StreamingHistory{str(count)}.json"

		# Gets the raw json data
		with open(_file_path) as f:
			data = json.load(f)


		# Append based on the selected choice
		for i in data:
			if METHOD == 0: myList.append(i["artistName"])
			elif METHOD == 1: myList.append(f"{i['trackName']}  ---  {i['artistName']}")
			elif METHOD == 2: myList.append(f"{i['artistName']}  ---  {i['trackName']}")


	# Counts how many of each song is played
	counted_data = Counter(myList)

	# Sorts the list (asending)
	sorted_data = {k: v for k, v in sorted(counted_data.items(), key=lambda item: item[1])}


	# Displays the sorted list (#TimesPlayed/Artist/SongTitle)
	for i in sorted_data:
		print(sorted_data[i], "-", i)


if __name__ == "__main__":
	main()
