import numpy as np

from Extension._record import AbstractRecord


class Record(AbstractRecord):
    """
    This data structure is used to store the actual arrival time. The length of this
    data structure is defined by the users as the parameter 'n'. It works as the following:
    This data structure only supports users to append new arrival times. If this structure is not full,
    the append behaviour is like the list. If this structure is full already, then it will dump the earliest
    arrival times and append the new arrival time into the structure.
    """

    def __init__(self, n):
        self.sum = 0
        self.max_length = n
        self.current_length = 0
        self.array = np.zeros(n, dtype=float)
        self.start_pointer = 0
        self.end_pointer = 0
        self.difference = np.array([float('-inf') for _ in range(n - 1)])
        self.start_pointer_difference = 0
        self.end_pointer_difference = 0

    def get_sum(self):
        return self.sum

    def get_length(self):
        return self.current_length

    def get_latest_one(self):
        return self.array[self.end_pointer - 1]

    def append(self, a):
        if self.current_length < self.max_length:
            self.array[self.end_pointer] = a
            self.end_pointer = (self.end_pointer + 1) % self.max_length
            self.current_length += 1
            self.sum += a
            if self.current_length > 1:
                origin = self.array[(self.end_pointer - 2) % self.max_length]
                difference = a - origin
                self.difference[self.end_pointer_difference] = difference
                self.end_pointer_difference = (self.end_pointer_difference + 1) % (self.max_length - 1)

        else:
            earliest_value = self.array[self.start_pointer]
            self.array[self.start_pointer] = a
            self.start_pointer = (self.start_pointer + 1) % self.max_length
            self.end_pointer = (self.end_pointer + 1) % self.max_length
            self.sum = self.sum + a - earliest_value
            if self.current_length > 1:
                origin = self.array[(self.end_pointer - 2) % self.max_length]
                difference = a - origin
                self.difference[self.start_pointer_difference] = difference
                self.end_pointer_difference = (self.end_pointer_difference + 1) % (self.max_length - 1)
                self.start_pointer_difference = (self.start_pointer_difference + 1) % (self.max_length - 1)
            return earliest_value

    def get_array(self):
        if self.current_length < self.max_length:
            return self.array[self.start_pointer:self.end_pointer]
        else:
            return np.concatenate((self.array[self.start_pointer:], self.array[:self.end_pointer]), axis=0)

    def get_difference(self):
        difference = self.difference[self.difference >= 0]
        return difference

    def get_jitter(self, epsilon):
        self.arrival_time = 90
        self.estimated_arrival_time = 80
        if abs(self.estimated_arrival_time - self.arrival_time) > epsilon:
            return True
        return False


if __name__ == '__main__':
    record = Record(5)
    l = [5, 8, 10, 15, 21, 30, 33, 40, 50, 61]
    for i in l:
        record.append(i)
        print(record.get_difference())
