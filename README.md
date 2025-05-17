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

### Slack
- For Slack to send a notification, you need to configure your own SLACK_TOKEN in .env file
