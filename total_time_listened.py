import json


def main():

    # File Path to Streaming History
    _file_path = "TestData/StreamingHistory0.json"

    # Initalize total
    total_listened = 0

    # Gets the raw json data
    with open(_file_path, "r", encoding="utf8") as f:
        data = json.load(f)

        # Loop through data and add to total_listened
        for i in data:
            total_listened += i["msPlayed"]

    # Display results 
    print("You've listened for:")
    print(total_listened, "ms")
    print('{:.2f}'.format(total_listened/1000), "Seconds")
    print('{:.2f}'.format(total_listened/60000), "Mins")
    print('{:.2f}'.format(total_listened/3600000), "Hours")
    print('{:.2f}'.format(total_listened/86400000), "Days")
    print('{:.2f}'.format(total_listened/604800000), "Weeks")
    print('{:.2f}'.format(total_listened/2628000000), "Months")


if __name__ == "__main__":
    main()
