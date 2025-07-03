from simiir.user.query_generators.base import BaseQueryGenerator
from ifind.common.utils import get_given_queries
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import torch
import os


class FinetunedBlockStrategy(BaseQueryGenerator):
    """
    Takes the first given query, and turns it into a question.
    """

    def __init__(self, stopword_file, query_file, user, background_file=[]):
        super().__init__(stopword_file, background_file=[])
        self.__query_filename = query_file
        self.__user = user

        self.CURRENT_DIRECTORY: str = os.path.dirname(__file__)
        self.ROOT_DIRECTORY: str = os.path.dirname(os.path.dirname(os.path.dirname(self.CURRENT_DIRECTORY)))
        self.MODELS_DIRECTORY: str = os.path.join(self.ROOT_DIRECTORY, "models")
        self.LORA_ADAPTER_DIRECTORY: str = os.path.join(self.MODELS_DIRECTORY, "block_checkpoint")
        self.BASE_MODEL_DIRECTORY: str = os.path.join(self.MODELS_DIRECTORY, "llama-3.2-3b")

        assert os.path.exists(self.MODELS_DIRECTORY), f"couldnt find the models directory at {self.MODELS_DIRECTORY}"

        # self.tokenizer = AutoTokenizer.from_pretrained(LORA_ADAPTER_DIRECTORY)
        # self.base_model = AutoModelForCausalLM.from_pretrained(BASE_MODEL_DIRECTORY)
        # self.model = PeftModel.from_pretrained(self.base_model, LORA_ADAPTER_DIRECTORY).to("cuda")

    def generate_query_list(self, user_context) -> list[tuple[str, int]]:
        return_queries: list[tuple[str, int]] = get_given_queries(
            self.__query_filename, self.__user, user_context.topic.id, task_a2=False
        )

        new_query: tuple[str, int] = (self._create_block_query(return_queries[-1][0]), 0)

        return_queries.append(new_query)

        return return_queries

    def _create_block_query(self, query: str) -> str:
        self.tokenizer = AutoTokenizer.from_pretrained(self.LORA_ADAPTER_DIRECTORY)
        self.base_model = AutoModelForCausalLM.from_pretrained(self.BASE_MODEL_DIRECTORY)
        self.model = PeftModel.from_pretrained(self.base_model, self.LORA_ADAPTER_DIRECTORY).to("cuda")

        zauberwort: str = "Output:"
        prompt: str = f"{query}. {zauberwort}"
        print()
        print(f"{prompt = }")
        print()
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        outputs = self.model.generate(**inputs, max_new_tokens=100)
        answer: str = str(self.tokenizer.decode(outputs[0], skip_special_tokens=True))[len(prompt)::1]
        print()
        print(f"{answer = }")
        print()
        del self.model
        del self.base_model
        del self.tokenizer
        torch.cuda.empty_cache()
        return answer