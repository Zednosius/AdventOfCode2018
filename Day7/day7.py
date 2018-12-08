import re
from collections import defaultdict
from bisect import insort
from copy import copy, deepcopy
matcher = re.compile("Step (.*?) must be finished before step (.*?) can begin.")


def parse(line):
    m = matcher.match(line)
    return m.group(1), m.group(2)


def get_unlocked(step, locks, unlock_chain):
    for new_step in unlock_chain[step]:  # Go through steps that might be unlocked
        locks[new_step].discard(step)  # Removed completed step from locks
        if len(locks[new_step]) == 0:  # If no locks we can add it to our available steps
            yield new_step


def part1(locks, unlock_chain):
    step_list = sorted(list(unlock_chain[None]))
    seen = set(step_list)
    completed_order = []

    while len(step_list) > 0:
        step = step_list.pop(0)
        completed_order.append(step)

        for unlocked_step in get_unlocked(step, locks, unlock_chain):
            seen.add(unlocked_step)  # Unnecessary?
            insort(step_list, unlocked_step)
    print("Construction order is: ", "".join(completed_order))


def step_time(step):
    return ord(step)-4


def make_worker(time, letter):
    for i in range(time):
        yield None if i < time-1 else letter


def part2(locks, unlock_chain):
    step_list = sorted(list(unlock_chain[None]))
    completed_order = []
    workers = set()
    t = 0
    while len(completed_order) < 26:
        # Add workers until we have 5 or there are no steps that can be done.
        while len(workers) < 5 and len(step_list) > 0:
            letter = step_list.pop(0)
            workers.add(make_worker(step_time(letter), letter))

        done_workers = set()
        for worker in workers:
            out = next(worker)  # See if worker outputs
            if out:  # If output, worker is done
                done_workers.add(worker)  # Add to remove worker
                completed_order.append(out)
                # Add the newly unlocked steps to list
                for unlocked_step in get_unlocked(out, locks, unlock_chain):
                    insort(step_list, unlocked_step)

        workers -= done_workers
        t += 1
    print("TIME: ", t)


if __name__ == '__main__':
    unlock_chain = defaultdict(set)
    unlock_chain[None] = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    locks = defaultdict(set)

    with open("input.txt", "r") as f:
        for line in f:
            before, step = parse(line)
            # Mapping of a step to the steps that are unlocked
            unlock_chain[None].discard(step)
            unlock_chain[before].add(step)
            # Mapping of a step to all its locks
            locks[step].add(before)

    part1(deepcopy(locks), deepcopy(unlock_chain))
    part2(deepcopy(locks), deepcopy(unlock_chain))
