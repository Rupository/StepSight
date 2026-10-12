from setup import take_snapshot, read_description 
from inference import get_desc

def stepsight_flow():
    take_snapshot()
    desc = get_desc()
    read_description(desc)

if __name__ == "__main__":
    while True:
        stepsight_flow()
