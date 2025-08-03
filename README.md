# College-Management-System

# Backend Part:

->The system uses Flask to dynamically render web pages based on 
user interactions and data stored in the backend;

->Pages like Results, Study Materials, and College Updates are 
dynamically populated with data;

# Frontend part:

->The system uses custom CSS styles and Google Fonts to provide a visually appealing and user-friendly interface;

->The navigation bar is centered and responsive, ensuring easy access to all features;

# Working procedure:

->The system supports two types of users: Students and Admin.

->Students can log in using their USN (University Seat Number) 
and password to access their semester-wise results;

->Admin can log in using predefined credentials to manage student results, 
add/remove college updates, and view contact messages;

->Students can access semester-wise study materials with links to resource;

->Students can view the latest college updates;

->Admin can update the marks of any student for any semester if they want;

->Admin can view messages sent by users through the contact form;

->All admin actions are logged with timestamps;

# Motivation for this Project:

->This project aims to streamline college management tasks such as result
viewing, updating study materials, and sharing college updates;

->The admin dashboard simplifies tasks like updating results and managing college 
updates, reducing manual effort and improving efficiency;

->This project was motivated by the desire to learn and apply web development skills
using Flask, HTML, CSS, and Python.

# Challenges Faced with Solutions:

->Challenge: Managing and displaying dynamic data like student results, college updates
required careful handling of data structures and Flask templates;

->Solution: Used Python dictionaries to store data and Flask's render_template_string 
to dynamically generate HTML content;

# Students and Admin Credentials

Admin username : nairy , Password : nairy123

Student Credential : username : USN1 to USN20 , Password : pass1 to pass20 (USN and pass number should be match)

# Procedure to Run

To access this project : python app.py


