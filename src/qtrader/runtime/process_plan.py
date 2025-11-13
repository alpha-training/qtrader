# runtime/process_plan.py

def topo_sort_processes(processes: dict) -> list:
    """
    Topologically sort processes based on "depends_on".
    Returns a list of process names in correct launch order.
    """

    # Kahn's algorithm
    in_degree = {name: 0 for name in processes}
    for name, cfg in processes.items():
        for dep in cfg.get("depends_on", []):
            in_degree[name] += 1

    queue = [name for name, indeg in in_degree.items() if indeg == 0]
    order = []

    while queue:
        node = queue.pop(0)
        order.append(node)

        for p, cfg in processes.items():
            if node in cfg.get("depends_on", []):
                in_degree[p] -= 1
                if in_degree[p] == 0:
                    queue.append(p)

    if len(order) != len(processes):
        raise RuntimeError("Cycle in process dependencies")

    return order


def build_launch_plan(cfg: dict) -> dict:
    """
    Build fully resolved launch plan:
    - compute full ports: base_port + offset
    - construct launch command: [qbin, script, "-p", port, ...args]
    - return ordered list of processes
    """
    vars = cfg["vars"]
    base_port = cfg["base_port"]
    processes = cfg["processes"]

    plan = {}

    for name, p in processes.items():           
        
        cmd = [vars["qbin"], "q/qi.q", "-name", name, "-loadf", "q/qtrader.q"]
        port = p.get("port", 0)
        port_offset = p.get("port_offset", 0)
        
        if port == 0 and port_offset != 0:
            port = base_port + port_offset
        
        if port != 0:
            cmd += ["-p", str(port)]

        if "args" in p:
            cmd += p["args"]

        plan[name] = {
            "cmd": cmd,
            "port": port,
            "depends_on": p.get("depends_on", [])
        }

    order = topo_sort_processes(processes)
    plan["_order"] = order

    return plan