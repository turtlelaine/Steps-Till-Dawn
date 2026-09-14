# Steps Till Dawn — Documentation  

**Author:** Turtle (Yi Ning Lam)  
**Course:** Tech Basics I  
**Date:** 14.09.2026  

---

## 1. Project Overview

**Steps Till Dawn** is a narrative-driven 2D pixel RPG built with Python and Pygame.  
The game explores themes of time, memory, and letting go. The player controls a character named Zyrou, who discovers a mysterious clock that can rewind time. Zyrou uses it repeatedly to try to save Seren, but every attempt falls just short.
  
The game features **5 different endings**, a time-rewind mechanic, and a save system with 3 slots.  

---

## Initial Sketches & Plan  
  
### 2.1 Concept  
  
The original story came from my short film last year, about a person who keeps rewinding time to save someone they love, only to realize that accepting loss is the only way forward.  
I wanted to show different endings for a long time, so I used the same story.
  
### 2.2 Early Sketches  
  
The original story link and storyboard: https://docs.google.com/document/d/150bIctI2PqlJcy5lcPoHBytz82SWYEXoIcR5rhbnJiw/edit?usp=sharing  
(all in Chinese)  
  
Earliest character design for the story:  
<img width="4000" height="5000" alt="Untitled_Artwork 13" src="https://github.com/user-attachments/assets/7cdcb170-df82-4721-b9f5-3a509b0b5369" />  
  
...And then I realized that's way too complex for me to draw anything for game, so I simplified Zyrou into:
<img width="2732" height="2048" alt="Screenshot 2026-09-13 at 10 58 10 PM" src="https://github.com/user-attachments/assets/ea296a56-9c31-4858-a88d-de953d5615d1" />  
  
...Yet still too much. And somehow at that time I was obsessed with pixel art, so it became like this:  
<img width="2732" height="2048" alt="Screenshot 2026-09-13 at 10 59 06 PM" src="https://github.com/user-attachments/assets/0ee13c0a-e4c2-4a33-8669-41cea98ec34a" />  
  
And then further simplify:  
<img width="1760" height="2240" alt="walk_1" src="https://github.com/user-attachments/assets/aa13aae3-b861-4cf4-afb5-87a3f3b4b30e" />  
<img width="2732" height="2048" alt="seren1" src="https://github.com/user-attachments/assets/33e908b7-bd33-482c-abbf-2d47d5f1a0de" />  
Here they are :)  

