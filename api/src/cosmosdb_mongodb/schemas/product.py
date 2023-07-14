import json
from typing import List, Optional
from pydantic import BaseModel

class Product(BaseModel):
    article_id: Optional[str]
    product_code: Optional[str]
    prod_name: str
    product_type_no: Optional[str]
    product_type_name: Optional[str]
    product_group_name: Optional[str]
    graphical_appearance_no: Optional[str]
    graphical_appearance_name: Optional[str]
    colour_group_code: Optional[str]
    colour_group_name: Optional[str]
    perceived_colour_value_id: Optional[str]
    perceived_colour_value_name: Optional[str]
    perceived_colour_master_id: Optional[str]
    perceived_colour_master_name: Optional[str]
    department_no: Optional[str]
    department_name: Optional[str]
    index_code: Optional[str]
    index_name: Optional[str]
    index_group_no: Optional[str]
    index_group_name: Optional[str]
    section_no: Optional[str]
    section_name: Optional[str]
    garment_group_no: Optional[str]
    garment_group_name: Optional[str]
    detail_desc: Optional[str]
    image_path: Optional[str]
    vectorContent: Optional[List[float]]

    def to_dict(self):
        # Convert the Product object to a dictionary
        product_dict = {
            "article_id": self.article_id,
            "product_code": self.product_code,
            "prod_name": self.prod_name,
            "product_type_no": self.product_type_no,
            "product_type_name": self.product_type_name,
            "product_group_name": self.product_group_name,
            "graphical_appearance_no": self.graphical_appearance_no,
            "graphical_appearance_name": self.graphical_appearance_name,
            "colour_group_code": self.colour_group_code,
            "colour_group_name": self.colour_group_name,
            "perceived_colour_value_id": self.perceived_colour_value_id,
            "perceived_colour_value_name": self.perceived_colour_value_name,
            "perceived_colour_master_id": self.perceived_colour_master_id,
            "perceived_colour_master_name": self.perceived_colour_master_name,
            "department_no": self.department_no,
            "department_name": self.department_name,
            "index_code": self.index_code,
            "index_name": self.index_name,
            "index_group_no": self.index_group_no,
            "index_group_name": self.index_group_name,
            "section_no": self.section_no,
            "section_name": self.section_name,
            "garment_group_no": self.garment_group_no,
            "garment_group_name": self.garment_group_name,
            "detail_desc": self.detail_desc,
            "image_path": self.image_path,
            "vectorContent": self.vectorContent
        }

        return product_dict
    
    def to_json(self):
        json_doc = json.dumps(self.to_dict())
        return json_doc