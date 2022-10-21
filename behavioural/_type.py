"""
file : _type.py
since: 2022/10/08
desc : types for handler chains
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s - %(levelname)-8s - %(name)s:%(lineno)s - %(message)s")
logger = logging.getLogger(__name__)


class HandlerError(Exception):
    """Raised when an operation attempts a state transition that's not allowed.

    Attributes:
        context -- context in chain
        current -- current handler
        next -- next handler in chain
        expression -- expression in which the error occurred
    """

    def __init__(
        self,
        context: DefaultContext,
        current: str,
        next: str,
        expression: Exception,
    ):
        self.context = context
        self.current = current
        self.next = next
        self.expression = expression

    def __str__(self) -> str:
        return f"HandlerError(current=[{self.current}], next=[{self.next}])"


class DefaultContext:
    """The default chaining context storage"""

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

    def handle(self, context: DefaultContext) -> DefaultContext:
        """
        The default handle mothod, logging before and after handle process.

        Args:
            context: Context for handle process.

        Returns:
            DefaultContext: all handler's context.

        Raises:
            HandlerError: if run do_predict failed in handler.
        """
        current = self.__class__.__name__  # current handler class name
        next_ = self._next_handler.__class__.__name__ if hasattr(self, "_next_handler") else None

        if context is None:
            logger.error("no context to handle")
            raise HandlerError(context=context, current=current, next=next_, expression=None)  # type: ignore

        try:
            ctx = self.do_predict(context)
        except Exception as ex:
            logger.error(f"do predict failed at {self.__class__.__name__}: {ex}")
            raise HandlerError(context=context, current=current, next=next_, expression=ex)  # type: ignore

        if hasattr(self, "_next_handler"):  # 继续下一个 Handler
            return self._next_handler.handle(ctx)

        logger.debug(f"finish chain at {self.__class__.__name__}")
        return ctx

    @abstractmethod
    def do_predict(self, context: DefaultContext) -> DefaultContext:
        pass
