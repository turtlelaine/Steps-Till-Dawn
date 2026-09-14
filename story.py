STORY = {
    "intro": {
        "lines": [
            "You opened your eyes. It was another sleepless night.",
            "You sighed, got out of bed.",
            "Something important seemed to be forgotten,",
            "but you couldn't remember.",
            "The clock paused.",
        ],
        "choices": None,
        "next": None
    },

    "clock_found": {
        "lines": [
            "You stared at the clock for a while.",
            "'Since when...?'",
            "You touched the clock.",
            "Time started to rewind.",
            "'Wait, what is happening here??'",
        ],
        "choices": [
            ("Check", "touch_clock"),
            ("Better get some sleep", "go_sleep")
        ]
    },

    "touch_clock": {
        "lines": [
            "You checked and touched the clock.",
            "Time started to rewind, everything felt distorted.",
        ],
        "choices": None,
        "on_end": "go_to_rooftop"
    },

    "go_sleep": {
        "lines": [
            "You put down the clock and wanted to get some sleep.",
            "'Whatever.'",
            "You closed your eyes.",
        ],
        "choices": None,
        "on_end": "sleep_count"
    },

    "ending1": {
        "lines": [
            "You fell asleep.",
            "'Zzz...'",
            "Well, at least you had got some sleep.",
            "",
            "—— Ending 1: At least you got some sleep. ——",
        ],
        "choices": None,
        "on_end": "ending"
    },

    "rooftop_arrival": {
        "lines": [
            "'Where... is this?'",
        ],
        "choices": None,
        "on_end": None,
        "position": "bottom"
    },

    "rooftop_trigger": {
        "lines": [
            "'Seren! Wait!'",
            "'No——!'",
        ],
        "choices": None,
        "on_end": "hide_seren_and_fade",
        "position": "bottom"
    },

    "rooftop_black": {
        "lines": [
            "He didn't turn around, but to leave you again.",
            "You know that you had to make a choice.",
        ],
        "choices": None,
        "on_end": "back_to_room1",
        "position": "center"
    },

    "wake_up": {
        "lines": [
            "You woke up, stared at the clock for a while.",
            "'Is that just a dream?'",
        ],
        "choices": None,
        "on_end": None,
        "position": "bottom"
    },

    "rewind_again": {
        "lines": [
            "You touched the clock, and it began to spin backwards.",
            "The world distorted, and time rewound again.",
        ],
        "choices": None,
        "on_end": "loop_count",
        "position": "center"
    },

    "reach_seren": {
        "lines": [
            "You reached out and grabbed Seren's hand.",
            "'I got you!'",
            "But he let go.",
            "You both fell.",
        ],
        "choices": None,
        "on_end": "hide_seren_and_start_timer",
        "position": "center"
    },

    "rooftop_fail": {
        "lines": [
            "You reached out, but he slipped through your fingers.",
            "'No... not again.'",
        ],
        "choices": None,
        "on_end": "hide_seren_and_back",
        "position": "center"
    },

    "rewind_final": {
        "lines": [
            "You touched the clock, and it began to spin backwards.",
            "The world distorted, and time rewound again.",
            "But this time... something felt different.",
        ],
        "choices": None,
        "on_end": "wake_up_kitchen",
        "position": "center"
    },

    "ending2": {
        "lines": [
            "You didn't rewind.",
            "The ground came closer and closer.",
            "'......'",
            "Once again, you lost him.",
            "",
            "—— Ending 2: Loop ——",
        ],
        "choices": None,
        "on_end": "ending",
        "position": "center"
    },

    "wake_up_kitchen": {
        "lines": [
            '"Hey. Wake up."',
            '"Hello?"',
            "'...Seren?'",
            '"Who else would it be?"',
            "Something in your mind is fading away in a millisecond.",
            "'Nothing...'",
            "'I think I just forgot something important.'",
            '"What was that?"',
            "'I dunno I forgor.'",

        ],
        "choices": None,
        "on_end": "start_kitchen_timer",
        "position": "bottom"
},

    "seren_talk": {
        "lines": [
            '"What?"',
            '"You\'re staring at me like I\'m-"',
            '"...Never mind."',
        ],
        "choices": None,
        "on_end": None,
        "position": "bottom"
    },

    "ending3": {
        "lines": [
            "The clock kept ticking.",
            "You are happy with your life now.",
            "The days passed peacefully.",
            "You felt a sense of happiness.",
            "...",
            "",
            "—— Ending 3: Simple Happiness...? ——",
        ],
        "choices": None,
        "on_end": "ending",
        "position": "center"
    },

    "tv_interact": {
        "lines": [
            "You walked to the TV.",
            "Do you want to watch the TV?",
        ],
        "choices": [
            ("Turn on", "tv_on_story"),
            ("Never mind", None)
        ],
        "position": "bottom"
    },

    "tv_on_story": {
        "lines": [
            "You turned on the TV.",
            "The screen flickered.",
            "Something was wrong.",
            '"....Following a report from a member of the public,"',
            '"police found a body beneath the building."',
            '"The deceased is a male half-ghost, approximately 20 years old..."',
            "You turned off the TV.",
            '"you shouldnt have turned it on..."',
            "'...'",
            '"you would be sorry."'
        ],
        "choices": None,
        "on_end": "tv_on",
        "position": "bottom"
    },

    "after_tv": {
        "lines": [
            "You felt something rushing into your head.",
            "You remembered every moment with Seren,",
            "His laugh, his jokes...",
            "...and his death.",
        ],
        "choices": None,
        "on_end": "back_to_kitchen",
        "position": "center"
    },

    "seren_confront": {
        "lines": [
            '"Why don\'t you just stay?"',
            '"We\'re so happy together."',
        ],
        "choices": None,
        "next": "zyrou_reply",
        "position": "bottom"
    },

    "zyrou_reply": {
        "lines": [
            "'...'",
            "'......yeah.'",
            "'We were so happy together,'",
            "'Then why are you leaving?'",
        ],
        "choices": None,
        "next": "seren_reply",
        "position": "bottom"
    },

    "seren_reply": {
        "lines": [
            '"It doesn\'t matter..."',
        ],
        "choices": None,
        "next": "zyrou_interrupt",
        "position": "bottom"
    },

    "zyrou_interrupt": {
        "lines": [
            "'You don't know the answer, don't you?'",
            "'Because you're not real.'",
            "'Here,'",
            "'This whole room,'",
            "'Whole space,'",
            "'They're not real and you know about it!'",
        ],
        "choices": None,
        "next": "seren_desperate",
        "position": "bottom"
    },

    "seren_desperate": {
        "lines": [
            '"No..."',
            '"No, please..."',
            '"But now I am here!"',
            '"That\'s what you wanted!"',
            '"Why don\'t you just stay and live here with me?"',
        ],
        "choices": None,
        "next": "zyrou_silent",
        "position": "bottom"
    },

    "zyrou_silent": {
        "lines": [
            "'...'",
        ],
        "choices": None,
        "next": "seren_final_choice",
        "position": "bottom"
    },

    "seren_final_choice": {
        "lines": [
            "'You know how to choose.'",
        ],
        "choices": [
            ("Stay", "ending4"),
            ("Leave", "leave_choice")
        ],
        "position": "bottom"
    },

    "ending4": {
        "lines": [
            "He is right,",
            "That's all you want, you want him to stay.",
            "You chose to stay.",
            "Something left quickly in your mind.",
            "You could feel that you forget a lot of things.",
            "But you don't remember anything.",
            "The weather was perfect outside.",
            "Everything was perfect.",
            "The clock kept on, tick-tack.",
            "Seren asked you to hang out.",
            "You changed your clothes and went out with him, as how you did.",
            "",
            "—— Ending 4: Normal Perfect Day ——",
        ],
        "choices": None,
        "on_end": "ending",
        "position": "center"
    },

    "leave_choice": {
        "lines": [
            '"...Why..."',
            '"Why Zyrou?"',
            '"Why don\'t you choose me???"',
        ],
        "choices": None,
        "next": "leave_continue",
        "position": "bottom"
    },

    "leave_continue": {
        "lines": [
            "He doesn't seemed to be sad or reluctant to see you go, but anger.",
            "You are now more convinced than ever of your hunch.",
        ],
        "choices": None,
        "next": "zyrou_final_words",
        "position": "bottom"
    },

    "zyrou_final_words": {
        "lines": [
            "'He's dead.'",
            "'Already.'",
            "'And I know about it, you know about it as well.'",
            "'That you're not real,'",
            "'That you just want to trap me in this world to keep you 'alive' here.'",
            "'That's not what Seren would do...'",
        ],
        "choices": None,
        "next": "leave_end",
        "position": "bottom"
    },

    "leave_end": {
        "lines": [
            "\"Seren\" became quiet.",
            "You decided to do something.",
        ],
        "choices": None,
        "on_end": "leave_kitchen",
        "position": "center"
    },

    "before_true_ending": {
        "lines": [
            "Time rewound faster than ever before.",
            "You heard 'Seren' saying something behind you angrily,",
            "but you couldn't hear what it was.",
            "Everything from this nightmare was gone,",
            "and your memories started to fade as well.",
        ],
        "choices": None,
        "on_end": "back_to_room1_true",
        "position": "center"
    },

    "true_ending_1": {
        "lines": [
            "You found yourself lying on the floor.",
            "You looked at the clock subconsciously, though you don't know why.",
            "It felt like a long, long dream.",
            "But somehow you felt a sense of peace.",
            "The clock doesn't work anymore.",
            "You replaced it with a new one.",
        ],
        "choices": None,
        "next": "true_ending_2",
        "position": "bottom"
    },

    "true_ending_2": {
        "lines": [
            "You returned to your daily life.",
            "You went to school, ate, hung out with friends.",
            "Sometimes you'd still send messages to Seren on social media,",
            "but there was never a reply.",
            "You complained that Seren hadn't even visited you once in your dreams.",
            "But it's okay.",
            "Because you believe you will meet again.",
            "",
            "—— Ending 5: Dawn ——",
        ],
        "choices": None,
        "on_end": "ending",
        "position": "center"
    },

    "seren_diary_1": {
        "lines": [
            "You opened Seren's diary.",
            "The first half of the diary was stuck.",
            "But you opened it by your strength.",
            "",
            "Page 1:",
            "'This is the 1st day streak of me writing a diary. Keep on!'",
            "",
            "Page 2:",
            "'This is harder than I think...'",
            "'Anyways it's the 2nd day of me writing a diary.'",
            "",
            "Page 3:",
            "'This is the 1st day streak of my writing!'",
            "'Man I tried idk how to keep long.'",
            "",
            "Page 5:",
            "'I just slept for 35 hours??'",
            "'That's a lot of sleep.'",
            "'And I think I dreamt of Zyrou dying.'",
            "'That's too real to be a dream tho...'",
            "",
            "Page 34:",
            "'I've had enough...'",
            "'Whatever I do I can't save him.'",
            "'What makes you so much in pain?'",
            "'I don't sleep so well these days.'",
            "'Guess I need some sports or sun. '",
            "'Is that just a dream or is it fr?'",
            "'idk.'",
            "",
            "Page 83:",
            "'He is back.'",
            "'Acting completely normal, as if nothing happened.'",
            "'Something feels off.'",
            "'But I don't remember what happened. Why do I feel so tired?'",
            "'anw This is the 1st day streak of me writing a diary.'",
            "",
            "'Why can't I flip the pages before btw?'",
            "",
            "Page 100:",
            "'I remembered all.'",
            "'Ts aint real chat wtf is going on'",
            "'he's supposed to be dead...'",
            "'but who is that outside living with me then??'",
            "",
            "Page 101:",
            "'I'm sorry. I'm so sorry I didn't choose to stay.'",
            "'But I have to find you.'",
        ],
        "choices": None,
        "next": "seren_diary_2",
        "position": "bottom"
    },

    "seren_diary_2": {
        "lines": [
            "You closed the diary.",
            "",
            "A strong feeling came up,",
            "that he's still alive somewhere.",
            '"I will find you. "',
            "You remembered the clock.",
            "An idea came up to your mind.",
            "",
            "Thanks for playing :)",
            "",
            "See you next time?",
            "",
        ],
        "choices": None,
        "on_end": "ending",
        "position": "center"
    },
    "books_secret": {
        "lines": [
            "You picked up a book.",
            "A photo fell out.",
            "It was a picture of you and Seren.",
            "You were both laughing.",
            "You put the photo back.",
        ],
        "choices": None,
        "on_end": None,
        "position": "bottom"
    },


}