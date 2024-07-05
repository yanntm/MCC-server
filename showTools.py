import requests
import pandas as pd

# Query the MCC server for tools and examinations
response = requests.get('http://localhost:1664/tools/descriptions')
data = response.json()

# Parse the data into a DataFrame
tools_info = data['tools_info']

# Simplify the table by combining related examinations into single columns
simplified_columns = {
    'LTL': ['LTLCardinality', 'LTLFireability'],
    'CTL': ['CTLCardinality', 'CTLFireability'],
    'Reachability': ['ReachabilityCardinality', 'ReachabilityFireability', 'ReachabilityDeadlock'],
    'StateSpace': ['StateSpace'],
    'UpperBounds': ['UpperBounds'],
    'Liveness': ['Liveness', 'QuasiLiveness'],
    'OneSafe': ['OneSafe'],
    'StableMarking': ['StableMarking']
}

# Create a simplified DataFrame
simplified_df = pd.DataFrame(index=[tool['tool'] for tool in tools_info], columns=simplified_columns.keys())

# Fill the simplified DataFrame with checkmarks
for tool_info in tools_info:
    tool = tool_info['tool']
    col_exams = set(tool_info['COLexaminations'])
    pt_exams = set(tool_info['PTexaminations'])
    for col, exams in simplified_columns.items():
        if col_exams.intersection(exams) or pt_exams.intersection(exams):
            simplified_df.at[tool, col] = '✓'

simplified_df = simplified_df.fillna('')
simplified_df['COL supported'] = ['✓' if tool_info['COLexaminations'] else '' for tool_info in tools_info]
simplified_df = simplified_df[['COL supported'] + list(simplified_columns.keys())]

# Add a column to count the number of supported examinations for sorting
simplified_df['Supported Count'] = simplified_df.apply(lambda row: row.value_counts().get('✓', 0), axis=1)

# Sort the DataFrame by the count of supported examinations in descending order
simplified_df = simplified_df.sort_values(by='Supported Count', ascending=False)

# Drop the count column for display
simplified_df = simplified_df.drop(columns=['Supported Count'])

# Convert the DataFrame to markdown format
markdown_table = simplified_df.to_markdown()

# Print the markdown table
print(markdown_table)

