# 🎯 Getting Started with Dialed In Fitness
## A Complete Guide for Non-Coders

This guide will walk you through everything you need to get your fitness tracking app running on your computer. **No coding experience required!**

---

## 📋 What You'll Need

- A computer (Windows, Mac, or Linux)
- 30 minutes of time
- Internet connection
- That's it!

---

## 🎬 The Big Picture

Here's what we're going to do:

1. **Download your app** from Claude
2. **Install Python** (the language the app is written in)
3. **Set up the app** on your computer
4. **Start using it!**

Think of it like downloading and installing any other app, just with a few extra steps.

---

## Step 1: Download Your App Files

### Option A: Download from Claude (You're Here!)

1. **Look for the project folder** in this conversation
   - It should be called `dialed-in-fitness`
   - You'll see it as a clickable link above

2. **Click on the folder link** to open it

3. **Download the entire folder**
   - Your browser might ask where to save it
   - Choose your **Desktop** or **Documents** folder (somewhere easy to find!)
   - The download might take 30 seconds

4. **Unzip the folder** (if needed)
   - On Windows: Right-click → "Extract All"
   - On Mac: Double-click the .zip file
   - You should now have a folder called `dialed-in-fitness`

✅ **Checkpoint:** You should have a folder on your computer with files inside like `start.sh`, `README.md`, and folders called `backend` and `frontend`.

---

## Step 2: Install Python

Python is the "engine" that runs your app. It's free and safe to install.

### For Windows Users:

1. **Go to python.org**
   - Open your web browser
   - Type: `python.org/downloads`
   - Press Enter

2. **Click the big yellow "Download Python" button**
   - It will automatically pick the right version for Windows
   - The file will be called something like `python-3.11.x-amd64.exe`

3. **Run the installer**
   - Find the downloaded file (usually in your Downloads folder)
   - Double-click it
   - ⚠️ **IMPORTANT:** Check the box that says "Add Python to PATH"
   - Click "Install Now"
   - Wait 2-3 minutes

4. **Verify it worked**
   - Open "Command Prompt" (search for "cmd" in Start menu)
   - Type: `python --version`
   - Press Enter
   - You should see something like "Python 3.11.5"

### For Mac Users:

1. **Go to python.org**
   - Open Safari or Chrome
   - Type: `python.org/downloads`
   - Press Enter

2. **Click "Download Python 3.11.x"**
   - The file will be called something like `python-3.11.x-macos11.pkg`

3. **Run the installer**
   - Find the downloaded file (usually in your Downloads folder)
   - Double-click it
   - Click "Continue" through the steps
   - Enter your Mac password when asked
   - Wait 2-3 minutes

4. **Verify it worked**
   - Open "Terminal" (search for "Terminal" in Spotlight - press Cmd+Space)
   - Type: `python3 --version`
   - Press Enter
   - You should see something like "Python 3.11.5"

✅ **Checkpoint:** When you type `python --version` (Windows) or `python3 --version` (Mac) in your terminal, you see a version number.

---

## Step 3: Navigate to Your App Folder

We need to tell your computer where your app is located.

### For Windows:

1. **Open Command Prompt**
   - Click Start
   - Type "cmd"
   - Click "Command Prompt"

2. **Navigate to your app**
   - If you saved to Desktop, type:
     ```
     cd Desktop\dialed-in-fitness
     ```
   - If you saved to Documents, type:
     ```
     cd Documents\dialed-in-fitness
     ```
   - Press Enter

3. **Verify you're in the right place**
   - Type: `dir`
   - Press Enter
   - You should see files like `start.sh`, `README.md`

### For Mac:

1. **Open Terminal**
   - Press Cmd + Space
   - Type "Terminal"
   - Press Enter

2. **Navigate to your app**
   - If you saved to Desktop, type:
     ```
     cd Desktop/dialed-in-fitness
     ```
   - If you saved to Documents, type:
     ```
     cd Documents/dialed-in-fitness
     ```
   - Press Enter

3. **Verify you're in the right place**
   - Type: `ls`
   - Press Enter
   - You should see files like `start.sh`, `README.md`

✅ **Checkpoint:** You're inside the `dialed-in-fitness` folder. When you list files, you see `backend`, `frontend`, `start.sh`.

---

## Step 4: Install the App's Dependencies

The app needs some extra components to run. Think of these like add-ons or plugins.

