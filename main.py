from setup import initialize, take_snapshot, read_description 
from inference import get_desc

def stepsight_flow():
    take_snapshot()
    desc = get_desc()
    if desc != 'No changes detected.':
        read_description(desc)

if __name__ == "__main__":
    initialize()
    while True:
        stepsight_flow()
