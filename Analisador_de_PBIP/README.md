# Analisador de PBIP

Analisador de PBIP is a Python application designed to analyze and process PBIP (Power BI Report) JSON files. The application provides a user-friendly interface built with Tkinter, allowing users to generate various reports and visualizations from the provided JSON data.

## Project Structure

The project is organized into the following structure:

```
Analisador_de_PBIP
├── src
│   ├── main.py               # Entry point for the application
│   ├── gui.py                # Tkinter interface definition
│   ├── utils                 # Utility functions for various operations
│   │   ├── file_operations.py # Functions for file operations
│   │   ├── json_processing.py # Functions for loading and validating JSON
│   │   ├── tree_generator.py  # Functions to generate tree diagrams
│   │   ├── excel_generator.py  # Functions to generate Excel reports
│   │   └── dataframes_generator.py # Functions to process data into DataFrames
│   └── config
│       └── settings.py       # Configuration settings for the application
├── Documentos Gerados        # Directory for storing generated documents
├── requirements.txt          # List of project dependencies
└── README.md                 # Project documentation
```

## Features

- **Tkinter Interface**: A graphical user interface that allows users to specify the path of the JSON file and generate reports.
- **Document Generation**: The application can generate:
  - Tree diagrams from the JSON data.
  - A base report (report_mapeado) in Excel format.
  - A compiled report (report_compilado) in Excel format.
- **File Operations**: Utility functions to check for file existence and create necessary directories.
- **JSON Processing**: Functions to load and validate the JSON structure required for analysis.

## Installation

To set up the project, follow these steps:

1. Clone the repository or download the project files.
2. Navigate to the project directory.
3. Install the required dependencies using the following command:

   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the application by executing the `main.py` file:

   ```
   python src/main.py
   ```

2. In the Tkinter interface, specify the path to the JSON file.
3. Click the buttons to generate the desired reports and visualizations.
4. The generated documents will be saved in the "Documentos Gerados" directory.

## Contributing

Contributions to the project are welcome. Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.