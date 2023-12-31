import os
from UI.display_utils import display_results
import LLMAPIInterface.llm_api as llm_api
import LLMAPIInterface.knowledge_asst as knower
import LLMAPIInterface.doppleganger as doppleganger
import json
import subprocess

minime = None

def generate_mvp(description, project_directory):
    knowledge_dir = f"{project_directory}/knowledge"
    mvp1 = llm_api.generate_mvp(description)
    mvp2 = llm_api.generate_mvp(description)
    mvp3 = llm_api.generate_mvp(description)
    mvp_final = llm_api.synthesize_best_mvp(mvp1, mvp2, mvp3)
    mvp_name = f"{knowledge_dir}/mvp_description.txt"
    with open(mvp_name, 'w') as file:
        file.write(mvp_final)

def generate_component_list(project_directory):
    knowledge_dir = f"{project_directory}/knowledge"
    mvp_description = ""
    with open(os.path.join(knowledge_dir, 'mvp_description.txt'), 'r') as file:
        mvp_description = file.read()
    comp_list = llm_api.get_component_list(mvp_description)
    comp_name = f"{knowledge_dir}/component_list.json"
    rcomp_name = f"{knowledge_dir}/component_list_readable.txt"
    with open(comp_name, 'w', newline='\r\n') as file:
        #comp_list = comp_list.replace('\n', '\r\n')
        json.dump(comp_list, file, indent=4)
    formatted_components = []
    for component in comp_list:
        formatted_components.append(component)
    # Join each formatted component with a newline for readability
    rcomp_list = '\n'.join(formatted_components)
    with open(rcomp_name, 'w') as file:
        file.write(rcomp_list)

def generate_python_files_for_component(component_name, project_directory):
    knowledge_dir = f"{project_directory}/knowledge"
    mvp_description = ""
    with open(f"{knowledge_dir}/mvp_description.txt", 'r') as file:
        mvp_description = file.read()
    with open(f"{knowledge_dir}/component_list.json", 'r') as file:
        json_data = json.load(file)

    component_description = None
    files = []
    for component in json_data.get("components", []):
        if component["name"] == component_name:
            component_description = component
            files = [file["filename"] for file in component.get("files", [])]
    for file_name in files:
        file_code = llm_api.generate_py_file_for_component(component_description, file_name, mvp_description)
        with open(f"{project_directory}/{file_name}", 'w') as file:
            file.write(file_code)

def generate_best_code_for_component(component_name, project_directory):
    knowledge_dir = f"{project_directory}/knowledge"
    mvp_description = ""
    with open(f"{knowledge_dir}/mvp_description.txt", 'r') as file:
        mvp_description = file.read()
    with open(f"{knowledge_dir}/component_list.json", 'r') as file:
        json_data = json.load(file)
        component_description = None
    files = []
    for component in json_data.get("components", []):
        if component["name"] == component_name:
            component_description = component
            files = [file["filename"] for file in component.get("files", [])]
    for file_name in files:
        file_code1 = llm_api.generate_py_file_for_component(component_description, file_name, mvp_description)
        file_code2 = llm_api.generate_py_file_for_component(component_description, file_name, mvp_description)
        file_code3 = llm_api.generate_py_file_for_component(component_description, file_name, mvp_description)
        file_code = llm_api.synthesize_best_code(component_description, mvp_description, file_name, file_code1, file_code2, file_code3)
        with open(f"{project_directory}/{file_name}", 'w') as file:
            file.write(file_code)

def document_component(component_name, project_directory):
    knowledge_dir = f"{project_directory}/knowledge"
    mvp_description = ""
    with open(f"{knowledge_dir}/mvp_description.txt", 'r') as file:
        mvp_description = file.read()
    with open(f"{knowledge_dir}/component_list.json", 'r') as file:
        json_data = json.load(file)

    component_description = None
    files = []
    for component in json_data.get("components", []):
        if component["name"] == component_name:
            component_description = component
            files = [file["filename"] for file in component.get("files", [])]
    for file_name in files:
        doc_name = file_name.rsplit('.', 1)[0] + '_doc.txt'
        full_name = f"{project_directory}/{file_name}"
        doc_code = llm_api.document_code_file(full_name, component_description,mvp_description)
        with open(f"{knowledge_dir}/{doc_name}", 'w') as file:
            file.write(doc_code)

def critique_component(component_name, project_directory):
    knowledge_dir = f"{project_directory}/knowledge"
    mvp_description = ""
    with open(f"{knowledge_dir}/mvp_description.txt", 'r') as file:
        mvp_description = file.read()
    with open(f"{knowledge_dir}/component_list.json", 'r') as file:
        json_data = json.load(file)
    
    component_description = None
    files = []
    for component in json_data.get("components", []):
        if component["name"] == component_name:
            component_description = component
            files = [file["filename"] for file in component.get("files", [])]
    for file_name in files:
        critique_name = file_name.rsplit('.', 1)[0] + '_critique.txt'
        full_name = f"{project_directory}/{file_name}"
        critique_code = llm_api.critique_code_file(full_name, component_description,mvp_description)
        with open(f"{knowledge_dir}/{critique_name}", 'w') as file:
            file.write(critique_code)

def generate_unit_tests_for_component(component_name, project_directory):
    knowledge_dir = f"{project_directory}/knowledge"
    mvp_description = ""
    with open(f"{knowledge_dir}/mvp_description.txt", 'r') as file:
        mvp_description = file.read()
    with open(f"{knowledge_dir}/component_list.json", 'r') as file:
        json_data = json.load(file)
    component_description = None
    files = []
    for component in json_data.get("components", []):
        if component["name"] == component_name:
            component_description = component
            files = [file["filename"] for file in component.get("files", [])]
    for file_name in files:
        unit_test_name = file_name.rsplit('.', 1)[0] + '_tests.py'
        full_name = f"{project_directory}/{file_name}"
        unit_test_code = llm_api.generate_unit_tests_for_file(full_name, component_description,mvp_description)
        with open(f"{project_directory}/{unit_test_name}", 'w') as file:
            file.write(unit_test_code)

