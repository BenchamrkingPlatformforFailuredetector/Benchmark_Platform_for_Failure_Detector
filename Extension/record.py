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
        """
        This method is used to calculate the sum of all arrival times stored in the data structure. It is necessary since
        Chen's and Bertier's algorithms both require this function to calculate the next expected arrival time.

        Args:
            None

        Returns:
            int: The sum of all arrival time stored in the data structure
        """
        return self.sum

    def get_length(self):
        """
        This method is used to calculate the current length of the data structure. It works together with get_sum function
        to calculate the next expected arrival time

        Args:
            None

        Returns:
            int: If the number of existing arrival time doesn't reach the max length of the data structure, which is defined
            by the user as the parameter 'n', it returns the current number of arrival time stored in the data structure.
            Else, it returns the max length of the data structure
        """
        return self.current_length

    def get_latest_one(self):
        """
        This method is used to get the latest arrival time in the data structure.

        Args:
            None

        Returns:
            int: The latest arrival time in the data structure
        """
        return self.array[self.end_pointer - 1]

    def append(self, a):
        """
        This method is used to add new arrival time into the data structure. If the current length of this data structure
        doesn't reach the max length of the data structure, this method will append the new arrival time into the data
        structure. Else, it will firstly pop out the earliest arrival time stored in the data structure and then append
        the new arrival time into the data structure. Moreover, during thr process of appending, this method also
        calculate the difference between adjacent arrival times.

        Args:
            a (int): next arrival time

        Returns:
            int: the earliest arrival time stored in the data structure
        """
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
        """
        This method is used to demonstrate the data structure as an numpy array.

        Args:
            None

        Returns:
            np.array: The data structure shown as numpy.array
        """
        if self.current_length < self.max_length:
            return self.array[self.start_pointer:self.end_pointer]
        else:
            return np.concatenate((self.array[self.start_pointer:], self.array[:self.end_pointer]), axis=0)

    def get_difference(self):
        """
        This method is used to show the difference between adjacent arrival times.

        Args:
            None

        Returns:
            np.array: The difference between adjacent arrival times shown as np.array
        """
        difference = self.difference[self.difference >= 0]
        return difference

    def get_jitter(self, epsilon, next_expected_arrival_time):
        """
        This method is used to show whether there is a jitter here. It works as the following way:
        if the absolute value of the difference between next expected arrival time
        (calculated by a specific failure detector algorithm) and the latest arrival time is bigger than epsilon,
        then we say there exists a jitter and returns True. Else, we say the network signal is kind of stable and return
        False.

        Args:
            epsilon (int): the value given by the user as a thereshold for the jitter.
            next_expected_arrival_time (int): The next expected heartbeat signal arrival time calculated by a specific
            failure detector

        Returns:
            Bool: determine whether there exists a jitter in the network enviornment.
        """
        arrival = self.get_latest_one()
        if abs(next_expected_arrival_time - arrival) > epsilon:
            return True
        else:
            return False


if __name__ == '__main__':
    record = Record(5)
    l = [5, 8, 10, 15, 21, 30, 33, 40, 50, 61]
    for i in l:
        record.append(i)
        print(record.get_difference())
