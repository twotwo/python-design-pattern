"""
file : _type.py
since: 2022/10/08
desc : types for handler chains
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Any

logging.basicConfig(level=logging.DEBUG, format="%(asctime)-15s - %(name)s:%(lineno)s - %(message)s")
logger = logging.getLogger(__name__)


class DefaultContext:
    """The default chaining context storage"""

    def __init__(self, task: AbstractTask) -> None:
        self.task = task
        self.process_flag: bool = True
        self._context: Any = {}

    def set_context(self, key: str, value):
        self._context[key] = value

    def get_content(self, key: str):
        if key in self._context:
            return self._context[key]
        return None

    def __repr__(self) -> str:
        return str(self._context)


class AbstractTask(ABC):
    pass


class AbstractHandler(ABC):
    """
    The abstract Handler declares a method for building the chain of handlers.
    It also declares a method for handle a task, default chaining behavior can
    be implemented inside a base handler class.
    """

    def set_next(self, handler: AbstractHandler) -> AbstractHandler:
        self._next_handler = handler
        # Returning a handler from here will let us link handlers in a
        # convenient way like this:
        # handler1.set_next(handler2).set_next(handler3)
        return handler

    def handle(self, task: AbstractTask, context=None) -> DefaultContext:
        """The default handle mothod, logging before and after handle process"""
        logger.info(f"enter {self.__class__}")
        if context is None:
            context = DefaultContext(task=task)
            logger.debug("create context")

        logger.info(f"do predict at {self.__class__.__name__}")
        ctx = self.do_predict(task, context)

        if ctx.process_flag and hasattr(self, "_next_handler"):  # 继续下一个 Handler
            return self._next_handler.handle(task, ctx)

        logger.info(f"finish chain at {self.__class__.__name__}")
        return ctx

    @abstractmethod
    def do_predict(self, task: AbstractTask, context: DefaultContext) -> DefaultContext:
        pass
