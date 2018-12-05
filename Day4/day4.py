import re
import time
from collections import defaultdict as ddict
from pprint import pprint
from datetime import datetime, date

matcher = re.compile("\\[(.+)\\] (.+)")
guardnum = re.compile(r".*#(\d+).*")


def parse(s):
    match = matcher.match(s)
    datestr = match.group(1)
    event = match.group(2)

    # ex. 1518-05-12 00:39
    timestamp = datetime.strptime(datestr, "%Y-%m-%d %H:%M")
    if event == "wakes up":
        return (timestamp, "wake")
    elif event == "falls asleep":
        return (timestamp, "sleep")
    else:
        return (timestamp, guardnum.match(event).group(1))


def analyze_sleep(events):
    guards = ddict(lambda: ddict(int))
    guard_minutes = ddict(int)
    current_guard = None
    asleep_time = None
    for event in events:
        if event[1] == "wake":
            slept_time = event[0] - asleep_time
            slept_minutes = slept_time.seconds//60
            guard_minutes[current_guard] += slept_minutes
            for t in range(slept_minutes):
                guards[current_guard][asleep_time.minute + t] += 1

        elif event[1] == "sleep":
            asleep_time = event[0]

        else:
            current_guard = event[1]
            print(current_guard)

    return guards, guard_minutes


def find_max_minute(guard_patterns):
    d = {}
    for guard in guard_patterns.items():
        d[guard[0]] = max(guard[1].items(), key=lambda x: x[1])
    return d


if __name__ == '__main__':
    with open("input.txt", 'r') as f:
        events = []
        for line in f:
            events.append(parse(line))
        events.sort(key=lambda x: x[0])
        guard_patterns, guard_minutes = analyze_sleep(events)

        sleepiest = max(guard_minutes.items(), key=lambda x: x[1])
        sleepy_id = sleepiest[0]

        sleepys_most_sleepy_minute = max(guard_patterns[sleepy_id].items(), key=lambda x: x[1])[0]

        # Part one
        print("The sleepiest is {} with {} minutes".format(*sleepiest))
        print("They fell asleep most often during minute {}".format(sleepys_most_sleepy_minute))
        print("The answer is: {}".format(sleepys_most_sleepy_minute*int(sleepy_id)))
        # Part 2
        for e in guard_patterns.items():
            print(e[0], e[1])
            print(e[1].items())
        max_minutes = find_max_minute(guard_patterns)

        # Access the minute tuple and then access the count
        most_regular = max(max_minutes.items(), key=lambda x: x[1][1])

        # most_regular = max(guard_patterns.items(), key=lambda guard_shift: max(
        # guard_shift[1].items(), key=lambda minute: minute[1]))
        print()
        most_regular_guard = int(most_regular[0])
        most_regular_minute = most_regular[1][0]
        print("The most regular was {} at minute {}".format(most_regular_guard, most_regular_minute))
        print("Answer: {}".format(most_regular_guard*most_regular_minute))
