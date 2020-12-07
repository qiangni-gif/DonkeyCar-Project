from flask import Flask
from flask import jsonify
from .control_relay import relay_on,relay_off
from .make_led_flash import light_on,light_off

app = Flask(__name__)


@app.route('/relay_on')
def frelay_on():
    print("receive relay on")
    code = 200
    desc = "success"
    try:
        light_on()
        relay_on()
    except Exception as err:
        code = 401
        desc = str(err)
    return jsonify({
        "code":code,
        "desc":desc
    })

@app.route('/relay_off')
def frelay_off():
    print("receive relay off")
    code = 200
    desc = "success"
    try:
        light_off()
        relay_off()
    except Exception as err:
        code = 401
        desc = str(err)
    return jsonify({
        "code":code,
        "desc":desc
    })

if __name__ == '__main__':
    app.run(host = "0.0.0.0",port=5000)