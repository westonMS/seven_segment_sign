import re
from selectors import DefaultSelector
import requests
import json
import datetime
import math


class Text_Scroll:
    """This is a boilerplate class for creating new demos/games for the SSS platform. It needs to include definitions for the following functions: init, run, stop.
    The init function needs to at least have the things shown below. Frame rate is in frames per second and demo time is in seconds. Demo time should be None if it is a game.
    The run function yields a generator. This generator will be called a specified frame rate, this controls what is being pushed to the screen.
    The stop function is called when the demo/game is being exited by the upper SSS software. It should reset the state for the game"""

    # User input is passed through input_queue
    # Game output is passed through output_queue
    # Screen updates are done through the screen object
    def __init__(self, input_queue, output_queue, screen):
        # Provide the framerate in frames/seconds and the amount of time of the demo in seconds
        self.frame_rate = 4
        self.demo_time = 300  # None for a game
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.screen = screen
        self.x = self.changeText()
        # init demo/game specific variables here
        # TICKER
        self.defaultSymbol = [
            "BA",
            "IBM",
            "AAPL",
            "GOOGL",
            "DIS",
            "NKE",
            "FB",
            "NFLX",
            "F",
            "AMZN",
            "MSFT",
            "TSLA",
            "MCD",
        ]
        (
            self.first_line,
            self.second_line,
            self.third_line,
            self.extra_line_one,
            self.extra_line_two,
        ) = superLines(self)
        self.first_line_text = ""
        self.second_line_text = ""
        self.third_line_text = ""
        self.extra_line_one_text = ""
        self.extra_line_two_text = ""
        # INFOBOX
        self.info_box_symbol = "IBM"
        self.info_box_name = ""
        self.info_box_open = ""
        self.info_box_close = ""
        self.info_box_percent = ""
        self.counter = counter()
        self.infobox = setupINFOBOX(self)
        self.graph = []

    def changeText(self):
        first_ind = 0
        last_ind = 47
        while True:
            self.first_line_text = self.first_line[first_ind:last_ind]
            self.second_line_text = self.second_line[first_ind:last_ind]
            self.third_line_text = self.third_line[first_ind:last_ind]
            self.extra_line_one_text = self.extra_line_one[first_ind:last_ind]
            self.extra_line_two_text = self.extra_line_two[first_ind:last_ind]
            first_ind += 1
            last_ind += 1

            if len(self.first_line) == last_ind:
                first_ind = 0
                last_ind = 47
            yield

    def run(self):
        for i in self.defaultSymbol:
            addCompanyData(i)
        # Create generator here
        next(self.infobox)
        while True:
            counter_value = next(self.counter)
            if counter_value == 16:
                next(self.infobox)
                print("Next")
                print(self.info_box_name)
                print(self.info_box_symbol)
            # -- Ticker --
            # Causes text to scroll
            next(self.x)

            # TOP LINE TICKER
            self.screen.draw_hline(start_y=3, start_x=0, length=48, push=True)
            # BOTTOM LINE TICKER
            self.screen.draw_hline(start_y=15, start_x=0, length=48, push=True)
            # GRAPH LINE
            self.screen.draw_hline(start_y=44, start_x=18, length=22, push=True)
            self.screen.draw_vline(start_y=-26, start_x=18, length=22, push=True)
            # First line ticker
            self.screen.draw_text(
                self.screen.x_width // 2 - 24,
                self.screen.y_height // 2 - 20,
                self.first_line_text,
                push=False,
            )
            # Second line Ticker
            self.screen.draw_text(
                self.screen.x_width // 2 - 24,
                self.screen.y_height // 2 - 18,
                self.extra_line_one_text,
                push=False,
            )
            # Third Line Ticker
            self.screen.draw_text(
                self.screen.x_width // 2 - 24,
                self.screen.y_height // 2 - 16,
                self.second_line_text,
                push=False,
            )
            # Fourth Line Ticker
            self.screen.draw_text(
                self.screen.x_width // 2 - 24,
                self.screen.y_height // 2 - 14,
                self.extra_line_two_text,
                push=False,
            )
            # Fifth Line Ticker
            self.screen.draw_text(
                self.screen.x_width // 2 - 24,
                self.screen.y_height // 2 - 12,
                self.third_line_text,
                push=False,
            )
            ## -- Info Box and Graph --

            # Reset Company Name
            self.screen.draw_text(
                self.screen.x_width // 2 - 24,
                self.screen.y_height // 2 - 6,
                " " * 36,
                push=False,
            )
            # Company Name
            self.screen.draw_text(
                self.screen.x_width // 2 - 20,
                self.screen.y_height // 2 - 6,
                self.info_box_name,
                push=False,
            )
            # Graph
            l = 4
            for i in self.graph:
                self.screen.draw_text(
                    self.screen.x_width // 2 - 4,
                    self.screen.y_height // 2 - l,
                    i,
                    push=False,
                )
                l -= 2
            self.screen.draw_text(
                self.screen.x_width // 2 - 0,
                self.screen.y_height // 2 - -22,
                "1 Day GRAPH",
                push=False,
            )
            # Daily Numbers
            self.screen.draw_text(
                self.screen.x_width // 2 - 22,
                self.screen.y_height // 2 - -4,
                "OPEN: " + self.info_box_open,
                push=False,
            )
            self.screen.draw_text(
                self.screen.x_width // 2 - 22,
                self.screen.y_height // 2 - -6,
                "CLOSE: " + self.info_box_close,
                push=False,
            )
            self.screen.draw_text(
                self.screen.x_width // 2 - 22,
                self.screen.y_height // 2 - -8,
                "CHANGE: " + self.info_box_percent,
                push=False,
            )
            # Company Symbol
            self.screen.draw_text(
                self.screen.x_width // 2 - 20,
                self.screen.y_height // 2 - 2,
                self.info_box_symbol,
                push=True,
            )
            yield

    def stop(self):
        # Reset the state of the demo if needed, else leave blank
        pass

    def get_input_buff(self):
        # Get all input off the queue
        return list(self.input_queue.queue)


