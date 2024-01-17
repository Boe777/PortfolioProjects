🛠 How to Run

Ensure:
      *Python and Django are installed.
      *Clone the repository to your local machine.
      *Navigate to the project directory.
      *Add your Pixabay API to views.py.
      *Add your django key to settings.py.
      *Run the following commands in the terminal:
          python manage.py migrate
          python manage.py runserver
      *Open your web browser and go to http://127.0.0.1:8000/ to view the website.

Notes
Make sure to replace 'YOUR_KEY' with your actual API keys in the Django views.py file and the Pixabay API key in the main.js file.

Ensure that you have Python, Pip, Node.js, and npm installed on your system before running the application.

The application is set to run in DEBUG mode. In a production environment, it is crucial to set the DEBUG setting to False and configure proper security measures.

Features
Country and Race Mapping:

The application fetches country information from 'Rest Countries' API and maps country names to their respective demonyms (races).
Dynamic Meal Selection:

Users can select a country, and the application dynamically loads associated meals for that country using 'The Meal DB' API.
Detailed Meal Information:

Upon selecting a meal, users can view detailed information, including ingredients and cooking instructions.
Dynamic Image Retrieval:

The application attempts to fetch a relevant food image from Pixabay using the meal name.

Technologies Used
Django (Backend):

A Python web framework used to handle backend logic, routing, and database interactions.
Next.js (Frontend):

A React framework used for building the frontend, providing a seamless and efficient user interface.
Tailwind CSS:

A utility-first CSS framework used for styling the frontend components.
Pixabay API:

Used to fetch food images based on meal names.
The Meal DB API:

Used to retrieve meal information based on country.
Rest Countries API:

Used to fetch country information, including country names and demonyms.


## 🤝 Contribution

If you find any issues with my projects or have suggestions for improvement, please open an issue or submit a pull request. Your contributions are highly appreciated!

## 📧 Contact

Feel free to reach out to me at [kaankuscu777@gmail.com](mailto:kaankuscu777@gmail.com) if you have any questions or inquiries.

---
© 2024 [Kaan Kuscu]
