import subprocess
import json
from datetime import datetime


def pm2list():
    res = []
    ls = subprocess.check_output(['pm2', 'jlist'])
    ls = json.loads(ls.decode())
    for count, item in enumerate(ls):
        pid = ls[count]['pid']
        name = ls[count]['name']
        restarts = ls[count]['pm2_env']['restart_time']
        uptime = ls[count]['pm2_env']['pm_uptime']
        status = ls[count]['pm2_env']['status']
        cpu = ls[count]['monit']['cpu']
        memory = ls[count]['monit']['memory'] / 1000000
        time_obj = datetime.fromtimestamp(uptime / 1000)
        pmid = ls[count]['pm_id']
        if 'pmx_module' in ls[count]['pm2_env']:
            continue
        res.append([pid, name, restarts, status, cpu, memory, time_obj, pmid])
        with open("programs.txt", "w") as file:
            file.write(f"{name}\n")
            file.close()
    return res


