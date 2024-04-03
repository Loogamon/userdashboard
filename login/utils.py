from django.contrib import messages
from django.contrib.messages import get_messages

class MessageSplit:
    @staticmethod
    def parse(request):
        message_dict={}
        errors=get_messages(request)
        for m in errors:
            try:
                SPLIT=m.message.split("|",1)
                if SPLIT[0] not in message_dict:
                    message_dict[SPLIT[0]]=[]
                if SPLIT[0] in message_dict:
                    message_dict[SPLIT[0]].append(SPLIT[1])
            except IndexError:
                STR=m.message
                if '' not in message_dict:
                     message_dict['']=[]
                if '' in message_dict:
                     message_dict[''].append(STR)
        return message_dict

class Flasher:
    debug=0
    info=1
    success=2
    warning=3
    error=4
    @classmethod
    def push_messages(c,r,d,t):
        if isinstance(d, dict):
            for k,v in d.items():
                if t==c.debug:
                    messages.debug(r,v)
                if t==c.info:
                    messages.info(r,v)
                if t==c.success:
                    messages.success(r,v)
                if t==c.warning:
                    messages.warning(r,v)
                if t==c.error:
                    messages.error(r,v)
        if isinstance(d, list):
            for v in d:
                if t==c.debug:
                    messages.debug(r,v)
                if t==c.info:
                    messages.info(r,v)
                if t==c.success:
                    messages.success(r,v)
                if t==c.warning:
                    messages.warning(r,v)
                if t==c.error:
                    messages.error(r,v)
        if isinstance(d, str):
            if t==c.debug:
                messages.debug(r,d)
            if t==c.info:
                messages.info(r,d)
            if t==c.success:
                messages.success(r,d)
            if t==c.warning:
                messages.warning(r,d)
            if t==c.error:
                messages.error(r,d)