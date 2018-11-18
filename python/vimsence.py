import vim
import rpc
import time


def get_project_name():
    return vim.eval('expand("%:p:h:t")')


start_time = int(time.time())
project_name = get_project_name()
base_activity = {
        'details': "Just opened Vim",
        'state': f"Working on {project_name}",
        'timestamps': {
            "start": start_time
        },
        'assets': {
            # 'small_text': 'Vim',
            # 'small_image': 'vim_logo',
            'large_text': 'Vim',
            'large_image': 'vim_logo'
        }
    }

client_id = '513185202051350550'

try:
    rpc_obj = rpc.DiscordIpcClient.for_platform(client_id)
    rpc_obj.set_activity(base_activity)
except Exception:
    # Discord is not running
    pass


def update_presence():
    """Update presence in Discord
    :returns: TODO

    """
    activity = base_activity

    filename = get_filename()
    extension = get_extension()
    if filename:
        activity['details'] = f"Editing {filename}"
        activity['assets']['large_text'] = f"Editing a .{get_extension()} file"
    if extension:
        activity['assets']['large_image'] = extension

    try:
        rpc_obj.set_activity(activity)
    except BrokenPipeError:
        # Connection to Discord is lost
        pass
    except NameError:
        # Discord is not running
        pass


def get_filename():
    """Get current filename that is being edited
    :returns: string
    """
    return vim.eval('expand("%:t")')


def get_extension():
    """Get exension for file that is being edited
    :returns: string
    """
    return vim.eval('expand("%:e")')
