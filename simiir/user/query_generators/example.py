from simiir.user.query_generators.base import BaseQueryGenerator

import random


class QuestionGenerator_A1(BaseQueryGenerator):
    """
    Takes the first given query, and turns it into a question.
    """

    def __init__(self, stopword_file, query_file, user, background_file=[]):
        super().__init__(stopword_file, background_file=[])
        self.__query_filename = query_file
        self.__user = user

    def generate_query_list(self, user_context) -> list[tuple[str, int]]:
        return_queries: list[tuple[str, int]] = self._get_given_queries(user_context)

        new_query: tuple[str, int] = (self._create_question(return_queries[0][0]), 0)

        return_queries.append(new_query)

        return return_queries

    def _create_question(self, query: str) -> str:
        prefixes: list[str] = [
            "What is",
            "How to",
            "How would I",
            "Why is",
            "Where is",
        ]
        chosen_prefix: str = random.choice(prefixes)
        question_query: str = f"{chosen_prefix} {query.strip()}?"
        return question_query

    def _get_given_queries(self, user_context) -> list[tuple[str, int]]:
        topic = user_context.topic
        given_queries: list = []
        queries_file = open(self.__query_filename, "r")

        for line in queries_file:
            line = line.strip()
            line = line.split(",")

            line_qid = line[0]
            line_user = line[1]
            line_topic = line[2]
            line_terms = line[3]
            print(line_terms)
            if line_user == self.__user and line_topic == topic.id:
                given_queries.append((line_terms, int(line_qid)))

        queries_file.close()
        return [given_queries[-2]]

class QuestionGenerator_A2(BaseQueryGenerator):
    """
    Takes the first given query, and turns it into a question.
    """

    def __init__(self, stopword_file, query_file, user, background_file=[]):
        super().__init__(stopword_file, background_file=[])
        self.__query_filename = query_file
        self.__user = user

    def generate_query_list(self, user_context) -> list[tuple[str, int]]:
        return_queries: list[tuple[str, int]] = self._get_given_queries(user_context)

        new_query: tuple[str, int] = (self._create_question(return_queries[0][0]), 0)

        return_queries.append(new_query)

        return return_queries

    def _create_question(self, query: str) -> str:
        prefixes: list[str] = [
            "What is",
            "How to",
            "How would I",
            "Why is",
            "Where is",
        ]
        chosen_prefix: str = random.choice(prefixes)
        question_query: str = f"{chosen_prefix} {query.strip()}?"
        return question_query

    def _get_given_queries(self, user_context) -> list[tuple[str, int]]:
        topic = user_context.topic
        given_queries: list = []
        queries_file = open(self.__query_filename, "r")

        for line in queries_file:
            line = line.strip()
            line = line.split(",")

            line_qid = line[0]
            line_user = line[1]
            line_topic = line[2]
            line_terms = line[3]

            if line_user == self.__user and line_topic == topic.id:
                given_queries.append((line_terms, int(line_qid)))

        queries_file.close()
        return given_queries[:-1]
    