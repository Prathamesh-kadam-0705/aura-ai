REMINDER_RULES = {

    "intent": "reminder",

    "patterns": [

        {
            "pattern": r"^(remind me|reminder|set reminder|create reminder)(.*)$",
            "action": "create"
        },

        {
            "pattern": r"^(show|list|all) reminders$",
            "action": "list"
        },

        {
            "pattern": r"^delete reminder (.+)$",
            "action": "delete"
        },

        {
            "pattern": r"^update reminder (.+)$",
            "action": "update"
        }

    ]
}