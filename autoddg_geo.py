from llm.prompt_builder import GeoAwarePromptBuilder
from llm.yaml_prompt_loader import YamlPromptLoader
from geo_profiler.geo_profiler import GeoProfiler
from geo_profiler.models import GeoProfile
from pandas import DataFrame
import pandas as pd

class AutoDDGGeo:

    def __init__(self, client, model_name: str, temperature: float = 0.0):
        self.client = client
        self.model_name = model_name
        self.temperature = float(temperature)
        self.loader = YamlPromptLoader("prompts.yaml")
        self.system_message = self.loader.get("system_message")

    def analyze_geo(self, semantic_profile: str, df: DataFrame) -> GeoProfile:
        return GeoProfiler.infer_geo_profile(semantic_profile, df)
    
    def generate_geoaware_description(self, dataset_sample: str,
        dataset_profile: str | None = None,
        use_profile: bool = False,
        semantic_profile: str | None = None,
        use_semantic_profile: bool = False,
        data_topic: str | None = None,
        use_topic: bool = False,
        geo_profile: GeoProfile | None = None,
        use_geo_profile: bool = False) -> tuple[str, str]:
        """
        Generates a geo-aware dataset description based on the inferred GeoProfile.
        """
        builder = GeoAwarePromptBuilder(prompt_type="dataset_description")

        prompt = builder.build_geo_aware_prompt(
            dataset_sample=dataset_sample,
            dataset_profile=dataset_profile,
            use_profile=use_profile,
            semantic_profile=semantic_profile,
            use_semantic_profile=use_semantic_profile,
            data_topic=data_topic,
            use_topic=use_topic,
            geo_profile=geo_profile,
            use_geo_profile=use_geo_profile
        )

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": self.system_message},
                {"role": "user", "content": prompt},
            ],
            temperature=self.temperature
        )

        description = response.choices[0].message.content.strip()

        return (description, prompt)