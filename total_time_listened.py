import json


def main():

    # File Path to Streaming History
    _file_path = "StreamingHistory0.json"

    # Initalize filepath
    sum = 0

    # Gets the raw json data
    with open(_file_path, "r") as f:
        data = json.load(f)

        # Loop through data and add to sum
        for i in data:
            sum += i["msPlayed"]

    # Display results 
    print("You've listened for:")
    print(sum, "ms")
    print('{:.2f}'.format(sum/1000), "Seconds")
    print('{:.2f}'.format(sum/60000), "Mins")
    print('{:.2f}'.format(sum/3600000), "Hours")
    print('{:.2f}'.format(sum/86400000), "Days")
    print('{:.2f}'.format(sum/604800000), "Weeks")
    print('{:.2f}'.format(sum/2628000000), "Months")


if __name__ == "__main__":
    main()
