## User guide
### Register face
- Regarding personal lockers at the company, if an employee requests one, the procedure is as follows:
    + The employee sends the administrator a personal image that clearly shows their face (in .jpg or .jpeg format).
    + The administrator runs the script **register-face.py** with the employee's name as metadata to register their face in the collection."
```bash
python register-face.py --path-to-image "karina.jpeg" --name "Karina"
```

### Detect
- The camera at each locker will continuously scan for faces. The current version of this script only verifies faces using a static image for demonstration purposes.
- Firstly, you need to change the path to image in the **test-dectect.py** :
```python
def main():
    image_binary = preprocess_image("gdragon.jpg")
```
- Then, run for detection
```bash
python test-detect.py
```

### Slack
- For Slack to send a notification, you need to configure your own SLACK_TOKEN in .env file
