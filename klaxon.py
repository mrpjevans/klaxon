import os
import time, random
from threading import Thread
from flask import Flask, render_template, jsonify

app = Flask(__name__)

topThreadId = 0

# What are we running on?
isRPi = False
if os.uname()[4][:3] == 'arm':
    import automationhat #pylint: disable=all
    isRPi = True

# Switch on one of the three lights (with a seonsible timeout)
def switchOnLight(outputId):
    if isRPi:
        automationhat.output[outputId].on()
        t = Thread(target=timeout, args=(60,))
        t.start()

# Disco mode!
def discoMode():
    global topThreadId
    myId = time.time()
    topThreadId = myId
    for i in range(200):
        if topThreadId == myId:
            outputId = random.randint(0,2)
            mapping = ['one', 'two', 'three']
            automationhat.output[mapping[outputId]].on()
            time.sleep(0.1)
            automationhat.output[mapping[outputId]].off()
        
# Switch everything off after three seconds
# topThreadId allows only the newest thread to switch everything off
def timeout(duration):
    global topThreadId
    myId = time.time()
    topThreadId = myId
    time.sleep(duration)
    if topThreadId == myId:
        allOff()

# This function runs every time a request is received before routing.
# We switch off all the lights here.
@app.before_request
def allOff():
    if isRPi:
        automationhat.output.one.off()
        automationhat.output.two.off()
        automationhat.output.three.off()
        automationhat.relay.one.off()

# Our default home page      
@app.route('/')
def index():
    return render_template('index.html')

# The next functions switch on the lights
@app.route('/red')
def red():
    switchOnLight('one')
    return jsonify(True)

@app.route('/yellow')
def yellow():
    switchOnLight('two')
    return jsonify(True)

@app.route('/green')
def green():
    switchOnLight('three')
    return jsonify(True)

# Sound the very loud buzzer (then switch it off again automatically)
@app.route('/buzzer')
def buzzer():
    if isRPi:
        automationhat.relay.one.on()
        t = Thread(target=timeout, args=(1,))
        t.start()
    return jsonify(True)

# D I S C O
@app.route('/disco')
def disco():
    if isRPi:
        t = Thread(target=discoMode)
        t.start()
    return jsonify(True)

# Switch everything off
@app.route('/off')
def off():
    global topThreadId
    topThreadId = 0
    return jsonify(True)

# Shutdown
@app.route('/shutdown')
def shutdown():
    import os
    os.system('sudo shutdown -h now')
    return jsonify(True)


# Let's announce ourselves by making the lights blink
if isRPi:
    automationhat.output.one.on()
    time.sleep(0.2)
    automationhat.output.one.off()
    automationhat.output.two.on()
    time.sleep(0.2)
    automationhat.output.two.off()
    automationhat.output.three.on()
    time.sleep(0.2)
    automationhat.output.three.off()

# Start the web server on port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0')
    