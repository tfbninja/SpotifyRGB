from serial import Serial


class RemoteManager:

    def __init__(self, ser: Serial):
        self.serial = ser
        self.pending_commands = []
        self.command_list = ["BDown", "BUp", "POW", "R", "G", "B", "W", "Orange", "Green", "Navy", "Magenta", "Yellow",
                             "Blue", "Purple", "Pink", "Demo", "Color", "Mode+", "Mode-", "Music1", "Music2", "Speed+",
                             "Speed-"]
        self.commands_list_raw = [255, 32895, 49215, 8415, 41055, 24735, 57375, 4335, 36975, 20655, 53295, 12495, 45135,
                                  28815, 61455, 2295, 34935, 18615, 51255, 10455, 43095, 26775, 59415]
        self.modes = ["static", "dynamic"]
        self.dynamic_modes = ["ambient", "music"]
        self.dynamic_mode_types = ["normal", "adhd"]
        self.state = {
            "power": True,
            "brightness": 100,
            "mode": "static",
            "static_color": "blue",
            "dynamic_mode": "music",
            "dynamic_mode_type": "adhd",
            "speed": 10
        }

    def rawToCommand(self, raw):
        return self.comands_list_raw[self.commands_list_raw.index(raw)]

    def receive(self):
        pass

    def hasPendingCommand(self):
        return len(self.pending_commands) > 0

    def getPendingCommand(self):
        command = self.pending_commands[0]
        self.pending_commands.remove(0)
        return command

    def getCommandList(self):
        return self.command_list
