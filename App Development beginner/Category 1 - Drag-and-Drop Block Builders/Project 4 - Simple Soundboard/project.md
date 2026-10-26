# Project 4 - Simple Soundboard (MIT App Inventor)

## 1. Project Title
**Simple Soundboard**

## 2. The Concept
This app has buttons that play different sound effects when tapped — like a digital piano keyboard where each key makes a different note. Behind the scenes, each button is "listening" for a tap, and when it hears one, it triggers its assigned sound file to play through your phone's speaker. It's like having a collection of sound effect buttons from a cartoon sound studio right on your phone.

## 3. What You Will Build/Do
You'll create an app with 4 colorful buttons, each playing a different sound when pressed. You can record your own sounds or use free sound files. The final app looks like a mini studio with fun buttons — tap "Cow" and hear "Moo!", tap "Bell" and hear a chime, and so on.

## 4. Core App Concept
**Event-Driven Programming with Media** — Each button waits silently until tapped, then fires off an action (playing sound). Like a jukebox where each button is a song selector: nothing happens until you press a button, and then the music plays.

## 5. Tools Needed
- **MIT App Inventor 2** (free, browser-based at ai2.appinventor.mit.edu)
- Android phone with MIT AI2 Companion app (free on Google Play)
- Sound files (either record your own or download free ones from sites like Freesound.org)
- Optional: Computer microphone for recording

## 6. What You Will Learn
- Loading and playing sound files in an app
- Creating multiple buttons with individual event handlers
- Designing a colorful, engaging UI layout

---

## Step-by-Step Instructions

### Step 1: Prepare Sound Files
1. Find or record 4 short sound effects (under 3 seconds each)
2. Recommended free sounds: cow moo, doorbell, applause, laser zap
3. Make sure files are in `.mp3` or `.wav` format
4. Save them with simple names: `cow.mp3`, `bell.mp3`, `clap.mp3`, `laser.mp3`

### Step 2: Set Up Your Project
1. Go to [ai2.appinventor.mit.edu](https://ai2.appinventor.mit.edu)
2. Create a new project named "Soundboard"

### Step 3: Design the Screen (Designer)
Add this structure:

**Main Layout:**
- Use a `VerticalArrangement` for the main container

Inside the VerticalArrangement, add 4 `HorizontalArrangement` blocks (one for each row), each containing:

| Component | From Palette | Name | Properties |
|-----------|-------------|------|-----------| 
| Button | User Interface | `CowButton` | Text: "🐄 Moo", FontSize: 20, Width: Fill Parent |
| Button | User Interface | `BellButton` | Text: "🔔 Bell", FontSize: 20, Width: Fill Parent |
| Button | User Interface | `ClapButton` | Text: "👏 Clap", FontSize: 20, Width: Fill Parent |
| Button | User Interface | `LaserButton` | Text: "🔫 Laser", FontSize: 20, Width: Fill Parent |
| Sound | User Interface | `Sound_Cow` | Source: cow.mp3 (upload your file) |
| Sound | User Interface | `Sound_Bell` | Source: bell.mp3 |
| Sound | User Interface | `Sound_Clap` | Source: clap.mp3 |
| Sound | User Interface | `Sound_Laser` | Source: laser.mp3 |

### Step 4: Upload Sound Files
1. In the Designer, select each Sound component
2. Click the "Source" property
3. Click "Upload File" and upload your corresponding .mp3 file
4. Do this for all 4 Sound components

### Step 5: Write the Blocks (Blocks Editor)
Create 4 event handlers, one for each button:

```
when CowButton.Click
└── call Sound_Cow.Play

when BellButton.Click
└── call Sound_Bell.Play

when ClapButton.Click
└── call Sound_Clap.Play

when LaserButton.Click
└── call Sound_Laser.Play
```

Optional: Add a "Stop All" button:
```
when StopAllButton.Click
├── call Sound_Cow.Stop
├── call Sound_Bell.Stop
├── call Sound_Clap.Stop
└── call Sound_Laser.Stop
```

### Complete Block Visual:
```
Screen1.Initialize (empty or set welcome message)

CowButton.Click → Sound_Cow.Play
BellButton.Click → Sound_Bell.Play
ClapButton.Click → Sound_Clap.Play
LaserButton.Click → Sound_Laser.Play
```

## Extension Ideas
- Add more buttons with custom sounds (record your own voice!)
- Add volume sliders for each sound
- Add a "random sound" button that plays a random effect
- Add a recording feature that saves custom sounds to the soundboard
