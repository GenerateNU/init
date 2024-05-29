import argparse
import inquirer

# Predefined Options
backend_languages = ['Python', 'Java', 'C++', 'RUST', 'Go']
frontend_languages = ['JavaScript', 'TypeScript']
databases = ['PostgreSQL', 'MySQL', 'SQLite', 'MongoDB']

# Setup for the Interactive flow of the CLI
def interactive_mode():
    questions = [
        inquirer.List('backend_language',
                      message="What backend language do you want to use?",
                      choices=backend_languages,
                     ),
        inquirer.List('frontend_language',
                      message="What frontend language do you want to use?",
                      choices=frontend_languages,
                     ),
        inquirer.List('database',
                      message="What database do you want to use?",
                      choices=databases,
                     )
    ]
    answers = inquirer.prompt(questions)
    return answers['backend_language'], answers['frontend_language'], answers['database']

# Setup for the Single Command flow of the CLI
def command_line_mode(args):
    backend_language, frontend_language, database = args.backend, args.frontend, args.db

    if backend_language not in backend_languages:
        raise ValueError(f"Invalid backend language. Choose from {backend_languages}")
    
    if frontend_language not in frontend_languages:
        raise ValueError(f"Invalid frontend language. Choose from {frontend_languages}")

    if database not in databases:
        raise ValueError(f"Invalid database. Choose from {databases}")
    
    return backend_language, frontend_language, database

def main():

    # Create the Argument Parser
    parser = argparse.ArgumentParser(description="Gather project requirements.")
    parser.add_argument('-backend', type=str, help="Backend language of choice")
    parser.add_argument('-frontend', type=str, help="Frontend language of choice")
    parser.add_argument('-db', type=str, help="Database of choice")
    
    args = parser.parse_args()

    # Check if any arguments are passed
    if not any(vars(args).values()):
        backend_language, frontend_language, database = interactive_mode()
    else:
        try:
            backend_language, frontend_language, database = command_line_mode(args)
        except ValueError as e:
            print(e)
            return
    
    print(f"Backend Language: {backend_language}")
    print(f"Frontend Language: {frontend_language}")
    print(f"Database: {database}")

if __name__ == "__main__":
    main()
