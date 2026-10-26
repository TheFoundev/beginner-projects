# Project 5 - Step Counter Pet (MIT App Inventor)

## 1. Project Title
**Step Counter Pet**

## 2. The Concept
This app turns your phone into a virtual pet that "walks" with you! Using your phone's built-in pedometer (step counter sensor), the app tracks how many steps you take and grows happier as you walk more. It's like having a tamagotchi that gets stronger when you exercise — the more steps you take, the more your digital pet thrives. Behind the scenes, the phone's sensor counts each step, and the app displays the total and gives your pet a happy or sleepy expression based on how active you've been.

## 3. What You Will Build/Do
You'll build an app with a cute pet character (emoji or image) that changes expression based on your step count. Low steps show a sad or sleepy face, medium shows a neutral face, and high steps show a happy and energetic face. The final app is your on-phone exercise companion that reacts to your daily movement.

## 4. Core App Concept
**Sensor Data Integration** — Your phone's sensors (hardware that detects physical motion) feed data into the app, which then processes it to show something meaningful. Like a fitness watch that reads your heartbeat — the sensor detects it, and the watch displays the number for you.

## 5. Tools Needed
- **MIT App Inventor 2** (free, browser-based at ai2.appinventor.mit.edu)
- Android phone with MIT AI2 Companion app (free on Google Play)
- Phone with a built-in pedometer/step sensor (most modern Android phones have this)

## 6. What You Will Learn
- Reading data from device sensors (pedometer/step detector)
- Conditional display logic (showing different content based on thresholds)
- Basic data tracking and persistence with TinyDB

---

## Step-by-Step Instructions

### Step 1: Set Up Your Project
1. Go to [ai2.appinventor.mit.edu](https://ai2.appinventor.mit.edu)
2. Create a new project named "StepCounterPet"

### Step 2: Design the Screen (Designer)
Add these components:

| Component | From Palette | Name | Properties to Set |
|-----------|-------------|------|-------------------|
| Label | User Interface | `TitleLabel` | Text: "Step Counter Pet", FontSize: 28, TextAlignment: center |
| Label | User Interface | `StepsLabel` | Text: "Steps: 0", FontSize: 22, TextAlignment: center |
| Label | User Interface | `PetLabel` | Text: "🐶", FontSize: 80, TextAlignment: center |
| Label | User Interface | `StatusLabel` | Text: "Take some steps to wake me up!", FontSize: 18, TextAlignment: center |
| Button | User Interface | `ResetButton` | Text: "Reset Steps", FontSize: 16 |
| Pedometer | Sensors | `Pedometer1` | (no changes) |
| TinyDB | Storage | `TinyDB1` | (for saving step data) |

Screen properties:
- `Screen1.Title` → "Step Counter Pet"
- `Screen1.BackgroundColor` → light blue

### Step 3: Write the Blocks (Blocks Editor)

```
when Screen1.Initialize
├── call Pedometer1.Start
├── set saved_steps to TinyDB1.getValue("total_steps", 0)
├── set total_steps to saved_steps
├── set StepsLabel.Text to join "Steps: " total_steps
├── set PetLabel.Text to "😴"
└── set StatusLabel.Text to "I'm sleeping. Walk around to wake me!"

when Pedometer1.IsReady
└── (Pedometer is ready to use)

when Pedometer1.StepCountChanged (newSteps)
├── set total_steps to newSteps
├── set StepsLabel.Text to join "Steps: " total_steps
├── call update_pet_status

define update_pet_status
├── if total_steps < 50
│   ├── set PetLabel.Text to "😴"
│   └── set StatusLabel.Text to "I'm sleeping. Walk more!"
├── else if total_steps < 200
│   ├── set PetLabel.Text to "🙂"
│   └── set StatusLabel.Text to "I'm getting active!"
├── else if total_steps < 500
│   ├── set PetLabel.Text to "😊"
│   └── set StatusLabel.Text to "I'm happy and energetic!"
└── else
    ├── set PetLabel.Text to "🏃‍♂️🐶"
    └── set StatusLabel.Text to "I'm zooming with joy! 🚀"

when ResetButton.Click
├── set total_steps to 0
├── set StepsLabel.Text to join "Steps: " total_steps
├── set PetLabel.Text to "😴"
├── set StatusLabel.Text to "Steps reset! Let's start again."
└── call TinyDB1.StoreValue "total_steps" 0
```

### Complete Block Logic Summary:
- Initialize: Start pedometer, load saved steps, set pet to sleeping
- On step change: Update step count, call update_pet_status procedure
- Update procedure: Change pet emoji and message based on step thresholds
- Reset button: Zero out steps, save to TinyDB, reset display

## Extension Ideas
- Let users name their pet and save the name
- Add multiple pets to choose from
- Show a progress bar that fills as you approach goals
- Add daily step goals with notifications
