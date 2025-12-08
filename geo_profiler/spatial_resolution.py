from .models import DatasetSemanticProfile

from .models import DatasetSemanticProfile
#Define rankings
RESOLUTION_PRIORITY = {"coordinates": 1, "street": 2, "zip": 3, "neighborhood": 4, "district": 5, "borough": 6, "city": 7}

#Helper function: map semantic values to our levels

def normalize_resolution(res): 
    if not res:        
        return None        
    r = res.lower()    
    if "coord" in r:        
        return "coordinates"    
    if "street" in r:        
        return "street"    
    if "zip" in r or "postal" in r:        
        return "zip"    
    if "neigh" in r:        
        return "neighborhood"    
    if "district" in r:        
        return "district"    
    if "borough" in r:        
        return "borough"    
    if "city" in r:        
        return "city"    
    return None

#Column name fallbacks:
def infer_resolution_from_name(name):    
    name = name.lower()    
    if any(k in name for k in ["lat", "lon", "latitude", "longitude"]):        
        return "coordinates"    
    if "street" in name:        
        return "street"    
    if "zip" in name:        
        return "zip"    
    if any(k in name for k in ["district", "tract"]):        
        return "district"    
    if "borough" in name:        
        return "borough"    
    if "city" in name:        
        return "city"    
    return None

def infer_spatial_resolution(profile: DatasetSemanticProfile) -> str:    
    resolutions = set()        
    for col in profile.columns:        
        
        # 1. Semantic profiler value        
        if col.spatial_resolution:            
            res = normalize_resolution(col.spatial_resolution)            
            if res:                
                resolutions.add(res)        
        
        # 2. Column name heuristic        
        name_res = infer_resolution_from_name(col.name)        
        if name_res:            
            resolutions.add(name_res)    
        
    if not resolutions:        
        return "unknown"    

    # If only one — use it directly    
    if len(resolutions) == 1:        
        return list(resolutions)[0] + "-level"    
    
    # If multiple -> multi-level    
    # BUT we still want: highest *priority* for sorting later if needed
    return "multi-level"