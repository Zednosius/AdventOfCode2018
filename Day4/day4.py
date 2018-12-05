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
    pprint(guards)
    return guards, guard_minutes


if __name__ == '__main__':
    with open("input.txt", 'r') as f:
        events = []
        for line in f:
            events.append(parse(line))
        events.sort(key=lambda x: x[0])
        guard_patterns, guard_minutes = analyze_sleep(events)
        sleepiest = max(guard_minutes.items(), key=lambda x: x[1])
        sleepy_id = sleepiest[0]
        print(guard_patterns[sleepiest])
        sleepys_most_sleepy_minute = max(guard_patterns[sleepy_id].items(), key=lambda x: x[1])[0]

        # Part one
        print("The sleepiest is {} with {} minutes".format(*sleepiest))
        print("They fell asleep most often during minute {}".format(sleepys_most_sleepy_minute))
        print("The answer is: {}".format(sleepys_most_sleepy_minute*int(sleepy_id)))

        # Part 2
