DEVICE_RULES = {

    "intent": "device",

    "patterns": [

        {
            "pattern": r"^open (.+)$",
            "action": "open"
        },

        {
            "pattern": r"^launch (.+)$",
            "action": "open"
        },

        {
            "pattern": r"^start (.+)$",
            "action": "open"
        },

        {
            "pattern": r"^close (.+)$",
            "action": "close"
        }

    ]

}