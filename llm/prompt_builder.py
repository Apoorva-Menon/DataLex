from .yaml_prompt_loader import YamlPromptLoader
from typing import Iterable

class GeoAwarePromptBuilder:
    
    def __init__(self, prompt_type="dataset_description"):
        self.loader = YamlPromptLoader("prompts.yaml")
        self.blocks = self.loader.get(prompt_type)
        self.system_message = self.blocks["system_message"]
        self.description_words = 150

    def build_geo_aware_prompt(
        self,
        dataset_sample: str,
        dataset_profile: str | None = None,
        use_profile: bool = False,
        semantic_profile: str | None = None,
        use_semantic_profile: bool = False,
        data_topic: str | None = None,
        use_topic: bool = False,
        geo_profile: str | None = None,
        use_geo_profile: bool = False
    ) -> str:
        """
        Builds a geo-aware AutoDDG prompt while preserving full backward compatibility.
        """
        # Introduction
        sections: Iterable[str] = [
            self.blocks["introduction"].format(dataset_sample=dataset_sample)
        ]
        prompt_parts = list(sections)

        # Profile
        if use_profile and dataset_profile:
            prompt_parts.append(
                self.blocks["profile_instruction"].format(
                    dataset_profile=dataset_profile
                )
            )

        # Semantic
        if use_semantic_profile and semantic_profile:
            prompt_parts.append(
                self.blocks["semantic_instruction"].format(
                    semantic_profile=semantic_profile
                )
            )

        # Geo
        if use_geo_profile and geo_profile:
            geo_text = (
                f"Spatial role: {geo_profile.spatial_role}\n"
                f"Geometry type: {geo_profile.geometry_type}\n"
                f"Spatial resolution: {geo_profile.spatial_resolution}\n"
                f"Spatial use cases: {', '.join(geo_profile.spatial_use_cases)}"
            )

            prompt_parts.append(
                self.blocks["geospatial_instruction"].format(
                    geospatial_profile=geo_text
                )
            )

        # Topic
        if use_topic and data_topic:
            prompt_parts.append(
                self.blocks["topic_instruction"].format(
                    data_topic=data_topic
                )
            )

        # closing
        prompt_parts.extend(
            [
                self.blocks["closing_instruction"],
                f"Target length: approximately {self.description_words} words.",
            ]
        )

        return "\n".join(prompt_parts)
    
    def build_geo_search_prompt(
        self,
        description: str,
        topic: str,
        geo_profile
    ) -> str:
        """
        Builds a geo-aware search expansion prompt.
        This mirrors AutoDDG's expand_description_for_search prompt
        but injects geospatial semantics.
        """

        spatial_role = geo_profile.spatial_role
        geometry_type = geo_profile.geometry_type
        spatial_resolution = geo_profile.spatial_resolution
        spatial_use_cases = ", ".join(geo_profile.spatial_use_cases)

        prompt = f"""
        You are given a dataset about the topic "{topic}", with the following initial description:

        {description}

        Additionally, this dataset has the following geospatial profile:

        - Spatial Role: {spatial_role}
        - Geometry Type: {geometry_type}
        - Spatial Resolution: {spatial_resolution}
        - Spatial Use Cases: {spatial_use_cases}

        Please expand the description by including the exact topic. Additionally, add as many related geospatial concepts, spatial terms, geometry-related keywords, and relevant domain-specific terms as possible based on the initial description, the topic, and the geo profile.

        Unlike the initial description, which is focused on presentation and readability, the expanded description is intended to be indexed at the backend of a dataset search engine to improve search-ability.

        Therefore, focus less on readability and more on including:

        - Spatial scale terms (e.g., street-level, ZIP-level, borough-level)
        - Geometry terms (e.g., point, polygon, polyline)
        - Analysis terms (e.g., hotspot mapping, spatial clustering, area aggregation)
        - Topic-specific synonyms and related terms

        Please follow the structure of the following template:

        Dataset Overview:
        - Keep the exact initial description as provided.

        Key Themes or Topics:
        - theme1
        - theme2

        Applications and Use Cases:
        - usecase1
        - usecase2

        Concepts and Synonyms:
        - concept1
        - concept2

        Keywords and Themes:
        - keyword1
        - keyword2

        Additional Context:
        - context1
        - context2
        """

        return prompt.strip()