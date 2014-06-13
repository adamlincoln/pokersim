from pubsub import pub

from Bank import Bank

# I'm not thrilled with how hacky this is, but it'll do for now.
# There's a mix of logic (like don't allow player chips to go < 0) and special cases (like the control return portion of between functions) that seem bad.
# Also converting from a None bet value to an int bet happens here.
class ChipConduit(object):
    @staticmethod
    def move(amt, frm, frm_attr_name, to, to_attr_name, frm_tracking=None, to_tracking=None, frm_call_args=[], to_call_args=[], between=None, between_args=[]):
        message_data = {}
        chips = []
        if frm_tracking is not None:
            message_data['from'] = frm_tracking 
        if to_tracking is not None:
            message_data['to'] = to_tracking 
        if isinstance(frm, Bank):
            chips.extend(frm.makeNewChips(amt))
        elif hasattr(frm, 'keys') or isinstance(frm, list):
            if len(frm[frm_attr_name]) < amt:
                amt = len(frm[frm_attr_name])
            #frm[frm_attr_name] -= amt
            chips.extend(frm[frm_attr_name][-amt:])
            frm[frm_attr_name] = frm[frm_attr_name][:-amt]
        else:
            frm_attr = getattr(frm, frm_attr_name)
            if len(frm_attr) < amt:
                amt = len(frm_attr)
            chips.extend(frm_attr[-amt:])
            setattr(frm, frm_attr_name, frm_attr[:-amt])
            #setattr(frm, frm_attr_name, (frm_attr - amt) if frm_attr - amt >= 0 else 0)

        to_return = None
        control = None
        if between is not None and hasattr(between, '__call__'):
            to_return, control = between(*between_args)

        if control is not None and 'amt' in control:
            # len(chips) - amt # Number of chips I have to move back to frm
            move_back = chips[control['amt']:]
            chips = chips[:control['amt']]
            if isinstance(frm, Bank):
                del move_back # Just drop them
            elif hasattr(frm, 'keys') or isinstance(frm, list):
                frm[frm_attr_name].extend(move_back)
            else:
                frm_attr = getattr(frm, frm_attr_name)
                frm_attr.extend(move_back)
                setattr(frm, frm_attr_name, frm_attr)

        if isinstance(to, Bank):
            raise Exception('The Bank should never get chips back.');
        elif hasattr(to, 'keys') or isinstance(to, list):
            #to[to_attr_name] = (to[to_attr_name] if to[to_attr_name] is not None else 0) + amt
            #chips.extend(frm[frm_attr_name][-amt:])
            #frm[frm_attr_name] = frm[frm_attr_name][:-amt]
            if to[to_attr_name] is None:
                to[to_attr_name] = []
            to[to_attr_name].extend(chips)
        else:
            to_attr = getattr(to, to_attr_name)
            if to_attr is None:
                to_attr = []
            to_attr.extend(chips)
            setattr(to, to_attr_name, to_attr)
        del chips[:]

        # publish about chip movement
        message_data['amt'] = amt
        pub.sendMessage('chip_movement', data=message_data)

        return to_return
