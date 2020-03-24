from pynput.keyboard import Key, Listener
import subprocess

isShiftPressed = False
def on_press(key):
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
                if keySupposed != "" and keySupposed != "SMART_OPEN":
                    k = ord(keySupposed[0])
                    if k > 95:
                        k = k - 32
                    elif k < 92:
                        k = k + 32
                    keySupposed = str(chr(k))
                    print(keySupposed, " ", keyPressed)
                    path = data[1].split("\n")[0]
                    path_list = list()
                    path_list.append(path)
                    if keySupposed == keyPressed:
                        print(keySupposed , " should open program ", path)
                        subprocess.Popen(path_list)

    except:
        print("special key is pressed")

with Listener(on_press=on_press) as listener:
    listener.join()
