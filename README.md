[![Build Status](https://github.com/davidbrochart/attrait/workflows/CI/badge.svg)](https://github.com/davidbrochart/attrait/actions)

# attrait

[traitlets](https://traitlets.readthedocs.io) allow variables to notify their
changes through callbacks. They are used in
[ipywidgets](https://ipywidgets.readthedocs.io) to let Python react to changes
in the browser. But using raw callbacks quickly leads to complicated,
unmaintainable code (a.k.a. "callback hell").

[attrait](https://github.com/davidbrochart/attrait) provides a higher-level
API that helps write simpler code. It also makes it possible to use traitlets
in an asynchronous framework (with async/await).

# How does it work?

attrait uses a new object called a `Signal`, which wraps a trait. This can be an
existing trait (e.g. a property of a widget) or a new trait created for this
signal (not attached to a widget):

```python
from attrait import Signal
from traitlets import Int, Float
from ipyleaflet import Map

# signals not attached to a widget property:
s1 = Signal(init=0)  # type is Any, initialized to 0
s2 = Signal(type=Int)  # type is Int
s3 = Signal(type=Float, init=0.)  # type is Float, initialized to 0

# signals attached to an ipyleaflet's Map property:
m = Map(center=(0, 0), zoom=5)
s_center = Signal(m, 'center')
s_zoom = Signal(m, 'zoom')
```

Then you can register callbacks on signal changes with an `on_change` decorator:

```python
from attrait import on_change

# callback triggered every time the provided signals change
@on_change(s_center, s_zoom)
def _():
    print('The center of the map is now', s_center.v, ', and the zoom level is', s_zoom.v)
```

You can also wait for a change using asynchronous programming:

```python
import asyncio
from attrait import change

async def recenter():
    # wait for the user to drag the map
    await change(s_center)
    # and set it back to the initial position after one second
    await asyncio.sleep(1)
    s_center.v = (0, 0)

asyncio.create_task(recenter())
```

You can also wait for a signal to change to a specific value. Useful signal
transformation functions are provided, like debouncing and throttling.

Signals can dump their value to a VCD file, so that it can be opened with e.g.
GTKWave. This can be useful to debug complex dashboards.
