CALENDAR_RULES = {

    "intent": "calendar",

    "patterns": [

        {
            "pattern": r"^schedule (.+)$",
            "action": "create"
        },

        {
            "pattern": r"^create meeting (.+)$",
            "action": "create"
        },

        {
            "pattern": r"^show calendar$",
            "action": "list"
        },

        {
            "pattern": r"^my meetings$",
            "action": "list"
        },

        {
            "pattern": r"^delete meeting (.+)$",
            "action": "delete"
        }

    ]

}