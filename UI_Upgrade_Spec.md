# 🎬 UI_Upgrade_Spec.md
## Welcome → Topic Selection Interaction Specification
---
## 1️⃣ Welcome Scene
```
┌────────────────────────────┐
│        模糊背景照片         │
│                              │
│      [ 清晰16:9照片 ]        │
│                              │
│           点击进入回忆 →      │
└────────────────────────────┘
```
### Structure
* Background: full-screen blurred image
* Foreground: same image, clear, 16:9, centered
* Enter button near foreground image
### Interaction
On click:
* Foreground image scales up to full screen
* Enter button fades out
* No page switch, same visual space continues
---
## 2️⃣ Topic Selection Appearance (Sync Entrance)
After image expansion finishes:
Left cards and right image **start appearing at the same time**.
```
┌────────────────────────────────────────────┐
│  │主题2│                                     │
│    │主题3│                                   │
│      │主题4│  ← 中心焦点    [主题图片]       │
│    │主题5│                                   │
│  │主题6│                                     │
└────────────────────────────────────────────┘
```
### Sync Rule (Important)
* Left cards enter
* Right image fades in + slight scale up
* Both start and end together
* No delayed loading
---
## 3️⃣ Left Card Area (Arc Layout)
### Layout
Cards are arranged on a slight arc.
Center card is the rightmost point of the arc.
```
      Upper Items
    │主题2│
  │主题3│
│主题4│   ← Center Focus (Rightmost)
  │主题5│
    │主题6│
      Lower Items
```
* Center card is most right
* Upper and lower cards shift slightly left
* Forms a curved vertical selector
### Movement
During vertical scroll:
* Cards move along the arc path
* Incoming center card moves right
* Leaving center card moves left
* Not pure vertical translation
### Visual Style
* Semi-transparent cards
* Frosted glass appearance
* Background slightly visible through cards
---
## 4️⃣ Right Image Area
* Displays content of selected card
* Changes smoothly with selection
* No flashing or instant replacement
Image transition:
* Old image slightly shrinks/fades
* New image scales/fades in simultaneously
* Continuous visual transition
---
## 5️⃣ Two-Step Confirmation (Important)
Interaction has three states:
### A. Selection State (Default)
* Center card selected
* Image displayed
* No emphasis animation
---
### B. Focus State (First Click)
Click center card **or** right image:
Both animate simultaneously:
Card:
* Moves slightly right
* Slight scale up
* Highest visual layer
Image:
* Slight scale up
* Increased visual focus
No playback starts here.
---
### C. Enter State (Second Click)
Second click on card or image:
→ Enter playback.
---
### State Flow
```
Scroll → Selection
Click → Focus (card突出 + image放大)
Click again → Playback
```
---
## 6️⃣ Exit / Return
When leaving focus state:
* Card returns to arc position
* Image returns to normal size
* Selection state restored
All transitions must be reversible.
---
## 7️⃣ Timeline Summary
```
T0 Welcome Scene
T1 Click enter
T2 Image expands + button fades
T3 Cards and image appear together
T4 Selection state
T5 Click → Focus state
T6 Click again → Playback
```
---
## 8️⃣ Animation Priority Rule
To ensure smoothness and synchronization:
1. **Sync Group:** Left cards and Right image must use the same timeline trigger.
2. **Parallel Execution:** Do not wait for one to finish before starting the other.
3. **Single Frame:** Render both elements in the same frame to avoid "stagger" effect.
---
✅ End of Specification
