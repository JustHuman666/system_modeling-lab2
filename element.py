import random_generator as generator


class Element:
    next_id = 0
    def __init__(self,  delay=None, name=None, distribution=None):
        self.name = name
        self.t_next = [0]
        self.delay_mean = delay
        self.delay_dev = None
        self.distribution = distribution
        self.quantity = 0
        self.t_curr = self.t_next
        self.state = [0]
        self.next_element = None
        self.id = Element.next_id
        Element.next_id += 1

    def get_delay(self):
        if self.distribution == "exponential":
            return generator.exponential(self.delay_mean)
        elif self.distribution == "normal":
            return generator.normal(self.delay_mean, self.delay_dev)
        elif self.distribution == "uniform":
            return generator.uniform(self.delay_mean, self.delay_dev)
        else:
            return self.delay_mean

    def in_act(self):
        pass

    def out_act(self):
        self.quantity += 1

    def do_statistics(self, delta):
        pass

    def print_result(self):
        print(f"{self.name} state: {self.state}, quantity: {self.quantity} t_next: {self.t_next}")
