CONTACTS_RULES = {

    "intent": "contacts",

    "patterns": [

        {
            "pattern": r"^save (.+)$",
            "action": "create"
        },

        {
            "pattern": r"^find (.+)$",
            "action": "search"
        },

        {
            "pattern": r"^show contacts$",
            "action": "list"
        },

        {
            "pattern": r"^list contacts$",
            "action": "list"
        },

        {
            "pattern": r"^delete contact (.+)$",
            "action": "delete"
        },

        {
            "pattern": r"^update contact (.+)$",
            "action": "update"
        }

    ]

}