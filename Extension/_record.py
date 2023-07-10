from abc import ABC, abstractmethod


class AbstractRecord(ABC):
    # Abstract class for Record data structure

    @abstractmethod
    def get_sum(self):
        raise NotImplementedError("abstract method 'get_sum' not implemented")

    @abstractmethod
    def get_length(self):
        raise NotImplementedError("abstract method 'get_length' not implemented")

    @abstractmethod
    def get_latest_one(self):
        raise NotImplementedError("abstract method 'get_latest_one' not implemented")

    @abstractmethod
    def append(self):
        raise NotImplementedError("abstract method 'append' not implemented")

    @abstractmethod
    def get_array(self):
        raise NotImplementedError("abstract method 'get_array' not implemented")

    @abstractmethod
    def get_difference(self):
        raise NotImplementedError("abstract method 'get_difference' not implemented")

    @abstractmethod
    def get_jitter(self):
        raise NotImplementedError("abstract method 'get_jitter' not implemented")
