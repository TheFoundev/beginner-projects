# Project 1 - Color Tap Challenge (MIT App Inventor)

## 1. Project Title
**Color Tap Challenge**

## 2. The Concept
This app displays a colored button on the screen. Every time the user taps the button, it changes to a new random color. Think of it like a magic mood ring — when you "ring" it (tap it), it instantly changes its mood (color). Behind the scenes, the app generates random red, green, and blue values (like mixing paint) and applies them to the button, creating over 16 million possible color combinations.

## 3. What You Will Build/Do
You'll build an app with a single large colored button that fills most of the screen. Each tap changes the button's color randomly. The button will also display the RGB values so you can see the color code. Final app looks like a colorful touch screen canvas — tap, tap, tap, and watch the colors dance!

## 4. Core App Concept
**Event Listeners** — A piece of code that "listens" and waits patiently for something to happen (like a tap), then springs into action when it detects that event. Just like a doorbell that waits quietly until someone pushes the button, then rings.

## 5. Tools Needed
- **MIT App Inventor 2** (free, browser-based at ai2.appinventor.mit.edu)
- An Android phone with the MIT AI2 Companion app installed (also free on Google Play)
- No installation required — everything runs in your web browser!

## 6. What You Will Learn
- Designing a single-screen UI with a large button
- Handling button tap events with event listeners
- Generating random numbers and applying them as RGB color values

---

## Step-by-Step Instructions

### Step 1: Set Up Your Project
1. Go to [ai2.appinventor.mit.edu](https://ai2.appinventor.mit.edu)
2. Sign in with a Google account
3. Click "Create Apps" → "Start New Project"
4. Name it "ColorTapChallenge"
5. Click "Create"

### Step 2: Design the Screen (Designer)
Drag these components from the palette onto your screen:

| Component | From Palette | Name | Properties to Set |
|-----------|-------------|------|-------------------|
| Button | User Interface | `ColorButton` | Text: empty (clear it), FontSize: 24 |
| Label | User Interface | `RGBLabel` | Text: "R: 0, G: 0, B: 0", FontSize: 18, Visible: true |
| TinyDB | Storage | `TinyDB1` | (no changes needed) |

Set the screen properties:
- `Screen1.Title` → "Color Tap Challenge"
- `Screen1.BackgroundColor` → black (or any dark color)

### Step 3: Add a Color Picker Helper (Optional)
Add a `ColorPicker` component from the "Custom things" section if you want a palette option. For this basic version, we'll use random colors.

### Step 4: Write the Blocks (Blocks Editor)
Switch to the "Blocks" tab and create these blocks:

#### When ColorButton is tapped:
```
when ColorButton.Click do
    set r = random integer from 0 to 255
    set g = random integer from 0 to 255
    set b = randominteger from 0 to 255
    
    set colorValue = call Color create from r g b
    
    set ColorButton.BackgroundColor to colorValue
    set RGBLabel.Text to join "R: " r ", G: " g ", B: " b
end when
```

In the Blocks editor, build this logic:

1. Drag `when ColorButton.Click do` block (from ColorButton in the palette)
2. From "Math" drawer → `random integer from 0 to 255` → store in a variable `r`
3. Repeat to create variables `g` and `b`
4. From "Color" drawer → `create color from r g b` (use the r, g, b variables)
5. Set `ColorButton.BackgroundColor` to that color value
6. Set `RGBLabel.Text` to a joined string: `"R: " + r + ", G: " + g + ", B: " + b`

### Step 5: Test and Save
1. Click "Connect" → "AI2 Companion"
2. Scan the QR code with your phone
3. Tap the button and watch colors change!

### Complete Block Code (Visual Representation)
```
when ColorButton.Click
├── set r ← random integer (0 to 255)
├── set g ← random integer (0 to 255)
├── set b ← random integer (0 to 255)
├── set ColorButton.BackgroundColor ← create color from (r, g, b)
└── set RGBLabel.Text ← join "R: " r ", G: " g ", B: " b
```

## Extension Ideas
- Add a "Reset" button to go back to a default color
- Save favorite colors to TinyDB and display them in a list
- Add sound effects when the button is tapped
