import csv
import json

import requests
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseNotFound, HttpResponse
from dicttoxml import dicttoxml
from xml.etree import cElementTree as ET

def xml_to_json(xml_str):
    response = {}
    for child in list(xml_str):
        if len(list(child)) > 0:
            response[child.tag] = xml_to_json(child)
        else:
            response[child.tag] = child.text or ''
    return response


def json_to_xml():
    pass

def csv_to_json(reader):
    result = {}
    for row in reader:
        for column, value in row.items():
            result.setdefault(column, []).append(value)
            print('Column -> ', column, '\nValue -> ', value)

def convert_txt(strs):
    strs = strs.replace('=', '')
    return strs.split('  ')


def json_to_csv():
    pass


def csv_to_text():
    pass


@csrf_exempt
def archive_convert(request):
    body_unicode = request.body.decode()
    if body_unicode == "":
        return HttpResponseNotFound("Request body is empty")
    body = json.loads(body_unicode)
    data = body['message']
    old_type = body['old_type']
    new_type = body['new_type']
    data_to_send = {'message': data, 'type': old_type}
    new_request = requests.post("http://localhost:8000/string", data_to_send)

    if old_type == "text":
        if new_type == "text":
            return new_request
        elif new_type == "json":
            txt = convert_txt(new_request)
            response = {'upper': txt[1], 'lower': txt[3], 'special': txt[5]}
            return HttpResponse(json.dumps(response), content_type='application/json')
        elif new_type == 'xml':
            txt = convert_txt(new_request)
            dict = {}
            for x in range(0, len(txt), 2):
                dict[txt[x]] = txt[x + 1]
            xml = dicttoxml(dict, custom_root='data', attr_type=False)
            return xml

        else:
            return HttpResponseNotFound("Invalid type")

    if old_type == "xml":
        if new_type == "text":
            return ET.fromstring(new_request)

        elif new_type == "json":
            return HttpResponse(xml_to_json(new_request), content_type='application/json')

        elif new_type == "csv":
            pass

        else:
            return HttpResponseNotFound("Invalid type")

    if old_type == "json":
        if new_type == "text":
            elements = ['upper', 'lower', 'special']
            str = ""
            for element in elements:
                str += element + " = " + new_request['element']
        
        elif new_type == "xml":
            return json_to_xml()
        
        elif new_type == "csv":
            return json_to_csv()

        else:
            return HttpResponseNotFound("Invalid type")

    if old_type == "csv":
        if new_type == "json":
            return HttpResponse(xml_to_json(new_request), content_type='application/json')

        elif new_type == "text":
            return csv_to_text()

        elif new_type == "xml":
            pass

        else:
            return HttpResponseNotFound("Invalid type")


@csrf_exempt
def convert(request):
    body_unicode = request.body.decode('utf-8')
    if body_unicode == "":
        return HttpResponseNotFound("Request body is empty")
    body = json.loads(body_unicode)
    data = body['message']
    type = body['type']
    data_to_send = {'message': data, 'type': type}
    request = request.post("http://localhost:8000/string", data_to_send)
    dict = request.text
    lower = dict['lower']
    upper = dict['upper']
    special = dict['special']
    if type == "txt":
        message = "lower = {} upper = {} special = {}".format(lower, upper, special)
        return message
    if type == "json":
        response = {'upper': upper, 'lower': lower, 'special': special}
        return HttpResponse(json.dumps(response), content_type='application/json')

    if type == "xml":
        xml = dicttoxml(dict, custom_root='data', attr_type=False)
        return xml

    if type == "csv":
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename="somefilename.csv"'},
        )
        writer = csv.writer(response)
        writer.writerow(['upper', upper])
        writer.writerow(['lower', lower])
        writer.writerow(['special', special])
        return response
