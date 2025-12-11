from .models import (
    GeoProfile
)
from .models import GeoProfile
from .profilers.spatial_role_profiler import SpatialRoleProfiler
from .profilers.geometry_type_profiler import GeometryTypeProfiler
from .profilers.spatial_resolution_profiler import SpatialResolutionProfiler
from .profilers.spatial_use_cases_profiler import SpatialUseCaseProfiler
from .semantic_parser import SemanticParser
import pandas as pd

class GeoProfiler:
    """
    Orchestrates all geospatial enrichment steps:
    - Spatial Role
    - Geometry Type
    - Spatial Resolution
    - Spatial Use Cases

    It only composes outputs from individual profilers.
    """

    @staticmethod
    def infer_geo_profile(semantic_profile: str, df: pd.DataFrame) -> GeoProfile:
        
        profile = SemanticParser.parse_semantic_profile_text(semantic_profile, df)
        # 1. Spatial Role
        spatial_role = SpatialRoleProfiler.infer_spatial_role(profile)

        # 2. Geometry Type
        geometry_type = GeometryTypeProfiler.infer_geometry_type(profile)

        # 3. Spatial Resolution
        spatial_resolution = SpatialResolutionProfiler.infer_spatial_resolution(profile)

        # 4. Spatial Use Cases
        spatial_use_cases = SpatialUseCaseProfiler.infer_spatial_use_cases(
            profile=profile,
            spatial_role=spatial_role,
            geometry_type=geometry_type
        )

        # 5. Bundle everything into a GeoProfile object
        geo_profile = GeoProfile(
            spatial_role=spatial_role,
            geometry_type=geometry_type,
            spatial_resolution=spatial_resolution,
            spatial_use_cases=spatial_use_cases
        )

        return geo_profile