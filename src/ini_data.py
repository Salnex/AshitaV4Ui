import re
ini_structure = {
    "ashita.launcher": {
        "autoclose": "1",
        "name": "",
    },
    "ashita.boot": {
        "file": ".\\bootloader\\pol.exe",
        "command": "--server yourserver.com",
        "gamemodule": "ffximain.dll",
        "script": "default.txt",
        "args": ""
    },
    "ashita.fonts": {
        "d3d8.disable_scaling": "0",
        "d3d8.family": "Arial",
        "d3d8.height": "10"
    },
    "ashita.input": {
        "gamepad.allowbackground": "0",
        "gamepad.disableenumeration": "0",
        "keyboard.blockinput": "0",
        "keyboard.blockbindsduringinput": "1",
        "keyboard.silentbinds ": "0",
        "keyboard.windowskeyenabled": "0",
        "mouse.blockinput": "0",
        "mouse.unhook": "1"
    },
    "ashita.language": {
        "playonline": "2",
        "ashita": "2"
    },
    "ashita.logging": {
        "level": "5",
        "crashdumps": "1"
    },
    "ashita.misc": {
        "addons.silent": "0",
        "aliases.silent": "0",
        "plugins.silent": "0"
    },
    "ashita.polplugins": {
        "sandbox": "0"
    },
    "ashita.polplugins.args": {
        ";sandbox": ""
    },
    "ashita.resources": {
        "offsets.use_overrides": "1",
        "pointers.use_overrides": "1",
        "resources.use_overrides": "1"
    },
    "ashita.taskpool": {
        "threadcount": "-1"
    },
    "ashita.window.startpos": {
        "x": "-1",
        "y": "-1"
    },
    "ffxi.direct3d8": {
        "presentparams.backbufferformat": "-1",
        "presentparams.backbuffercount": "-1",
        "presentparams.multisampletype": "-1",
        "presentparams.swapeffect": "-1",
        "presentparams.enableautodepthstencil": "-1",
        "presentparams.autodepthstencilformat": "-1",
        "presentparams.flags": "-1",
        "presentparams.fullscreen_refreshrateinhz": "-1",
        "presentparams.fullscreen_presentationinterval": "-1",
        "behaviorflags.fpu_preserve": "0"
    },
    "ffxi.registry": {
        "0000": "6",
        "0001": "1920",
        "0002": "1080",
        "0003": "4096",
        "0004": "4096",
        "0005": "-1",
        "0006": "-1",
        "0007": "1",
        "0008": "-1",
        "0009": "-1",
        "0010": "-1",
        "0011": "2",
        "0012": "-1",
        "0013": "-1",
        "0014": "-1",
        "0015": "-1",
        "0016": "-1",
        "0017": "0",
        "0018": "2",
        "0019": "1",
        "0020": "0",
        "0021": "1",
        "0022": "0",
        "0023": "0",
        "0024": "-1",
        "0025": "-1",
        "0026": "-1",
        "0027": "-1",
        "0028": "0",
        "0029": "20",
        "0030": "0",
        "0031": "1002740646",
        "0032": "0",
        "0033": "0",
        "0034": "1",
        "0035": "1",
        "0036": "2",
        "0037": "1920",
        "0038": "1080",
        "0039": "1",
        "0040": "0",
        "0041": "0",
        "0042": "C:\\Program Files (x86)\\SquareEnix\\FINAL FANTASY XI",
        "0043": "1",
        "0044": "1",
        "0045": "0",
        "padmode000": "-1",
        "padsin000": "-1",
        "padguid000": "-1"
    }
}
tooltips = {
    "ashita.launcher": {
        "autoclose": (
            "Sets if the launcher should automatically close after successfully launching this configuration.\n"
            "Type: boolean"
        ),
        "name": (
            "The name of the configuration to display in the launcher. "
            "If left empty, the launcher will use the file name instead.\n"
            "Type: string"
        ),
    },
    "ashita.boot": {
        "file": (
            "Sets the boot file to launch to start FFXI.\n"
            "If playing on retail, this can be left empty. Ashita will automatically find a valid install and launch the game. "
            "However, you may want to directly set this still if you have multiple game installs of FFXI. "
            "If playing on a private server, this should point to the boot loader used with the server.\n"
            "Type: string"
        ),
        "command": (
            "Sets the boot command that is passed to the boot loader (file) on launch.\n"
            "If playing on a private server, this should be the commands required by the server you are playing on in order to properly connect. "
            "(Usually the --server <ip> command is enough.)\n"
            "Type: string"
        ),
        "gamemodule": (
            "Sets the name of the main game module Ashita should use when doing game module lookups.\n"
            "If left blank, this will resolve to FFXiMain.dll. This should only be changed if the private server you are playing on has renamed FFXiMain.dll to something else.\n"
            "Type: string"
        ),
        "script": (
            "Sets the script file to execute after Ashita has successfully injected into the game.\n"
            "If left blank, Ashita will not execute any script automatically.\n"
            "Type: string"
        ),
        "args": (
            "Sets the script arguments to pass to the 'script' (if set) above when it's executed.\n"
            "This can be useful if you share a script between multiple characters, but want to use specific values for token replacements. "
            "Such as binds/aliases that use the profiles specific character name.\n"
            "Type: string"
        ),
    },
    "ashita.fonts": {
        "d3d8.disable_scaling": (
            "Sets if Ashita will disable scaling the Direct3D font objects by default.\n"
            "If false, Ashita attempts to scale font objects based on the system's DPI setting. "
            "Otherwise, Ashita will default to its old behavior of an enforced scaling size.\n"
            "Type: boolean"
        ),
        "d3d8.family": (
            "Sets the default font family (face) that is used when creating a font object but not specifying one.\n"
            "Type: string"
        ),
        "d3d8.height": (
            "Sets the default font height that is used when creating a font but not specifying one.\n"
            "Type: number"
        ),
    },
    "ashita.input": {
        "gamepad.allowbackground": (
            "Sets if controllers should still work if the game is out of focus.\n"
            "Type: boolean"
        ),
        "gamepad.disableenumeration": (
            "Sets if Ashita should disable the ability for game controllers to be discovered.\n"
            "This is useful to turn on if you leave controllers enabled but not use one. You may notice a micro-stutter while playing. "
            "Turning this on will usually fix that micro-stutter. However, while this is on, you will not be able to use a controller until its turned off.\n"
            "Type: boolean"
        ),
        "keyboard.blockinput": (
            "Sets if Ashita should completely disable all keyboard input.\n"
            "Type: boolean"
        ),
        "keyboard.blockbindsduringinput": (
            "Sets if Ashita should ignore keybinds while the game is expecting input.\n"
            "This will block keybinds while entering chat into the chat box, or editing things like search comments, bazaar comments, etc.\n"
            "Type: boolean"
        ),
        "keyboard.silentbinds ": (
            "Sets if Ashita should announce bind related information, such as setting a new keybind.\n"
            "If enabled, Ashita will not print bind related messages to the chat log.\n"
            "Type: boolean"
        ),
        "keyboard.windowskeyenabled": (
            "Sets if the Windows key should be enabled and work like normal.\n"
            "Type: boolean"
        ),
        "mouse.blockinput": (
            "Sets if Ashita should completely block all mouse input.\n"
            "Type: boolean"
        ),
        "mouse.unhook": (
            "Sets if Ashita should unhook the mouse from being automatically repositioned by the game menu system.\n"
            "Type: boolean"
        ),
    },
    "ashita.language": {
        "playonline": (
            "Sets the default PlayOnline language the launcher will use when trying to launch retail and no direct boot file was given.\n"
            "If set to 0, Ashita will default to English.\n"
            "Valid values are: 0 = Default, 1 = Japanese, 2 = English, 3 = European\n"
            "Type: number"
        ),
        "ashita": (
            "Sets the default language used with the internal ResourceManager string data.\n"
            "If set to 0 or 3, Ashita will default to English. (SE no longer translates strings to European.)\n"
            "Valid values are: 0 = Default, 1 = Japanese, 2 = English, 3 = European\n"
            "Type: number"
        ),
    },
    "ashita.logging": {
        "level": (
            "Sets the level of debugging information Ashita will output to its log files.\n"
            "Valid values are: 0 = None, 1 = Critical, 2 = Error, 3 = Warn, 4 = Info, 5 = Debug\n"
            "Type: number"
        ),
        "crashdumps": (
            "Sets if Ashita should create crash dumps automatically when a critical error occurs.\n"
            "Type: number"
        ),
    },
    "ashita.misc": {
        "addons.silent": (
            "Sets if Ashita should stop announcing loading and unloading addons to the chat window.\n"
            "Type: boolean"
        ),
        "aliases.silent": (
            "Sets if Ashita should stop announcing alias related command results to the chat window.\n"
            "Type: boolean"
        ),
        "plugins.silent": (
            "Sets if Ashita should stop announcing loading and unloading plugins to the chat window.\n"
            "Type: boolean"
        ),
    },
    "ashita.polplugins": {
        "sandbox": (
            "Contains the list of plugins Ashita will launch immediately as it injects. (IPolPlugin instances.)\n"
            "This does not work with normal plugins! This will only work for 'PlayOnline Plugins'.\n"
            "This section expects each entry to be the name of the plugin and a boolean value (0 or 1) if it should be enabled.\n"
            "Type: boolean"
        ),
    },
    "ashita.polplugins.args": {
        ";sandbox": (
            "Contains the plugin-specific arguments to pass to a 'PlayOnline Plugin' when its loaded.\n"
            "This section expects each entry to be the name of the plugin and a string value of arguments to be passed to the plugin when its loaded.\n"
            "Type: string"
        ),
    },
    "ashita.resources": {
        "offsets.use_overrides": (
            "Sets if Ashita should load and merge in the custom overrides within the custom.offsets.ini configuration file.\n"
            "Type: boolean"
        ),
        "pointers.use_overrides": (
            "Sets if Ashita should load and merge in the custom overrides within the custom.pointers.ini configuration file.\n"
            "Type: boolean"
        ),
        "resources.use_overrides": (
            "Sets if Ashita should load and merge in the custom overrides within the custom.datmap.ini configuration file.\n"
            "Type: boolean"
        ),
    },
    "ashita.taskpool": {
        "threadcount": (
            "Sets the maximum number of threads the task queue will attempt to use.\n"
            "If set to 0 or lower, the internal task queue will query the system for the available number of logical cores and determine the best number of threads to use. "
            "It is recommended to leave this as -1 and let the system determine the best number itself.\n"
            "Type: number"
        ),
    },
    "ashita.window.startpos": {
        "x": (
            "Sets the X screen position to start the game window at.\n"
            "If set to -1, will use the center X position of the screen.\n"
            "Type: number"
        ),
        "y": (
            "Sets the Y screen position to start the game window at.\n"
            "If set to -1, will use the center Y position of the screen.\n"
            "Type: number"
        ),
    },
    "ffxi.direct3d8": {
        "presentparams.backbufferformat": (
            "Sets the back buffer format passed with the device creation present parameters.\n"
            "Type: number"
        ),
        "presentparams.backbuffercount": (
            "Sets the back buffer count passed with the device creation present parameters.\n"
            "Type: number"
        ),
        "presentparams.multisampletype": (
            "Sets the multisample type passed with the device creation present parameters.\n"
            "Type: number"
        ),
        "presentparams.swapeffect": (
            "Sets the swap effect passed with the device creation present parameters.\n"
            "Type: number"
        ),
        "presentparams.enableautodepthstencil": (
            "Sets the auto-depth stencil enabled flag passed with the device creation present parameters.\n"
            "Type: number"
        ),
        "presentparams.autodepthstencilformat": (
            "Sets the auto-depth stencil format passed with the device creation present parameters.\n"
            "Type: number"
        ),
        "presentparams.flags": (
            "Sets the flags passed with the device creation present parameters.\n"
            "Type: number"
        ),
        "presentparams.fullscreen_refreshrateinhz": (
            "Sets the fullscreen refresh rate passed with the device creation present parameters.\n"
            "Type: number"
        ),
        "presentparams.fullscreen_presentationinterval": (
            "Sets the fullscreen presentation interval passed with the device creation present parameters.\n"
            "Type: number"
        ),
        "behaviorflags.fpu_preserve": (
            "Sets if the fpu preserve behavior flag is enabled by force.\n"
            "Type: number"
        ),
    },
    "ffxi.registry": {
        "0000": (
            "Sets the games mip mapping setting.\n"
            "Valid values: 0 = Off, 1 = On, Lowest Quality ... 6 = On, Best Quality\n"
            "Type: number"
        ),
        "0001": (
            "Sets the games window resolution width.\n"
            "Type: number"
        ),
        "0002": (
            "Sets the games window resolution height.\n"
            "Type: number"
        ),
        "0003": (
            "Sets the games background resolution width.\n"
            "For best performance, this value is best if divisible by 2.\n"
            "Type: number"
        ),
        "0004": (
            "Sets the games background resolution height.\n"
            "For best performance, this value is best if divisible by 2.\n"
            "Type: number"
        ),
        "0005": (
            "Unknown / unused.\n"
            "Type: number"
        ),
        "0006": (
            "Unknown / unused.\n"
            "Type: number"
        ),
        "0007": (
            "Sets if the games sound is enabled.\n"
            "Valid values: 0 = Disabled, 1 = Enabled\n"
            "Type: number"
        ),
        "0008": (
            "Unknown / unused.\n"
            "Type: number"
        ),
        "0009": (
            "Unknown / unused.\n"
            "Type: number"
        ),
        "0010": (
            "Unknown / unused.\n"
            "Type: number"
        ),
        "0011": (
            "Sets the games environment animations mode.\n"
            "Value values: 0 = Off, 1 = Normal, 2 = Smooth\n"
            "Type: number"
        ),
        "0012": (
            "Unknown / unused.\n"
            "Type: number"
        ),
        "0013": (
            "Unknown / unused.\n"
            "Type: number"
        ),
        "0014": (
            "Unknown / unused.\n"
            "Type: number"
        ),
        "0015": (
            "Unknown / unused.\n"
            "Type: number"
        ),
        "0016": (
            "Unknown / unused.\n"
            "Type: number"
        ),
        "0017": (
            "Sets the games bump mapping.\n"
            "Valid values: 0 = Off, 1 = On\n"
            "Type: number"
        ),
        "0018": (
            "Sets the games texture compression level.\n"
            "Valid values: 0 = High, 1 = Low, 2 = Uncompressed\n"
            "Type: number"
        ),
        "0019": (
            "Sets the games texture compression level.\n"
            "Valid values: 0 = Compressed, 1 = Uncompressed\n"
            "Type: number"
        ),
        "0020": (
            "Unknown / unused.\n"
            "Type: number"
        ),
        "0021": (
            "Sets the games hardware mouse option.\n"
            "Valid values: 0 = Off, 1 = On\n"
            "Type: number"
        ),
        "0022": (
            "Sets the games show opening movie option.\n"
            "Valid values: 0 = Off, 1 = On\n"
            "Type: number"
        ),
        "0023": (
            "Sets the games simplified character creation visuals option.\n"
            "Valid values: 0 = Off, 1 = On\n"
            "Type: number"
        ),
        "0024": (
            "Unknown / unused.\n"
            "Type: number"
        ),
        "0025": (
            "Unknown / unused.\n"
            "Type: number"
        ),
        "0026": (
            "Unknown / unused.\n"
            "Type: number"
        ),
        "0027": (
            "Unknown / unused.\n"
            "Type: number"
        ),
        "0028": (
            "Sets the games gamma base.\n"
            "Float based value, 0 is the default game value.\n"
            "Type: number"
        ),
        "0029": (
            "Sets the games maximum number of sounds.\n"
            "Valid values: 12 = Lowest ... 20 = Highest\n"
            "Type: number"
        ),
        "0030": (
            "Sets the games 3D LCD mode.\n"
            "Valid values: 0 = Disabled, 1 = Enabled\n"
            "Type: number"
        ),
        "0031": (
            "Unknown / unused.\n"
            "Type: number"
        ),
        "0032": (
            "Unknown / unused.\n"
            "Type: number"
        ),
        "0033": (
            "Unknown / unused.\n"
            "Type: number"
        ),
        "0034": (
            "Sets the games windowed mode.\n"
            "Valid values: 0 = Fullscreen, 1 = Windowed, 2 = Fullscreen Windowed (Undocumented), 3 = Borderless Windowed\n"
            "Note: There is a bug in the official client handling of this setting where Borderless Windowed is actually Fullscreen Windowed, and Fullscreen Windowed is actually Borderless Windowed.\n"
            "Type: number"
        ),
        "0035": (
            "Sets the games sound always on option. (Play sound while game is in background.)\n"
            "Valid values: 0 = Off, 1 = On\n"
            "Type: number"
        ),
        "0036": (
            "Sets the games font compression.\n"
            "Valid values: 0 = Compressed, 1 = Uncompressed, 2 = High Quality\n"
            "Type: number"
        ),
        "0037": (
            "Sets the games menu resolution width.\n"
            "Type: number"
        ),
        "0038": (
            "Sets the games menu resolution height.\n"
            "Type: number"
        ),
        "0039": (
            "Sets the games IME mode.\n"
            "Valid values: 0 = v1, 1 = v2\n"
            "Type: number"
        ),
        "0040": (
            "Sets the games graphics stabilization option.\n"
            "Valid values: 0 = Off, 1 = On\n"
            "Type: number"
        ),
        "0041": (
            "Sets the games beta UI option.\n"
            "Valid values: 0 = Disabled, 1 = Enabled\n"
            "Note: This is not available in the retail client.\n"
            "Type: number"
        ),
        "0042": (
            "Sets the games default screenshot path.\n"
            "Note: This path is only used for the games built-in screenshots. The included Screenshots plugin from Ashita does not use this path.\n"
            "Type: string"
        ),
        "0043": (
            "Sets the games screenshot in screen resolution option.\n"
            "Valid values: 0 = Off, 1 = On\n"
            "Note: The included Screenshots plugin from Ashita does not use this option.\n"
            "Type: number"
        ),
        "0044": (
            "Sets the games maintain window aspect ratio option.\n"
            "Valid values: 0 = Off, 1 = On\n"
            "Type: number"
        ),
        "0045": (
            "Unknown / unused.\n"
            "Type: number"
        ),
        "padmode000": (
            "Sets the games gamepad configuration settings.\n"
            "Type: array"
        ),
        "padsin000": (
            "Sets the games gamepad button map settings.\n"
            "Type: array"
        ),
        "padguid000": (
            "Sets the games gamepad GUID that the client will attempt to automatically attach to.\n"
            "Type: string"
        ),
    },
}

