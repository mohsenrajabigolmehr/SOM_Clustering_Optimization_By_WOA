def ConvertFromClass(Obj, ExcludedKeys = []) -> dict:
     if Obj == None:
          return []

     return dict(
         (key, value)
         for (key, value) in Obj.__dict__.items()
         if key not in ExcludedKeys
     )

