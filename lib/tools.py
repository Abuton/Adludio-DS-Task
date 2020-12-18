import json
import numpy as np
def load_input(request):
    json_str = request.get_data()
    if json_str is None:
        json_str = request.get_json()
    else:
        try:
            json_str = json.loads(json_str)
        except:
            json_str = None
    return json_str


def json_response(dict_):
    return json.dumps(dict_, cls=NumpyEncoder), 200, {'Content-Type': 'text/plain;charset=utf-8'}


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)
