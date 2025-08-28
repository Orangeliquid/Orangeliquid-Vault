# Orangeliquid Vault

Orangeliquid Vault is a Streamlit front-end application that lets users create a single master password to access their vault. Within the vault, users can securely store login entries, keeping all credentials in one safe location. All entries are encrypted using Fernet and are salted and hashed for secure storage.

Entries can be searched by Service, Username, or Email, with partial matching for easier access. Users can also sort entries via a dropdown by A-Z, Z-A, or Most Recent. Within each entry, data is displayed with the password hidden by default, with the option to view it in plain text. Passwords are evaluated for strength. Users can edit entries and use the 'Generate Random Password' feature with customizable parameters.

IMPORTANT: If the master password is forgotten, all information will be lost due to encryption. Additionally, if .vault_salt, .secret_key, or vault.db are deleted, all data will be lost.


## Table of Contents

- [Installation](#installation)
- [Getting-Started](#getting-started)
- [Screenshots](#screenshots)
  - [Master-Password-Creation](#master-password-creation)
  - [Login-With-Master-Password](#login-with-master-password)
  - [Entry-Creation](#entry-creation)
  - [Generate-Random-Password](#generate-random-password)
  - [View-Entries](#view-entries)
  - [Search-Entries](#search-entries)
  - [Sort-Entries](#sort-entries)
  - [Edit-Entry](#edit-entry)
  - [Save-Edit-Entry](#save-edit-entry)
- [License](#license)

## Installation

To run Orangeliquid Vault, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/Orangeliquid/Orangeliquid-Vault
   cd Orangeliquid-Vault
   ```

2. Ensure UV is downloaded:
   - If UV is not downloaded on your system, download it via pip:
   ```bash
   pip install uv
   ```
   
3. Sync dependencies with UV:
   ```bash
   uv sync
   ```

## Getting Started

1. Navigate to Orangeliquid-Vault and open main.py
   - At the bottom under __main__ there are further directions.
   - in terminal run:
      ```bash
      uv run streamlit run main.py
      ```
2. IMPORTANT - On first run, you will be prompted to set a Master Password
   - Please remember this password. If forgot, all data will be lost.

3. Now that Master Password is set, Enter Master Password to log in

4. Notice the buttons at the top
   - Create New Entry
   - View All Entries
   - Exit Vault

5. Start by creating an entry
   - All fields are required besides Email and Notes.
   - Password may be set by user or generated via generate random password button found at the bottom of the form.
   - Password generation has multiple customizable criteria.
   - save entry.

6. View your new entry by clicking "View All Entries"

   Sorting
   - Chose your sorting method by selecting a category via the dropdown "Sort by".
   - Alternatively, use the search box and enter desired Service, Username, or Email to locate entries.
   - If no entries match your search, remove what you typed to return to all entries or search a new term.

   Entry Selection
   - Select an entry on the right and view entry data.
   - Notice your password being hidden, feel free to check the eye box on the right of password to view the password.

   Entry Information
   - Each entry will have the following information
   - Service at the top in orange
   - Username
   - Password hidden by dots unless eye box is pressed
   - All passwords are evaluated for strength based on Length, Digits, Symbols, Uppercase characters
   - Evaluation is seen under password with description of strength and color 
   - Email if this data exists in entry
   - Notes if this data exists in entry
   - Created for creation timeline

   Edit Entry
   - You may edit your entry by pressing "Edit" on the top right of the entry.
   - The Generate Random Password option is preset once again, once generated, this new password will fill the New Password field.
   - If no data has been changed and a new password is not entered, pressing submit will alert you that nothing has changed.
   - Feel free to adjust info and press Save at the bottom left to update an entry.
   - If "Save" is not pressed, nothing in the entry will be updated.
   - Cancel Edit mode via the bottom right "Cancel" button.

8. Log out of vault by pressing "Exit Vault" button at the top right of the application

9. Check Project within Orangeliquid-Vault to verify the following files have been created:
   - .vault_salt
   - .secret_key
   - vault.db

10. DO NOT DELETE FILES ABOVE TO KEEP CURRENT VAULT DATA or Delete all files above to start new on when running the application again. 

## Screenshots

### Master Password Creation
<img width="1018" height="735" alt="OV_Master_Set" src="https://github.com/user-attachments/assets/b5360f93-9525-49b6-91ee-4316e2b4eddd" />

### Login With Master Password
<img width="1095" height="677" alt="OV_Login" src="https://github.com/user-attachments/assets/b2686ce3-60d8-44a4-818c-8e4657cb4bc1" />

### Entry Creation
<img width="1159" height="851" alt="OV_Entry_Creation" src="https://github.com/user-attachments/assets/9f0654be-24f0-4b35-b32e-8f66d715f800" />

### Generate Random Password
<img width="853" height="819" alt="OV_Gen_Ran_Pass" src="https://github.com/user-attachments/assets/c4f13793-0e5a-4ed9-a9bd-23bf01129628" />

### View Entries
<img width="1088" height="851" alt="OV_View_Ent" src="https://github.com/user-attachments/assets/4cd19ff2-a00e-4dcc-96ed-aa45fbf4ee83" />

### Search Entries
<img width="1123" height="845" alt="OV_Search_Ent" src="https://github.com/user-attachments/assets/05802e9e-e509-4f26-8ed7-fd28bb79b05f" />

### Sort Entries
<img width="968" height="864" alt="OV_Sort_Ent" src="https://github.com/user-attachments/assets/c4f47c46-0c45-4c85-b4b0-2365c24c4254" />

### Edit Entry
<img width="969" height="891" alt="OV_Edit_Ent" src="https://github.com/user-attachments/assets/2e641341-9184-4c7e-9aca-3527e4fe587f" />

### Save Edit Entry
<img width="959" height="859" alt="OV_Edit_Saved" src="https://github.com/user-attachments/assets/29b6314a-a73f-417a-8efb-b41f459f33c7" />

## License
This project is licensed under the [MIT License](LICENSE.txt).
