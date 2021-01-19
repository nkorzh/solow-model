import matplotlib.pyplot as plt
import pylab
import numpy as np


# Sliders: alpha, g, n, delta, s, E_0, K_0,
def k1(t, alpha, g, n, delta, s, e0, k0):
    exp = np.e ** (-alpha * (n + g + delta) * t)
    mid = s * alpha * (e0 ** (1 - alpha))
    divider = alpha * (n + delta) + g
    divisible = np.e ** (divider * t)
    # const counting
    left = ((k0 * 10 ** 3) ** alpha) / (s * alpha * (e0 ** (1 - alpha)))
    right = 1 / (alpha * (n + delta) + g)
    const = left - right
    return (exp * mid * (divisible / divider + const)) ** (1.0 / alpha)


def k(t, alpha, g, n, delta, s, e0, k0, l0):
    beta = 1.0 - alpha
    deg = g * (1 - alpha)
    divisible = alpha * s * (e0 ** beta) * (np.e ** (t * deg))
    divider = alpha * (n + delta) + g
    return (divisible / divider) ** (1.0 / alpha) * (e0 * l0 * (np.e ** ((g + n) * t)))


# time, k_t, alpha, init tech, tech growth, s
def ys(t, kt, alpha, e0, g, s):
    tech = e0 * (np.e ** (g * t))
    beta = 1.0 - alpha
    return (kt ** beta) * (tech ** (-beta))


def y(t, kt, alpha, l0, n, e0, g):
    beta = 1.0 - alpha
    labour = l0 * (np.e ** (n * t))
    tech = e0 * (np.e ** (g * t))
    return (kt ** beta) * (labour ** alpha) * tech


def update(_):
    kvalues = k(time, sliders['alpha'].val, sliders['tech growth'].val, sliders['population growth'].val,
                sliders['capital removal, %'].val, sliders['savings rate'].val,
                sliders['init tech'].val, sliders['init capital'].val, sliders['init population'].val)
    print(kvalues)
    capitalLine.set_ydata(kvalues)

    yvalues = []
    for ind in range(0, len(time)):
        yvalues.append(y(time[ind], kvalues[ind], sliders['alpha'].val, sliders['init population'].val,
                         sliders['population growth'].val, sliders['init tech'].val, sliders['tech growth'].val))
    yieldLine.set_data(kvalues, yvalues)
    outflowLine.set_data(kvalues, kvalues * (sliders['population growth'].val + sliders['tech growth'].val +
                                             sliders['capital removal, %'].val))


fig = plt.figure(figsize=(10, 8))
ax1, ax2 = fig.subplots(nrows=1, ncols=2)

time = np.arange(1920, 2020, 1)
lineColor = '#92000A'
outflowColor = 'red'

# tech level calculation
techGrowth = np.log(2.09) / (2008.0 - 1948)
techInit = 4.60 / (np.e ** (1948 * techGrowth))
popGrowth = np.log(1.1 / 100 + 1)
print(popGrowth)
axNames = ['alpha', 'tech growth', 'population growth', 'capital removal, %', 'savings rate',
           'init tech', 'init capital', 'init population']
axLimits = [(.01, .99), (.0, 5.0), (.001, 0.1), (.01, 0.5), (.001, 0.4),
            (1.0e-12, 1.0e-5), (.0, 40.0), (.0, 40.0)]
axInitVal = [0.67, techGrowth, popGrowth, 0.04, 0.05,
             techInit, 1.0, 4.62]

# Sliders: alpha, g, n, delta, s, E_0, K_0,
initK = k(time, axInitVal[axNames.index('alpha')], axInitVal[axNames.index('tech growth')],
          axInitVal[axNames.index('population growth')], axInitVal[axNames.index('capital removal, %')],
          axInitVal[axNames.index('savings rate')], axInitVal[axNames.index('init tech')],
          axInitVal[axNames.index('init capital')], axInitVal[axNames.index('init population')])
print(initK)
initY = []
for i in range(0, len(time)):
    # time, k_t, alpha, init tech, tech growth, s
    initY.append(y(time[i], initK[i], axInitVal[axNames.index('alpha')], axInitVal[axNames.index('init population')],
                   axInitVal[axNames.index('population growth')],  axInitVal[axNames.index('init tech')],
                   axInitVal[axNames.index('tech growth')]))

initOutflow = initK * (axInitVal[axNames.index('population growth')] + axInitVal[axNames.index('tech growth')] +
                       axInitVal[axNames.index('capital removal, %')])
capitalLine, = ax1.plot(time, initK, color=lineColor)
yieldLine, = ax2.plot(initK, initY, color=lineColor, label='yield')
outflowLine, = ax2.plot(initK, initOutflow, color=outflowColor, label='capital outflow')

fig.subplots_adjust(left=0.095, right=0.97, bottom=0.44, top=0.95, wspace=0.2)
fig.canvas.set_window_title('Solow model ©Kozhukharov-Batalenkov')

ax1.set_title('K(t)')
ax1.set_xlabel('time')
ax1.set_ylabel('capital')
ax1.grid(True)
# ax1.set_yscale('log')

ax2.set_title('Y(K)')
ax2.set_xlabel('capital')
ax2.set_ylabel('yield')
ax2.grid(True)
# ax2.set_yscale('log')
ax2.legend()
axes = []

leftSpace = 0.2
startY = 0.05
deltaY = 0.04
axcolor = '#E4AC9A'
for name in axNames:
    axes.append(plt.axes([leftSpace, startY, 0.65, 0.03], facecolor=axcolor))
    startY += deltaY

# creating sliders with their names
sliderColor = '#755A57'
sliders = {}
for i in range(0, len(axes)):
    leftB, rightB = axLimits[i]
    sliders[axNames[i]] = pylab.Slider(axes[i], axNames[i], leftB, rightB, valinit=axInitVal[i], color=sliderColor)
    sliders[axNames[i]].on_changed(update)

plt.show()
