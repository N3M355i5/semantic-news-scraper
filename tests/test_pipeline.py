from pathlib import Path

from pipeline.company_pipeline import CompanyPipeline


pipeline = CompanyPipeline()

pipeline.run(
    Path("data/semantic_index.json")
)