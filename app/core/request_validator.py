class RequestValidator:

    REQUIRED_FIELDS = {

        ("alarm", "create"): [
            "time"
        ],

        ("reminder", "create"): [
            "task",
            "time"
        ],

        ("calendar", "create"): [
            "title",
            "date"
        ],

        ("contact", "create"): [
            "name",
            "phone"
        ],

        ("note", "create"): [
            "title"
        ],

        ("todo", "create"): [
            "task"
        ]

    }

    @classmethod
    def validate(cls, request):

        required = cls.REQUIRED_FIELDS.get(
            (request.intent, request.action),
            []
        )

        missing = []

        for field in required:

            if not request.entities.get(field):
                missing.append(field)

        return missing