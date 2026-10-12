from termux import take_snapshot, read_description 
from vlm import get_desc


take_snapshot()
desc = get_desc()
if desc != 'null':
    read_description(desc)

