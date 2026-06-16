import inspect
import re
from pathlib import Path
from telethon import events
import THANOSPRO
from THANOSPRO.state import CMD_LIST, SUDO_LIST, LOAD_PLUG
from THANOSPRO.config import Config

def admin_cmd(pattern=None, command=None, **args):
    args["func"] = lambda e: e.via_bot_id is None
    stack = inspect.stack()
    previous_stack_frame = stack[1]
    file_test = Path(previous_stack_frame.filename)
    file_test = file_test.stem.replace(".py", "")
    allow_sudo = args.get("allow_sudo", False)
    
    if pattern is not None:
        if pattern.startswith(r"\#"):
            args["pattern"] = re.compile(pattern)
        elif pattern.startswith(r"^"):
            args["pattern"] = re.compile(pattern)
            cmd = pattern.replace("$", "").replace("^", "").replace("\\", "")
            try:
                CMD_LIST[file_test].append(cmd)
            except BaseException:
                CMD_LIST.update({file_test: [cmd]})
        else:
            handler = Config.HANDLER
            if len(handler) == 2:
                rishureg = "^" + handler
                reg = handler[1]
            else:
                rishureg = "^\\" + handler
                reg = handler
            args["pattern"] = re.compile(rishureg + pattern)
            cmd = reg + (command or pattern.replace("$", "").replace("\\", "").replace("^", ""))
            try:
                CMD_LIST[file_test].append(cmd)
            except BaseException:
                CMD_LIST.update({file_test: [cmd]})

    args["outgoing"] = True
    if allow_sudo:
        args["from_users"] = list(Config.SUDO_USERS)
        args["incoming"] = True
        if "allow_sudo" in args: del args["allow_sudo"]
    elif "incoming" in args and not args["incoming"]:
        args["outgoing"] = True

    args["blacklist_chats"] = True
    black_list_chats = list(Config.BL_CHAT)
    if black_list_chats:
        args["chats"] = black_list_chats

    return events.NewMessage(**args)

def sudo_cmd(pattern=None, command=None, **args):
    args["func"] = lambda e: e.via_bot_id is None
    stack = inspect.stack()
    previous_stack_frame = stack[1]
    file_test = Path(previous_stack_frame.filename)
    file_test = file_test.stem.replace(".py", "")
    allow_sudo = args.get("allow_sudo", False)
    
    if pattern is not None:
        if pattern.startswith(r"\#"):
            args["pattern"] = re.compile(pattern)
        elif pattern.startswith(r"^"):
            args["pattern"] = re.compile(pattern)
            cmd = pattern.replace("$", "").replace("^", "").replace("\\", "")
            try:
                SUDO_LIST[file_test].append(cmd)
            except BaseException:
                SUDO_LIST.update({file_test: [cmd]})
        else:
            handler = Config.SUDO_HANDLER
            if len(handler) == 2:
                rishureg = "^" + handler
                reg = handler[1]
            else:
                rishureg = "^\\" + handler
                reg = Config.HANDLER
            args["pattern"] = re.compile(rishureg + pattern)
            cmd = reg + (command or pattern.replace("$", "").replace("\\", "").replace("^", ""))
            try:
                SUDO_LIST[file_test].append(cmd)
            except BaseException:
                SUDO_LIST.update({file_test: [cmd]})
    
    args["outgoing"] = True
    if allow_sudo:
        args["from_users"] = list(Config.SUDO_USERS)
        args["incoming"] = True
        if "allow_sudo" in args: del args["allow_sudo"]
    elif "incoming" in args and not args["incoming"]:
        args["outgoing"] = True
        
    args["blacklist_chats"] = True
    black_list_chats = list(Config.BL_CHAT)
    if black_list_chats:
        args["chats"] = black_list_chats
        
    return events.NewMessage(**args)

def on(**args):
    def decorator(func):
        if THANOSPRO.bot:
            THANOSPRO.bot.add_event_handler(func, events.NewMessage(**args))
        from THANOSPRO.clients.session import get_multi_clients
        multi_clients = get_multi_clients()
        for client in multi_clients.values():
            if client:
                client.add_event_handler(func, events.NewMessage(**args))
        return func
    return decorator

def register(**args):
    # Simplified version for compatibility
    def decorator(func):
        if THANOSPRO.bot:
            THANOSPRO.bot.add_event_handler(func, events.NewMessage(**args))
        return func
    return decorator
