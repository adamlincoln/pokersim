class ChipConduit(object):
    @staticmethod
    def move(amt, frm, frm_attr_name, to, to_attr_name, frm_call_args=[], to_call_args=[], between=None, between_args=[]):
        # publish about chip movement
        frm_attr = getattr(frm, frm_attr_name)
        to_attr = getattr(to, to_attr_name)
        # If frm_attr is a class method, then the first arg will go along.  For tests, though, it won't, so in those I have to pass the object in via call_args.
        if hasattr(frm_attr, '__call__'):
            frm_attr(amt, *frm_call_args)
        else:
            setattr(frm, frm_attr_name, frm_attr - amt)
        to_return = None
        if between is not None and hasattr(between, '__call__'):
            to_return = between(*between_args)
        if hasattr(to_attr, '__call__'):
            to_attr(amt, *to_call_args)
        else:
            setattr(to, to_attr_name, to_attr + amt)

        return to_return
