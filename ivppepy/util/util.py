from flask import request as flask_request
from flask import session, current_app
from datetime import datetime
import json
import re
import pandas as pd



def get_request_val(request_key, default_val=None):
    val = default_val
    try:
        val = flask_request.args.get(request_key)
        if flask_request.method == "POST":
            val = flask_request.form.get(request_key)
    except:
        pass
    if val == None:
        val = default_val
    else :
        val = val.strip()
    return val

def redirect(url):
    url_str = """
        <script>
            location.href = "%s";
        </script>
    """%(url,)
    return url_str

def get_datetime_now(only_day=False, time_format = None) :
    _default = "%Y-%m-%d %H:%M:%S"
    
    if time_format != None :
        _format = time_format
    else :
        _format = _default
        if only_day == True :
            _format = "%Y-%m-%d"
    try: 
        return datetime.strftime(datetime.now(), _format)
    except :
        return datetime.strftime(datetime.now(), _default)

def response(dataset):
    return json.dumps(dataset, ensure_ascii=False)

def response_evt(success, dataset = None, message = "", is_json=True):
    if is_json :
        return json.dumps({
            "success" : success,
            "dataset" : dataset,
            "message" : message
        }, ensure_ascii=False)
    else :
        return {
            "success" : success,
            "dataset" : dataset,
            "message" : message
        }

def load_root_config(setting=None):
    if setting != None:
        curr_load_config = setting
    else:
        try :
            #config_file = open("/data/iclass_pe/config/load_config.json", "r")
            #curr_load_config = json.load(config_file)["load_config"]
            curr_load_config = current_app.config.get('LOAD_CONFIG')
            #config_file.close()
        except:
            curr_load_config = "dev1"
        
    config_file = open("/home/ryan-tku/project/iclass_pe/config/config.json", "r")
    config = json.load(config_file)
    config_file.close()
    
    return config[curr_load_config]

def load_file(file_name):
    """
    filepath路徑設定在config.json中的key=file_path
    """
    config = load_root_config()
    f = open(config['file_path'][file_name], "r")
    obj = json.load(f)
    f.close()
    return obj

def load_config(setting=None):
    config = load_root_config(setting)
    return config['config']

def load_db(db_name):
    config = load_root_config()
    return config['db'][db_name]