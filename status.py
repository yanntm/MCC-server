import os

def list_tools():
    tools_dir = '/home/mcc/BenchKit'
    all_folders = [f for f in os.listdir(tools_dir) if os.path.isdir(os.path.join(tools_dir, f))]
    tools = []

    for folder in all_folders:
        if folder in ['bin', '.git', '.settings', 'run', 'reducer' ]:
            continue
        tools.append(folder)

    return tools

def list_examinations(tool):
    tool_dir = f'/home/mcc/BenchKit/{tool}'
    pt_examinations = []
    col_examinations = []

    if not os.path.exists(tool_dir):
        return {'PTexaminations': pt_examinations, 'COLexaminations': col_examinations}

    exam_file_path = os.path.join(tool_dir, 'SupportedExamination.txt')
    if not os.path.isfile(exam_file_path):
        return {'PTexaminations': pt_examinations, 'COLexaminations': col_examinations}

    with open(exam_file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith('#'):
                exam_name, exam_type = line.split()
                if exam_type == 'PT':
                    pt_examinations.append(exam_name)
                elif exam_type == 'COL':
                    col_examinations.append(exam_name)

    return {'PTexaminations': pt_examinations, 'COLexaminations': col_examinations}

def get_all_tools_and_examinations():
    tools_info = []
    tools = list_tools()

    for tool in tools:
        examinations = list_examinations(tool)
        tools_info.append({
            'tool': tool,
            'PTexaminations': examinations['PTexaminations'],
            'COLexaminations': examinations['COLexaminations']
        })

    return tools_info