### For Windows:

1. **In Command Prompt** (should still be in the dialed-in-fitness folder):
   ```
   pip install -r requirements.txt
   ```
   - Press Enter
   - You'll see a LOT of text scrolling by
   - This is normal! It's downloading everything the app needs
   - This takes 2-3 minutes

2. **Wait for it to finish**
   - You'll know it's done when you see a new line appear where you can type
   - You might see some yellow "warnings" - these are fine!

### For Mac:

1. **In Terminal** (should still be in the dialed-in-fitness folder):
   ```
   pip3 install -r requirements.txt
   ```
   - Press Enter
   - You'll see a LOT of text scrolling by
   - This is normal! It's downloading everything the app needs
   - This takes 2-3 minutes

2. **Wait for it to finish**
   - You'll know it's done when you see a new line appear where you can type
   - You might see some yellow "warnings" - these are fine!

✅ **Checkpoint:** The installation completed without red "ERROR" messages. Some warnings are okay!

---

## Step 5: Start Your App! 🚀

This is the exciting part - we're going to turn on your app!

### For Windows:

Since Windows can't run `.sh` files directly, we'll start the app manually:

1. **Open TWO Command Prompt windows**
   - Click Start → type "cmd" → Enter
   - Do this twice so you have two windows

2. **In the FIRST window** (Backend):
   ```
   cd Desktop\dialed-in-fitness\backend
   python -m uvicorn app.main:app --reload
   ```
   - Press Enter
   - You should see: "Application startup complete"
   - Leave this window open - don't close it!

3. **In the SECOND window** (Frontend):
   ```
   cd Desktop\dialed-in-fitness\frontend
   streamlit run Home.py
   ```
   - Press Enter
   - You should see: "You can now view your Streamlit app in your browser"
   - A browser window should open automatically!

### For Mac:

Mac can use the easy startup script:

1. **Make the startup script executable** (one-time setup):
   ```
   chmod +x start.sh
   ```
   - Press Enter

2. **Run the startup script**:
   ```
   ./start.sh
   ```
   - Press Enter
   - You'll see text about "Starting backend" and "Starting frontend"
   - A browser window should open automatically!

### What You Should See:

