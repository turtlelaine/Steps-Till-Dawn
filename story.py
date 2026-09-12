STORY = {
    # scene 1 intro
    "intro": {
        "lines": [
            "You opened your eyes. It was another sleepless night.",
            "You sighed, got out of bed.",
            "Something important seemed to be forgotten, but you couldn't remember.",
            "The clock paused.",
        ],
        "choices": None,
        "next": None
    },

    # interact with clock
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

    # interact with bed
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
            "Ending 1: At least you got some sleep.",
        ],
        "choices": None,
        "on_end": "ending"
    },
}