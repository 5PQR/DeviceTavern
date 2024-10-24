# DeviceTavern
Simple local API endpoints built in python for various devices. It's an executable that installs Miniconda and allows doing local API calls at the port 7068.

# Endpoints
The file current\builtin\ui\demo.html should  contain more info about the endpoints and it has buttons to test the calls.

* GET http://127.0.0.1:7068/status - checks if the tool is running
* GET http://127.0.0.1:7068/bhaptics?device1=gloveLFrame&device2=GloveL&point=0&intensity=50&duration=100 - triggers haptic feedback for bHaptics devices if bHaptics Player is running


# bHaptics devices haptic feedback

This tool tools sends simple calls to the bHaptics Player and requires bHaptic devices https://www.bhaptics.com/ like TactGlove & TactSuit X40 for haptic feedback to get triggered. It's mostly just a wrapper to streamline setting up the connection through python by installing Miniconda on Windows devices with a simple executable. For more advanced implementations for the bHaptics devices and for haptic applications I recommend checking the bHaptics SDK https://www.bhaptics.com/en/support/developers/ 
