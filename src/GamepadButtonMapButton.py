from qtpy import QtWidgets, QtCore
import threading
import pygame

class GamepadButtonMapButton(QtWidgets.QPushButton):
    mapping_changed = QtCore.Signal(str)  # Now emits a string (name or code)

    def __init__(self, index, initial_value, parent=None):
        super().__init__(str(initial_value), parent)
        self.index = index
        self.setText(str(initial_value))
        self.listening = False
        self.clicked.connect(self.start_listening)
        self._init_pygame()

    def _init_pygame(self):
        pygame.init()
        pygame.joystick.init()
        self.joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
        for js in self.joysticks:
            js.init()

    def start_listening(self):
        if not self.joysticks:
            QtWidgets.QMessageBox.warning(self, "No Gamepad", "No gamepad detected. Please connect a gamepad and try again.")
            return
        self.setText("Press a gamepad button...")
        self.listening = True
        threading.Thread(target=self.listen_for_gamepad, daemon=True).start()

    def listen_for_gamepad(self):
        TRIGGER_AXIS_IDS = [2, 5]  # LT and RT for Xbox controllers
        IGNORE_AXIS_IDS = [6]      # Ignore axis 6 (often tied to triggers or not used)
        TRIGGER_THRESHOLD = 0.5
        STICK_DEADZONE = 0.5

        while self.listening:
            pygame.event.pump()
            for js in self.joysticks:
                # Buttons
                for btn_id in range(js.get_numbuttons()):
                    if js.get_button(btn_id):
                        btn_name = self.button_index_to_name(js, btn_id)
                        QtCore.QMetaObject.invokeMethod(
                            self, "set_mapping", QtCore.Qt.QueuedConnection, QtCore.Q_ARG(str, btn_name)
                        )
                        self.listening = False
                        return
                # DPad (hat)
                for hat_id in range(js.get_numhats()):
                    hat = js.get_hat(hat_id)
                    if hat != (0, 0):
                        dpad_name = self.hat_value_to_name(hat)
                        if dpad_name:
                            QtCore.QMetaObject.invokeMethod(
                                self, "set_mapping", QtCore.Qt.QueuedConnection, QtCore.Q_ARG(str, dpad_name)
                            )
                            self.listening = False
                            return
                # Sticks and triggers
                for axis_id in range(js.get_numaxes()):
                    if axis_id in IGNORE_AXIS_IDS:
                        continue  # Skip ignored axes
                    axis_val = js.get_axis(axis_id)
                    if axis_id in TRIGGER_AXIS_IDS:
                        if axis_val > TRIGGER_THRESHOLD:
                            trigger_name = self.trigger_axis_to_name(axis_id)
                            QtCore.QMetaObject.invokeMethod(
                                self, "set_mapping", QtCore.Qt.QueuedConnection, QtCore.Q_ARG(str, trigger_name)
                            )
                            self.listening = False
                            return
                    else:
                        if abs(axis_val) > STICK_DEADZONE:
                            stick_name = self.stick_axis_to_name(axis_id, axis_val)
                            QtCore.QMetaObject.invokeMethod(
                                self, "set_mapping", QtCore.Qt.QueuedConnection, QtCore.Q_ARG(str, stick_name)
                            )
                            self.listening = False
                            return
            pygame.time.wait(10)

    def button_index_to_name(self, joystick, btn_id):
        # Xbox controller button mapping (common for XInput devices)
        xbox_names = [
            "A",        # 0
            "B",        # 1
            "X",        # 2
            "Y",        # 3
            "LB",       # 4
            "RB",       # 5
            "Back",     # 6
            "Start",    # 7
            "Guide",    # 8
            "LStick",   # 9 (press)
            "RStick",   # 10 (press)
        ]
        if btn_id < len(xbox_names):
            return xbox_names[btn_id]
        return f"Button{btn_id}"

    def hat_value_to_name(self, hat):
        # DPad mapping for a single hat (common for Xbox controllers)
        hat_map = {
            (0, 1): "DPad Up",
            (0, -1): "DPad Down",
            (-1, 0): "DPad Left",
            (1, 0): "DPad Right",
            (1, 1): "DPad UpRight",
            (-1, 1): "DPad UpLeft",
            (1, -1): "DPad DownRight",
            (-1, -1): "DPad DownLeft",
        }
        return hat_map.get(hat, None)

    def trigger_axis_to_name(self, axis_id):
        # Map trigger axis IDs to names for Xbox controller
        trigger_names = {
            2: "LT (Left Trigger)",
            5: "RT (Right Trigger)",
        }
        return trigger_names.get(axis_id, f"Trigger{axis_id}")

    def stick_axis_to_name(self, axis_id, axis_val):
        # Map stick axis IDs to names for Xbox controller
        # 0: Left Stick X, 1: Left Stick Y, 3: Right Stick X, 4: Right Stick Y
        stick_names = {
            0: ("Left Stick Left", "Left Stick Right"),
            1: ("Left Stick Up", "Left Stick Down"),
            3: ("Right Stick Left", "Right Stick Right"),
            4: ("Right Stick Up", "Right Stick Down"),
        }
        if axis_id in stick_names:
            neg, pos = stick_names[axis_id]
            return pos if axis_val > 0 else neg
        return f"Axis{axis_id}_{'+' if axis_val > 0 else '-'}"

    @QtCore.Slot(str)
    def set_mapping(self, btn_name):
        self.setText(btn_name)
        self.mapping_changed.emit(btn_name)