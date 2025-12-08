from typing import List
from .models import DatasetSemanticProfile

USECASES = {"event_temporal": 
            ["spatio-temporal incident analysis", 
             "hotspot mapping", "event clustering", 
             "trend analysis over time",
            ],    
            "event_spatial_only": [
                "hotspot detection", 
                "spatial clustering",
            ],   
            "observation": [
                "location inventory", 
                "sensor mapping", 
                "proximity analysis",
            ],    
            "infrastructure": [
                "accessibility mapping", 
                "navigation support", 
                "facility density analysis",
            ],    
            "boundary": [
                "area-based aggregation", 
                "choropleth visualization", 
                "administrative-region analysis", 
            ],    
            "polyline": [
                "route analysis", 
                "street-segment mapping", 
                "mobility pathway visualization",
            ],    
            "multi": [
                "combined geometric overlays", 
                "multi-layer spatial visualization", 
            ]}

#inference function:
def has_temporal_columns(profile):    
    return any(col.is_temporal for col in profile.columns)

def infer_spatial_use_cases(profile: DatasetSemanticProfile,                            
    spatial_role: str,                            
    geometry_type: str) -> List[str]:    
    temporal = has_temporal_columns(profile)       
    
    # Boundary    
    if spatial_role == "boundary":        
        return USECASES["boundary"]        
    
    # Infrastructure    
    if spatial_role == "infrastructure":        
        return USECASES["infrastructure"]        
    
    # Event datasets    
    if spatial_role == "event":        
        if temporal:
            return USECASES["event_temporal"]        
        else:            
            return USECASES["event_spatial_only"]        
        
    # Observations    
    if spatial_role == "observation":        
        return USECASES["observation"]        
    
    # Geometry-driven fallbacks    
    if geometry_type == "polyline":        
        return USECASES["polyline"]    
    if geometry_type == "multi":        
        return USECASES["multi"]
            
    # If nothing matches 
    return []