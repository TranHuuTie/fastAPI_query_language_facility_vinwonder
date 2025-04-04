from fastapi import FastAPI, Query
from enum import Enum
import pandas as pd

app = FastAPI()

# Load dữ liệu từ file
df = pd.read_excel("/home/tiennh/FastAPI_product_vinwonder/Data_product_vinwonder.xlsx", engine="openpyxl")

# Tạo enum sử dụng tên biến làm input và tên hiển thị là value
class FacilityEnum(str, Enum):
    vinwonders_nha_trang = "vinwonders_nha_trang"
    vinwonders_cua_hoi = "vinwonders_cua_hoi"
    vinpearl_harbour_nha_trang = "vinpearl_harbour_nha_trang"
    cong_vien_grand_park = "cong_vien_grand_park"
    vinwonders_wave_park_water_park = "vinwonders_wave_park_water_park"
    vinke_aquarium_times_city = "vinke_aquarium_times_city"
    vinwonders_nam_hoi_an = "vinwonders_nam_hoi_an"
    grand_world_phu_quoc = "grand_world_phu_quoc"
    vinwonders_phu_quoc = "vinwonders_phu_quoc"
    vinpearl_safari_phu_quoc = "vinpearl_safari_phu_quoc"
    tam_bun_hon_tam = "tam_bun_hon_tam"

# Mapping từ enum key → tên cơ sở thực tế trong Excel
FACILITY_MAP = {
    "vinwonders_nha_trang": 'VinWonders Nha Trang',
    "vinwonders_cua_hoi": 'VinWonders Cửa Hội',
    "vinpearl_harbour_nha_trang": 'Vinpearl Harbour Nha Trang',
    "cong_vien_grand_park": 'Công viên Grand Park',
    "vinwonders_wave_park_water_park": 'VinWonders Wave Park & Water Park',
    "vinke_aquarium_times_city": 'VinKE & Aquarium Times City',
    "vinwonders_nam_hoi_an": 'VinWonders Nam Hội An',
    "grand_world_phu_quoc": 'Grand World Phú Quốc',
    "vinwonders_phu_quoc": 'VinWonders Phú Quốc',
    "vinpearl_safari_phu_quoc": 'Vinpearl Safari Phú Quốc',
    "tam_bun_hon_tam": 'Tắm bùn Hòn Tằm'
}

class Language(str, Enum):
    vi = "vi"
    en = "en"
    zh = "zh"
    ko = "ko"

LANGUAGE_MAP = {
    "vi": ["name_vi", "description_vi", "info_vi", "image_link_vi"],
    "en": ["name_en", "description_en", "info_en", "image_link_en"],
    "zh": ["name_zh", "description_zh", "info_zh", "image_link_zh"],
    "ko": ["name_ko", "description_ko", "info_ko", "image_link_ko"]
}

def clean_dataframe(df):
    df.replace([float('inf'), float('-inf'), float('nan')], None, inplace=True)
    return df

@app.get("/get_data/")
def get_data(
    facility: list[FacilityEnum] = Query(..., description="Tên các cơ sở"),
    language: Language = Query("vi", description="Chọn ngôn ngữ : vi, en, zh, ko")
):
    # Map enum keys sang tên thật trong dữ liệu
    facility_names = [FACILITY_MAP[f.value] for f in co_so]

    # Lọc dữ liệu
    filtered_df = df[df["facility"].isin(facility_names)]

    if filtered_df.empty:
        return {"message": "Không tìm thấy dữ liệu cho các cơ sở đã chọn."}

    filtered_df = clean_dataframe(filtered_df)

    columns_to_remove = []
    for lang, cols in LANGUAGE_MAP.items():
        if lang != language:
            columns_to_remove.extend(cols)

    columns_to_keep = [col for col in df.columns if col not in columns_to_remove]
    result = filtered_df[columns_to_keep].to_dict(orient="records")

    return {"data": result}