- **Two terminal windows running** (don't close them!)
- **A web browser opens** automatically
- **The URL is:** `http://localhost:8501`
- **You see a page** that says "💪 Dialed In Fitness"

✅ **Checkpoint:** You see the Dialed In Fitness homepage in your web browser!

---

## 🎉 You're Running! Now What?

### First Time Setup:

1. **Create Your First Plan**
   - Click on "Plan" in the sidebar
   - Click "Create/Edit Plan" tab
   - Fill in your information:
     - Plan name: "My First Plan"
     - Goal: Choose Bulk, Cut, or Maintain
     - Calorie target: Your daily calorie goal
     - Macro targets: Your protein, carbs, fat goals
     - Training days: How many days per week you'll workout
     - Body part targets: Reps per week for each muscle
     - Sleep target: Hours of sleep you're aiming for
     - Steps: Daily step goal
     - Hydration: Ounces of water per day
     - Supplements: List what you take
   - Click "Save Plan"

2. **Log Your First Day**
   - Click on "Today" in the sidebar
   - Fill in what you've eaten/done today
   - Add your workouts (if you worked out)
   - Click "Save Log"
   - **You'll see your first Dialed In Score!**

3. **View Your Dashboard**
   - Click "Home" in the sidebar
   - See your score!
   - The more days you log, the better the dashboard gets

---

## 💡 Daily Use

### Starting the App:

**Every time you want to use the app:**

**Windows:**
1. Open two Command Prompts
2. In first: `cd Desktop\dialed-in-fitness\backend` then `python -m uvicorn app.main:app --reload`
3. In second: `cd Desktop\dialed-in-fitness\frontend` then `streamlit run Home.py`
4. Browser opens automatically

**Mac:**
1. Open Terminal
2. Type: `cd Desktop/dialed-in-fitness`
3. Type: `./start.sh`
4. Browser opens automatically

### Stopping the App:

**When you're done for the day:**
- Close the browser tab
- In the terminal windows, press `Ctrl + C` (Windows) or `Cmd + C` (Mac)
- Close the terminal windows

---

## 🆘 Troubleshooting

### "Command not found" or "'python' is not recognized"

**Problem:** Python wasn't installed correctly or isn't in your PATH.

**Fix:**
- Reinstall Python
- ⚠️ Make sure to check "Add Python to PATH" during installation
- Restart your computer after installing

### "Port 8000 is already in use"

**Problem:** Something else is using that port, or you didn't close the app properly last time.

**Fix:**
- Close all terminal/command prompt windows
- Restart your computer
- Try starting the app again

### "No module named 'fastapi'" or similar

**Problem:** Dependencies didn't install properly.

**Fix:**
- Go back to Step 4
- Run the install command again: `pip install -r requirements.txt`

### Browser doesn't open automatically

**Problem:** Automatic browser launch failed.

**Fix:**
- Manually open your browser
- Type this in the address bar: `http://localhost:8501`
- Press Enter

### I see errors in red text

**Problem:** Something went wrong.

**Fix:**
- Take a screenshot of the error
- Try closing and restarting the app
- If it persists, you may need technical help

### The app looks broken or blank

**Problem:** Frontend didn't start properly.

**Fix:**
- Make sure BOTH terminal windows are running
- Check that you see "Application startup complete" in the backend window
- Refresh your browser (press F5 or Cmd+R)

---

## 📱 Can I Use This on My Phone?

Not yet! Right now, this is a computer-only app. However:

- In Phase 3, we can move this to the cloud and make it mobile-accessible
- For now, you can access it on your computer anytime
- You could also access it from other devices on your home network (ask for help with this)

---

## 💾 Your Data

### Where is my data stored?

- Everything is saved on your computer
- The database file is: `dialed-in-fitness/backend/dialed_in.db`
- Your data never leaves your computer (unless you choose to share it)

### How do I backup my data?

**Easy method:**
1. Close the app
2. Copy the entire `dialed-in-fitness` folder
3. Paste it somewhere safe (external drive, cloud storage)
4. That's your backup!

### How do I reset everything?

If you want to start fresh:
1. Close the app
2. Go to: `dialed-in-fitness/backend/`
3. Delete the file called `dialed_in.db`
4. Restart the app - it will create a fresh database

---

## 🎓 Learning Resources

### Want to understand more about what you're running?

- **Python:** The programming language - [python.org](https://www.python.org)
- **Streamlit:** Makes the web interface - [streamlit.io](https://streamlit.io)
- **FastAPI:** Powers the backend - [fastapi.tiangolo.com](https://fastapi.tiangolo.com)

### Want to customize the app?

- Read `SCORING_REFERENCE.md` to understand the scoring
- Read `PROJECT_SUMMARY.md` to see how it's built
- You can change colors, text, and settings without coding!

---

## ✅ Quick Reference Card

**Print this out for easy reference:**

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  DIALED IN FITNESS - QUICK START      ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│                                        │
│  WINDOWS:                              │
│  1. Open two Command Prompts           │
│  2. First window:                      │
│     cd Desktop\dialed-in-fitness\      │
│        backend                         │
│     python -m uvicorn app.main:app     │
│        --reload                        │
│  3. Second window:                     │
│     cd Desktop\dialed-in-fitness\      │
│        frontend                        │
│     streamlit run Home.py              │
│                                        │
│  MAC:                                  │
│  1. Open Terminal                      │
│  2. cd Desktop/dialed-in-fitness       │
│  3. ./start.sh                         │
│                                        │
│  BROWSER:                              │
│  http://localhost:8501                 │
│                                        │
│  TO STOP:                              │
│  Press Ctrl+C (Win) or Cmd+C (Mac)    │
│  in both terminal windows              │
│                                        │
└────────────────────────────────────────┘
```

---

## 🎉 Congratulations!

You've successfully:
- ✅ Downloaded your fitness app
- ✅ Installed Python
- ✅ Set up the application
- ✅ Started using it!

**You're now running your own personal fitness tracking system!**

Remember:
- The app runs on your computer (not the cloud yet)
- Your data is private and local
- You need to start the app each time you want to use it
- Keep both terminal windows open while using the app

**Ready to get Dialed In?** 💪

Start by creating your first plan, logging a few days, and watching your score improve!

---

**Need Help?**

If you get stuck:
1. Check the Troubleshooting section above
2. Make sure both terminal windows are running
3. Try restarting your computer
4. Review the error messages carefully

**Have fun tracking your fitness journey!** 🎯
