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
- The user can see their project on 3 separate maps provided by mapbox – neighborhood site plan, 3D map, and city map.

### Included in Project Information
What is included in project information?
- Functions in geocoding.py (code developed by Google Maps) help automatically derive latitude and longitude of the given address. The coordinates get plugged into the mapbox JavaScript tags to correctly showcase the location of the project. In list.html the map displays all of the active projects the user currently has with their respective locations.
- Functions in site_info.py help extract informatino from Zimas and Zola databases for the City of Los Angeles and New York City. Functions such as zimas_info and zola_info analyze whether the project falls under their governing authorities, and if yes, queries public databases to locate the site and information pertaining to the site. In M.A.P 1.0 version, the information extracted includes lot area, parcel number, zoning, year built, lot width, and lot depth. This information is logged into the SQL table "projectinfo".

### Deleting a project
The projects never get deleted, but their status changes in the SQL database to "Deleted". Javascript double checks whether the user confirms the deletion of the project.

### Site Inquiry
Aside from creating and changing projects, the user can simply inquire about the site. The user can fill out the address (supplemented with Google Maps Autocomplete function) and see the map corresponding to the location and latitude/longitude of the project. Then, the user has the option to save this inquiry as a new project.

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
