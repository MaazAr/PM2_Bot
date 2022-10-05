import subprocess


def pm2logger(process):
    ls = subprocess.check_output(['pm2', 'logs', f'{process}', '--out', '--nostream'])
    ls = ls.decode()
    return ls
