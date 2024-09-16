# AI exhibit - Computer vision / Object detection

## INSTRUCTIONS:
----
Run:

`python/python3 -m http.server`

Access game from browser:

`localhost:8000`

### Access to Webcam
The Browser needs to access the webcam, you need to change the settings for this. 
For Chrome, you need to follow these steps.
1. Navigate to `chrome://flags/#unsafely-treat-insecure-origin-as-secure` in Chrome.
2. Find and enable the `Insecure origins treated as secure` section.
3. Add any addresses you want to ignore the secure origin policy for. Remember to include the port number too (if required). Here: `localhost:8000`


-----

Training/object detection based on: https://codelabs.developers.google.com/tensorflowjs-transfer-learning-teachable-machine#0

Game inspired by: https://github.com/google/emoji-scavenger-hunt
