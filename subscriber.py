import argparse
# import os
# import signal
# import subprocess
import io

import paho.mqtt.client as mqtt
import matplotlib.pyplot as plt

# pro = None
plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True
plt.axis('off')

image_ = None

def on_message(client, obj, msg):
    try:
        on_message.counter += 1
    except AttributeError:
        on_message.counter = 1
    # global pro
    # if pro:
    #     os.killpg(os.getpgid(pro.pid), signal.SIGTERM)
    # f = open(f'./output/output.png', "wb")
    # f.write(msg.payload)
    print("Image Received")
    fio = io.BytesIO(msg.payload)
    global image_
    if image_ is None:
        fio = plt.imread(fio)
        image_ = plt.imshow(fio)
    else:
        fio = plt.imread(fio)
        image_.set_data(fio)

    # f = open(f'./output/output{on_message.counter}.png', "wb")
    # f.close()
    plt.pause(0.0001)
    plt.draw()
    # cmd = f"xdg-open ./output/output.png"
    # pro = subprocess.Popen(cmd,  stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT,
    #                     shell=True, preexec_fn=os.setsid)

def main(args):
    # Establish connection to mqtt broker
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(host=args['ip'], port=args['port'])
    client.subscribe('png', 0)

    try:
        client.loop_forever()
    except KeyboardInterrupt as e:
        pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",
                        default="localhost",
                        help="service ip of MQTT broker")
    parser.add_argument("--port",
                        default=1883,
                        type=int,
                        help="service port of MQTT broker")
    args = vars(parser.parse_args())
    main(args)