# Code to Get Stock Market Data


def getDate():
    date = datetime.date.today()
    date = str(date)
    return date


def getYesterday():
    date = datetime.date.today()
    date = date - datetime.timedelta(days=1)
    return str(date)


# Make the API call and make sure it is valid
def getNumbers(symbol):
    url = (
        "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=%s&apikey=AVLP38QDYPWJ4NEP"
        % symbol
    )
    print(url)
    r = requests.get(url)
    print(r.status_code)
    if r.status_code != 200:
        return 1
    data = r.json()
    date = getDate()
    try:
        name = data["Meta Data"]["2. Symbol"]
    except:
        return 1
    try:
        open_value = data["Time Series (Daily)"][date]["1. open"]
        close = data["Time Series (Daily)"][date]["4. close"]
    except:
        print("Yesterday")
        date = getYesterday()
        open_value = data["Time Series (Daily)"][date]["1. open"]
        close = data["Time Series (Daily)"][date]["4. close"]
    temp = [open_value, close, date]
    return temp


# Takes in a list of data and puts it into the json
def setData(symbol, numbers):
    print(symbol)
    print(numbers)
    open_value = numbers[0]
    close = numbers[1]
    date = numbers[2]
    with open("demos/text_scroll/data.json", "r+") as f:
        data = json.load(f)
        temp = data["symbols"]
        date = getDate()
        try:
            numbers[1]
        except:
            return 1
        data["symbols"] = temp  # <--- add `id` value.
        data["symbols"][symbol]["open"] = open_value
        data["symbols"][symbol]["close"] = close
        data["symbols"][symbol]["date"] = date
        f.seek(0)  # <--- should reset file position to the beginning.
        json.dump(data, f, indent=4)
        f.truncate()  # remove remaining part


# If stock symbol is not in json create a template for it
def addSymbol(symbol):
    with open("demos/text_scroll/data.json", "r+") as f:
        data = json.load(f)
        try:
            data["symbols"][symbol]
        except:
            temp = data["symbols"]
            values = {"open": 1, "close": 1, "date": 1}
            temp[symbol] = values
            data["symbols"] = temp  # <--- add `id` value.
            f.seek(0)  # <--- should reset file position to the beginning.
            json.dump(data, f, indent=4)
            f.truncate()  # remove remaining part


