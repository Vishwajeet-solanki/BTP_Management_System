<p align="center">
  <img src="https://cdn-icons-png.flaticon.com/512/6295/6295417.png" width="100" />
</p>
<p align="center">
    <h1 align="center">BTP_MANAGEMENT_SYSTEM</h1>
</p>
<p align="center">
    <em>No BT for BTP!!!</em>
</p>
<p align="center">
	<img src="https://img.shields.io/github/license/Vishwajeet-solanki/BTP_Management_System?style=flat&color=0080ff" alt="license">
	<img src="https://img.shields.io/github/last-commit/Vishwajeet-solanki/BTP_Management_System?style=flat&logo=git&logoColor=white&color=0080ff" alt="last-commit">
	<img src="https://img.shields.io/github/languages/top/Vishwajeet-solanki/BTP_Management_System?style=flat&color=0080ff" alt="repo-top-language">
	<img src="https://img.shields.io/github/languages/count/Vishwajeet-solanki/BTP_Management_System?style=flat&color=0080ff" alt="repo-language-count">
<p>
<p align="center">
		<em>Developed with the software and tools below.</em>
</p>
<p align="center">
	<img src="https://img.shields.io/badge/HTML5-E34F26.svg?style=flat&logo=HTML5&logoColor=white" alt="HTML5">
	<img src="https://img.shields.io/badge/Python-3776AB.svg?style=flat&logo=Python&logoColor=white" alt="Python">
	<img src="https://img.shields.io/badge/Flask-000000.svg?style=flat&logo=Flask&logoColor=white" alt="Flask">
</p>
<hr>

##  Quick Links

