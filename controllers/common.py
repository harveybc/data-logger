""" Common Controller Functions 
    Description: Contains functions used by most controllers
"""

def as_dict(model):   
    """ Transform a sqlalchemy result into a dict
        Args:
        model (sqlalachemy result): the result of a sqlalachemy query for an individual register.

        Returns:
        res (dict): the model transformed into a dict.
    """ 
    r2 = {}
    for c in model.__table__.columns:
        attr = getattr(model, c.name)
        if is_num(attr):
            r2[c.name]=attr
        else:
            r2[c.name]=str(attr)
    return r2

def is_num(n):
    """ Verify if an input variable is int or float.

        Args:
        n (variable): The variable to be verified as number

        Returns:
        res (dict): true if the variable is a float or int, false otherwise
    """ 
    if isinstance(n, int):
        return True
    if isinstance(n, float):
        return n.is_integer()
    return False
      