And all the maps below:  
<img width="1280" height="800" alt="background" src="https://github.com/user-attachments/assets/b5869267-f6cf-46aa-b5ca-cd7d54956492" />  
<img width="2240" height="1400" alt="Corridor" src="https://github.com/user-attachments/assets/311d1c59-4f45-4ea9-9163-0a95a5047b6a" />  
<img width="2240" height="1400" alt="Room3bg" src="https://github.com/user-attachments/assets/33537345-2290-4374-8159-3cc7954d006a" />  
<img width="2240" height="1400" alt="Room3bg 3" src="https://github.com/user-attachments/assets/466c6dc1-ff38-4891-ad85-c0ffa2593480" />  
<img width="2240" height="1400" alt="Room3bg 2" src="https://github.com/user-attachments/assets/48b1c6bc-6ed2-4beb-bdd0-dcd1e3adf2f0" />  
<img width="2240" height="1400" alt="Main page" src="https://github.com/user-attachments/assets/3941b5c6-863c-4a01-adfe-3b716dedb32a" />  
(I forgot to name them after room 3 background image so they're now all now room3bg somehow)  
  
Was about to add some more visual, but time is running too fast that I don't have enough time to do all that.  
Here's the only one that I attempted to do, posture referencing from Pinterest:  
<img width="2240" height="1400" alt="UntitledArtwork9" src="https://github.com/user-attachments/assets/ed453631-7655-4b14-a494-48eec3c78f8f" />  
Maybe somewhere in the future I'll really complete this part :)  
  
### 2.3 Planned Features  
I love rpg games (esp. those made from rpg maker e.g. Angels of Death, Ib, Noel the Mortal Fate, etc.), so I plan to follow that kind of game style but using python to complete it.  
And I have to script all endings that I wanted to show, draw character movements, save and load function, draw ending collection images, some basic but stunning python stuff to let me show off myself, etc.  


---

## 3. Development Process  
04.07.2026 update: updated README.md, designed title and story abstract.  
  
05.07.2026 update: minor update on README.md, updated game control plan.  
  
07.07.2026 update: character design, pixel art  

16.07.2026 update: updated script, finding reference on map and code, tried to put everything in a file. Grabbed some burgers.   

(moving with my family during between these days, went back to HK and filmed for the other project)  

10.08.2026 update: updated scene 1 map background and props.  
  
13.08.2026 update: updated character design (Zyrou), fixed some room 1 map collision, added in interaction between props and character, emotional breakdown for a while because I feel like I can never finish it.  

09.09.2026 update: updated a lot of stuff ~~because I forgot that we can commit and push in PyCharm so when I realized I should do this its already 09.09.2026~~  
completed full character animation and scene 1 interaction & collision maps anyways, done drawing the other maps, got some power naps and didn't lock in, regretted on not locking in bur still kinda procrastinated.  

12.09.2026 update: updated a LOT of stuff. Fixed image size, asked AI "how to solve using key and going to the other room and go back", separated code by class, separated code into main.py, scene.py, story.py and game.py to keep code easier to edit and watch. Completed ending 1, locked in, updated README.md.  

13.09.2026 update: updated the rest of the endings, getting burnt and cooked, got an hour power nap, turns out became powerless.  
Fixed save and load function, simplified some parts, got some cookies from digi lab, got some drinks from Alex, Arsen and Jasper, got some treats from Carina and Casper, didn't get enough sleep, getting home late, updated collision map in kitchen, made dinner, added in .gitignore file and at last updated README.md with the final game control, code structure, and stuff you can see in README.md  
  
14.09.2026 update: updated documentation.md and requirement.md, Dobby is freeeeeeeeee (actually far from free but yeah)   
  
## 4. Challenges Faced

### 4.1 Collision
The character sometimes would get out of the walls or walking in somewhere they shouldn't be waliking. So then I searched for tutorial and try to use `pygame.mask.overlap()` to check only non-transparent pixels for props, and applied to collision map masking to set a certain space for character to move.  
  
### 4.2 Save/Load System
At first when loading a save during a story event, the story would not trigger correctly, and characters would disappear.  
After changing the save function, it only saves the place but not with story and character status.

Solved by adding character's state (position, visibility, facing direction) to the save data, and reset all temporary story states on load.

### 4.3 Dialogue Bubbles
Those dialogues were only floating somewhere in the screen and didn't seem to be dialogues.  
Didn't fully solved, I don't have enough time for building one more dialogue system so I just added in a rectangle underneath the maps and set them to be fitting in.  

### 4.4 Time Management
Got four projects at the same time, didn't plan well on each so I'm always in a rush.  
Didn't really solve this issue but I tried to finish them all within the date.   
  
---  
  
## 5. Future Improvements

- Add more rooms and outdoor areas  
- Add more sound effects  
- Improve dialogue box and inventory design  
- Port to browser (by using Pygbag?)  
- Add language toggle  
- Add keyboard remapping and text size options
- Better time management
- Longer storyline

---

## 6. Known Limitations

- The game only runs on desktop (Python required).
- No mobile support.
- Some story branches are linear and could be expanded.
- Save files are local only (not cloud-synced).

---

## 7. References

- BGM: 人狼の為の子守唄 https://dova-s.jp/zh-tw/bgm/detail/2853  
- Reference (tutorial): https://youtu.be/tJiKYMQJnYg?si=fmmF3sYKbU2sBsAI (collision map)  
- https://youtu.be/__mZO-53PPM?si=SRh9qqoho6ruJoFU (how to save and load)  
- Assets reference:  
  https://www.pinterest.com/pin/979181143990275060/  
  https://www.pinterest.com/pin/979181143987484547/  
  https://www.pinterest.com/pin/754282637614821948/  
  
Original story: https://youtu.be/Sh820Sh9ffQ?si=uLel9zMxDBi2LJZQ  
(I'll be happy if you like it. :])  
  
---  
  
## 8. Appendix  
  
### 8.1 Controls   
- `arrows` : Move  
- `SPACE`: Interact/ continue  
- `Esc`: Quit game  
- `i`: Open inventory  
- `s`: Save  
  
### 8.2 Endings  
  
1. **At least you got some sleep**: Ignore the clock and go to bed 3 times  
2. **Loop**: Fail to rewind in time  
3. **Simple Happiness...?**: Never turn on the TV  
4. **Normal Perfect Day**: Choose to stay in the illusion
5. **Dawn (True Ending)**: Choose to leave and face reality
6. **Diary (Hidden Story)**: Collect all 5 endings to unlock key3 and get access to Seren's room.

---

*End of documentation.*
