#!/usr/bin/python3

import re
import sys

class Guard:
    def __init__(self, gid):
        self.gid = gid
        self.sleep_start = None
        self.schedule = [0] * 60
        self.total_sleep_time = 0
    def sleep(self, timestamp):
        if self.sleep_start is not None:
            print('Guard', gid, 'is already sleeping!')
        self.sleep_start = timestamp
    def wakeup(self, timestamp):
        if self.sleep_start is None:
            print('Guard', gid, 'is not sleeping!')
        duration = timestamp - self.sleep_start
        self.total_sleep_time += duration
        for i in range(self.sleep_start % 100, timestamp % 100):
            self.schedule[i] += 1
        self.sleep_start = None
    def sleepiest_minute(self):
        times_slept = max(self.schedule)
        minute = self.schedule.index(times_slept)
        return (minute, times_slept)
        
def parse_number(text):
    num = 0
    for ch in text:
        if ch.isdigit():
            num = num * 10 + int(ch)
    return num

with open('../input/04.txt') as infile:
    events = [(parse_number(line[1:17]), line[19:-1]) for line in infile]
    events.sort(key=lambda event: event[0])

guards = {}
current_guard = None

for timestamp, event in events:
    if event.startswith('Guard'):
        gid = parse_number(event)
        if gid not in guards:
            guards[gid] = Guard(gid)
        current_guard = guards[gid]
    elif event.startswith('falls'):
        current_guard.sleep(timestamp)
    elif event.startswith('wakes'):
        current_guard.wakeup(timestamp)
        
data = []
for guard in guards.values():
    minute, times_slept = guard.sleepiest_minute()
    data.append((guard.gid, minute, times_slept, guard.total_sleep_time))

sleepiest_guard = sorted(data, key=lambda guard: guard[3])[-1]
print(sleepiest_guard[0] * sleepiest_guard[1])

sleepiest_minute = sorted(data, key=lambda guard: guard[2])[-1]
print(sleepiest_minute[0] * sleepiest_minute[1])
