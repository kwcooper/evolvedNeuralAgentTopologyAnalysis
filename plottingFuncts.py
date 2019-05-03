
from matplotlib import pyplot as plt
from matplotlib.patches import Circle
import matplotlib.lines as lines
import matplotlib.cm as cm
import numpy as np

from math import sin
from math import cos
from math import radians


def plot_organism2(x1, y1, theta, fit, ax):
# TODO: Could make color relaitive to the genetic parent to see agent clustering
#            The border could be this and the inside could be fitness?
#       Could also add a dotted or thin line to the food that the agent is
#        currently persuing. This is like "vision"

##    plt.plot(x1, y1, marker=(3, 1, theta+33), markersize=11, color='darkslateblue', linestyle='None')
##    plt.plot(x1, y1, marker=(3, 1, theta+33), markersize=6, color='mediumslateblue', linestyle='None')
##
    plt.plot(x1, y1, marker=(3, 1, theta+33), markersize=11, color=cm.hot(fit/200), linestyle='None')
    plt.plot(x1, y1, marker=(3, 1, theta+33), markersize=6, color='grey', linestyle='None')
    
    dir_len = 0.075
    
    x2 = cos(radians(theta)) * dir_len + x1
    y2 = sin(radians(theta)) * dir_len + y1
    ax.add_line(lines.Line2D([x1,x2],[y1,y2], color=cm.hot(fit/200), linewidth=1, zorder=10))

    pass


def plot_food(x1, y1, ax):

    circle = Circle([x1,y1], 0.03, edgecolor='darkgreen', facecolor ='darkgoldenrod', zorder=5)
    ax.add_artist(circle)
    
    pass


def fitness_plot():
    y = [range(20) + 3 * i for i in np.random.randn(3, 20)]
    x = list(range(20))

    #calculate the min and max series for each x
    min_ser = [min(i) for i in np.transpose(y)]
    max_ser = [max(i) for i in np.transpose(y)]

    #initial plot
    fig, axs = plt.subplots()
    axs.plot(x, x)
    for s in y:
        axs.scatter(x, s)

    #plot the min and max series over the top
    axs.fill_between(x, min_ser, max_ser, alpha=0.2)
    plt.show()


def plot_frame(params, agents, foods, gen, tme):
    fig, ax = plt.subplots()
    fig.set_size_inches(9.6, 5.4)

    plt.xlim([params['x_min'] + params['x_min'] * 0.25, params['x_max'] + params['x_max'] * 0.25])
    plt.ylim([params['y_min'] + params['y_min'] * 0.25, params['y_max'] + params['y_max'] * 0.25])

    # Plot the agents and the food
    for agent in agents:
        plot_organism2(agent.x, agent.y, agent.r, agent.fitness, ax)

    for food in foods:
        plot_food(food.x, food.y, ax)

    ax.set_aspect('equal')
    frame = plt.gca()
    frame.axes.get_xaxis().set_ticks([])
    frame.axes.get_yaxis().set_ticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    #plt.figtext(0.025, 0.95,r'GEN: '+str(gen))
    #plt.figtext(0.025, 0.90,r'Step: '+str(tme))

    plt.savefig('img/'+str(gen)+'-'+str(tme)+'.png', dpi=100)
##    plt.show()



if __name__ == "__main__":

    # Testing
    
    if 0:
        fitness_plot()
    
    if 0:
        params = {}
        params['x_min'] = -2.0        
        params['x_max'] =  2.0        
        params['y_min'] = -2.0        
        params['y_max'] =  2.0        
        
        fig, ax = plt.subplots()
        #fig.set_size_inches(9.6, 5.4)
        
        plt.xlim([params['x_min'] + params['x_min'] * 0.25, params['x_max'] + params['x_max'] * 0.25])
        plt.ylim([params['y_min'] + params['y_min'] * 0.25, params['y_max'] + params['y_max'] * 0.25])

        plot_organism(1, 1, 20, ax)
        plot_organism2(-1, -1, 124, 100, ax)

        plt.show()

# BONEYARD
##def plot_organism(x1, y1, theta, ax):
##
##    circle = Circle([x1,y1], 0.05, edgecolor = 'b', facecolor ='mediumslateblue', zorder=8)
##    ax.add_artist(circle)
##
##    edge = Circle([x1,y1], 0.05, facecolor='None', edgecolor ='darkslateblue', zorder=8)
##    ax.add_artist(edge)
##
##    tail_len = 0.075
##    
##    x2 = cos(radians(theta)) * tail_len + x1
##    y2 = sin(radians(theta)) * tail_len + y1
##
##    ax.add_line(lines.Line2D([x1,x2],[y1,y2], color='darkslateblue', linewidth=1, zorder=10))
##
##    pass
