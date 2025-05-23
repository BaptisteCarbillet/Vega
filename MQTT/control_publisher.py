from pynput import keyboard
from pynput.keyboard import Controller
import time
import paho.mqtt.client as mqtt

broker = 'argus.paris.inria.fr'

keyboard_controller = Controller()

def on_press(key):
    try:
        if key.char == 't':
            #mv_wheel x -x -x x
            mqttc.publish("mqtt/control", "FORWARD", qos=1)
            
        if key.char == 'y':
            #mv_wheel -x x x -x
            keyboard_controller.type('Hello')
            pass
        elif key.char == 'h':
            #mv_wheel -x x -x x
            pass
        elif key.char == 'f':
            #mv_wheel x -x x -x
            # Simulate pressing Enter
            pass
            keyboard_controller.press(keyboard.Key.enter)
            keyboard_controller.release(keyboard.Key.enter)
        elif key.char == 's':
            mqttc.publish("mqtt/control", "STOP", qos=1)
    except AttributeError:
        pass  # Special keys (like shift) won't have .char


def on_publish(client, userdata, mid, reason_code, properties):
    # reason_code and properties will only be present in MQTTv5. It's always unset in MQTTv3
    try:
        userdata.remove(mid)
    except KeyError:
        print("on_publish() is called with a mid not present in unacked_publish")
        print("This is due to an unavoidable race-condition:")
        print("* publish() return the mid of the message sent.")
        print("* mid from publish() is added to unacked_publish by the main thread")
        print("* on_publish() is called by the loop_start thread")
        print("While unlikely (because on_publish() will be called after a network round-trip),")
        print(" this is a race-condition that COULD happen")
        print("")
        print("The best solution to avoid race-condition is using the msg_info from publish()")
        print("We could also try using a list of acknowledged mid rather than removing from pending list,")
        print("but remember that mid could be re-used !")

unacked_publish = set()
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_publish = on_publish

mqttc.user_data_set(unacked_publish)
mqttc.connect(broker)
mqttc.loop_start()



# Start listening
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
