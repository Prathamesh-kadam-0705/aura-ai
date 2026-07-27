MEMORY_RULES = {

    "intent": "memory",

    "patterns": [

        {
            "pattern": r"^my name is (.+)$",
            "action": "create"
        },

        {
            "pattern": r"^my birthday is (.+)$",
            "action": "create"
        },

        {
            "pattern": r"^my favorite color is (.+)$",
            "action": "create"
        },

        {
            "pattern": r"^what is my name$",
            "action": "read"
        },

        {
            "pattern": r"^when is my birthday$",
            "action": "read"
        },

        {
            "pattern": r"^what is my favorite color$",
            "action": "read"
        }

    ]

}