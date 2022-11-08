from IPython.display import SVG

BIOME_ICON_MAP_D2 = {
    "root:engineered": "engineered",
}

BIOME_ICON_MAP_D3 = {
    "root:engineered:wastewater": "wastewater",
    "root:environmental:air": "air",
    "root:host-associated:amphibia": "amphibian",
    "root:host-associated:arthropoda": "arthropoda",
    "root:host-associated:fish": "fish",
    "root:host-associated:human": "human_host",
    "root:host-associated:insecta": "insect",
    "root:host-associated:mammals": "mammals",
    "root:host-associated:mollusca": "mollusca",
    "root:host-associated:plants": "plant",
    "root:host-associated:porifera": "porifera",
}

BIOME_ICON_MAP_D4 = {
    "root:environmental:aquatic:freshwater": "freshwater",
    "root:environmental:aquatic:marine": "marine",
    "root:environmental:aquatic:thermal springs": "hotspring",
    "root:environmental:terrestrial:soil": "soil",
    "root:environmental:terrestrial:volcanic": "vulcano",
    "root:host-associated:human:digestive system": "gut",
    "root:host-associated:human:skin": "skin",
}

BIOME_ICON_MAP_D5 = {
    "root:environmental:aquatic:freshwater:drinking water": "drinking_water",
    "root:environmental:aquatic:freshwater:groundwater": "groundwater",
    "root:environmental:aquatic:freshwater:ice": "ice",
    "root:environmental:aquatic:freshwater:lake": "lake",
    "root:environmental:aquatic:freshwater:lotic": "river",
    "root:environmental:aquatic:marine:hydrothermal vents": "hydrothermal_vents",
    "root:environmental:terrestrial:soil:wetlands": "wetlands",
    "root:host-associated:human:digestive system:oral": "mouth",
    "root:host-associated:human:respiratory system:pulmonary system": "lung",
    "root:host-associated:mammals:nervous system:brain": "brain",
}

BIOME_ICON_MAP_D6 = {
    "root:environmental:aquatic:freshwater:groundwater:cave water": "cave",
    "root:environmental:aquatic:freshwater:ice:glacier": "glacier",
    "root:environmental:terrestrial:soil:grasslands": "grassland",
    "root:environmental:terrestrial:soil:loam:forest soil": "forest",
    "root:environmental:terrestrial:soil:sand:desert": "desert",
}


def biome_icon(lineage):
    """Obtain the biome SVG icon for the lineage

    :param lineage: the biome lineage
    """
    if not lineage:
        return

    lineage_list = [el.lower() for el in lineage.split(":")]

    lineage_D2 = ":".join(lineage_list[0:2])
    lineage_D3 = ":".join(lineage_list[0:3])
    lineage_D4 = ":".join(lineage_list[0:4])
    lineage_D5 = ":".join(lineage_list[0:5])
    lineage_D6 = ":".join(lineage_list[0:6])

    biome = (
        BIOME_ICON_MAP_D6.get(lineage_D6)
        or BIOME_ICON_MAP_D5.get(lineage_D5)
        or BIOME_ICON_MAP_D4.get(lineage_D4)
        or BIOME_ICON_MAP_D3.get(lineage_D3)
        or BIOME_ICON_MAP_D2.get(lineage_D2)
        or "default"
    )
    
    # TODO: fix relative path issue
    return SVG(filename=f"../_resources/biome_icons/biome_{biome}.svg")
