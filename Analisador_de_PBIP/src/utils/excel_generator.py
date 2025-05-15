import pandas as pd
def generate_report_mapeado(data, output_path):
    import pandas as pd
    import openpyxl
    from openpyxl.styles import Font
    from utils.json_processing import flatten_json
    flattened_data = flatten_json(data)

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Estrutura Base"

    ws.append(["Chave", "Valor"] + [f"Parte {i+1}" for i in range(10)])
    header_font = Font(bold=True)
    for cell in ws[1]:
        cell.font = header_font

    for key, value in flattened_data.items():
        key_parts = key.split('.')
        row = [key, value] + key_parts
        ws.append(row)

    for column in ws.columns:
        max_length = 0
        column_letter = column[0].column_letter
        for cell in column:
            try:
                if cell.value:
                    max_length = max(max_length, len(str(cell.value)))
            except:
                pass
        ws.column_dimensions[column_letter].width = max_length + 2

    wb.save(output_path)


def generate_report_compilado(df_sections, df_visual_containers, df_vc_complemento, output_path):
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        df_sections.to_excel(writer, sheet_name="Sections", index=False)
        df_visual_containers.to_excel(writer, sheet_name="VisualContainers", index=False)
        df_vc_complemento.to_excel(writer, sheet_name="VC_Complemento", index=False)