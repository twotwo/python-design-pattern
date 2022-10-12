"""
file : chain-of-responsibility.py
since: 2022/10/07
desc : Variant of Chain of Responsibility in Python
"""

from __future__ import annotations

import logging

from _type import AbstractHandler, AbstractTask, DefaultContext, HandlerError

logger = logging.getLogger(__name__)


class SetMealTask(AbstractTask):
    """Set meal for customer"""

    def __init__(self, appetizer: str = "vegetable soup", main_course: str = "roast duck"):
        self.appetizer = appetizer
        self.main_course = main_course

    def __repr__(self) -> str:
        return f"appetizer: {self.appetizer}, main_course: {self.main_course}"

    @staticmethod
    def from_abstract_task(task: AbstractTask) -> SetMealTask:
        if isinstance(task, SetMealTask):
            return task
        raise RuntimeError(f"Can't cast to SetMealTask: {task}")


class OrderHandler(AbstractHandler):
    """Do order work in handler"""

    def do_predict(self, task: AbstractTask, context: DefaultContext) -> DefaultContext:
        task = SetMealTask.from_abstract_task(task)
        if task.main_course not in ["roast duck", "veal"]:
            raise RuntimeError(f"Main course [{task.main_course}] not in menu!")
        context.set_context("order", {"appetizer": task.appetizer, "main_course": task.main_course})

        return context


class CookHandler(AbstractHandler):
    """Do cook work in handler"""

    # Inventory for cook recipe
    INGREDIENTS = {
        "roast duck": True,
        "veal": False,
    }

    def do_predict(self, task: AbstractTask, context: DefaultContext) -> DefaultContext:
        order = context.get_content("order")
        if order is None:
            raise RuntimeError("order not in context!")
        main_course = order["main_course"]
        if not self._check_inventory(main_course):
            raise RuntimeError(f"Main course [{main_course}] can't be cooked!")
        cook = {}
        if "appetizer" in order:
            cook["appetizer"] = order["appetizer"]
        if "main_course" in order:
            cook["main_course"] = main_course
        context.set_context("cook", cook)

        return context

    def _check_inventory(self, course):
        if course not in CookHandler.INGREDIENTS:
            return False
        return CookHandler.INGREDIENTS[course]


class WaitressHandler(AbstractHandler):
    """Serve food in handler"""

    def do_predict(self, task: AbstractTask, context: DefaultContext) -> DefaultContext:
        cook = context.get_content("cook")
        if cook is None:
            raise RuntimeError("cook not in context!")
        waitress = {}
        if "appetizer" in cook:
            waitress["appetizer"] = cook["appetizer"]
        if "main_course" in cook:
            waitress["main_course"] = cook["main_course"]
        context.set_context("waitress", waitress)

        return context


def client_code(chain: AbstractHandler):
    logger.info("Let's order a set meal!")

    for order in [
        SetMealTask(),  # default order
        SetMealTask(main_course="lamb"),  # select lamb but not in set meal
        SetMealTask(appetizer="salad", main_course="veal"),  # select veal but can't cook
    ]:
        try:
            ctx = chain.handle(order)
        except HandlerError as ex:
            logger.info(f"order=({order}), error={ex}, ctx={ex.context}, stack={ex.expression}")
        else:
            logger.info(f"order=({order}), serve={ctx.get_content('waitress')}")


if __name__ == "__main__":
    order_handler = OrderHandler()  # ordering process
    cook_handler = CookHandler()  # cooking process
    waitress_handler = WaitressHandler()  # serving process

    order_handler.set_next(cook_handler).set_next(waitress_handler)

    logger.info("Set up the restaurant process in chain!")

    client_code(order_handler)
