from pynput.keyboard import Key, Listener
import subprocess
isAltPressed = False
def on_press(key):
    global isAltPressed
    try:
        keyPressed = '{0}'.format(key.char)
        with open('smart_open.txt', 'r') as myfile:
            for line in myfile:
                data = line.split("=")
                if data[0] == "SMART_OPEN":
                    if data[1].split("\n")[0] == "1":
                        return
            myfile.close()
        with open('var.txt', 'r') as myfile:
            for line in myfile:
                data = line.split("=")
                keySupposed = data[0]
                if keySupposed != "" and isAltPressed == True:
                    print(keySupposed, " ", keyPressed)
                    path = data[1].split("\n")[0]
                    path_list = list()
                    path_list.append(path)
                    if keySupposed == keyPressed:
                        print(keySupposed , " should open program ", path)
                        subprocess.Popen(path_list)

    except:
        if key == Key.alt_l:
            isAltPressed = True

def on_release(key):
    if key == Key.alt:
        global isAltPressed
        isAltPressed = False

with Listener(on_press=on_press,on_release=on_release) as listener:
    listener.join()
