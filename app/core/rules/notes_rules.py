NOTES_RULES = {

    "intent": "notes",

    "patterns": [

        {
            "pattern": r"^create note (.+)$",
            "action": "create"
        },

        {
            "pattern": r"^show notes$",
            "action": "list"
        },

        {
            "pattern": r"^list notes$",
            "action": "list"
        },

        {
            "pattern": r"^delete note (.+)$",
            "action": "delete"
        },

        {
            "pattern": r"^update note (.+)$",
            "action": "update"
        }

    ]

}