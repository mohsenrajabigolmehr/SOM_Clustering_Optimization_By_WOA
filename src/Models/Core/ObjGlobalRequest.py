from typing import TypeVar, Generic

T = TypeVar('T')

class ObjGlobalRequest:

    def __init__(self, Item: Generic[T] = None):
        self.Item = Item
        
