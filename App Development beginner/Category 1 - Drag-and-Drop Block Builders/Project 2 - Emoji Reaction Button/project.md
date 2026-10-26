# Project 2 - Emoji Reaction Button (MIT App Inventor)

## 1. Project Title
**Emoji Reaction Button**

## 2. The Concept
This app shows a big smiley emoji face on the screen. When you tap it, it cycles through different emoji expressions — a smile, a surprised face, a laughing face, and even a sleeping face. It's like having a digital pet whose facial expression changes with each petting. Behind the scenes, the app keeps track of which emoji is showing (using a "counter" variable) and switches to the next one each time it gets tapped.

## 3. What You Will Build/Do
You'll create an app with a large emoji displayed in a button or image. Each tap changes the emoji to a different reaction face. Your phone screen becomes a cute little companion that reacts to your touches. The final app looks like a fun, interactive emoji that changes expressions with every tap.

## 4. Core App Concept
**State Management (Basic)** — The app remembers which "step" it is in a sequence (like remembering which page you're on in a photo album) and shows different content based on that current step. Think of it as a flip-book — each flip takes you to the next drawing.

## 5. Tools Needed
- **MIT App Inventor 2** (free, browser-based at ai2.appinventor.mit.edu)
- Android phone with MIT AI2 Companion app (free on Google Play)

## 6. What You Will Learn
- Cycling through a list of values using state tracking
- Changing displayed content (text/images) dynamically
- Basic counter logic in block-based programming

---

## Step-by-Step Instructions

### Step 1: Set Up Your Project
1. Go to [ai2.appinventor.mit.edu](https://ai2.appinventor.mit.edu)
2. Sign in and click "Create Apps" → "Start New Project"
3. Name it "EmojiReactionButton" and click "Create"

### Step 2: Design the Screen (Designer)
Drag these components:

| Component | From Palette | Name | Properties to Set |
|-----------|-------------|------|-------------------|
| Button | User Interface | `EmojiButton` | Text: 😀 , FontSize: 64 |
| Label | User Interface | `StatusLabel` | Text: "Tap me!", FontSize: 18, TextAlignment: center |
| TinyDB | Storage | `TinyDB1` | (no changes) |

Screen properties:
- `Screen1.Title` → "Emoji Reaction Button"
- `Screen1.BackgroundColor` → light yellow or white

### Step 3: Define the Global Variable
In the Blocks editor:
1. Create a global variable: `reaction_index` set to `0`

### Step 4: Create the Emoji List
1. Create a procedure called `setup_emoji_list` that sets a global list variable `emoji_reactions` to:
```
[😀, 😂, 😮, 😴, 😎, 🥳, 😊, 😉]
```

### Step 5: Write the Tap Handler
Build these blocks:

```
when Screen1.Initialize
├── call setup_emoji_list
└── set reaction_index to 0

when EmojiButton.Click
├── set temp_emoji to select list item emoji_reactions at index reaction_index + 1
└── set EmojiButton.Text to temp_emoji

when EmojiButton.Click (alternative with cycling)
├── set reaction_index to (reaction_index + 1) mod 8
├── set temp_emoji to select list item emoji_reactions at index reaction_index + 1
├── set EmojiButton.Text to temp_emoji
└── set StatusLabel.Text to join "Mood: tapped " (reaction_index + 1) " times!"
```

### Complete Block Logic:
```
when Screen1.Initialize
├── call setup_emoji_list
├── set reaction_index to 0
└── set EmojiButton.Text to 😀

when EmojiButton.Click
├── set reaction_index to (reaction_index + 1) mod 8
├── set EmojiButton.Text to select list item emoji_reactions at index (reaction_index + 1)
└── set StatusLabel.Text to join "Mood #" (reaction_index + 1) " of 8"
```

## Extension Ideas
- Add sound effects for each emoji
- Let users add their own custom emojis
- Add vibration feedback on tap
