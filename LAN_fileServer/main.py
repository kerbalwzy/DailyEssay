from flask import Flask, make_response, jsonify
from werkzeug.routing import BaseConverter
import os


class MyReConverter(BaseConverter):
    def __init__(self, url_map, my_regex):
        super(MyReConverter, self).__init__(url_map)
        self.regex = my_regex


app = Flask(__name__)
app.url_map.converters['re'] = MyReConverter

@app.route('/<re(r".*"):file_name>')
def static_source(file_name):
    if not file_name:
        file_name = 'index.html'

    resp = make_response(app.send_static_file(filename=file_name))

    return resp

@app.route('/mulu')
def get_mulu():
    kejian_static_path = '/static/zipFiles/kejians'
    shipin_static_path = '/static/zipFiles/shipins'
    zuoye_static_path = '/static/zipFiles/zuoyes'

    local_path = os.path.dirname(__file__)
    kejian_files_path = local_path + kejian_static_path
    shipin_files_path = local_path + shipin_static_path
    zuoye_files_path = local_path + zuoye_static_path

    kejian_names = os.listdir(kejian_files_path)
    shipin_names = os.listdir(shipin_files_path)
    zuoye_names = os.listdir(zuoye_files_path)

    kejian_infos = [{'name': name, 'url': kejian_static_path + '/' + name} for name in kejian_names]
    shipin_infos = [{'name': name, 'url': shipin_static_path + '/' + name} for name in shipin_names]
    zuoye_infos = [{'name': name, 'url': zuoye_static_path + '/' + name} for name in zuoye_names]

    data = dict(kejian=kejian_infos, shipin=shipin_infos, zuoye=zuoye_infos)

    return jsonify(errno=1, errmgs='suc', data=data)


if __name__ == '__main__':
    app.run(host="192.168.15.200", port=8000)