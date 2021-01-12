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
