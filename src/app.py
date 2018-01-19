import urllib
from flask import Flask, render_template, url_for, json, jsonify, Response
from pabx_dialer.pgfetch import PostgresRegistrationSource
from pabx_dialer.pabx import PabxTarget

CRM_FMT = "https://api.production.apolloagriculture.com/call_center?{}"

source = PostgresRegistrationSource("dbname='registrations' user='postgres' host='localhost' password='Dev-2010'")
target = PabxTarget("http://192.168.88.36:8088", "test", "test", "+254709164000")

def get_goto_url(reg, ext):
    """gets the crm_fmt query
    reg = registration details
    ext = calling extension
    """
    if CRM_FMT is None:
        return ''
    query = urllib.urlencode({'callId': reg.reg_id, 'agentId':ext, 'campaign':'Registration', 'phoneNumber': reg.phone_number})
    return CRM_FMT.format(query)


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", jquery = url_for('static', filename='jquery3.2.1.min.js'))

@app.route("/call/<extension>", methods=['POST'])
def call(extension):
    reg = source.get_next_registration()
    if reg is not None:
        goto = get_goto_url(reg, extension)
        target.call(reg.phone_number, extension)
        source.mark_as_processed(reg)
        return Response(json.dumps({'called':'true', 'phoneNumber':reg.phone_number, 'goto': goto }), content_type="application/json")
    else:
        return Response(json.dumps({'called':'false'}), content_type="application/json")

app.run(debug=True)

