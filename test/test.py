from functools import singledispatch
import json


@singledispatch
def remove_null_bool(ob):
    return ob

@remove_null_bool.register(list)
def _process_list(ob):
    return [remove_null_bool(v) for v in ob]

@remove_null_bool.register(dict)
def _process_list(ob):
    return {k: remove_null_bool(v) for k, v in ob.items()
            if v is not None and v is not True and v is not False}

with open('tempJson.json') as json_file:
    data = json.load(json_file)
    #print(data)
    output_data = json.dumps(remove_null_bool(data), sort_keys=True)
    with open("output_json2.json", "w") as f:
        f.write(output_data)