padmode000_options = [
    ("Enable Gamepad", "Enables or disables the gamepad functionality."),
    ("Enable Force Feedback", "Enables or disables the gamepad force feedback (rumble) features."),
    ("Enable Sliders", "Enables or disables the gamepad slider controls."),
    ("Enable Hat Switches", "Enables or disables the gamepad hat switch controls."),
    ("Enable When Inactive", "Enables or disables the gamepad working if the game window is not focused."),
    ("Enable XInput", "Enables or disables if the gamepad should be detected as XInput or not."),
]

padsin000_options = [
    ("Toggle auto-run.", "Button for toggling auto-run."),
    ("Toggle CTRL macro bar display.", "Button for toggling CTRL macro bar display."),
    ("Toggle first/third person view.", "Button for toggling first/third person view."),
    ("Toggle ALT macro bar display.", "Button for toggling ALT macro bar display."),
    ("Toggle /heal, lock target.", "Button for /heal or lock target."),
    ("Cancel.", "Button for cancel."),
    ("Main menu.", "Button for main menu."),
    ("Select, Confirm selection.", "Button for select/confirm."),
    ("Select active window.", "Button for selecting active window."),
    ("Toggle menu/window visibility.", "Button for toggling menu/window visibility."),
    ("Menu navigation with movement thumbstick while held.", "Button for menu navigation with thumbstick."),
    ("Move camera with movement thumbstick while held.", "Button for moving camera with thumbstick."),
    ("Toggle logout window.", "Button for toggling logout window."),
    ("Player movement. (up)", "Button for player movement up."),
    ("Player movement. (down)", "Button for player movement down."),
    ("Player movement. (left)", "Button for player movement left."),
    ("Player movement. (right)", "Button for player movement right."),
    ("Camera movement. (up)", "Button for camera movement up."),
    ("Camera movement. (down)", "Button for camera movement down."),
    ("Camera movement. (left)", "Button for camera movement left."),
    ("Camera movement. (right)", "Button for camera movement right."),
    ("Menu movement. (up)", "Button for menu movement up (also targeting)."),
    ("Menu movement. (down)", "Button for menu movement down (also targeting)."),
    ("Menu movement. (left)", "Button for menu movement left (also targeting)."),
    ("Menu movement. (right)", "Button for menu movement right (also targeting)."),
    ("Take screenshot. (Menu/windows must be hidden.)", "Button for taking screenshot."),
    ("Toggle use of movement, menu and camera controls.", "Button for toggling use of movement/menu/camera controls."),
]

