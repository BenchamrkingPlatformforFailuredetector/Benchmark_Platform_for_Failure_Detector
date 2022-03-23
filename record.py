import numpy as np


class Record:
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

        else:
            earliest_value = self.array[self.start_pointer]
            self.array[self.start_pointer] = a
            self.start_pointer = (self.start_pointer + 1) % self.max_length
            self.end_pointer = (self.end_pointer + 1) % self.max_length
            self.sum = self.sum + a - earliest_value
            return earliest_value

    def get_array(self):
        if self.current_length < self.max_length:
            return self.array[self.start_pointer:self.end_pointer]
        else:
            return np.concatenate((self.array[self.start_pointer:], self.array[:self.end_pointer]), axis=0)


if __name__ == '__main__':
    record = Record(10)
    for i in range(10):
        record.append(i)
        print(record.get_array())
        print(record.get_sum())
    for i in range(10, 20):
        record.append(i)
        print(record.get_array())
        print(record.get_sum())