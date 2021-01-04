# attrait: asynchronous traitlets

[traitlets](https://traitlets.readthedocs.io) lets variables notify their
changes through callbacks. They are a key component of
[ipywidgets](https://ipywidgets.readthedocs.io) to build reactive UIs. But using
callbacks usually leads to complicated, unmaintainable code (also known as
"callback hell"). [attrait](https://github.com/davidbrochart/attrait) can
greatly simplify this task by providing an asynchronous framework around
traitlets. The goal is to make it easy to build complex dashboards using a
modular design.
