"""
file : chain-of-responsibility.py
since: 2022/10/07
desc : Variant of Chain of Responsibility in Python
"""

from __future__ import annotations

import logging

from _type import AbstractHandler, DefaultContext, HandlerError

logger = logging.getLogger(__name__)


class SetMealOrder:
    """Customer place an order of set meal"""

    def __init__(self, appetizer: str = "vegetable soup", main_course: str = "roast duck"):
        self.appetizer = appetizer
        self.main_course = main_course

    def __repr__(self) -> str:
        return f"appetizer: {self.appetizer}, main_course: {self.main_course}"


class DemoContext(DefaultContext):
    """Context for this demo chain's handler"""

    def __init__(self, order: SetMealOrder) -> None:
        self.order = order
        self.status = "init"

    def __repr__(self) -> str:
        return f"DemoContext(order={self.order}, status={self.status})"

    @staticmethod
    def from_abstract_context(context: DefaultContext) -> DemoContext:
        if isinstance(context, DemoContext):
            return context
        raise RuntimeError(f"Can't cast to DemoContext: {context}")


class DemoHandler(AbstractHandler):
    """Do order work in handler"""

    def do_predict(self, context: DefaultContext) -> DefaultContext:
        ctx = DemoContext.from_abstract_context(context)
        return self._predict(ctx)

    def _predict(self, context: DemoContext) -> DemoContext:
        raise RuntimeError("Not implement yet")


class OrderHandler(DemoHandler):
    """Do order work in handler"""

    def _predict(self, ctx: DemoContext) -> DemoContext:
        if ctx.order.main_course not in ["roast duck", "veal"]:  # verify order
            raise RuntimeError(f"Main course [{ctx.order.main_course}] not in menu!")

        ctx.status = "orderd"
        return ctx


class CookHandler(DemoHandler):
    """Do cook work in handler"""

    # Inventory for cook recipe
    INGREDIENTS = {
        "roast duck": True,
        "veal": False,
    }

    def _predict(self, ctx: DemoContext) -> DemoContext:
        order = ctx.order
        if order is None:
            raise RuntimeError("order not in context!")
        if not self._check_inventory(order.main_course):
            raise RuntimeError(f"Main course [{order.main_course}] can't be cooked!")
        logger.info("cooking ...")
        ctx.status = "cooked"

        return ctx

    def _check_inventory(self, course):
        if course not in CookHandler.INGREDIENTS:
            return False
        return CookHandler.INGREDIENTS[course]


class WaitressHandler(DemoHandler):
    """Serve food in handler"""

    def _predict(self, ctx: DemoContext) -> DemoContext:
        if ctx.status != "cooked":
            raise RuntimeError("cook not done!")
        logger.info("serving ...")
        ctx.status = "serving"

        return ctx


def client_code(chain: AbstractHandler):
    logger.info("Let's order a set meal!")

    for order in [
        SetMealOrder(),  # default order
        SetMealOrder(main_course="lamb"),  # select lamb but not in set meal
        SetMealOrder(appetizer="salad", main_course="veal"),  # select veal but can't cook
    ]:
        ctx = DemoContext(order)
        try:
            ctx = DemoContext.from_abstract_context(chain.handle(ctx))
        except HandlerError as ex:
            logger.info(f"order=({order}), error={ex}, ctx={ex.context}, stack={ex.expression}")
        else:
            logger.info(f"order=({order}), status={ctx.status}")


if __name__ == "__main__":
    order_handler = OrderHandler()  # ordering process
    cook_handler = CookHandler()  # cooking process
    waitress_handler = WaitressHandler()  # serving process

    order_handler.set_next(cook_handler).set_next(waitress_handler)

    logger.info("Set up the restaurant process in chain!")

    client_code(order_handler)
