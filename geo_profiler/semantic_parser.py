import re
from .models import ColumnSemantic, DatasetSemanticProfile

def parse_semantic_profile_text(text: str) -> DatasetSemanticProfile:    
    columns = []    
    
    # Split per column block using '**ColumnName**'    
    blocks = re.split(r"\*\*(.*?)\*\*:", text)[1:]    
    
    # blocks comes as: [name1, content1, name2, content2, ...]    
    for i in range(0, len(blocks), 2):        
        name = blocks[i].strip()        
        content = blocks[i + 1]        
        
        # Defaults        
        is_spatial = False        
        spatial_resolution = None        
        domain_type = None        
        function = None        
        is_temporal = False        
        
        # Detect spatial        
        if "Contains spatial data" in content:            
            is_spatial = True            
            
            # Extract spatial resolution            
            res_match = re.search(r"resolution:\s*([^)]+)", content)            
            if res_match:                
                spatial_resolution = res_match.group(1).strip()        
                
        # Detect temporal (if ever present)        
        if "Contains temporal data" in content:            
            is_temporal = True        
            
        # Domain type        
        dom_match = re.search(r"Domain-specific type:\s*([^.]+)", content)        
        if dom_match:            
            domain_type = dom_match.group(1).strip()        
            
        # Function
        func_match = re.search(r"Function/Usage context:\s*([^.]+)", content)        
        if func_match:            
            function = func_match.group(1).strip()        
        
        columns.append(            
            ColumnSemantic(name=name, is_spatial=is_spatial, spatial_resolution=spatial_resolution, is_temporal=is_temporal, domain_type=domain_type, function=function))
    
    return columns