#!/usr/bin/env python3
"""
pH Calculator for Natural Cosmetic Formulas
Calculadora de pH para Fórmulas Cosméticas Naturales
Auro Labs — formulation tool / herramienta de formulación
"""

import math
import sys
from typing import Optional

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.prompt import Prompt, Confirm
    from rich.text import Text
    from rich import box
    from rich.rule import Rule
except ImportError:
    print("Installing dependencies / Instalando dependencias...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "rich", "--break-system-packages", "-q"])
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.prompt import Prompt, Confirm
    from rich.text import Text
    from rich import box
    from rich.rule import Rule

console = Console()

# ─────────────────────────────────────────────────────────────
# UI Strings
# ─────────────────────────────────────────────────────────────

STRINGS = {
    "en": {
        # startup
        "lang_prompt":        "Select language / Selecciona idioma",
        "lang_choices":       ["en", "es"],
        "lang_default":       "en",
        # header
        "header_title":       "pH Calculator",
        "header_sub":         "Auro Labs · Natural Cosmetic Formulation Tool",
        "header_note":        "Theoretical estimation — always confirm with a calibrated pH meter",
        # main menu
        "menu_title":         "What would you like to do?",
        "menu_1":             "New custom formula",
        "menu_2":             "Preset: Natural deodorant stick",
        "menu_3":             "Preset: Hyaluronic acid serum",
        "menu_4":             "Preset: AHA/BHA exfoliant",
        "menu_5":             "Preset: Facial mist (hydrolat + centella)",
        "menu_6":             "View ingredient database",
        "menu_0":             "Exit",
        "menu_prompt":        "Select an option",
        # formula flow
        "custom_title":       "Custom Formula",
        "water_ph":           "pH of distilled water",
        "water_pct":          "Water percentage in formula (%)",
        "ingr_title":         "Ingredient #{n}",
        "ingr_name":          "  Ingredient name",
        "ingr_hint":          "  Type 'db' to see the ingredient database",
        "ingr_found":         "  ✓ Found:",
        "ingr_use_vals":      "  Use these values?",
        "ingr_pct":           "  Percentage in formula (%)",
        "ingr_pka":           "  pKa value",
        "ingr_type":          "  Type",
        "ingr_type_choices":  ["acid", "base", "neutral", "strong_base"],
        "ingr_type_default":  "neutral",
        "ingr_add_another":   "  Add another ingredient?",
        "ingr_none":          "No active ingredients were added.",
        # adjustor
        "adj_title":          "pH Adjustor",
        "adj_none":           "No adjustor",
        "adj_prompt":         "  Select",
        "adj_pct":            "  Adjustor percentage (%)",
        # preset
        "preset_title":       "Preset",
        "preset_preview":     "Formula preview",
        "preset_confirm":     "Proceed with this formula?",
        "preset_edit":        "Would you like to edit the percentages?",
        "preset_water_ph":    "Distilled water pH",
        "preset_water_pct":   "Water %",
        "preset_adj_pct":     "(adjustor)",
        # result
        "result_title":       "Result",
        "result_ph":          "Estimated pH",
        "result_total":       "Formula total",
        "result_over":        "⚠  Total exceeds 100%. Please adjust your percentages.",
        "result_col_ingr":    "Ingredient",
        "result_col_pct":     "% formula",
        "result_col_pka":     "pKa",
        "result_col_type":    "Type",
        "result_col_ph":      "pH approx.",
        "result_water":       "Distilled water",
        "result_adjustor":    "(adjustor)",
        "result_diag_title":  "Diagnosis & Recommendations",
        "result_meter_note":  "⚡ Always confirm with a calibrated digital pH meter before packaging.",
        "result_zone":        "pH zone",
        "result_diagnosis":   "Diagnosis",
        # db
        "db_title":           "Ingredient Database",
        "db_col_key":         "Key",
        "db_col_name":        "Name",
        "db_col_pka":         "pKa",
        "db_col_type":        "Type",
        # axis
        "axis_acid":          "0 acid",
        "axis_neutral":       "neutral",
        "axis_basic":         "14 basic",
        # types
        "t_acid":             "acid",
        "t_base":             "base",
        "t_neutral":          "neutral",
        "t_strong_base":      "strong base",
        # zones
        "zone_very_acid":     "Extremely acidic",
        "zone_eff_acid":      "Effective acid range",
        "zone_mild_acid":     "Mildly acidic",
        "zone_neutral":       "Neutral-acidic",
        "zone_mild_base":     "Mildly alkaline",
        "zone_alkaline":      "Alkaline",
        "zone_very_base":     "Very alkaline",
        # zone messages
        "msg_very_acid":      "Extremely acidic pH. Risk of severe irritation. Professional use only.",
        "msg_eff_acid":       "Ideal range for AHA/BHA exfoliants (3.2–3.8) and Vitamin C serums (2.5–3.5). Verify this is intentional.",
        "msg_mild_acid":      "Optimal for shampoos, conditioners, and facial cleansers. Compatible with the skin's acid mantle (pH ≈ 5.5).",
        "msg_neutral":        "Suitable for moisturizers, HA serums, toners, and facial mists. Good range for most cosmetics.",
        "msg_mild_base":      "Suitable for natural deodorants with baking soda (7.5–9.0). May irritate sensitive skin.",
        "msg_alkaline":       "Elevated alkalinity. Only suitable for specific deodorant formulas. Consider reducing the alkaline agent.",
        "msg_very_base":      "Dangerously high pH for cosmetic use. Review your formula — may damage the skin barrier.",
        # navigation
        "press_enter":        "\n[dim]Press Enter to return to the menu[/dim]",
        "goodbye":            "\n[gold1]Goodbye — Auro Labs ✨[/gold1]\n",
    },
    "es": {
        # startup
        "lang_prompt":        "Select language / Selecciona idioma",
        "lang_choices":       ["en", "es"],
        "lang_default":       "en",
        # header
        "header_title":       "Calculadora de pH",
        "header_sub":         "Auro Labs · Herramienta de Formulación Cosmética Natural",
        "header_note":        "Estimación teórica — confirma siempre con pHmetro calibrado",
        # main menu
        "menu_title":         "¿Qué quieres hacer?",
        "menu_1":             "Nueva fórmula personalizada",
        "menu_2":             "Preset: Desodorante natural (stick seco)",
        "menu_3":             "Preset: Sérum de ácido hialurónico",
        "menu_4":             "Preset: Exfoliante AHA/BHA",
        "menu_5":             "Preset: Mist facial (hidrolato + centella)",
        "menu_6":             "Ver base de datos de ingredientes",
        "menu_0":             "Salir",
        "menu_prompt":        "Selecciona una opción",
        # formula flow
        "custom_title":       "Fórmula Personalizada",
        "water_ph":           "pH del agua destilada",
        "water_pct":          "Porcentaje de agua en la fórmula (%)",
        "ingr_title":         "Ingrediente #{n}",
        "ingr_name":          "  Nombre del ingrediente",
        "ingr_hint":          "  Escribe 'db' para ver la base de datos de ingredientes",
        "ingr_found":         "  ✓ Encontrado:",
        "ingr_use_vals":      "  ¿Usar estos valores?",
        "ingr_pct":           "  Porcentaje en fórmula (%)",
        "ingr_pka":           "  Valor pKa",
        "ingr_type":          "  Tipo",
        "ingr_type_choices":  ["acido", "base", "neutro", "base_fuerte"],
        "ingr_type_default":  "neutro",
        "ingr_add_another":   "  ¿Agregar otro ingrediente?",
        "ingr_none":          "No se ingresaron ingredientes activos.",
        # adjustor
        "adj_title":          "Ajustador de pH",
        "adj_none":           "Sin ajustador",
        "adj_prompt":         "  Selecciona",
        "adj_pct":            "  Porcentaje del ajustador (%)",
        # preset
        "preset_title":       "Preset",
        "preset_preview":     "Vista previa de la fórmula",
        "preset_confirm":     "¿Continuar con esta fórmula?",
        "preset_edit":        "¿Deseas editar los porcentajes?",
        "preset_water_ph":    "pH agua destilada",
        "preset_water_pct":   "% agua",
        "preset_adj_pct":     "(ajustador)",
        # result
        "result_title":       "Resultado",
        "result_ph":          "pH estimado",
        "result_total":       "Total fórmula",
        "result_over":        "⚠  La suma supera 100%. Ajusta los porcentajes.",
        "result_col_ingr":    "Ingrediente",
        "result_col_pct":     "% fórmula",
        "result_col_pka":     "pKa",
        "result_col_type":    "Tipo",
        "result_col_ph":      "pH aprox.",
        "result_water":       "Agua destilada",
        "result_adjustor":    "(ajustador)",
        "result_diag_title":  "Diagnóstico y Recomendaciones",
        "result_meter_note":  "⚡ Confirma siempre con pHmetro digital calibrado antes de envasar.",
        "result_zone":        "Zona de pH",
        "result_diagnosis":   "Diagnóstico",
        # db
        "db_title":           "Base de Datos de Ingredientes",
        "db_col_key":         "Clave",
        "db_col_name":        "Nombre",
        "db_col_pka":         "pKa",
        "db_col_type":        "Tipo",
        # axis
        "axis_acid":          "0 ácido",
        "axis_neutral":       "neutro",
        "axis_basic":         "14 básico",
        # types
        "t_acid":             "ácido",
        "t_base":             "base",
        "t_neutral":          "neutro",
        "t_strong_base":      "base fuerte",
        # zones
        "zone_very_acid":     "Muy ácido",
        "zone_eff_acid":      "Ácido efectivo",
        "zone_mild_acid":     "Ligeramente ácido",
        "zone_neutral":       "Neutro-ácido",
        "zone_mild_base":     "Ligeramente básico",
        "zone_alkaline":      "Alcalino",
        "zone_very_base":     "Muy alcalino",
        # zone messages
        "msg_very_acid":      "pH extremadamente ácido. Riesgo de irritación severa. Solo para uso profesional controlado.",
        "msg_eff_acid":       "Rango ideal para exfoliantes AHA/BHA (3.2–3.8) y sérum vitamina C (2.5–3.5). Verifica que sea intencional.",
        "msg_mild_acid":      "Óptimo para champú, acondicionador y limpiadores faciales. Compatible con el manto ácido cutáneo (pH ≈ 5.5).",
        "msg_neutral":        "Adecuado para cremas hidratantes, sérums de ácido hialurónico, tónicos y mists. Buen rango para la mayoría de cosméticos.",
        "msg_mild_base":      "Zona adecuada para desodorantes naturales con bicarbonato (7.5–9.0). Puede ser irritante para piel muy sensible.",
        "msg_alkaline":       "Alcalinidad elevada. Solo apto para fórmulas específicas de desodorantes. Considera reducir el agente alcalino.",
        "msg_very_base":      "pH peligrosamente alto para uso cosmético. Revisa la fórmula — puede dañar la barrera cutánea.",
        # navigation
        "press_enter":        "\n[dim]Presiona Enter para volver al menú[/dim]",
        "goodbye":            "\n[gold1]Hasta la próxima — Auro Labs ✨[/gold1]\n",
    },
}

LANG = "en"

def t(key: str, **kwargs) -> str:
    s = STRINGS[LANG].get(key, STRINGS["en"].get(key, key))
    return s.format(**kwargs) if kwargs else s

# ─────────────────────────────────────────────────────────────
# Ingredient Database
# ─────────────────────────────────────────────────────────────

INGREDIENTS_DB = {
    # ── ACIDS ──────────────────────────────────────────────────────────────────
    "citric acid":          {"name_en":"Citric acid",                  "name_es":"Ácido cítrico",               "pka":3.13,  "type":"acid",       "cat":"acids"},
    "lactic acid":          {"name_en":"Lactic acid",                  "name_es":"Ácido láctico",               "pka":3.86,  "type":"acid",       "cat":"acids"},
    "salicylic acid":       {"name_en":"Salicylic acid",               "name_es":"Ácido salicílico",            "pka":2.97,  "type":"acid",       "cat":"acids"},
    "glycolic acid":        {"name_en":"Glycolic acid",                "name_es":"Ácido glicólico",             "pka":3.83,  "type":"acid",       "cat":"acids"},
    "mandelic acid":        {"name_en":"Mandelic acid",                "name_es":"Ácido mandélico",             "pka":3.37,  "type":"acid",       "cat":"acids"},
    "malic acid":           {"name_en":"Malic acid",                   "name_es":"Ácido málico",                "pka":3.40,  "type":"acid",       "cat":"acids"},
    "tartaric acid":        {"name_en":"Tartaric acid",                "name_es":"Ácido tartárico",             "pka":2.98,  "type":"acid",       "cat":"acids"},
    "ascorbic acid":        {"name_en":"Ascorbic acid (Vitamin C)",    "name_es":"Ácido ascórbico (Vitamina C)","pka":4.17,  "type":"acid",       "cat":"acids"},
    "ferulic acid":         {"name_en":"Ferulic acid",                 "name_es":"Ácido ferúlico",              "pka":4.40,  "type":"acid",       "cat":"acids"},
    "kojic acid":           {"name_en":"Kojic acid",                   "name_es":"Ácido kójico",                "pka":7.90,  "type":"acid",       "cat":"acids"},
    "azelaic acid":         {"name_en":"Azelaic acid",                 "name_es":"Ácido azelaico",              "pka":4.55,  "type":"acid",       "cat":"acids"},
    "benzoic acid":         {"name_en":"Benzoic acid",                 "name_es":"Ácido benzoico",              "pka":4.20,  "type":"acid",       "cat":"acids"},
    "sorbic acid":          {"name_en":"Sorbic acid",                  "name_es":"Ácido sórbico",               "pka":4.76,  "type":"acid",       "cat":"acids"},
    "silicic acid":         {"name_en":"Silicic acid",                 "name_es":"Ácido silícico",              "pka":9.90,  "type":"neutral",    "cat":"acids"},
    "tranexamic acid":      {"name_en":"Tranexamic acid",              "name_es":"Ácido tranexámico",           "pka":4.30,  "type":"acid",       "cat":"acids"},
    "phytic acid":          {"name_en":"Phytic acid",                  "name_es":"Ácido fítico",                "pka":1.90,  "type":"acid",       "cat":"acids"},

    # ── BASES / ALKALIZERS ─────────────────────────────────────────────────────
    "baking soda":          {"name_en":"Baking soda",                  "name_es":"Bicarbonato de sodio",        "pka":10.33, "type":"base",       "cat":"bases"},
    "tea":                  {"name_en":"Triethanolamine (TEA)",        "name_es":"Trietanolamina (TEA)",        "pka":8.15,  "type":"base",       "cat":"bases"},
    "arginine":             {"name_en":"Arginine",                     "name_es":"Arginina",                    "pka":12.50, "type":"base",       "cat":"bases"},
    "naoh":                 {"name_en":"NaOH (caustic soda)",          "name_es":"NaOH (sosa cáustica)",        "pka":14.0,  "type":"strong_base","cat":"bases"},
    "koh":                  {"name_en":"KOH (potassium hydroxide)",    "name_es":"KOH (hidróxido de potasio)",  "pka":14.0,  "type":"strong_base","cat":"bases"},
    "sodium carbonate":     {"name_en":"Sodium carbonate (soda ash)",  "name_es":"Carbonato de sodio",          "pka":10.33, "type":"base",       "cat":"bases"},
    "ammonium bicarbonate": {"name_en":"Ammonium bicarbonate",         "name_es":"Bicarbonato de amonio",       "pka":9.25,  "type":"base",       "cat":"bases"},
    "sodium hydroxide":     {"name_en":"Sodium hydroxide lye",         "name_es":"Lejía de sosa",               "pka":14.0,  "type":"strong_base","cat":"bases"},
    "lysine":               {"name_en":"Lysine",                       "name_es":"Lisina",                      "pka":10.53, "type":"base",       "cat":"bases"},

    # ── HUMECTANTS / WATER-PHASE ACTIVES ──────────────────────────────────────
    "glycerin":             {"name_en":"Glycerin (vegetable)",         "name_es":"Glicerina vegetal",           "pka":14.0,  "type":"neutral",    "cat":"humectants"},
    "hyaluronic acid":      {"name_en":"Sodium Hyaluronate (HA)",      "name_es":"Hialuronato de sodio (AH)",   "pka":7.0,   "type":"neutral",    "cat":"humectants"},
    "ha low":               {"name_en":"HA low molecular weight",      "name_es":"AH bajo peso molecular",      "pka":7.0,   "type":"neutral",    "cat":"humectants"},
    "ha high":              {"name_en":"HA high molecular weight",     "name_es":"AH alto peso molecular",      "pka":7.0,   "type":"neutral",    "cat":"humectants"},
    "panthenol":            {"name_en":"Panthenol (Vitamin B5)",       "name_es":"Pantenol (Vitamina B5)",      "pka":7.0,   "type":"neutral",    "cat":"humectants"},
    "pentylene glycol":     {"name_en":"Pentylene glycol",             "name_es":"Pentilen glicol",             "pka":7.0,   "type":"neutral",    "cat":"humectants"},
    "propylene glycol":     {"name_en":"Propylene glycol",             "name_es":"Propilenglicol",              "pka":7.0,   "type":"neutral",    "cat":"humectants"},
    "butylene glycol":      {"name_en":"1,3-Butylene glycol",          "name_es":"Butilenglicol",               "pka":7.0,   "type":"neutral",    "cat":"humectants"},
    "urea":                 {"name_en":"Urea",                         "name_es":"Urea",                        "pka":0.18,  "type":"neutral",    "cat":"humectants"},
    "sorbitol":             {"name_en":"Sorbitol",                     "name_es":"Sorbitol",                    "pka":13.6,  "type":"neutral",    "cat":"humectants"},
    "betaine":              {"name_en":"Betaine (natural)",            "name_es":"Betaína (natural)",           "pka":7.0,   "type":"neutral",    "cat":"humectants"},
    "sodium pca":           {"name_en":"Sodium PCA",                   "name_es":"Sodio PCA",                   "pka":7.0,   "type":"neutral",    "cat":"humectants"},
    "inositol":             {"name_en":"Inositol",                     "name_es":"Inositol",                    "pka":7.0,   "type":"neutral",    "cat":"humectants"},

    # ── VEGETABLE OILS ────────────────────────────────────────────────────────
    "coconut oil":          {"name_en":"Coconut oil",                  "name_es":"Aceite de coco",              "pka":7.0,   "type":"neutral",    "cat":"oils"},
    "jojoba oil":           {"name_en":"Jojoba oil",                   "name_es":"Aceite de jojoba",            "pka":7.0,   "type":"neutral",    "cat":"oils"},
    "rosehip oil":          {"name_en":"Rosehip oil",                  "name_es":"Aceite de rosa mosqueta",     "pka":7.0,   "type":"neutral",    "cat":"oils"},
    "argan oil":            {"name_en":"Argan oil",                    "name_es":"Aceite de argán",             "pka":7.0,   "type":"neutral",    "cat":"oils"},
    "sweet almond oil":     {"name_en":"Sweet almond oil",             "name_es":"Aceite de almendras dulces",  "pka":7.0,   "type":"neutral",    "cat":"oils"},
    "castor oil":           {"name_en":"Castor oil",                   "name_es":"Aceite de ricino",            "pka":7.0,   "type":"neutral",    "cat":"oils"},
    "sunflower oil":        {"name_en":"Sunflower oil",                "name_es":"Aceite de girasol",           "pka":7.0,   "type":"neutral",    "cat":"oils"},
    "olive oil":            {"name_en":"Olive oil",                    "name_es":"Aceite de oliva",             "pka":7.0,   "type":"neutral",    "cat":"oils"},
    "hemp seed oil":        {"name_en":"Hemp seed oil",                "name_es":"Aceite de semilla de cáñamo", "pka":7.0,   "type":"neutral",    "cat":"oils"},
    "calendula oil":        {"name_en":"Calendula macerate oil",       "name_es":"Aceite macerado de caléndula","pka":7.0,   "type":"neutral",    "cat":"oils"},
    "sea buckthorn oil":    {"name_en":"Sea buckthorn oil",            "name_es":"Aceite de espino amarillo",   "pka":7.0,   "type":"neutral",    "cat":"oils"},
    "evening primrose oil": {"name_en":"Evening primrose oil",         "name_es":"Aceite de onagra",            "pka":7.0,   "type":"neutral",    "cat":"oils"},
    "avocado oil":          {"name_en":"Avocado oil",                  "name_es":"Aceite de aguacate",          "pka":7.0,   "type":"neutral",    "cat":"oils"},
    "marula oil":           {"name_en":"Marula oil",                   "name_es":"Aceite de marula",            "pka":7.0,   "type":"neutral",    "cat":"oils"},
    "squalane":             {"name_en":"Squalane (olive)",             "name_es":"Escualano (oliva)",           "pka":7.0,   "type":"neutral",    "cat":"oils"},
    "baobab oil":           {"name_en":"Baobab oil",                   "name_es":"Aceite de baobab",            "pka":7.0,   "type":"neutral",    "cat":"oils"},
    "prickly pear oil":     {"name_en":"Prickly pear seed oil",        "name_es":"Aceite de semilla de higo chumbo","pka":7.0,"type":"neutral",  "cat":"oils"},
    "black seed oil":       {"name_en":"Black seed oil (nigella)",     "name_es":"Aceite de comino negro",      "pka":7.0,   "type":"neutral",    "cat":"oils"},
    "tamanu oil":           {"name_en":"Tamanu oil",                   "name_es":"Aceite de tamanu",            "pka":7.0,   "type":"neutral",    "cat":"oils"},
    "neem oil":             {"name_en":"Neem oil",                     "name_es":"Aceite de neem",              "pka":7.0,   "type":"neutral",    "cat":"oils"},
    "meadowfoam oil":       {"name_en":"Meadowfoam seed oil",          "name_es":"Aceite de meadowfoam",        "pka":7.0,   "type":"neutral",    "cat":"oils"},
    "borage oil":           {"name_en":"Borage oil",                   "name_es":"Aceite de borraja",           "pka":7.0,   "type":"neutral",    "cat":"oils"},
    "sultry castor":        {"name_en":"Sulfated castor oil",          "name_es":"Aceite de ricino sulfatado",  "pka":7.0,   "type":"neutral",    "cat":"oils"},

    # ── BUTTERS ───────────────────────────────────────────────────────────────
    "shea butter":          {"name_en":"Shea butter",                  "name_es":"Manteca de karité",           "pka":7.0,   "type":"neutral",    "cat":"butters"},
    "cocoa butter":         {"name_en":"Cocoa butter",                 "name_es":"Manteca de cacao",            "pka":7.0,   "type":"neutral",    "cat":"butters"},
    "mango butter":         {"name_en":"Mango butter",                 "name_es":"Manteca de mango",            "pka":7.0,   "type":"neutral",    "cat":"butters"},
    "kokum butter":         {"name_en":"Kokum butter",                 "name_es":"Manteca de kokum",            "pka":7.0,   "type":"neutral",    "cat":"butters"},
    "cupuacu butter":       {"name_en":"Cupuaçu butter",               "name_es":"Manteca de cupuazú",          "pka":7.0,   "type":"neutral",    "cat":"butters"},
    "murumuru butter":      {"name_en":"Murumuru butter",              "name_es":"Manteca de murumuru",         "pka":7.0,   "type":"neutral",    "cat":"butters"},
    "tucuma butter":        {"name_en":"Tucuma butter",                "name_es":"Manteca de tucumá",           "pka":7.0,   "type":"neutral",    "cat":"butters"},
    "illipe butter":        {"name_en":"Illipe butter",                "name_es":"Manteca de illipe",           "pka":7.0,   "type":"neutral",    "cat":"butters"},
    "sal butter":           {"name_en":"Sal butter",                   "name_es":"Manteca de sal",              "pka":7.0,   "type":"neutral",    "cat":"butters"},

    # ── WAXES ─────────────────────────────────────────────────────────────────
    "beeswax":              {"name_en":"Beeswax",                      "name_es":"Cera de abeja",               "pka":7.0,   "type":"neutral",    "cat":"waxes"},
    "candelilla wax":       {"name_en":"Candelilla wax",               "name_es":"Cera de candelilla",          "pka":7.0,   "type":"neutral",    "cat":"waxes"},
    "carnauba wax":         {"name_en":"Carnauba wax",                 "name_es":"Cera de carnauba",            "pka":7.0,   "type":"neutral",    "cat":"waxes"},
    "rice bran wax":        {"name_en":"Rice bran wax",                "name_es":"Cera de salvado de arroz",    "pka":7.0,   "type":"neutral",    "cat":"waxes"},
    "japan wax":            {"name_en":"Japan wax",                    "name_es":"Cera de Japón",               "pka":7.0,   "type":"neutral",    "cat":"waxes"},
    "myrica wax":           {"name_en":"Myrica (bayberry) wax",        "name_es":"Cera de mirto",               "pka":7.0,   "type":"neutral",    "cat":"waxes"},

    # ── EMULSIFIERS ──────────────────────────────────────────────────────────
    "emulsifying wax":      {"name_en":"Emulsifying wax NF",           "name_es":"Cera emulsionante NF",        "pka":7.0,   "type":"neutral",    "cat":"emulsifiers"},
    "olivem 1000":          {"name_en":"Olivem 1000",                  "name_es":"Olivem 1000",                 "pka":7.0,   "type":"neutral",    "cat":"emulsifiers"},
    "olivem 300":           {"name_en":"Olivem 300",                   "name_es":"Olivem 300",                  "pka":7.0,   "type":"neutral",    "cat":"emulsifiers"},
    "lecithin":             {"name_en":"Sunflower lecithin",           "name_es":"Lecitina de girasol",         "pka":7.0,   "type":"neutral",    "cat":"emulsifiers"},
    "cetearyl alcohol":     {"name_en":"Cetearyl alcohol",             "name_es":"Alcohol cetearílico",         "pka":7.0,   "type":"neutral",    "cat":"emulsifiers"},
    "glyceryl stearate":    {"name_en":"Glyceryl stearate",            "name_es":"Gliceril estearato",          "pka":7.0,   "type":"neutral",    "cat":"emulsifiers"},
    "montanov 68":          {"name_en":"Montanov 68 (cetearyl glucoside)","name_es":"Montanov 68",              "pka":7.0,   "type":"neutral",    "cat":"emulsifiers"},
    "sucrose esters":       {"name_en":"Sucrose esters",               "name_es":"Ésteres de sacarosa",         "pka":7.0,   "type":"neutral",    "cat":"emulsifiers"},
    "polysorbate 20":       {"name_en":"Polysorbate 20",               "name_es":"Polisorbato 20",              "pka":7.0,   "type":"neutral",    "cat":"emulsifiers"},
    "polysorbate 80":       {"name_en":"Polysorbate 80",               "name_es":"Polisorbato 80",              "pka":7.0,   "type":"neutral",    "cat":"emulsifiers"},
    "solubol":              {"name_en":"Solubol (dispersant)",         "name_es":"Solubol (dispersante)",       "pka":7.0,   "type":"neutral",    "cat":"emulsifiers"},

    # ── SURFACTANTS / TENSIOACTIVES ───────────────────────────────────────────
    "slsa":                 {"name_en":"SLSA (sodium lauryl sulfoacetate)","name_es":"SLSA (sulfoacetato de sodio)","pka":7.0,"type":"neutral",   "cat":"surfactants"},
    "sles":                 {"name_en":"SLES (sodium laureth sulfate)","name_es":"SLES (lauréter sulfato sodio)","pka":7.0,  "type":"neutral",    "cat":"surfactants"},
    "scs":                  {"name_en":"Sodium coco sulfate (SCS)",    "name_es":"Sulfato de coco (SCS)",       "pka":7.0,   "type":"neutral",    "cat":"surfactants"},
    "coco glucoside":       {"name_en":"Coco glucoside",               "name_es":"Glucósido de coco",           "pka":7.0,   "type":"neutral",    "cat":"surfactants"},
    "decyl glucoside":      {"name_en":"Decyl glucoside",              "name_es":"Glucósido de decilo",         "pka":7.0,   "type":"neutral",    "cat":"surfactants"},
    "caprylyl glucoside":   {"name_en":"Caprylyl/Capryl glucoside",    "name_es":"Glucósido caprílico",         "pka":7.0,   "type":"neutral",    "cat":"surfactants"},
    "betaine surf":         {"name_en":"Cocamidopropyl betaine",       "name_es":"Cocamidopropil betaína",      "pka":7.0,   "type":"neutral",    "cat":"surfactants"},
    "sodium cocoyl isethionate":{"name_en":"SCI (sodium cocoyl isethionate)","name_es":"SCI (isethionato sódico)","pka":7.0,"type":"neutral",    "cat":"surfactants"},
    "lauryl glucoside":     {"name_en":"Lauryl glucoside",             "name_es":"Glucósido de laurilo",        "pka":7.0,   "type":"neutral",    "cat":"surfactants"},

    # ── PRESERVATIVES ────────────────────────────────────────────────────────
    "leucidal":             {"name_en":"Leucidal (radish ferment)",    "name_es":"Leucidal (fermento de rábano)","pka":7.0,  "type":"neutral",    "cat":"preservatives"},
    "geogard":              {"name_en":"Geogard ECT",                  "name_es":"Geogard ECT",                 "pka":4.50,  "type":"acid",       "cat":"preservatives"},
    "naticide":             {"name_en":"Naticide (fragrance preserv.)","name_es":"Naticide",                    "pka":5.0,   "type":"neutral",    "cat":"preservatives"},
    "euxyl pe 9010":        {"name_en":"Euxyl PE 9010",                "name_es":"Euxyl PE 9010",               "pka":7.0,   "type":"neutral",    "cat":"preservatives"},
    "dermosoft":            {"name_en":"Dermosoft decalact",           "name_es":"Dermosoft decalact",          "pka":3.80,  "type":"acid",       "cat":"preservatives"},
    "vitamin e":            {"name_en":"Vitamin E (tocopherol)",       "name_es":"Vitamina E (tocoferol)",      "pka":7.0,   "type":"neutral",    "cat":"preservatives"},
    "rosemary extract":     {"name_en":"Rosemary antioxidant (CO2)",   "name_es":"Extracto de romero (CO2)",    "pka":7.0,   "type":"neutral",    "cat":"preservatives"},
    "grapefruit seed ext":  {"name_en":"Grapefruit seed extract",      "name_es":"Extracto semilla de pomelo",  "pka":7.0,   "type":"neutral",    "cat":"preservatives"},
    "phenoxyethanol":       {"name_en":"Phenoxyethanol",               "name_es":"Fenoxietanol",                "pka":9.99,  "type":"neutral",    "cat":"preservatives"},

    # ── ACTIVE INGREDIENTS ───────────────────────────────────────────────────
    "niacinamide":          {"name_en":"Niacinamide (Vitamin B3)",     "name_es":"Niacinamida (Vitamina B3)",   "pka":7.20,  "type":"neutral",    "cat":"actives"},
    "retinol":              {"name_en":"Retinol (Vitamin A)",          "name_es":"Retinol (Vitamina A)",        "pka":7.0,   "type":"neutral",    "cat":"actives"},
    "coenzyme q10":         {"name_en":"Coenzyme Q10",                 "name_es":"Coenzima Q10",                "pka":7.0,   "type":"neutral",    "cat":"actives"},
    "resveratrol":          {"name_en":"Resveratrol",                  "name_es":"Resveratrol",                 "pka":9.10,  "type":"neutral",    "cat":"actives"},
    "ceramides":            {"name_en":"Ceramides",                    "name_es":"Ceramidas",                   "pka":7.0,   "type":"neutral",    "cat":"actives"},
    "collagen hydrolyzed":  {"name_en":"Hydrolyzed collagen",          "name_es":"Colágeno hidrolizado",        "pka":7.0,   "type":"neutral",    "cat":"actives"},
    "silk amino acids":     {"name_en":"Silk amino acids",             "name_es":"Aminoácidos de seda",         "pka":7.0,   "type":"neutral",    "cat":"actives"},
    "allantoin":            {"name_en":"Allantoin",                    "name_es":"Alantoína",                   "pka":7.0,   "type":"neutral",    "cat":"actives"},
    "bisabolol":            {"name_en":"Alpha-bisabolol",              "name_es":"Alfa-bisabolol",              "pka":7.0,   "type":"neutral",    "cat":"actives"},
    "centella asiatica":    {"name_en":"Centella asiatica extract",    "name_es":"Extracto centella asiática",  "pka":7.0,   "type":"neutral",    "cat":"actives"},
    "aloe vera":            {"name_en":"Aloe vera extract",            "name_es":"Extracto de aloe vera",       "pka":7.0,   "type":"neutral",    "cat":"actives"},
    "green tea extract":    {"name_en":"Green tea extract (EGCG)",     "name_es":"Extracto de té verde (EGCG)", "pka":7.0,   "type":"neutral",    "cat":"actives"},
    "licorice extract":     {"name_en":"Licorice root extract",        "name_es":"Extracto de regaliz",         "pka":7.0,   "type":"neutral",    "cat":"actives"},
    "bakuchiol":            {"name_en":"Bakuchiol",                    "name_es":"Bakuchiol",                   "pka":7.0,   "type":"neutral",    "cat":"actives"},
    "caffeine":             {"name_en":"Caffeine",                     "name_es":"Cafeína",                     "pka":10.4,  "type":"neutral",    "cat":"actives"},
    "colloidal oat":        {"name_en":"Colloidal oatmeal",            "name_es":"Avena coloidal",              "pka":7.0,   "type":"neutral",    "cat":"actives"},
    "sea kelp":             {"name_en":"Sea kelp extract",             "name_es":"Extracto de alga kelp",       "pka":7.0,   "type":"neutral",    "cat":"actives"},
    "spirulina":            {"name_en":"Spirulina powder",             "name_es":"Espirulina en polvo",         "pka":7.0,   "type":"neutral",    "cat":"actives"},
    "turmeric extract":     {"name_en":"Turmeric extract",             "name_es":"Extracto de cúrcuma",         "pka":7.0,   "type":"neutral",    "cat":"actives"},
    "ginger extract":       {"name_en":"Ginger root extract",          "name_es":"Extracto de jengibre",        "pka":7.0,   "type":"neutral",    "cat":"actives"},
    "madecassoside":        {"name_en":"Madecassoside",                "name_es":"Madecassósido",               "pka":7.0,   "type":"neutral",    "cat":"actives"},
    "beta glucan":          {"name_en":"Beta-glucan (oat/yeast)",      "name_es":"Beta-glucano (avena)",        "pka":7.0,   "type":"neutral",    "cat":"actives"},
    "epidermal growth":     {"name_en":"EGF (plant growth factor)",    "name_es":"Factor de crecimiento EGF",   "pka":7.0,   "type":"neutral",    "cat":"actives"},
    "peptides":             {"name_en":"Matrixyl 3000 / peptide blend","name_es":"Matrixyl 3000 / mezcla péptidos","pka":7.0,"type":"neutral",   "cat":"actives"},

    # ── CLAYS & MINERALS ─────────────────────────────────────────────────────
    "kaolin":               {"name_en":"Kaolin white clay",            "name_es":"Arcilla blanca caolín",       "pka":7.0,   "type":"neutral",    "cat":"clays"},
    "bentonite":            {"name_en":"Bentonite clay",               "name_es":"Arcilla bentonita",           "pka":8.50,  "type":"base",       "cat":"clays"},
    "green clay":           {"name_en":"Green illite clay",            "name_es":"Arcilla verde illita",        "pka":7.50,  "type":"neutral",    "cat":"clays"},
    "pink clay":            {"name_en":"Pink (rose) clay",             "name_es":"Arcilla rosa",                "pka":7.0,   "type":"neutral",    "cat":"clays"},
    "red clay":             {"name_en":"Red clay",                     "name_es":"Arcilla roja",                "pka":7.0,   "type":"neutral",    "cat":"clays"},
    "yellow clay":          {"name_en":"Yellow clay",                  "name_es":"Arcilla amarilla",            "pka":7.0,   "type":"neutral",    "cat":"clays"},
    "rhassoul":             {"name_en":"Rhassoul (ghassoul) clay",     "name_es":"Arcilla rhassoul (ghassoul)", "pka":8.0,   "type":"base",       "cat":"clays"},
    "dead sea salt":        {"name_en":"Dead Sea salt",                "name_es":"Sal del Mar Muerto",          "pka":7.0,   "type":"neutral",    "cat":"clays"},
    "sea salt":             {"name_en":"Sea salt",                     "name_es":"Sal marina",                  "pka":7.0,   "type":"neutral",    "cat":"clays"},
    "epsom salt":           {"name_en":"Epsom salt (MgSO4)",           "name_es":"Sal de Epsom (MgSO4)",        "pka":7.0,   "type":"neutral",    "cat":"clays"},
    "zinc oxide":           {"name_en":"Zinc oxide",                   "name_es":"Óxido de zinc",               "pka":8.90,  "type":"base",       "cat":"clays"},

    # ── HYDROLATS / FLORAL WATERS ─────────────────────────────────────────────
    "neroli hydrolat":      {"name_en":"Neroli hydrolat",              "name_es":"Hidrolato de neroli",         "pka":7.0,   "type":"neutral",    "cat":"hydrolats"},
    "rose hydrolat":        {"name_en":"Rose (damask) hydrolat",       "name_es":"Hidrolato de rosa de damasco","pka":7.0,   "type":"neutral",    "cat":"hydrolats"},
    "lavender hydrolat":    {"name_en":"Lavender hydrolat",            "name_es":"Hidrolato de lavanda",        "pka":7.0,   "type":"neutral",    "cat":"hydrolats"},
    "chamomile hydrolat":   {"name_en":"Chamomile hydrolat",           "name_es":"Hidrolato de manzanilla",     "pka":7.0,   "type":"neutral",    "cat":"hydrolats"},
    "witch hazel":          {"name_en":"Witch hazel hydrolat",         "name_es":"Hidrolato de hamamelis",      "pka":7.0,   "type":"neutral",    "cat":"hydrolats"},
    "calendula hydrolat":   {"name_en":"Calendula hydrolat",           "name_es":"Hidrolato de caléndula",      "pka":7.0,   "type":"neutral",    "cat":"hydrolats"},
    "peppermint hydrolat":  {"name_en":"Peppermint hydrolat",          "name_es":"Hidrolato de menta piperita", "pka":7.0,   "type":"neutral",    "cat":"hydrolats"},
    "rosemary hydrolat":    {"name_en":"Rosemary hydrolat",            "name_es":"Hidrolato de romero",         "pka":7.0,   "type":"neutral",    "cat":"hydrolats"},
    "ylang hydrolat":       {"name_en":"Ylang ylang hydrolat",         "name_es":"Hidrolato de ylang ylang",    "pka":7.0,   "type":"neutral",    "cat":"hydrolats"},
    "sea water":            {"name_en":"Sea water",                    "name_es":"Agua de mar",                 "pka":8.10,  "type":"base",       "cat":"hydrolats"},
    "green tea water":      {"name_en":"Green tea infusion",           "name_es":"Infusión de té verde",        "pka":7.0,   "type":"neutral",    "cat":"hydrolats"},

    # ── THICKENERS / GELLING AGENTS ──────────────────────────────────────────
    "carbomer":             {"name_en":"Carbomer (acrylate gel)",      "name_es":"Carbomer (gel acrílico)",     "pka":6.00,  "type":"acid",       "cat":"thickeners"},
    "xanthan gum":          {"name_en":"Xanthan gum",                  "name_es":"Goma xantana",                "pka":7.0,   "type":"neutral",    "cat":"thickeners"},
    "guar gum":             {"name_en":"Guar gum",                     "name_es":"Goma guar",                   "pka":7.0,   "type":"neutral",    "cat":"thickeners"},
    "hydroxyethylcellulose":{"name_en":"Hydroxyethylcellulose (HEC)",  "name_es":"Hidroxietilcelulosa (HEC)",   "pka":7.0,   "type":"neutral",    "cat":"thickeners"},
    "hydroxypropyl guar":   {"name_en":"Hydroxypropyl guar",           "name_es":"Goma guar hidroxipropil",     "pka":7.0,   "type":"neutral",    "cat":"thickeners"},
    "agar agar":            {"name_en":"Agar agar",                    "name_es":"Agar agar",                   "pka":7.0,   "type":"neutral",    "cat":"thickeners"},
    "carrageenan":          {"name_en":"Carrageenan",                  "name_es":"Carragenano",                 "pka":7.0,   "type":"neutral",    "cat":"thickeners"},
    "sodium alginate":      {"name_en":"Sodium alginate",              "name_es":"Alginato de sodio",           "pka":7.0,   "type":"neutral",    "cat":"thickeners"},
    "gelatin":              {"name_en":"Gelatin (hydrolyzed)",         "name_es":"Gelatina hidrolizada",        "pka":7.0,   "type":"neutral",    "cat":"thickeners"},
    "cetyl alcohol":        {"name_en":"Cetyl alcohol",                "name_es":"Alcohol cetílico",            "pka":7.0,   "type":"neutral",    "cat":"thickeners"},

    # ── STARCHES / POWDERS ────────────────────────────────────────────────────
    "corn starch":          {"name_en":"Corn starch",                  "name_es":"Almidón de maíz",             "pka":7.0,   "type":"neutral",    "cat":"exfoliants"},
    "rice starch":          {"name_en":"Rice starch",                  "name_es":"Almidón de arroz",            "pka":7.0,   "type":"neutral",    "cat":"exfoliants"},
    "arrowroot powder":     {"name_en":"Arrowroot powder",             "name_es":"Almidón de arrurruz",         "pka":7.0,   "type":"neutral",    "cat":"exfoliants"},
    "sugar scrub":          {"name_en":"Fine sugar (exfoliant)",       "name_es":"Azúcar fino (exfoliante)",    "pka":7.0,   "type":"neutral",    "cat":"exfoliants"},
    "sea salt exf":         {"name_en":"Fine sea salt (exfoliant)",    "name_es":"Sal marina fina (exfoliante)","pka":7.0,   "type":"neutral",    "cat":"exfoliants"},
    "pumice":               {"name_en":"Pumice powder",                "name_es":"Piedra pómez en polvo",       "pka":7.0,   "type":"neutral",    "cat":"exfoliants"},
    "bamboo powder":        {"name_en":"Bamboo powder",                "name_es":"Polvo de bambú",              "pka":7.0,   "type":"neutral",    "cat":"exfoliants"},
    "jojoba beads":         {"name_en":"Jojoba beads",                 "name_es":"Microperlas de jojoba",       "pka":7.0,   "type":"neutral",    "cat":"exfoliants"},
}

def ingr_name(entry: dict) -> str:
    return entry["name_es"] if LANG == "es" else entry["name_en"]

def type_label(t_key: str) -> str:
    map_ = {
        "acid":        t("t_acid"),
        "base":        t("t_base"),
        "neutral":     t("t_neutral"),
        "strong_base": t("t_strong_base"),
    }
    return map_.get(t_key, t_key)

def type_color(t_key: str) -> str:
    map_ = {
        "acid":        "[red]{v}[/red]",
        "base":        "[blue]{v}[/blue]",
        "neutral":     "[dim]{v}[/dim]",
        "strong_base": "[bold blue]{v}[/bold blue]",
    }
    lbl = type_label(t_key)
    return map_.get(t_key, "{v}").format(v=lbl)

# ─────────────────────────────────────────────────────────────
# Presets
# ─────────────────────────────────────────────────────────────

def get_presets() -> dict:
    return {
        "1": {
            "name_en": "Natural deodorant stick (dry touch)",
            "name_es": "Desodorante natural (stick seco)",
            "water_ph": 6.5, "water_pct": 50.0,
            "ingredients": [
                {"name_en": "Baking soda",    "name_es": "Bicarbonato de sodio", "pct": 8.0,  "pka": 8.30, "type": "base"},
                {"name_en": "Corn starch",    "name_es": "Almidón de maíz",      "pct": 10.0, "pka": 7.00, "type": "neutral"},
                {"name_en": "Shea butter",    "name_es": "Manteca de karité",    "pct": 20.0, "pka": 7.00, "type": "neutral"},
                {"name_en": "Coconut oil",    "name_es": "Aceite de coco",       "pct": 10.0, "pka": 7.00, "type": "neutral"},
            ],
            "adjustor": {"name_en": "Citric acid", "name_es": "Ácido cítrico", "pct": 1.5, "pka": 3.13, "type": "acid"},
        },
        "2": {
            "name_en": "Hyaluronic acid serum",
            "name_es": "Sérum de ácido hialurónico",
            "water_ph": 6.5, "water_pct": 78.0,
            "ingredients": [
                {"name_en": "Hyaluronic acid",    "name_es": "Ácido hialurónico", "pct": 1.0,  "pka": 3.50, "type": "acid"},
                {"name_en": "Glycerin",           "name_es": "Glicerina",         "pct": 5.0,  "pka": 14.0, "type": "neutral"},
                {"name_en": "Niacinamide",        "name_es": "Niacinamida",       "pct": 5.0,  "pka": 7.20, "type": "neutral"},
                {"name_en": "Centella asiatica",  "name_es": "Centella asiática", "pct": 3.0,  "pka": 5.50, "type": "acid"},
            ],
            "adjustor": {"name_en": "Triethanolamine (TEA)", "name_es": "Trietanolamina (TEA)", "pct": 0.8, "pka": 8.15, "type": "base"},
        },
        "3": {
            "name_en": "AHA/BHA exfoliant",
            "name_es": "Exfoliante AHA/BHA",
            "water_ph": 6.5, "water_pct": 60.0,
            "ingredients": [
                {"name_en": "Lactic acid",     "name_es": "Ácido láctico",    "pct": 10.0, "pka": 3.86, "type": "acid"},
                {"name_en": "Salicylic acid",  "name_es": "Ácido salicílico", "pct": 2.0,  "pka": 2.97, "type": "acid"},
                {"name_en": "Glycerin",        "name_es": "Glicerina",        "pct": 5.0,  "pka": 14.0, "type": "neutral"},
                {"name_en": "Aloe vera",       "name_es": "Aloe vera",        "pct": 5.0,  "pka": 6.00, "type": "acid"},
            ],
            "adjustor": {"name_en": "Triethanolamine (TEA)", "name_es": "Trietanolamina (TEA)", "pct": 1.5, "pka": 8.15, "type": "base"},
        },
        "4": {
            "name_en": "Facial mist (hydrolat + centella)",
            "name_es": "Mist facial (hidrolato + centella)",
            "water_ph": 6.5, "water_pct": 65.0,
            "ingredients": [
                {"name_en": "Neroli hydrolat",    "name_es": "Hidrolato de neroli", "pct": 20.0, "pka": 5.50, "type": "acid"},
                {"name_en": "Centella asiatica",  "name_es": "Centella asiática",   "pct": 3.0,  "pka": 5.50, "type": "acid"},
                {"name_en": "Glycerin",           "name_es": "Glicerina",           "pct": 5.0,  "pka": 14.0, "type": "neutral"},
            ],
            "adjustor": None,
        },
    }

def preset_name(p: dict) -> str:
    return p["name_es"] if LANG == "es" else p["name_en"]

def ing_display_name(ing: dict) -> str:
    if "name_es" in ing:
        return ing["name_es"] if LANG == "es" else ing["name_en"]
    return ing.get("nombre", ing.get("name", "?"))

# ─────────────────────────────────────────────────────────────
# pH Calculation
# ─────────────────────────────────────────────────────────────

def ph_of_ingredient(pka: float, pct: float, itype: str) -> float:
    if itype == "neutral":
        return 7.0
    if itype == "strong_base":
        conc = max(pct / 100 * 0.5, 1e-10)
        return min(14.0, 14 + math.log10(conc))
    if itype == "acid":
        C = max(pct / 100 * 0.1, 1e-10)
        ph = 0.5 * (pka - math.log10(C))
        return max(1.0, min(13.0, ph))
    if itype in ("base", "base_fuerte"):
        C = max(pct / 100 * 0.05, 1e-10)
        ph = 14 - 0.5 * (pka - math.log10(C))
        return max(1.0, min(13.0, ph))
    return 7.0


def calculate_ph(water_ph: float, water_pct: float,
                 ingredients: list[dict],
                 adjustor: Optional[dict] = None) -> float:
    h_total = 0.0
    weight_total = 0.0

    h_total += math.pow(10, -water_ph) * water_pct
    weight_total += water_pct

    for ing in ingredients:
        pct = ing["pct"]
        ph_i = ph_of_ingredient(ing["pka"], pct, ing["type"])
        h_total += math.pow(10, -ph_i) * pct
        weight_total += pct

    if adjustor and adjustor["pct"] > 0:
        pct = adjustor["pct"]
        ph_a = ph_of_ingredient(adjustor["pka"], pct, adjustor["type"])
        h_total += math.pow(10, -ph_a) * pct
        weight_total += pct

    if weight_total == 0:
        return 7.0

    h_avg = h_total / weight_total
    ph_final = -math.log10(max(h_avg, 1e-14))
    return round(max(0.5, min(13.5, ph_final)), 2)


def get_zone(ph: float) -> tuple[str, str, str]:
    if ph < 2.0:   return "zone_very_acid",  "bold red",     "msg_very_acid"
    if ph < 4.5:   return "zone_eff_acid",   "yellow",       "msg_eff_acid"
    if ph < 5.5:   return "zone_mild_acid",  "green",        "msg_mild_acid"
    if ph < 7.0:   return "zone_neutral",    "bright_green", "msg_neutral"
    if ph < 8.5:   return "zone_mild_base",  "cyan",         "msg_mild_base"
    if ph < 10.0:  return "zone_alkaline",   "blue",         "msg_alkaline"
    return              "zone_very_base",    "bold red",     "msg_very_base"


def ph_color(ph: float) -> str:
    if ph < 4:   return "red"
    if ph < 5.5: return "yellow"
    if ph < 7.5: return "bright_green"
    if ph < 9:   return "cyan"
    return "blue"


def ph_bar(ph: float, width: int = 50) -> str:
    pos = int((ph / 14) * width)
    pos = max(0, min(width - 1, pos))
    bar = ["─"] * width
    bar[pos] = "▲"
    return "".join(bar)

# ─────────────────────────────────────────────────────────────
# UI
# ─────────────────────────────────────────────────────────────

def show_header():
    console.clear()
    console.print(Panel.fit(
        f"[bold gold1]{t('header_title')}[/bold gold1]\n"
        f"[dim]{t('header_sub')}[/dim]\n"
        f"[dim italic]{t('header_note')}[/dim italic]",
        border_style="gold1",
        padding=(0, 2),
    ))
    console.print()


def show_db():
    console.print()
    table = Table(
        title=t("db_title"),
        box=box.ROUNDED,
        border_style="dim",
        show_lines=False,
    )
    table.add_column(t("db_col_key"),  style="dim", min_width=16)
    table.add_column(t("db_col_name"), min_width=24)
    table.add_column(t("db_col_pka"),  justify="right")
    table.add_column(t("db_col_type"), justify="center")
    for k, v in INGREDIENTS_DB.items():
        table.add_row(k, ingr_name(v), str(v["pka"]), type_color(v["type"]))
    console.print(table)
    console.print()


def show_preset_preview(p: dict):
    console.print()
    console.print(Rule(f"[bold]{t('preset_preview')}[/bold]", style="gold1"))
    console.print()

    table = Table(box=box.SIMPLE, show_header=True, header_style="bold dim")
    table.add_column(t("result_col_ingr"), min_width=26)
    table.add_column(t("result_col_pct"),  justify="right")
    table.add_column(t("result_col_pka"),  justify="right")
    table.add_column(t("result_col_type"), justify="center")

    table.add_row(
        t("result_water"),
        f"{p['water_pct']:.1f}%",
        f"{p['water_ph']:.2f}",
        f"[dim]{t('t_neutral')}[/dim]",
    )
    for ing in p["ingredients"]:
        table.add_row(
            ing_display_name(ing),
            f"{ing['pct']:.1f}%",
            f"{ing['pka']:.2f}",
            type_color(ing["type"]),
        )
    adj = p.get("adjustor")
    if adj:
        adj_label = f"[italic]{ing_display_name(adj)}[/italic] {t('result_adjustor')}"
        table.add_row(adj_label, f"{adj['pct']:.1f}%", f"{adj['pka']:.2f}", type_color(adj["type"]))

    console.print(table)

    total = p["water_pct"] + sum(i["pct"] for i in p["ingredients"])
    if adj:
        total += adj["pct"]
    color_total = "green" if 98 <= total <= 102 else "yellow"
    console.print(f"  {t('result_total')}: [{color_total}]{total:.1f}%[/{color_total}]")
    console.print()


def show_result(ph: float, ingredients: list[dict],
                water_ph: float, water_pct: float,
                adjustor: Optional[dict]):

    total_pct = water_pct + sum(i["pct"] for i in ingredients)
    if adjustor and adjustor.get("pct"):
        total_pct += adjustor["pct"]

    zone_key, color, msg_key = get_zone(ph)
    c = ph_color(ph)

    console.print(Rule(f"[bold]{t('result_title')}[/bold]", style="gold1"))
    console.print()

    # pH panel
    ph_line = Text()
    ph_line.append(f"  {t('result_ph')}: ", style="bold")
    ph_line.append(f"{ph:.2f}", style=f"bold {c}")
    ph_line.append(f"  ·  {t(zone_key)}", style=c)
    console.print(Panel(ph_line, border_style=c, padding=(0, 1)))

    # pH bar
    bar = ph_bar(ph)
    console.print(f"  [dim]{t('axis_acid')}[/dim] [{c}]{bar}[/{c}] [dim]{t('axis_basic')}[/dim]")
    console.print(f"  [dim]{'':>12}{t('axis_neutral')}[/dim]")
    console.print()

    # Ingredients table
    table = Table(box=box.SIMPLE, show_header=True, header_style="bold dim")
    table.add_column(t("result_col_ingr"), min_width=26)
    table.add_column(t("result_col_pct"),  justify="right")
    table.add_column(t("result_col_pka"),  justify="right")
    table.add_column(t("result_col_type"), justify="center")
    table.add_column(t("result_col_ph"),   justify="right")

    table.add_row(
        t("result_water"),
        f"{water_pct:.1f}%",
        f"{water_ph:.2f}",
        f"[dim]{t('t_neutral')}[/dim]",
        f"[cyan]{water_ph:.2f}[/cyan]",
    )
    for ing in ingredients:
        ph_i = ph_of_ingredient(ing["pka"], ing["pct"], ing["type"])
        table.add_row(
            ing_display_name(ing),
            f"{ing['pct']:.1f}%",
            f"{ing['pka']:.2f}",
            type_color(ing["type"]),
            f"{ph_i:.2f}",
        )
    if adjustor and adjustor.get("pct", 0) > 0:
        ph_a = ph_of_ingredient(adjustor["pka"], adjustor["pct"], adjustor["type"])
        adj_label = f"[italic]{ing_display_name(adjustor)}[/italic] {t('result_adjustor')}"
        table.add_row(adj_label, f"{adjustor['pct']:.1f}%", f"{adjustor['pka']:.2f}",
                      type_color(adjustor["type"]), f"{ph_a:.2f}")

    console.print(table)

    color_total = "green" if 98 <= total_pct <= 102 else "yellow" if total_pct <= 105 else "red"
    console.print(f"  {t('result_total')}: [{color_total}]{total_pct:.1f}%[/{color_total}]")
    if total_pct > 102:
        console.print(f"  [yellow]{t('result_over')}[/yellow]")
    console.print()

    # Diagnosis panel
    console.print(Panel(
        f"[bold]{t('result_diagnosis')}:[/bold] [{c}]{t(zone_key)}[/{c}]\n\n"
        f"{t(msg_key)}\n\n"
        f"[dim]{t('result_meter_note')}[/dim]",
        title=f"[bold dim]{t('result_diag_title')}[/bold dim]",
        border_style="dim",
        padding=(0, 1),
    ))
    console.print()

# ─────────────────────────────────────────────────────────────
# Input flows
# ─────────────────────────────────────────────────────────────

def normalize(s: str) -> str:
    return (s.lower()
            .replace("á","a").replace("é","e").replace("í","i")
            .replace("ó","o").replace("ú","u").replace("ü","u"))


def ask_ingredient(number: int) -> Optional[dict]:
    console.print(f"\n[bold]{t('ingr_title', n=number)}[/bold]")
    console.print(t("ingr_hint"))

    raw = Prompt.ask(t("ingr_name"))

    if raw.lower() == "db":
        show_db()
        raw = Prompt.ask(t("ingr_name"))

    # Try autocomplete from DB
    key_norm = normalize(raw)
    match = None
    match_key = None
    for k, v in INGREDIENTS_DB.items():
        k_norm = normalize(k)
        name_norm = normalize(ingr_name(v))
        if k_norm in key_norm or key_norm in k_norm or name_norm in key_norm or key_norm in name_norm:
            match = v
            match_key = k
            break

    if match:
        console.print(
            f"  {t('ingr_found')} [green]{ingr_name(match)}[/green] · "
            f"pKa={match['pka']} · {type_color(match['type'])}"
        )
        use_it = Confirm.ask(t("ingr_use_vals"), default=True)
        if use_it:
            pct = float(Prompt.ask(t("ingr_pct"), default="5.0"))
            return {
                "name_en": match["name_en"],
                "name_es": match["name_es"],
                "pct": pct,
                "pka": match["pka"],
                "type": match["type"],
            }

    # Manual entry
    pct  = float(Prompt.ask(t("ingr_pct"),  default="5.0"))
    pka  = float(Prompt.ask(t("ingr_pka"),  default="5.0"))
    choices = t("ingr_type_choices")
    itype = Prompt.ask(t("ingr_type"), choices=choices, default=t("ingr_type_default"))

    # Normalize type key to internal
    type_map = {
        "acid": "acid", "acido": "acid",
        "base": "base",
        "neutral": "neutral", "neutro": "neutral",
        "strong_base": "strong_base", "base_fuerte": "strong_base",
    }
    itype = type_map.get(itype, "neutral")

    return {"name_en": raw, "name_es": raw, "pct": pct, "pka": pka, "type": itype}


def ask_adjustor() -> Optional[dict]:
    console.print(f"\n[bold]{t('adj_title')}[/bold]")

    adj_options = {
        "1": {"name_en": "Citric acid",              "name_es": "Ácido cítrico",           "pka": 3.13, "type": "acid"},
        "2": {"name_en": "Lactic acid",              "name_es": "Ácido láctico",           "pka": 3.86, "type": "acid"},
        "3": {"name_en": "Triethanolamine (TEA)",    "name_es": "Trietanolamina (TEA)",    "pka": 8.15, "type": "base"},
        "4": {"name_en": "Arginine",                 "name_es": "Arginina",                "pka": 5.01, "type": "base"},
        "5": {"name_en": "Baking soda",              "name_es": "Bicarbonato de sodio",    "pka": 8.30, "type": "base"},
        "6": {"name_en": "NaOH (caustic soda)",      "name_es": "NaOH (sosa cáustica)",   "pka": 14.0, "type": "strong_base"},
        "0": None,
    }
    for k, v in adj_options.items():
        if v:
            tc = type_color(v["type"])
            console.print(f"  [{k}] {ing_display_name(v)} · pKa {v['pka']} · {tc}")
        else:
            console.print(f"  [0] {t('adj_none')}")

    choice = Prompt.ask(t("adj_prompt"), choices=list(adj_options.keys()), default="0")
    if choice == "0":
        return None
    adj = dict(adj_options[choice])
    adj["pct"] = float(Prompt.ask(t("adj_pct"), default="0.5"))
    return adj


def flow_custom():
    show_header()
    console.print(f"[bold]{t('custom_title')}[/bold]\n")

    water_ph  = float(Prompt.ask(t("water_ph"),  default="6.5"))
    water_pct = float(Prompt.ask(t("water_pct"), default="70.0"))

    ingredients = []
    n = 1
    while True:
        ing = ask_ingredient(n)
        if ing is None:
            break
        ingredients.append(ing)
        n += 1
        if not Confirm.ask(t("ingr_add_another"), default=True):
            break

    if not ingredients:
        console.print(f"[yellow]{t('ingr_none')}[/yellow]")

    adjustor = ask_adjustor()
    ph = calculate_ph(water_ph, water_pct, ingredients, adjustor)
    show_result(ph, ingredients, water_ph, water_pct, adjustor)


def flow_preset(key: str):
    presets = get_presets()
    p = presets[key]
    show_header()
    console.print(f"[bold]{t('preset_title')}:[/bold] [gold1]{preset_name(p)}[/gold1]")

    show_preset_preview(p)

    proceed = Confirm.ask(t("preset_confirm"), default=True)
    if not proceed:
        return

    water_ph  = p["water_ph"]
    water_pct = p["water_pct"]
    ingredients = [dict(i) for i in p["ingredients"]]
    adjustor = dict(p["adjustor"]) if p["adjustor"] else None

    if Confirm.ask(t("preset_edit"), default=False):
        water_ph  = float(Prompt.ask(t("preset_water_ph"),  default=str(water_ph)))
        water_pct = float(Prompt.ask(t("preset_water_pct"), default=str(water_pct)))
        for ing in ingredients:
            ing["pct"] = float(Prompt.ask(f"  % {ing_display_name(ing)}", default=str(ing["pct"])))
        if adjustor:
            adjustor["pct"] = float(Prompt.ask(
                f"  % {ing_display_name(adjustor)} {t('preset_adj_pct')}",
                default=str(adjustor["pct"])
            ))

    ph = calculate_ph(water_ph, water_pct, ingredients, adjustor)
    show_result(ph, ingredients, water_ph, water_pct, adjustor)

# ─────────────────────────────────────────────────────────────
# Menu
# ─────────────────────────────────────────────────────────────

def main_menu():
    while True:
        show_header()
        console.print(f"[bold]{t('menu_title')}[/bold]\n")
        console.print(f"  [1] {t('menu_1')}")
        console.print(f"  [2] {t('menu_2')}")
        console.print(f"  [3] {t('menu_3')}")
        console.print(f"  [4] {t('menu_4')}")
        console.print(f"  [5] {t('menu_5')}")
        console.print(f"  [6] {t('menu_6')}")
        console.print(f"  [0] {t('menu_0')}\n")

        choice = Prompt.ask(t("menu_prompt"), choices=["0","1","2","3","4","5","6"])

        if choice == "0":
            console.print(t("goodbye"))
            break
        elif choice == "1":
            flow_custom()
            Prompt.ask(t("press_enter"))
        elif choice in ("2","3","4","5"):
            flow_preset(str(int(choice) - 1))
            Prompt.ask(t("press_enter"))
        elif choice == "6":
            show_header()
            show_db()
            Prompt.ask(t("press_enter"))

# ─────────────────────────────────────────────────────────────
# Entry point — language selection
# ─────────────────────────────────────────────────────────────

def select_language():
    global LANG
    console.clear()
    console.print(Panel.fit(
        "[bold gold1]pH Calculator / Calculadora de pH[/bold gold1]\n"
        "[dim]Auro Labs · Natural Cosmetics[/dim]",
        border_style="gold1",
        padding=(0, 2),
    ))
    console.print()
    console.print("  [1] English  [default]")
    console.print("  [2] Español\n")
    lang_choice = Prompt.ask("Select / Selecciona", choices=["1","2","en","es"], default="1")
    LANG = "es" if lang_choice in ("2","es") else "en"


if __name__ == "__main__":
    select_language()
    main_menu()