friendly_names = {
    "ashita.launcher": {
        "autoclose": "Auto Close Launcher",
        "name": "Profile Name",
    },
    "ashita.boot": {
        "file": "Boot File",
        "command": "Boot Command",
        "gamemodule": "Game Module",
        "script": "Startup Script",
        "args": "Script Arguments",
    },
    "ashita.fonts": {
        "d3d8.disable_scaling": "Disable Font Scaling",
        "d3d8.family": "Font Family",
        "d3d8.height": "Font Height",
    },
    "ashita.input": {
        "gamepad.allowbackground": "Allow Gamepad in Background",
        "gamepad.disableenumeration": "Disable Gamepad Enumeration",
        "keyboard.blockinput": "Block Keyboard Input",
        "keyboard.blockbindsduringinput": "Block Binds During Input",
        "keyboard.silentbinds ": "Silent Keybinds",
        "keyboard.windowskeyenabled": "Enable Windows Key",
        "mouse.blockinput": "Block Mouse Input",
        "mouse.unhook": "Unhook Mouse",
    },
    "ashita.language": {
        "playonline": "PlayOnline Language",
        "ashita": "Ashita Language",
    },
    "ashita.logging": {
        "level": "Log Level",
        "crashdumps": "Enable Crash Dumps",
    },
    "ashita.misc": {
        "addons.silent": "Silent Addons",
        "aliases.silent": "Silent Aliases",
        "plugins.silent": "Silent Plugins",
    },
    "ashita.polplugins": {
        "sandbox": "Enable Sandbox Plugin",
    },
    "ashita.polplugins.args": {
        ";sandbox": "Sandbox Plugin Arguments",
    },
    "ashita.resources": {
        "offsets.use_overrides": "Use Offsets Overrides",
        "pointers.use_overrides": "Use Pointers Overrides",
        "resources.use_overrides": "Use Resources Overrides",
    },
    "ashita.taskpool": {
        "threadcount": "Thread Count",
    },
    "ashita.window.startpos": {
        "x": "Window Start X",
        "y": "Window Start Y",
    },
    "ffxi.direct3d8": {
        "presentparams.backbufferformat": "Back Buffer Format",
        "presentparams.backbuffercount": "Back Buffer Count",
        "presentparams.multisampletype": "Multisample Type",
        "presentparams.swapeffect": "Swap Effect",
        "presentparams.enableautodepthstencil": "Enable Auto Depth Stencil",
        "presentparams.autodepthstencilformat": "Auto Depth Stencil Format",
        "presentparams.flags": "Flags",
        "presentparams.fullscreen_refreshrateinhz": "Fullscreen Refresh Rate (Hz)",
        "presentparams.fullscreen_presentationinterval": "Fullscreen Presentation Interval",
        "behaviorflags.fpu_preserve": "FPU Preserve Flag",
    },
    "ffxi.registry": {
        "0000": "Mip Mapping",
        "0001": "Window Resolution Width",
        "0002": "Window Resolution Height",
        "0003": "Background Resolution Width",
        "0004": "Background Resolution Height",
        "0005": "Unknown Setting 5",
        "0006": "Unknown Setting 6",
        "0007": "Enable Sound",
        "0008": "Unknown Setting 8",
        "0009": "Unknown Setting 9",
        "0010": "Unknown Setting 10",
        "0011": "Environment Animations",
        "0012": "Unknown Setting 12",
        "0013": "Unknown Setting 13",
        "0014": "Unknown Setting 14",
        "0015": "Unknown Setting 15",
        "0016": "Unknown Setting 16",
        "0017": "Bump Mapping",
        "0018": "Texture Compression Level",
        "0019": "Texture Compression",
        "0020": "Unknown Setting 20",
        "0021": "Hardware Mouse",
        "0022": "Show Opening Movie",
        "0023": "Simplified Character Creation",
        "0024": "Unknown Setting 24",
        "0025": "Unknown Setting 25",
        "0026": "Unknown Setting 26",
        "0027": "Unknown Setting 27",
        "0028": "Gamma Base",
        "0029": "Max Sounds",
        "0030": "3D LCD Mode",
        "0031": "Unknown Setting 31",
        "0032": "Unknown Setting 32",
        "0033": "Unknown Setting 33",
        "0034": "Windowed Mode",
        "0035": "Sound Always On",
        "0036": "Font Compression",
        "0037": "Menu Resolution Width",
        "0038": "Menu Resolution Height",
        "0039": "IME Mode",
        "0040": "Graphics Stabilization",
        "0041": "Beta UI",
        "0042": "Screenshot Path",
        "0043": "Screenshot in Screen Resolution",
        "0044": "Maintain Aspect Ratio",
        "0045": "Unknown Setting 45",
        "padmode000": "Gamepad Configuration",
        "padsin000": "Gamepad Button Map",
        "padguid000": "Gamepad GUID",
    },
}

