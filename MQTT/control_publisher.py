from pynput import keyboard
from pynput.keyboard import Controller
from pynput.keyboard import Key
import time
import paho.mqtt.client as mqtt

broker = 'argus.paris.inria.fr'

keyboard_controller = Controller()

def on_press(key):
    try:
        if key.char == 't':
            #mv_wheel x -x -x x
            mqttc.publish("mqtt/control", "FORWARD", qos=1)
            
        elif key.char == 's':
            #stop_wheel
            mqttc.publish("mqtt/control", "STOP", qos=1)

        elif key.char == 'g':
            #mv_wheel -x -x -x -x
            mqttc.publish("mqtt/control", "BACKWARD", qos=1)
        elif key.char == 'h':
            #mv_wheel -x x -x x
            mqttc.publish("mqtt/control", "RIGHT", qos=1)
        elif key.char == 'f':
            #mv_wheel x -x x -x
            mqttc.publish("mqtt/control", "LEFT", qos=1)
        elif key.char == 'y':
            #mv_wheel -x x x -x
            mqttc.publish("mqtt/control", "ROTATION_RIGHT", qos=1)
        elif key.char == 'r':
            #mv_wheel x -x -x x
            mqttc.publish("mqtt/control", "ROTATION_LEFT", qos=1)
        elif key.char == 'a':
            mqttc.publish("mqtt/control", "DECREASE_SPEED", qos=1)
        elif key.char == 'd':
            mqttc.publish("mqtt/control", "INCREASE_SPEED", qos=1)
        elif key.char == 'l':
            #mv_gimbal x 0 
            mqttc.publish("mqtt/control", "RIGHT_GIMBAL", qos=1)
        elif key.char == 'j':
            #mv_gimbal -x 0
            mqttc.publish("mqtt/control", "LEFT_GIMBAL", qos=1)
        elif key.char == 'i':
            #mv_gimbal 0 x
            mqttc.publish("mqtt/control", "UP_GIMBAL", qos=1)
        elif key.char == 'k':
            #mv_gimbal 0 -x
            mqttc.publish("mqtt/control", "DOWN_GIMBAL", qos=1)
        elif key.char == 'z':
            # center_gimbal
            mqttc.publish("mqtt/control", "CENTER_GIMBAL", qos=1)
    except AttributeError:
        pass  # Special keys (like shift) won't have .char


def on_publish(client, userdata, mid, reason_code, properties):
    # reason_code and properties will only be present in MQTTv5. It's always unset in MQTTv3
    try:
        userdata.remove(mid)
    except KeyError:
        print('Error')
        
unacked_publish = set()
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_publish = on_publish

mqttc.user_data_set(unacked_publish)
mqttc.connect(broker)
mqttc.loop_start()



# Start listening
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
