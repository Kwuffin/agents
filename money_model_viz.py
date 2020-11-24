from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer, VisualizationElement
from mesa.visualization.UserParam import UserSettableParameter
from money_model import *
import numpy as np

import asyncio
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


class HistogramModule(VisualizationElement):
    package_includes = ["Chart.min.js"]
    local_includes = ["histmodule.js"]

    def __init__(self, bins, canvas_height, canvas_width):
        self.canvas_height = canvas_height
        self.canvas_width = canvas_width
        self.bins = bins
        new_element = "new HistogramModule({}, {}, {})"
        new_element = new_element.format(bins,
                                         canvas_width,
                                         canvas_height)
        self.js_code = "elements.push(" + new_element + ");"

    def render(self, model):
        wealth_vals = [agent.wealth for agent in model.schedule.agents]
        hist = np.histogram(wealth_vals, bins=self.bins)[0]
        return [int(x) for x in hist]


def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "r": 0.2}

    if agent.wealth == 0:
        portrayal["Color"] = "#000000"
        portrayal["Layer"] = 3
    elif 0 < agent.wealth < 3:
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 2
        portrayal["r"] = 0.5
    elif 3 <= agent.wealth < 6:
        portrayal["Color"] = "green"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.8
    else:
        portrayal["Color"] = "blue"
        portrayal["Layer"] = 0
        portrayal["r"] = 1
    return portrayal


# Eigen toevoeging
agent_amount_slider = UserSettableParameter("slider", "Amount of agents", value=200, min_value=200, max_value=1000, step=1)


grid = CanvasGrid(agent_portrayal, 30, 30, 800, 800)

chart = ChartModule([{"Label": "Gini",
                      "Color": "Black"}],
                    data_collector_name='datacollector')

histogram = HistogramModule(list(range(10)), 200, 500)

server = ModularServer(MoneyModel,
                       [grid, histogram, chart],
                       "Money Model",
                       {"N":agent_amount_slider, "width":30, "height":30})

server.port = 8521  # The default
server.launch()
