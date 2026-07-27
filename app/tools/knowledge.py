class KnowledgeModule:

    def answer(self, request):

        # Extract topic from cognitive engine
        topic = request.entities.get("topic")


        # Safety fallback
        if not topic:

            topic = request.entities.get("raw_response")


        if not topic:

            return {
                "success": False,
                "message": "No topic found"
            }


        # Convert topic safely
        topic = str(topic).strip()


        answers = {

            "flutter":
            "Flutter is Google's UI toolkit used to build Android, iOS and web applications using Dart programming language.",


            "python":
            "Python is a high-level programming language used for AI, automation, backend development and data science.",


            "fastapi":
            "FastAPI is a modern Python framework used to build fast and scalable APIs.",


            "postgresql":
            "PostgreSQL is an open-source relational database management system used to store and manage structured data.",


            "llama":
            "Llama is a family of large language models developed for natural language understanding and generation.",


            "ai":
            "Artificial Intelligence is a technology that enables machines to understand, learn and perform tasks similar to human intelligence.",


            "machine learning":
            "Machine Learning is a branch of AI where systems learn patterns from data and improve performance.",


            "dart":
            "Dart is a programming language developed by Google and used mainly for Flutter application development.",


            "android":
            "Android is a mobile operating system developed by Google used in smartphones and other devices."

        }


        # Find answer
        answer = answers.get(
            topic.lower(),
            f"I don't have information about {topic} yet."
        )


        return {

            "success": True,

            "message":
            "Answer generated successfully.",

            "data": {

                "topic": topic,

                "answer": answer

            }

        }