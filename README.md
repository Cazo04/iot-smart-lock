## User guide
### Register face
- Regarding personal lockers at the company, if an employee requests one, the procedure is as follows:
    + The employee sends the administrator a personal image that clearly shows their face (in .jpg or .jpeg format).
    + The administrator runs the script **register-face.py** with the employee's name as metadata to register their face in the collection."
```bash
python register-face.py --path-to-image "karina.jpeg" --name "Karina"
```

### Detect
```bash
python app.py
```

### Using the Keypad
The smart lock can be opened using either a PIN code or face recognition:
```bash
python keypad.py
```

#### PIN Code Access
1. Press 'A' on the keypad to enter PIN mode
2. Enter the 6-digit PIN (default: 123456)
3. The lock will open automatically if the PIN is correct
4. To clear an incorrect entry, press 'C'
5. To cancel the operation, press 'D'

#### Face Recognition Access
1. Press 'B' on the keypad to activate face recognition
2. Position your face in front of the camera
3. The lock will open automatically if your face is recognized

### Slack
- For Slack to send a notification, you need to configure your own SLACK_TOKEN in .env file
