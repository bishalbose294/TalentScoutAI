from transformers import TokenClassificationPipeline, AutoModelForTokenClassification, AutoTokenizer
from transformers.pipelines import AggregationStrategy
import numpy as np
import configparser

config = configparser.ConfigParser()
config.read("TalentScoutAI/backend/src/configs/config.cfg")
embed_config = config["EMBEDDINGS"]

class KeyphraseExtractionPipeline(TokenClassificationPipeline):

    def __init__(self,):
        super().__init__(
            model=AutoModelForTokenClassification.from_pretrained(str(embed_config["KEYWORD_EXTRACTOR"])),
            tokenizer=AutoTokenizer.from_pretrained(embed_config["KEYWORD_EXTRACTOR"], device_map = 'cuda')
        )

    def postprocess(self, all_outputs):
        results = super().postprocess(
            all_outputs=all_outputs,
            aggregation_strategy=AggregationStrategy.FIRST,
        )
        return np.unique([result.get("word").strip() for result in results])