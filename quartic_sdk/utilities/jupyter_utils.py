import requests, os,subprocess, json

def get_ipynb_name():
    import ipykernel
    connection_file = os.path.basename(ipykernel.get_connection_file())
    kernel_id = connection_file.split('-', 1)[1].split('.')[0]
    token = os.getenv('JPY_API_TOKEN')
    server_url = json.loads(subprocess.check_output(['jupyter', 'server', 'list', '--json']))['url']
    sessions_url = server_url+'api/sessions/?token='+token
    sessions_resp = requests.get(sessions_url)
    sessions = sessions_resp.json()
    nb_path = None
    for session in sessions:
        if session['kernel']['id'] == kernel_id:
            nb_path = session['notebook']['path']
            break
    return nb_path
    