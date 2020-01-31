from .tyd_collection import TydCollection


class TydList(TydCollection):
    def __str__(self):
        return f"{self.name} (TydList, {len(self)})"
