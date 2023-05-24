import angr
import sys

main_addr = 0x4011a9
find_addr = 0x401371
avoid_addr = 0x40134d

VARIABLE_CNT = 15
CHUNK_SIZE = 10

def main():
    proj = angr.Project('./src/prog', load_options={'auto_load_libs': False})
    state = proj.factory.blank_state(addr=main_addr)
    simgr = proj.factory.simulation_manager(state)
    simgr.explore(find=find_addr, avoid=avoid_addr)

    if simgr.found:
        find_result = simgr.found[0].posix.dumps(sys.stdin.fileno())

        for i in range(0, VARIABLE_CNT):
            data = find_result[i * CHUNK_SIZE : (i+1) * CHUNK_SIZE]
            print(int(data))

    else:
        print('Failed')

main()
