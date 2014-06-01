from pubsub import pub

# I'm not thrilled with how hacky this is, but it'll do for now.
# There's a mix of logic (like don't allow player chips to go < 0) and special cases (like the control return portion of between functions) that seem bad.
# Also converting from a None bet value to an int bet happens here.
class ChipConduit(object):
    @staticmethod
    def move(amt, frm, frm_attr_name, to, to_attr_name, frm_call_args=[], to_call_args=[], between=None, between_args=[]):
        message_data = {}
        if hasattr(frm, 'keys'):
            if frm[frm_attr_name] < amt:
                amt = frm[frm_attr_name]
            frm[frm_attr_name] -= amt
        else:
            frm_attr = getattr(frm, frm_attr_name)
            # If frm_attr is a class method, then the first arg will go along.  For tests, though, it won't, so in those I have to pass the object in via call_args.
            setattr(frm, frm_attr_name, (frm_attr - amt) if frm_attr - amt >= 0 else 0)

        to_return = None
        control = None
        if between is not None and hasattr(between, '__call__'):
            to_return, control = between(*between_args)

        if control is not None and 'amt' in control:
            amt = control['amt']

        if hasattr(to, 'keys'):
            to[to_attr_name] = (to[to_attr_name] if to[to_attr_name] is not None else 0) + amt
        else:
            to_attr = getattr(to, to_attr_name)
            setattr(to, to_attr_name, (to_attr if to_attr is not None else 0) + amt)

        # publish about chip movement
        pub.sendMessage('chip_movement', data=message_data)

        return to_return