ui_metadata = {
    "ashita.launcher": {
        "autoclose": {"widget": "checkbox", "show": True, "tab": "Ashita"},
        "name": {"widget": "lineedit", "show": True, "tab": "Ashita"},
    },
    "ashita.boot": {
        "file": {"widget": "lineedit", "show": True, "tab": "Ashita"},
        "command": {"widget": "lineedit", "show": True, "tab": "Ashita"},
        "gamemodule": {"widget": "lineedit", "show": True, "tab": "Ashita"},
        "script": {"widget": "lineedit", "show": True, "tab": "Ashita"},
        "args": {"widget": "lineedit", "show": True, "tab": "Ashita"},
    },
    "ashita.fonts": {
        "d3d8.disable_scaling": {"widget": "checkbox", "show": True, "tab": "Ashita"},
        "d3d8.family": {"widget": "lineedit", "show": True, "tab": "Ashita"},
        "d3d8.height": {"widget": "spinbox", "show": True, "tab": "Ashita"},
    },
    "ashita.input": {
        "gamepad.allowbackground": {"widget": "checkbox", "show": True, "tab": "Ashita"},
        "gamepad.disableenumeration": {"widget": "checkbox", "show": True, "tab": "Ashita"},
        "keyboard.blockinput": {"widget": "checkbox", "show": True, "tab": "Ashita"},
        "keyboard.blockbindsduringinput": {"widget": "checkbox", "show": True, "tab": "Ashita"},
        "keyboard.silentbinds ": {"widget": "checkbox", "show": True, "tab": "Ashita"},
        "keyboard.windowskeyenabled": {"widget": "checkbox", "show": True, "tab": "Ashita"},
        "mouse.blockinput": {"widget": "checkbox", "show": True, "tab": "Ashita"},
        "mouse.unhook": {"widget": "checkbox", "show": True, "tab": "Ashita"},
    },
    "ashita.language": {
        "playonline": {"widget": "combobox", "show": True, "tab": "Ashita"},
        "ashita": {"widget": "combobox", "show": True, "tab": "Ashita"},
    },
    "ashita.logging": {
        "level": {"widget": "combobox", "show": True, "tab": "Ashita"},
        "crashdumps": {"widget": "checkbox", "show": True, "tab": "Ashita"},
    },
    "ashita.misc": {
        "addons.silent": {"widget": "checkbox", "show": True, "tab": "Ashita"},
        "aliases.silent": {"widget": "checkbox", "show": True, "tab": "Ashita"},
        "plugins.silent": {"widget": "checkbox", "show": True, "tab": "Ashita"},
    },
    "ashita.polplugins": {
        "sandbox": {"widget": "checkbox", "show": True, "tab": "Ashita"},
    },
    "ashita.polplugins.args": {
        ";sandbox": {"widget": "lineedit", "show": True, "tab": "Ashita"},
    },
    "ashita.resources": {
        "offsets.use_overrides": {"widget": "checkbox", "show": True, "tab": "Ashita"},
        "pointers.use_overrides": {"widget": "checkbox", "show": True, "tab": "Ashita"},
        "resources.use_overrides": {"widget": "checkbox", "show": True, "tab": "Ashita"},
    },
    "ashita.taskpool": {
        "threadcount": {"widget": "spinbox", "show": True, "tab": "Ashita"},
    },
    "ashita.window.startpos": {
        "x": {"widget": "spinbox", "show": True, "tab": "Ashita"},
        "y": {"widget": "spinbox", "show": True, "tab": "Ashita"},
    },
    "ffxi.direct3d8": {
        "presentparams.backbufferformat": {"widget": "spinbox", "show": True, "tab": "Direct3D8"},
        "presentparams.backbuffercount": {"widget": "spinbox", "show": True, "tab": "Direct3D8"},
        "presentparams.multisampletype": {"widget": "spinbox", "show": True, "tab": "Direct3D8"},
        "presentparams.swapeffect": {"widget": "spinbox", "show": True, "tab": "Direct3D8"},
        "presentparams.enableautodepthstencil": {"widget": "spinbox", "show": True, "tab": "Direct3D8"},
        "presentparams.autodepthstencilformat": {"widget": "spinbox", "show": True, "tab": "Direct3D8"},
        "presentparams.flags": {"widget": "spinbox", "show": True, "tab": "Direct3D8"},
        "presentparams.fullscreen_refreshrateinhz": {"widget": "spinbox", "show": True, "tab": "Direct3D8"},
        "presentparams.fullscreen_presentationinterval": {"widget": "spinbox", "show": True, "tab": "Direct3D8"},
        "behaviorflags.fpu_preserve": {"widget": "checkbox", "show": True, "tab": "Direct3D8"},
    },
    "ffxi.registry": {
        "0000": {"widget": "spinbox", "show": True, "tab": "FFXI Registry"},
        "0001": {"widget": "spinbox", "show": True, "tab": "FFXI Registry"},
        "0002": {"widget": "spinbox", "show": True, "tab": "FFXI Registry"},
        "0003": {"widget": "spinbox", "show": True, "tab": "FFXI Registry"},
        "0004": {"widget": "spinbox", "show": True, "tab": "FFXI Registry"},
        "0005": {"widget": "spinbox", "show": False, "tab": "FFXI Registry"},
        "0006": {"widget": "spinbox", "show": False, "tab": "FFXI Registry"},
        "0007": {"widget": "checkbox", "show": True, "tab": "FFXI Registry"},
        "0008": {"widget": "spinbox", "show": False, "tab": "FFXI Registry"},
        "0009": {"widget": "spinbox", "show": False, "tab": "FFXI Registry"},
        "0010": {"widget": "spinbox", "show": False, "tab": "FFXI Registry"},
        "0011": {"widget": "combobox", "show": True, "tab": "FFXI Registry"},
        "0012": {"widget": "spinbox", "show": False, "tab": "FFXI Registry"},
        "0013": {"widget": "spinbox", "show": False, "tab": "FFXI Registry"},
        "0014": {"widget": "spinbox", "show": False, "tab": "FFXI Registry"},
        "0015": {"widget": "spinbox", "show": False, "tab": "FFXI Registry"},
        "0016": {"widget": "spinbox", "show": False, "tab": "FFXI Registry"},
        "0017": {"widget": "checkbox", "show": True, "tab": "FFXI Registry"},
        "0018": {"widget": "combobox", "show": True, "tab": "FFXI Registry"},
        "0019": {"widget": "combobox", "show": True, "tab": "FFXI Registry"},
        "0020": {"widget": "spinbox", "show": False, "tab": "FFXI Registry"},
        "0021": {"widget": "checkbox", "show": True, "tab": "FFXI Registry"},
        "0022": {"widget": "checkbox", "show": True, "tab": "FFXI Registry"},
        "0023": {"widget": "checkbox", "show": True, "tab": "FFXI Registry"},
        "0024": {"widget": "spinbox", "show": False, "tab": "FFXI Registry"},
        "0025": {"widget": "spinbox", "show": False, "tab": "FFXI Registry"},
        "0026": {"widget": "spinbox", "show": False, "tab": "FFXI Registry"},
        "0027": {"widget": "spinbox", "show": False, "tab": "FFXI Registry"},
        "0028": {"widget": "spinbox", "show": True, "tab": "FFXI Registry"},
        "0029": {"widget": "spinbox", "show": True, "tab": "FFXI Registry"},
        "0030": {"widget": "checkbox", "show": True, "tab": "FFXI Registry"},
        "0031": {"widget": "spinbox", "show": False, "tab": "FFXI Registry"},
        "0032": {"widget": "spinbox", "show": False, "tab": "FFXI Registry"},
        "0033": {"widget": "spinbox", "show": False, "tab": "FFXI Registry"},
        "0034": {"widget": "combobox", "show": True, "tab": "FFXI Registry"},
        "0035": {"widget": "checkbox", "show": True, "tab": "FFXI Registry"},
        "0036": {"widget": "combobox", "show": True, "tab": "FFXI Registry"},
        "0037": {"widget": "spinbox", "show": True, "tab": "FFXI Registry"},
        "0038": {"widget": "spinbox", "show": True, "tab": "FFXI Registry"},
        "0039": {"widget": "combobox", "show": True, "tab": "FFXI Registry"},
        "0040": {"widget": "checkbox", "show": True, "tab": "FFXI Registry"},
        "0041": {"widget": "checkbox", "show": True, "tab": "FFXI Registry"},
        "0042": {"widget": "lineedit", "show": True, "tab": "FFXI Registry"},
        "0043": {"widget": "checkbox", "show": True, "tab": "FFXI Registry"},
        "0044": {"widget": "checkbox", "show": True, "tab": "FFXI Registry"},
        "0045": {"widget": "spinbox", "show": False, "tab": "FFXI Registry"},
        "padmode000": {"widget": "padmode_group", "show": True, "tab": "Gamepad"},
        "padsin000": {"widget": "padsin_group", "show": True, "tab": "Gamepad"},
        "padguid000": {"widget": "lineedit", "show": True, "tab": "Gamepad"},
    }
}

valid_values = {}

for section, keys in tooltips.items():
    for key, tip in keys.items():
        # Look for lines like "Valid values: 0 = Off, 1 = On, 2 = Something"
        match = re.search(r"Valid values?:\s*(.+)", tip, re.IGNORECASE)
        if match:
            values_str = match.group(1)
            # Split by comma, then by '='
            value_map = {}
            for part in values_str.split(','):
                if '=' in part:
                    val, desc = part.split('=', 1)
                    value_map[desc.strip()] = val.strip()
            if value_map:
                if section not in valid_values:
                    valid_values[section] = {}
                valid_values[section][key] = value_map
