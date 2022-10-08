"""
file : chain-of-responsibility.py
since: 2022/10/07
desc : Variant of Chain of Responsibility in Python
"""

from _type import AbstractHandler, AbstractTask, DefaultContext


class SetMealTask(AbstractTask):
    """Set meal for customer"""

    def __init__(self, appetizer: str = None, main_course: str = None):
        self.appetizer = appetizer
        self.main_course = main_course

    def __repr__(self) -> str:
        return f"appetizer: {self.appetizer}, main_course: {self.main_course}"


class OrderHandler(AbstractHandler):
    """Do order work in handler"""

    def do_predict(self, task: AbstractTask, context: DefaultContext) -> DefaultContext:
        appetizer = task.appetizer if task.appetizer else "vegetable soup"
        main_course = task.main_course if task.main_course else "veal"
        if main_course not in ["roast duck", "veal"]:
            print(f"Main course {main_course} not in menu!")
            context.process_flag = False
        context.set_context("order", {"appetizer": appetizer, "main_course": main_course})

        return context


class CookHandler(AbstractHandler):
    """Do cook work in handler"""

    def do_predict(self, task: AbstractTask, context: DefaultContext) -> DefaultContext:
        order = context.get_content("order")
        if order is None:
            context.process_flag = False
            return context
        cook = {}
        if "appetizer" in order:
            cook["appetizer"] = order["appetizer"]
        if "main_course" in order:
            cook["main_course"] = order["main_course"]
        context.set_context("cook", cook)

        return context


class WaitressHandler(AbstractHandler):
    """Serve food in handler"""

    def do_predict(self, task: AbstractTask, context: DefaultContext) -> DefaultContext:
        cook = context.get_content("cook")
        if cook is None:
            context.process_flag = False
            return context
        waitress = {}
        if "appetizer" in cook:
            waitress["appetizer"] = cook["appetizer"]
        if "main_course" in cook:
            waitress["main_course"] = cook["main_course"]
        context.set_context("waitress", waitress)

        return context


def client_code(chain: AbstractHandler):
    print("Let's order a set meal!")
    order = SetMealTask()  # default order
    ctx = chain.handle(order)
    print(f"order=({order})", "ctx", ctx.get_content("waitress"))

    order = SetMealTask(main_course="roast duck")  # select roast duck
    print(f"order=({order})", "ctx", chain.handle(order).get_content("waitress"))

    order = SetMealTask(appetizer="salad", main_course="lamb")
    print(f"order=({order})", "ctx", chain.handle(order).get_content("waitress"))


if __name__ == "__main__":
    print("Set up the kitchen in chain!")
    order_handler = OrderHandler()
    cook_handler = CookHandler()
    waitress_handler = WaitressHandler()

    order_handler.set_next(cook_handler).set_next(waitress_handler)

    client_code(order_handler)
