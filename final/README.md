# M.A.P. Web Built Environment Tool
#### Video Demo:  <URL HERE>
## Description:

### General Information about M.A.P
The story of M.A.P starts on University of Southern California campus where a certain B.Arch student was dissatisfied with how the world of architecture was set up. Why were all these architects spending hours on end on monotonous mundane tasks that could be automated? A need for an optimized solution has arisen.

Who is M.A.P for? Any person professionally involved in the realm of built environment. Feel free to add your projects and understand the opportunities and limitations of each site. Whether you are an architect, real estate developet, civil engineer, or an investor, you will find M.A.P very useful.

The web application utilizes HTML/CSS/JS framework alongside Python, Flask, and SQL. **The main goal is to let a user create an account, add various physical sites to their portfolio (limited to the U.S. for now), and instantly review information about the site including zoning, lot area, year built, etc.** No more struggling when it comes down to obtaining site information! The project is saved in each user's individual library. The maps displayed on the project page showcase the vicinity map, 3D view of the neighborhood, and city map.

### SQL database
The project has a critical map.db file where project data is stored. Three tables are currently included in map.db file: users, projects, and project info.
- "Users" table contains unique user id, username and hashed password.
- "Projects" table contains user id, unique project id, title, address of the site, date created, date changed, municipal authority governing the site, status ("Active" or "Deleted"), latitude, longitude, and notes.
- "Project Info" table contains information obtained through third-party websites. For now, it is only able to collect data from Zimas (City of Los Angeles) and Zola (New York City). Queries for projects with other site locations yield "NA" results in this table. "Project info" table contains project id, address, lot area, parcel number, zoning, year built, lot width, and lot depth.


### User Account Functionality
The users can take advantage of the following functions: register, log in, log out, view their projects and account stats.
- Home page (home.html) greets the users with the option to log in or register and spinning mapbox map.
- Registering (def register from app.py) requires for users to input their unique username and password. Hash function encodes the password.
- If the conditions aren't satisfied, apology function from helpers.py is rendered.
- Users can log in if their account already exists (def login from app.py).
- Once logged in, users land on userhome.html. From there, they can view a list of their projects, create a new project, submit a site inquiry, or view account information.
- Viewing account information redirects user to account.html via def account in app.py. The webpage displays username of the user, number of active projects and number of deleted projects (extracted from the SQL map.db file).
- Log out (def logout from app.py) logs user out.

### Creating and Changing Projects
MAP Web allows users to create new projects, view a list of existing projects, change and delete projects, as they see fit.
- Via list.html, they can see all of their active projects and press on the links for individual project. Each project has its own individual page. Google Maps Autocomplete provides functionality for address input.

### Included in Project Information

### Deleting a project

### Site Inquiry


### Plans for the Future
M.A.P. will continue expanding to cover other municipalities besides Los Angeles and New York. The goal is to create a system that unites city codes across the United States.

### List of files
Functionality files:
- app.py
- helpers.py
- geocoding.py
- site_info.py

Styles files:
- styles.css

Templates:
- layout.html (main file)
- account.html
- apology.html
- delete.html
- home.html
- inquiry.html
- list.html
- login.html
- new.html
- project.html
- register.html
- userhome.html
