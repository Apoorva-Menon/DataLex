# AutoDDG-Geo  
**Geospatial Extension of AutoDDG for Spatially-Aware Dataset Descriptions**

AutoDDG-Geo enhances the original AutoDDG pipeline with geospatial reasoning.  
It introduces a Geo Profiler that infers spatial role, geometry type, spatial resolution, and geospatial use-cases from tabular datasets, enabling LLM-generated descriptions that better support dataset discovery.

For methodology details, refer to:  
- Project Proposal :contentReference[oaicite:1]{index=1}  

---

## 🔧 Features
- Deterministic rule-based Geo Profiler  
- Spatial role identification (event, boundary, infrastructure, observation)  
- Geometry type inference (point, polygon, polyline, multi)  
- Spatial resolution detection (street-level, ZIP-level, borough-level, multi-level)  
- Geospatial Faithfulness Score (GFS) evaluation metric  
- LLM-based geospatial dataset description generation  

---

## Installation and Setup

### 1. Install Application Dependencies  
Use the repository’s `requirements.txt`:

cd DataLex 

pip install -r requirements.txt

This installs AutoDDG, profiling utilities, LLM clients, retrieval tools, and core dependencies.

---

## Conda Environment (Recommended for Notebook)

Create an environment:

conda create -n autoddg-geo python=3.10  
conda activate autoddg-geo

Install required Python packages:

pip install pandas numpy openai google-genai
pip install -e .                  # optional: install this repo as a package

For Jupyter Notebook support:

pip install jupyter ipykernel  
python -m ipykernel install --user --name autoddg-geo

These cover all packages needed for the notebook imports (AutoDDG, GeoProfiler, AutoDDG-Geo, OpenAI client, Google GenAI client, BM25, numpy, pandas).

---

## Running the Notebook

conda activate autoddg-geo  
jupyter-notebook

Make sure to set up your API keys before running
Refer notebooks package for initial setup

---

## Repository Structure

```text
DataLex/
├── examples/
│   ├── Centerline.csv
│   ├── CPI_Zones.csv
│   ├── Landmarks_Complaints.csv
│   ├── Parking_Meters_Locations_and_Status.csv
│   └── Parks_Zones.csv
│
├── geo_profiler/
│   ├── profilers/
│   │   ├── geometry_type_profiler.py
│   │   ├── spatial_resolution_profiler.py
│   │   ├── spatial_role_profiler.py
│   │   └── spatial_use_cases_profiler.py
│   │
│   ├── geo_profiler.py
│   ├── models.py
│   └── semantic_parser.py
│
├── llm/
│   ├── prompt_builder.py
│   ├── prompts.yaml
│   └── yaml_prompt_loader.py
│
├── notebooks/
│   └── AutoDDGGeo.ipynb
│
├── autoddg_geo.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Citation  
If referencing this project academically, cite:  
“AutoDDG-Geo: Enhancing AutoDDG for Generating Geo-Spatially Aware Descriptions using LLMs.”

---

## Contributors  
Apoorva Menon • Anuhiya Suresh Babu • Pavan Veeramani  

---

## GitHub Repository  
https://github.com/Apoorva-Menon/DataLex