def index_python_file(file_name, project_directory):
    knowledge_dir = os.path.join(project_directory, 'knowledge')
    with open(os.path.join(project_directory, file_name), 'r') as file:
        file_content = file.read()
    index = llm_api.index_python_file(file_content)
    with open(os.path.join(knowledge_dir, f'{file_name}_index.json'), 'w') as file:
        json.dump(index, file, indent=4)

def load_rag_assistant(project_directory):
    knower.init_load_files(project_directory)

def run_unit_test_and_get_output(unit_test_path):
    """
    Runs a unit test and returns its output.

    Args:
        unit_test_path: str, path to the unit test file.

    Returns:
        str: Output from the unit test.
    """
    result = subprocess.run(['python', '-m', 'unittest', unit_test_path], capture_output=True, text=True)
    return result.stdout + result.stderr

def fix_unit_test_failure(file_name, unit_test_name, project_directory):
    knowledge_dir = os.path.join(project_directory, 'knowledge')
    file_path = os.path.join(project_directory, file_name)
    unit_test_path = os.path.join(knowledge_dir, unit_test_name)

    # Read the file content
    with open(file_path, 'r') as file:
        file_content = file.read()

    # Read the unit test content
    with open(unit_test_path, 'r') as file:
        unit_test_content = file.read()

    # Run the unit test and get the output
    unit_test_output = run_unit_test_and_get_output(unit_test_path)

    # Attempt to fix the unit test failure
    fixed_unit_test = llm_api.fix_unit_test_failure(file_content, unit_test_content, unit_test_output)

    # Write the fixed unit test back to file
    with open(unit_test_path, 'w') as file:
        file.write(fixed_unit_test)

def generate_main_entry_point(project_directory):
    knowledge_dir = f"{project_directory}/knowledge"
    mvp_file = f"{knowledge_dir}/mvp_description.txt"
    with open(mvp_file, 'r') as file:
        mvp_description = file.read()
    comp_file = f"{knowledge_dir}/component_list.json"
    with open(comp_file, 'r') as file:
        comp_list = json.load(file)
    main_file = llm_api.generate_main_entry_point(mvp_description, comp_list)
    with open(os.path.join(project_directory, 'main.py'), 'w') as file:
        file.write(main_file)

def save_project_directory(project_directory, config_file='config.txt'):
    """
    Saves the project directory to a configuration file.

    Args:
        project_directory: str, the project directory to save.
        config_file: str, the path to the configuration file.
    """
    with open(config_file, 'w') as file:
        file.write(project_directory)

def read_project_directory(config_file='config.txt'):
    """
    Reads the project directory from a configuration file.

    Args:
        config_file: str, the path to the configuration file.
3
    Returns:
        str: The project directory or None if the config file doesn't exist.
    """
    try:
        with open(config_file, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return None


def main_menu():
    """
    Displays the main menu and handles user input for task selection.
    """
    print("\nWelcome to CodeSorcerer!")
    print("0. Set Project")
    print("1. Generate MVP")
    print("2. Get Component List")
    print("3. Generate Code Files for Component")
    print("4. Document Component")
    print("5. Load RAG assistant")
    print("6. Criitique Component")
    print("7. Generate Unit Tests for Component")
    print("8. Fix Component")
    print("9. Exit")
    print("10. Find missing links")
    print("11. Find redundancies")
    print("12. Load Doppleganger")
    print("13. Converse with Doppleganger")

    choice = input("Enter your choice (0-13): ")
    return choice

def main():
    project_directory = read_project_directory()
    while True:
        choice = main_menu()
        
        if choice == '0':
            project_name = input("Enter project name: ")
            project_directory = f"C:/{project_name}"
            # Check if the directory exists, create if it doesn't
            if not os.path.exists(project_directory):
                os.makedirs(project_directory)
                print(f"Project directory created at {project_directory}")
                knowledge_dir = os.path.join(project_directory, 'knowledge')
                os.makedirs(knowledge_dir, exist_ok=True)
            else:
                print(f"Project directory already exists at {project_directory}")
            save_project_directory(project_directory)
        elif choice == '1' and project_directory:
            task_description = input("Enter task description for MVP: ")
            generate_mvp(task_description, project_directory)
        elif choice == '2' and project_directory:
            generate_component_list(project_directory)
        elif choice == '3' and project_directory:
            component_name = input("Enter component name: ")
            generate_best_code_for_component(component_name, project_directory)
        elif choice == '4' and project_directory:
            component_name = input("Enter component name: ")
            document_component(component_name, project_directory)
        elif choice == '5' and project_directory:
            load_rag_assistant(project_directory)
        elif choice == '6' and project_directory:
            component_name = input("Enter component name: ")
            critique_component(component_name, project_directory)
        elif choice == '7' and project_directory:
            component_name = input("Enter component name: ")
            generate_unit_tests_for_component(component_name, project_directory)
        elif choice == '8' and project_directory:
            generate_main_entry_point(project_directory)
        elif choice == '9':
            print("Exiting CodeSorcerer. Goodbye!")
            break
        elif choice == "12":
            minime = doppleganger.init_or_load()
        elif choice == "13":
            prompt = input("Enter your prompt: ")
            print(doppleganger.iterate_conversation(prompt, minime))
        else:
            print("Invalid choice or project not set. Please select a valid option or set a project.")

if __name__ == "__main__":
    main()
