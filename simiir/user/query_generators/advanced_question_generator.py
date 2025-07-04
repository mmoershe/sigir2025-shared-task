import random
from simiir.user.query_generators.base import BaseQueryGenerator
from ifind.common.utils import get_given_queries

class AdvancedQuestionQueryGenerator(BaseQueryGenerator):
    """
        This generator uses a combination of randomly selected "wh-words" (e.g. How, What, Why)
        and predefined question templates to form meaningful questions related to the topic.
        It adds realistic sentence endings (question mark, period, or none) based on
        observed user behavior.
    """

    def __init__(self, stopword_file=None, query_file=None, user=None, background_file=[]):
        super().__init__(stopword_file, background_file=background_file)
        self.__query_filename = query_file
        self.__user = user

    
        self.w_words = {
            "How": 0.455,
            "What": 0.269,
            "Why": 0.095,
            "Is": 0.035,
            "Does": 0.034,
            "Do": 0.033,
            "Can": 0.031,
            "Are": 0.025,
            "When": 0.021,
            "Who": 0.011,
        }

        
        self.templates = [
            "{w_word} does {topic} affect people in different regions",
            "{w_word} are the main causes of {topic}",
            "{w_word} can be done to prevent {topic}",
            "{w_word} is the cultural significance of {topic}",
            "{w_word} are the effects of {topic} on education",
            "{w_word} can governments do about {topic}",
            "{w_word} is public opinion on {topic}",
            "{w_word} can we raise awareness about {topic}",
            "{w_word} role does media play in shaping views on {topic}",
            "{w_word} are common misconceptions about {topic}"
        ]

    def weighted_choice(self, choices: dict) -> str:
        elements, weights = zip(*choices.items())
        return random.choices(elements, weights=weights, k=1)[0]

    def generate_query_list(self, user_context) -> list[tuple[str, int]]:
        return_queries: list[tuple[str, int]] = get_given_queries(
            self.__query_filename, self.__user, user_context.topic.id, task_a2=False
        )

    
        for _ in range(10):
            new_query: tuple[str, int] = (self._create_question(return_queries[-1][0]), 1)
            return_queries.append(new_query)

        return return_queries


    def _create_question(self, topic: str) -> str:
        w_word = self.weighted_choice(self.w_words)
        template = random.choice(self.templates)
        question = template.format(w_word=w_word, topic=topic).strip()
        question += self._choose_ending()
        return question

    def _choose_ending(self) -> str:
        endings = ["?", ".", ""]  
        weights = [0.29, 0.22, 0.49]
        return random.choices(endings, weights=weights, k=1)[0]