def dateCheck(symbol):
    with open("demos/text_scroll/data.json", "r+") as f:
        data = json.load(f)
        date = data["symbols"][symbol]["date"]
        if date != getDate() and date != getYesterday():  # Neither date is right
            return False
        else:
            return True


def getData(symbol):
    addSymbol(symbol)
    if not dateCheck(symbol):  # If its not up to date, reload the data
        print("UPDATING SMTH")
        data = getNumbers(symbol)  # Get the data
        if type(data) is list:  # If its a list update
            setData(symbol, data)
        getINTRADAY(symbol)

    else:
        print("Up to date")


def makeLines(symbol):
    # Get Variables
    open_value = 0
    close_value = 0
    with open("demos/text_scroll/data.json", "r") as f:
        data = json.load(f)
        open_value = float(data["symbols"][symbol]["open"])
        close_value = round(float(data["symbols"][symbol]["close"]), 3)
    difference = close_value - open_value
    percentage = round(100 * (close_value / open_value - 1), 3)
    return symbol, str(close_value), str(open_value), str(difference), str(percentage)


def superLines(self):
    line1 = ""
    line2 = ""
    line3 = ""
    line4 = ""
    line5 = ""
    spaces = 10
    for i in self.defaultSymbol:
        getData(i)
        values = makeLines(i)
        whitespace = spaces - len(values[0])
        line1 += whitespace * " " + values[0]
        # print(line1)
        whitespace = spaces - len(values[1])
        line2 += whitespace * " " + values[1]
        # print(line2)
        whitespace = spaces - 1 - len(values[4])
        line3 += whitespace * " " + values[4] + "%"
        line4 += spaces * " "
        line5 += spaces * " "
        if float(values[4]) > 0:
            line1 += "     8    l"
            line4 += "    888   l"
            line2 += "   88888  l"
            line3 += "     8    l"
            line5 += "     8    l"
        else:
            line1 += "     8    l"
            line4 += "     8    l"
            line2 += "   88888  l"
            line5 += "    888   l"
            line3 += "     8    l"
        # print(line3)
    line1 += line1 * 10
    line2 += line2 * 10
    line3 += line3 * 10
    line4 += line4 * 10
    line5 += line5 * 10

    return line1, line2, line3, line4, line5


def addCompanyData(symbol):
    try:
        with open("demos/text_scroll/data.json", "r+") as f:
            data = json.load(f)
            data["symbols"][symbol]["Name"]
    except:
        print("Finding " + symbol + " name")
        url = (
            "https://www.alphavantage.co/query?function=OVERVIEW&symbol=%s&apikey==AVLP38QDYPWJ4NEP"
            % symbol
        )
        r = requests.get(url)
        name = r.json()
        with open("demos/text_scroll/data.json", "r+") as f:
            data = json.load(f)
            try:
                print(name["Name"])
                # print("Updating JSON")
                data["symbols"][symbol]["Name"] = name["Name"]
                f.seek(0)  # <--- should reset file position to the beginning.
                json.dump(data, f, indent=4)
                f.truncate()  # remove remaining part
            except:
                pass


def counter():
    i = 0
    while True:
        i += 1
        yield i
        if i > 20:
            i = 0


def setupINFOBOX(self):
    hours = [
        "10:00:00",
        "11:00:00",
        "12:00:00",
        "13:00:00",
        "14:00:00",
        "15:00:00",
        "16:00:00",
        "17:00:00",
        "18:00:00",
        "19:00:00",
    ]
    while True:
        for i in self.defaultSymbol:
            if not dateCheck(i):
                getData(i)
                getINTRADAY(i)
            self.graph = makeGraph(i)
            with open("demos/text_scroll/data.json", "r+") as f:
                try:
                    # Get Name
                    data = json.load(f)
                    self.info_box_symbol = i + " " * 6
                    self.info_box_name = data["symbols"][i]["Name"]
                    self.info_box_name = self.info_box_name.upper()
                    open_value = round(float(data["symbols"][i]["open"]), 3)
                    close_value = round(float(data["symbols"][i]["close"]), 3)
                    self.info_box_open = str(open_value)
                    self.info_box_close = str(close_value)
                    self.info_box_percent = (
                        str(
                            round(
                                100 * (close_value / open_value - 1),
                                3,
                            )
                        )
                        + "%"
                    )

                except:
                    continue
            yield

    pass


