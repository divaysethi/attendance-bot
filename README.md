# 🕒 Attendance Bot (Slack + Notion Integration)

A lightweight attendance tracking system that logs check-ins, check-outs, and breaks via Slack commands directly into a Notion database.

🔧 Features
- `/checkin`, `/checkout`, `/breakstart`, `/breakend` commands
- Auto-calculates total working hours
- Stores logs in Notion for each user, each day
- Runs 24/7 using `tmux` and deployed on DigitalOcean with Gunicorn

🧰 Tech Stack
- Python + Flask
- Notion SDK
- Slack API
- Gunicorn
- DigitalOcean (Ubuntu Server)
- `tmux` for persistent running
