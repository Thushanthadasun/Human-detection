# Human Detection with Region-Based Camera Analysis

This project implements a "human detection system using YOLOv5" that runs entirely on the computer's CPU. The system uses a "live camera feed" (either a built-in laptop camera or a USB webcam), divides the view into multiple regions, and detects humans in each region. Based on the region where humans are detected, it can **communicate with an Arduino board over serial (USB)** to perform actions such as **switching lights**.

Features:
Human detection** using pre-trained YOLOv5s model.
Supports **any webcam** (built-in or USB-connected).
Camera view is divided into regions.
Case 1: Two regions (left and right)
Case 2**: Four regions (quadrants)
Based on detection, sends commands over **serial (USB)** to an Arduino.
Arduino can then perform actions such as **turning ON/OFF lights** in corresponding regions.

Requirements

Here’s how to **run your YOLOv5 human detection code using Visual Studio Code (VS Code)** step by step:

Step-by-Step Guide to Run the Code in VS Code

1. **Install VS Code**
Download from: [https://code.visualstudio.com/](https://code.visualstudio.com/)
Install the **Python extension** (you'll be prompted the first time you open a Python file).

2. **Install Python**

Make sure Python is installed on your system:
Download: [https://www.python.org/](https://www.python.org/)
During installation, check **“Add Python to PATH”**

You can verify installation by opening a terminal and typing:

```bash
python --version
```

3. **Open the file in VS Code **


4. **Create and Activate a Virtual Environment**

In the VS Code **terminal** (View > Terminal or `Ctrl + backtick` `` ` ``):

```bash
python -m venv venv
```

Then activate it:

* **Windows:**

  ```bash
  .\venv\Scripts\activate
  ```

You should now see `(venv)` in the terminal prompt.

---

5. **Install Required Packages**

Still in the terminal:

```bash
pip install opencv-python torch torchvision torchaudio
```

This installs OpenCV and PyTorch, which are needed for your code.

---

6. **Ensure Correct Python Interpreter Is Selected**

At the **bottom-left** of VS Code (or press `Ctrl+Shift+P` and search for “Python: Select Interpreter”):

* Select the interpreter from your virtual environment:

  ```
  .\venv\Scripts\python.exe
  ```

---

8. **Run the Script**

Press "q" to stop the programm.

---
When running the two-region version of the human detection system, the project includes serial communication with an Arduino board. This means the Arduino must be connected to your computer via USB, and the correct COM port should be specified in the Python script (you can modify the port in the code depending on your system—for example, "COM3" or "COM5" on Windows). Additionally, if you're using a USB-connected webcam instead of your laptop's built-in camera, make sure to change the cv2.VideoCapture(0) line in the code to another index like cv2.VideoCapture(1) or cv2.VideoCapture(2), depending on your setup.

For the four-region version, only the Python script is used and no Arduino communication is required. This version is designed purely for visual human detection across four sections of the camera view. Therefore, you do not need to connect the Arduino to your computer while running this version.
