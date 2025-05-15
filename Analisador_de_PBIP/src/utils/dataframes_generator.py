import pandas as pd
import json

def generate_vc_complemento(json_data):
    """
    Gera o DataFrame df_vc_complemento a partir do JSON fornecido.
    """
    vc_complemento_data = []

    # Processa as sections e visualContainers
    for section in json_data.get("sections", []):
        for visual_container in section.get("visualContainers", []):
            config = json.loads(visual_container.get("config", "{}"))
            single_visual = config.get("singleVisual", {})
            prototype_query = single_visual.get("prototypeQuery", {}).get("Select", [])

            for select_item in prototype_query:
                tipo = None
                table = None
                column = None
                aggregation = None
                expression_type = None

                if "Column" in select_item:
                    tipo = "column"
                    expression_type = "Column"
                    table = select_item["Column"].get("Expression", {}).get("SourceRef", {}).get("Entity")
                    column = select_item["Column"].get("Property")
                elif "Aggregation" in select_item:
                    tipo = "aggregation"
                    expression_type = "Aggregation"
                    aggregation_value = select_item["Aggregation"].get("Function")
                    aggregation_map = {1: "SUM", 2: "AVG", 3: "COUNT", 4: "MIN", 5: "MAX"}
                    aggregation = aggregation_map.get(aggregation_value, f"Unknown ({aggregation_value})")
                    table = select_item["Aggregation"].get("Expression", {}).get("SourceRef", {}).get("Entity")
                    column = select_item["Aggregation"].get("Expression", {}).get("Property")
                elif "Measure" in select_item:
                    tipo = "measure"
                    expression_type = "Measure"
                    table = select_item["Measure"].get("Expression", {}).get("SourceRef", {}).get("Entity")
                    column = select_item["Measure"].get("Property")

                vc_complemento_data.append({
                    "VisualContainers_id": visual_container.get("id"),
                    "tipo": tipo,
                    "Tabela": table,
                    "nome": column,
                    "nomeNoVisual": select_item.get("NativeReferenceName", column),
                    "Agregacao": aggregation,
                    "expression": expression_type
                })

    # Retorna o DataFrame gerado
    return pd.DataFrame(vc_complemento_data)

def process_sections(json_data):
    sections_data = []
    visual_containers_data = []
    vc_complemento_data = []

    section_id_counter = 1
    visual_container_id_counter = 1

    for section in json_data.get("sections", []):
        section_id = section_id_counter
        section_id_counter += 1

        sections_data.append({
            "id_section": section_id,
            "sections": section.get("name"),
            "DisplayName": section.get("displayName"),
            "DisplayOption": section.get("displayOption"),
            "height": section.get("height"),
            "width": section.get("width"),
            "VisualContainers_id": [],
            "config": json.dumps(section)
        })

        for visual_container in section.get("visualContainers", []):
            visual_container_id = visual_container_id_counter
            visual_container_id_counter += 1

            sections_data[-1]["VisualContainers_id"].append(visual_container_id)

            config = json.loads(visual_container.get("config", "{}"))
            single_visual = config.get("singleVisual", {})
            prototype_query = single_visual.get("prototypeQuery", {}).get("Select", [])

            visual_type = single_visual.get("visualType", "")
            is_group = visual_type == ""

            visual_containers_data.append({
                "VisualContainers_id": visual_container_id,
                "id_section": section_id,
                "height": visual_container.get("height"),
                "width": visual_container.get("width"),
                "x": visual_container.get("x"),
                "y": visual_container.get("y"),
                "z": visual_container.get("z"),
                "name": config.get("name"),
                "visualType": "group" if is_group else visual_type,
                "config": visual_container.get("config")
            })

            for select_item in prototype_query:
                tipo = None
                table = None
                column = None
                aggregation = None
                expression_type = None

                if "Column" in select_item:
                    tipo = "column"
                    expression_type = "Column"
                    table = select_item["Column"].get("Expression", {}).get("SourceRef", {}).get("Entity")
                    column = select_item["Column"].get("Property")
                elif "Aggregation" in select_item:
                    tipo = "aggregation"
                    expression_type = "Aggregation"
                    aggregation_value = select_item["Aggregation"].get("Function")
                    aggregation_map = {1: "SUM", 2: "AVG", 3: "COUNT", 4: "MIN", 5: "MAX"}
                    aggregation = aggregation_map.get(aggregation_value, f"Unknown ({aggregation_value})")
                    table = select_item["Aggregation"].get("Expression", {}).get("SourceRef", {}).get("Entity")
                    column = select_item["Aggregation"].get("Expression", {}).get("Property")
                elif "Measure" in select_item:
                    tipo = "measure"
                    expression_type = "Measure"
                    table = select_item["Measure"].get("Expression", {}).get("SourceRef", {}).get("Entity")
                    column = select_item["Measure"].get("Property")

                vc_complemento_data.append({
                    "VisualContainers_id": visual_container_id,
                    "tipo": tipo,
                    "Tabela": table,
                    "nome": column,
                    "nomeNoVisual": select_item.get("NativeReferenceName", column),
                    "Agregacao": aggregation,
                    "expression": expression_type
                })

    df_sections = pd.DataFrame(sections_data)
    df_visual_containers = pd.DataFrame(visual_containers_data)
    df_vc_complemento = pd.DataFrame(vc_complemento_data)

    df_sections["VisualContainers_id"] = df_sections["VisualContainers_id"].apply(lambda x: ", ".join(map(str, x)))

    return df_sections, df_visual_containers, df_vc_complemento

def process_config(json_data, df_sections, df_visual_containers):
    bookmarks_data = []
    bookmark_detalhamento_data = []

    bookmark_id_counter = 1

    config = json.loads(json_data.get("config", "{}"))
    bookmarks = config.get("bookmarks", [])

    def process_bookmark(bookmark, parent_id=None, parent_name=None, child_index=None):
        nonlocal bookmark_id_counter

        id_pai = parent_id
        nome_pai = parent_name

        current_id = bookmark_id_counter
        bookmark_id_counter += 1

        options = bookmark.get("options", {})
        apply_only_to_target_visuals = options.get("applyOnlytoTargetVisuals", False)
        supress_data = options.get("suppressData", False)

        bookmarks_data.append({
            "id_bookmark": current_id,
            "name": bookmark.get("name"),
            "displayName": bookmark.get("displayName"),
            "parent_id": id_pai,
            "parent_name": nome_pai,
            "child_index": child_index,
            "applyOnlyToTargetVisuals": apply_only_to_target_visuals,
            "suppressData": supress_data
        })

        children = bookmark.get("children", [])
        for index, child in enumerate(children):
            process_bookmark(child, parent_id=current_id, parent_name=bookmark.get("name"), child_index=index)

    for index, bookmark in enumerate(bookmarks):
        process_bookmark(bookmark, child_index=index)

    df_bookmarks = pd.DataFrame(bookmarks_data)
    df_bookmark_detalhamento = pd.DataFrame(bookmark_detalhamento_data)

    return df_bookmarks, df_bookmark_detalhamento