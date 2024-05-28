from kivy import Logger
from mods._fpsgraph import FPSGraph

__all__ = ('start', 'stop')

# Create an instance of FPSGraph
fps_graph = FPSGraph()


def start(win, ctx):
    print('FPSGraph: Starting')
    fps_graph.start()


def stop(win, ctx):
    print('FPSGraph: Stopping')
    fps_graph.stop()
    fps_graph.plot()
