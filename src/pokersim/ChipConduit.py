class ChipConduit(object):
    @staticmethod
    def move(amt, frm, frm_attr_name, to, to_attr_name, frm_call_args=[], to_call_args=[]):
        # publish about chip movement
        frm_attr = getattr(frm, frm_attr_name)
        to_attr = getattr(to, to_attr_name)
        if hasattr(frm_attr, '__call__'):
            frm_attr(frm, amt, *frm_call_args)
        else:
            setattr(frm, frm_attr_name, frm_attr - amt)
        if hasattr(to_attr, '__call__'):
            to_attr(to, amt, *to_call_args)
        else:
            setattr(to, to_attr_name, to_attr + amt)
