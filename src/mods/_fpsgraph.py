import matplotlib.pyplot as plt
from kivy.clock import Clock


class FPSGraph:
    def __init__(self):
        self.start_time = Clock.get_time()
        self.times = []
        self.fps = []

    def start(self):
        self.event = Clock.schedule_interval(self.update, 0.1)

    def stop(self):
        Clock.unschedule(self.event)

    def update(self, dt):
        current_time = Clock.get_time() - self.start_time
        fps = Clock.get_rfps()
        self.times.append(current_time)
        self.fps.append(fps)
        print(f"Update called. Current time: {current_time}, FPS: {fps}")

    def plot(self):
        plt.plot(self.times, self.fps)
        plt.savefig('fpsgraph.png')
        plt.show()