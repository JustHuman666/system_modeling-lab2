import numpy as np

from element import Element


class Process(Element):
    def __init__(self, delay, channels=1):
        super().__init__(delay)
        self.queue = 0
        self.max_queue = float('inf')
        self.failure = 0
        self.mean_queue = 0.0
        self.mean_load = 0
        self.channels = channels
        self.state = [0] * self.channels
        self.t_next = [np.inf] * self.channels

    def in_act(self):
        channels = self.get_channels()
        if len(channels) > 0:
            for channel in channels:
                self.state[channel] = 1
                self.t_next[channel] = self.t_curr + self.get_delay()
                break
        else:           
            if self.queue < self.max_queue:
                self.queue = self.queue + 1
            else:
                self.failure += 1
            
    def out_act(self):
        channels = self.get_current_channel()
        for channel in channels:
            super().out_act()
            self.t_next[channel] = float('inf')
            self.state[channel] = 0

            if self.queue > 0:
                self.queue -= 1
                self.state[channel] = 1
                self.t_next[channel] = self.t_curr + self.get_delay()

            if self.next_element is not None:
                next_element = np.random.choice(a=self.next_element)
                next_element.in_act() 

    def get_channels(self):
        channels = []
        for i in range(self.channels):
            if self.state[i] == 0:
                channels.append(i)
        return channels

    def get_current_channel(self):
        channels = []
        for i in range(self.channels):
            if self.t_next[i] == self.t_curr:
                channels.append(i)
        return channels

    def print_result(self):
        super().print_result()
        print(f"failure: {self.failure}")

    def do_statistics(self, delta):
        self.mean_queue += self.queue * delta

        for i in range(self.channels):
            self.mean_load += self.state[i] * delta

        self.mean_load = self.mean_load / self.channels