def getINTRADAY(symbol):
    print("INTRADAY")
    date = getDate()
    yesterday = getYesterday()
    hours = [
        "10:00:00",
        "11:00:00",
        "12:00:00",
        "13:00:00",
        "14:00:00",
        "15:00:00",
        "16:00:00",
        "17:00:00",
        "18:00:00",
        "19:00:00",
    ]
    url = (
        "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=%s&interval=60min&apikey=AVLP38QDYPWJ4NEP"
        % symbol
    )
    r = requests.get(url)
    data = r.json()
    json_formatted_str = json.dumps(data, indent=2)
    # print(json_formatted_str)
    values = []
    try:
        for i in hours:
            time = date + " " + i
            print(data["Time Series (60min)"][time]["1. open"])
            values.append(float(data["Time Series (60min)"][time]["1. open"]))
    except:
        try:
            for i in hours:
                date = yesterday
                time = date + " " + i
                print(data["Time Series (60min)"][time]["1. open"])
                values.append(float(data["Time Series (60min)"][time]["1. open"]))
        except:
            pass
    # print(values)
    # print((max(values)))
    # print(min(values))
    try:
        maximum = max(values)
    except:
        print("API Call Failed")
        return 1
    minimum = min(values)
    line_height = 10
    line_width = (maximum - minimum) / line_height
    heights = []
    for i in values:
        heights.append(math.ceil((i - minimum) / line_width))
    for i in range(len(values)):
        with open("demos/text_scroll/data.json", "r+") as f:
            data = json.load(f)
            hour = hours[i]
            value = values[i]
            data["symbols"][symbol][hour] = value
            print(data["symbols"][symbol][hours[i]])
            f.seek(0)  # <--- should reset file position to the beginning.
            json.dump(data, f, indent=4)
            f.truncate()  # remove remaining part
    print("Updated all of those cool things.")


def makeGraph(symbol):
    hours = [
        "10:00:00",
        "11:00:00",
        "12:00:00",
        "13:00:00",
        "14:00:00",
        "15:00:00",
        "16:00:00",
        "17:00:00",
        "18:00:00",
        "19:00:00",
    ]
    values = []
    print(symbol)
    with open("demos/text_scroll/data.json", "r+") as f:
        data = json.load(f)
        for i in range(len(hours)):
            try:
                x = data["symbols"][symbol]["Name"]
                values.append(data["symbols"][symbol][hours[i]])
            except:
                print("Invalid Hour " + hours[i])
                continue
    try:
        maximum = max(values)
        # print(maximum)
    except:
        return 1
    minimum = min(values)
    line_height = 10
    # print(minimum)
    line_width = (maximum - minimum) / line_height
    heights = []
    for i in values:
        heights.append(math.ceil((i - minimum) / line_width))
    # print(heights)
    lines = ["" for i in range(line_height + 1)]
    h = 0
    for j in heights:
        for i in range(len(lines)):
            lines[i] += "  "
            # print(i)
            # print(j)
            if i == j:
                lines[i] = lines[i][:-2]
                lines[i] += "__"
        try:
            print(heights[h])
            print(heights[h + 1])
            if heights[h] < heights[h + 1]:
                print("CHANGING TO L")
                lines[heights[h]] = lines[heights[h]][:-1]
                lines[heights[h]] += "j"
                for z in range(heights[h] + 1, heights[h + 1]):
                    lines[z] = lines[z][:-1]
                    lines[z] += "1"
                pass
            elif heights[h] > heights[h + 1]:
                lines[heights[h + 1]] = lines[heights[h + 1]][:-1]
                lines[heights[h + 1]] += "1"
                lines[heights[h] - 1] = lines[heights[h] - 1][:-1]
                lines[heights[h] - 1] += "1"
                for c in range(2, 10):
                    if heights[h] - c > heights[h + 1]:
                        lines[heights[h] - c] = lines[heights[h] - c][:-1]
                        lines[heights[h] - c] += "1"
                print("Height A" + str(heights[h]) + "Height B" + str(heights[h + 1]))
        except:
            pass
        h += 1
    lines.reverse()
    for i in lines:
        print(i)
    print(lines)
    return lines
