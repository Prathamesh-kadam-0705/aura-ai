TODO_RULES = {

    "intent": "todo",

    "patterns": [

        {
            "pattern": r"^add (.+) to my todo$",
            "action": "create"
        },

        {
            "pattern": r"^show todo$",
            "action": "list"
        },

        {
            "pattern": r"^show my todo$",
            "action": "list"
        },

        {
            "pattern": r"^delete todo (.+)$",
            "action": "delete"
        },

        {
            "pattern": r"^update todo (.+)$",
            "action": "update"
        }

    ]

}