> - [ Overview](#overview)
> - [ Features](#features)
> - [ Repository Structure](#repository-structure)
> - [ Modules](#-modules)
> - [ Getting Started](#getting-started)
>   - [ Installation](#installation)
>   - [ Running BTP_Management_System](#running-BTP_Management_System)
>   - [ Screenshots](#screenshots)
> - [ Testing](#testing)
> - [ Contributing](#contributing)
> - [ Acknowledgments](#acknowledgments)

---

##  Overview

The BTP Management System is designed to facilitate the management of BTP (Bachelor Thesis Project) allocations, applications, and report submissions using a NoSQL database. This system caters to the needs of students and professors by providing a seamless interface for applying to projects, tracking application status, and managing project approvals and evaluations.

---

##  Features

- User authentication and authorization for students, professors, and admins.
- Project listing, searching, and application management for students.
- Application review, approval, and rejection process for professors and co-guides.
- Final approval workflow involving the Head of Department (HOD).
- Comprehensive BTP report submission and grading system.
- Flexibility of MongoDB to handle varying document structures.


---

##  Repository Structure

```sh
└── BTP_Management_System/
    ├── README.md
    ├── __pycache__
    │   └── app.cpython-310.pyc
    ├── app.py
    ├── requirements.txt
    ├── static
    │   ├── 2.png
    │   ├── chip.png
    │   ├── reg.jpg
    │   └── visa.png
    └── templates
        ├── application_list.html
        ├── apply_to_co_guide.html
        ├── approved_list.html
        ├── btp_list.html
        ├── co_guide_applications.html
        ├── confirm_project.html
        ├── forgot_password.html
        ├── list_and_delete_applications.html
        ├── login.html
        ├── marks_submissions.html
        ├── profile.html
        ├── reset_password.html
        ├── select_co_guides.html
        ├── set_submission_details.html
        ├── signup.html
        ├── submit_report.html
        ├── upload_project.html
        ├── verify_otp.html
        ├── view_marks.html
        ├── view_projects.html
        └── view_users.html
```

---

##  Modules


| File                                                                                                   | Summary                                      |
| ---                                                                                                    | ---                                          |
| [requirements.txt](https://github.com/Vishwajeet-solanki/BTP_Management_System/blob/main/requirements.txt) | Dependencies for running the application |
| [app.py](https://github.com/Vishwajeet-solanki/BTP_Management_System/blob/main/app.py)                     | Main application file            |



| File                                                                                                                                               | Summary                                                                 |
| ---                                                                                                                                                | ---                                                                     |
| [list_and_delete_applications.html](https://github.com/Vishwajeet-solanki/BTP_Management_System/blob/main/templates/list_and_delete_applications.html) | Manage student applications |
| [approved_list.html](https://github.com/Vishwajeet-solanki/BTP_Management_System/blob/main/templates/approved_list.html)                               | View approved applications                |
| [upload_project.html](https://github.com/Vishwajeet-solanki/BTP_Management_System/blob/main/templates/upload_project.html)                             | Form for professors to upload projects               |
| [login.html](https://github.com/Vishwajeet-solanki/BTP_Management_System/blob/main/templates/login.html)                                               | User login page                     |
| [profile.html](https://github.com/Vishwajeet-solanki/BTP_Management_System/blob/main/templates/profile.html)                                           |User profile view                      |
| [btp_list.html](https://github.com/Vishwajeet-solanki/BTP_Management_System/blob/main/templates/btp_list.html)                                         | List of available BTP projects                     |
| [verify_otp.html](https://github.com/Vishwajeet-solanki/BTP_Management_System/blob/main/templates/verify_otp.html)                                     | OTP verification page                   |
| [view_projects.html](https://github.com/Vishwajeet-solanki/BTP_Management_System/blob/main/templates/view_projects.html)                               | View projects page                |
| [apply_to_co_guide.html](https://github.com/Vishwajeet-solanki/BTP_Management_System/blob/main/templates/apply_to_co_guide.html)                       | Form for applying to co-guides            |
| [co_guide_applications.html](https://github.com/Vishwajeet-solanki/BTP_Management_System/blob/main/templates/co_guide_applications.html)               | View co-guide applications        |
| [confirm_project.html](https://github.com/Vishwajeet-solanki/BTP_Management_System/blob/main/templates/confirm_project.html)                           | Confirm project application page              |
| [view_users.html](https://github.com/Vishwajeet-solanki/BTP_Management_System/blob/main/templates/view_users.html)                                     | Admin view for managing users                   |
| [set_submission_details.html](https://github.com/Vishwajeet-solanki/BTP_Management_System/blob/main/templates/set_submission_details.html)             | Set BTP submission details form       |
| [submit_report.html](https://github.com/Vishwajeet-solanki/BTP_Management_System/blob/main/templates/submit_report.html)                               | Form for students to submit BTP reports                |
| [application_list.html](https://github.com/Vishwajeet-solanki/BTP_Management_System/blob/main/templates/application_list.html)                         | List of student applications             |
| [reset_password.html](https://github.com/Vishwajeet-solanki/BTP_Management_System/blob/main/templates/reset_password.html)                             | Password reset form              |
| [signup.html](https://github.com/Vishwajeet-solanki/BTP_Management_System/blob/main/templates/signup.html)                                             | User signup page                       |
| [select_co_guides.html](https://github.com/Vishwajeet-solanki/BTP_Management_System/blob/main/templates/select_co_guides.html)                         | Form for selecting co-guides             |
| [marks_submissions.html](https://github.com/Vishwajeet-solanki/BTP_Management_System/blob/main/templates/marks_submissions.html)                       | View and submit BTP marks            |
| [view_marks.html](https://github.com/Vishwajeet-solanki/BTP_Management_System/blob/main/templates/view_marks.html)                                     | View submitted BTP marks                   |
| [forgot_password.html](https://github.com/Vishwajeet-solanki/BTP_Management_System/blob/main/templates/forgot_password.html)                           | Forgot password form              |

---

##  Getting Started

***Requirements***

Ensure you have the following dependencies installed on your system:

* **Python**: `at least version 3`

###  Installation

1. Clone the BTP_Management_System repository:

```sh
git clone https://github.com/Vishwajeet-solanki/BTP_Management_System
```

2. Change to the project directory:

```sh
cd BTP_Management_System
```

3. Install the dependencies:

```sh
pip install -r requirements.txt
```

###  Running BTP_Management_System

Use the following command to run BTP_Management_System:

```sh
python app.py
```

###  Screenshots
1. Sign Up
![image](https://github.com/Vishwajeet-solanki/BTP_Management_System/assets/108367037/d38c117a-14df-4f66-8ab9-c33900e2761e)
2. Login
![image](https://github.com/Vishwajeet-solanki/BTP_Management_System/assets/108367037/ccfa3d9f-1c20-48c4-949b-8c7bc446b80c)
3. Forgot password
![image](https://github.com/Vishwajeet-solanki/BTP_Management_System/assets/108367037/45dad357-94b4-425d-8f06-4b9a65b54bd8)
4. View Profile
![image](https://github.com/Vishwajeet-solanki/BTP_Management_System/assets/108367037/5a38d37e-f5cb-45cf-97f5-369d75744dc1)
5. Project List
![image](https://github.com/Vishwajeet-solanki/BTP_Management_System/assets/108367037/97d6ee5d-e66b-40b3-b162-7a7f4f77c07d)
6. Search in Project List (below is example of search by Department) 
![image](https://github.com/Vishwajeet-solanki/BTP_Management_System/assets/108367037/b3779d17-49b9-4260-9c3a-f7b5a790d398)
7. View Pending Approvals (by Faculty): 
![image](https://github.com/Vishwajeet-solanki/BTP_Management_System/assets/108367037/5ea85f56-6f78-4d5f-8dfc-adb009d7c7a4)
8. View approved applications (by Faculty): 
![image](https://github.com/Vishwajeet-solanki/BTP_Management_System/assets/108367037/707cf223-d534-400c-b154-cc5dde3c3e09)
9.  Upload new project (by Faculty)
![image](https://github.com/Vishwajeet-solanki/BTP_Management_System/assets/108367037/f80956f2-9c35-4d3d-b4b6-5c1d96e582b1)
10. Forgot Password OTP
![image](https://github.com/Vishwajeet-solanki/BTP_Management_System/assets/108367037/3a6a29de-1a4d-4319-83b1-55eeddde128b)

---
## Testing
Achieved **80% code coverage** across a 743-line Flask-based BTP Report Management System by implementing comprehensive unit and integration tests using pytest.
![image](https://github.com/Vishwajeet-solanki/BTP_Management_System/assets/108367037/d7a3275d-f70c-4822-9bfe-cc80fddca3f6)

Use the following command to test BTP_Management_System with test_app.py:
```sh
pytest --cov=app
```
---
##  Contributing

Contributions are welcome! Here are several ways you can contribute:

- **[Submit Pull Requests](https://github.com/Vishwajeet-solanki/BTP_Management_System/blob/main/CONTRIBUTING.md)**: Review open PRs, and submit your own PRs.
- **[Join the Discussions](https://github.com/Vishwajeet-solanki/BTP_Management_System/discussions)**: Share your insights, provide feedback, or ask questions.
- **[Report Issues](https://github.com/Vishwajeet-solanki/BTP_Management_System/issues)**: Submit bugs found or log feature requests for Btp_management_system.

<details closed>
    <summary>Contributing Guidelines</summary>

1. **Fork the Repository**: Start by forking the project repository to your GitHub account.
2. **Clone Locally**: Clone the forked repository to your local machine using a Git client.
   ```sh
   git clone https://github.com/Vishwajeet-solanki/BTP_Management_System
   ```
3. **Create a New Branch**: Always work on a new branch, giving it a descriptive name.
   ```sh
   git checkout -b new-feature-x
   ```
4. **Make Your Changes**: Develop and test your changes locally.
5. **Commit Your Changes**: Commit with a clear message describing your updates.
   ```sh
   git commit -m 'Implemented new feature x.'
   ```
6. **Push to GitHub**: Push the changes to your forked repository.
   ```sh
   git push origin new-feature-x
   ```
7. **Submit a Pull Request**: Create a PR against the original project repository. Clearly describe the changes and their motivations.

Once your PR is reviewed and approved, it will be merged into the main branch.

</details>

---

##  Acknowledgments

- Special thanks to Prof. Pabitra Mitra and Prof. K S Rao for guidance and mentorship throughout the project.

[**Return**](#quick-links)

---
