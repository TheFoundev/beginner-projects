# Project 3 - Magic 8-Ball Fortune Teller (MIT App Inventor)

## 1. Project Title
**Magic 8-Ball Fortune Teller**

## 2. The Concept
This app mimics a classic Magic 8-Ball toy. You ask the phone a yes/no question (out loud or in your head), then shake your phone or tap the screen. The app randomly picks a response like "Yes" or "Ask again later" and displays it. Think of it like a digital crystal ball — you pose a question, give it a good shake, and it reveals your fate. Behind the scenes, the app uses a random number generator to pick from a list of pre-written answers, just like how the real 8-Ball has a dice inside that floats to random sides.

## 3. What You Will Build/Do
You'll build an app with a large 8-ball graphic that the user "shakes." When shaken, the ball flips to reveal a random fortune answer with text and color changes. The final app looks like a classic black 8-ball that magically shows answers when you shake your phone.

## 4. Core App Concept
**Random Selection** — The app picks an item from a list at random, giving each item an equal chance of being chosen. Just like drawing a card blindly from a shuffled deck — you know all the possibilities, but you can't predict which one you'll get.

## 5. Tools Needed
- **MIT App Inventor 2** (free, browser-based at ai2.appinventor.mit.edu)
- Android phone with MIT AI2 Companion app (free on Google Play)
- The built-in **Accelerometer** (motion sensor) on your phone

## 6. What You Will Learn
- Using the device's motion sensor (accelerometer) to detect shaking
- Randomly selecting items from a list
- Changing screen content dynamically based on sensor input

---

## Step-by-Step Instructions

### Step 1: Set Up Your Project
1. Go to [ai2.appinventor.mit.edu](https://ai2.appinventor.mit.edu)
2. Sign in and create a new project named "Magic8Ball"

### Step 2: Design the Screen (Designer)
Drag these components:

| Component | From Palette | Name | Properties to Set |
|-----------|-------------|------|-------------------|
| Image | User Interface | `BallImage` | Image: upload an 8-ball image or use a colored circle, Width/Height: fill parent |
| Label | User Interface | `AnswerLabel` | Text: "?", FontSize: 36, TextAlignment: center, Visible: true |
| Button | User Interface | `TapButton` | Text: "Or Tap Me Instead", FontSize: 16 |
| Accelerometer | Sensors | `AccelerometerSensor1` | (no changes) |
| TinyDB | Storage | `TinyDB1` | (optional, for saving history) |

Screen properties:
- `Screen1.Title` → "Magic 8-Ball"
- `Screen1.BackgroundColor` → white

### Step 3: Define the Answers List
In the Blocks editor, create a global variable:

```
global fortunes = [
    "Yes", "No", "It is certain", "Don't count on it",
    "Ask again later", "Outlook good", "Very doubtful",
    "Signs point to yes", "Better not tell you now",
    "My sources say no", "Yes - definitely", "Reply hazy, try again"
]
```

### Step 4: Write the Shake Detection Blocks
Build this logic in the Blocks editor:

```
when Screen1.Initialize
├── set current_acceleration to 0
└── set last_shake_time to 0

when AccelerometerSensor1.AccelerationChanged (xAccel, yAccel, zAccel)
├── set total_accel to sqrt(xAccel^2 + yAccel^2 + zAccel^2)
├── if total_accel > 2.0 and (clock.now - last_shake_time > 1000)
│   ├── set last_shake_time to clock.now
│   └── call check_fortune
└── end if

when TapButton.Click
└── call check_fortune

define check_fortune
├── set random_index to random integer from 0 to 11
├── set random_answer to select list item fortunes at index random_index + 1
├── set AnswerLabel.Text to random_answer
├── set BallImage.Visible to false (or change image to "reveal" side)
└── set Screen1.BackgroundColor to random color
```

### Complete Block Logic:
```
when AccelerometerSensor1.AccelerationChanged x y z
├── set acceleration to sqrt((x * x) + (y * y) + (z * z))
├── if acceleration > 2.5
│   ├── set idx to random integer (0 to 11)
│   ├── set AnswerLabel.Text to select list item fortunes at (idx + 1)
│   ├── set BallImage.Image to "magic_8_ball_reveal" (or flip to a color circle)
│   └── set Screen1.BackgroundColor to (random-ish color based on idx)
└── end if
```

## Extension Ideas
- Add an animated flip transition on the ball image
- Show a history of past answers
- Let users add their own custom fortunes
