# Python Design Patterns

## Reference

- [](https://plantuml.com/zh/class-diagram)
- [refactoring.guru](https://refactoring.guru/design-patterns/)
- <https://github.com/rebuild-123/Python-Head-First-Design-Patterns>

## setup for running

    # newer for poetry
    curl -sSL https://install.python-poetry.org | POETRY_VERSION=1.2.1 python3 -
    # install dependency
    poetry install
    poetry shell
    # install pre-commit and run checks
    pre-commit install
    pre-commit run -a

## Design patterns : elements of reusable object-oriented software

The authors of the book called "gang of four" (Erich Gamma, Richard Helm, Ralph Johnson, and John Vlissides) investigated various common software design problems, and identified best-practice solutions that are commonly used in the software industry.

These common solutions were called [design patterns](https://www.pythoninformer.com/programming-techniques/design-patterns/).

A design pattern describes a basic approach to solving a particular design problem. It doesn't exist as a code library, or a set of detailed instructions for implementing a solution. Instead it describes the basic elements involved in the design, and how they relate to each other. It is up to the software designer to apply the pattern to their own software design.

In all, the authors identified 23 patterns, which they divided into 3 categories.

### Creational patterns

### Structural patterns

### Behavioural patterns

[Behavioural patterns](https://www.pythoninformer.com/programming-techniques/design-patterns/behavioural-patterns/) relate to the interactions between classes at runtime. These include:

- Observer (which allows objects to notified other object when their state changes).
- Strategy that allows alternate algorithms to be selected.
- Chain of responsibility is a behavioural design pattern. It is used to process command objects, where different types of command objects might need to be processed in different ways.

## The Factory

- [Python Design Patterns: -03- The Factory](https://medium.com/@mrfksiv/python-design-patterns-03-the-factory-86cb351c68b0)
- [simple_factory.py](./simple_factory.py)
- [factory_method.py](./factory_method.py) [factory-method example](https://refactoringguru.cn/design-patterns/abstract-factory/python/example)
- [abstract_factory.py](./abstract_factory.py) [abstract-factory example](https://refactoringguru.cn/design-patterns/abstract-factory/python/example)

## Bridge

''Bridge'' is a structural design pattern that divides business logic or huge class into separate class hierarchies that can be developed independently.

- [pazdera/bridge.py](https://gist.github.com/pazdera/1173009) python 2 implementation
- [Bridge in Python](https://sourcemaking.com/design_patterns/bridge/python/1)
- [Bridge pattern in Python](https://www.giacomodebidda.com/bridge-pattern-in-python/)

``plantuml
@startuml
'Class Diagram for Bridge Design Pattern

Website <|-- FreeWebsite
Website <|-- PaidWebsite

Website : __init__(self, implementation)
Website : show_page(self)

Implementation <|-- ImplementationA
Implementation <|-- ImplementationB

Implementation : get_excerpt(self)
Implementation : get_article(self)
Implementation : get_ads(self):

@enduml
``
