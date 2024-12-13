# Flask Final Exam

**Directions**: For this project, you will build a website with a Flask backend that will keep track of students
grades in their courses based on the assignments in the course. You will have to create a database and a model to work
with it, build the front end (AI is highly encouraged for this part), and create your controller to link it all
together.

## Part 1 - Model (35 Points)

When using the MVC architecture, it is very common to start with building your model first. Follow the steps below to
start creating your model for you database.

1. Use the following structure to create functions that add to and access all the data inside the database. Assume all
   grading categories are Formative, Summative, Final Exam with 30, 50, 20 weights, respectively.

```json
{
  "Courses": {
    "Computer Science": {
      "Assignments": {
        "Formative": {
          "Homework 1": 75,
          "Quiz 1": 85,
          "Homework 2": 95
        },
        "Summative": {
          "Test 1": 90,
          "Project 1": 100
        },
        "Final Exam": 99
      },
      "isAP": true,
      "Average": 95
    }
  },
  "Numeric GPA": 93.25,
  "Unweighted GPA": 3.75,
  "Weighted GPA": 3.8
}
```

2. When creating the data within the database, initialize the *Numeric GPA, Unweighted GPA, Weighted GPA, and Final
   Exam* to -1. This way you can recognize if the values have not been set, and use the add_assignment function to set
   the values for each
   course and all the GPAs.

3. There are quite a few functions that you will need in order to successfully manipulate the database. Create functions
   to do the following:

    - **get_all_courses()** - returns a list of all course keys
    - **get_course(course)** - returns a dictionary of the param course
    - **add_assignment(course, category, name, grade)** - creates a new assignment in the specified category of that
      class and assigns it a grade. This function will also call *set_course_average(), set_numeric_gpa(),
      set_unweighted_gpa(), and set_weighted_gpa()*. See those methods below.
    - **remove_assignment(course, category, name)** - removes assignment from category of course. This function will
      also call *set_course_average(), set_numeric_gpa(), set_unweighted_gpa(), and set_weighted_gpa()*. See those
      methods below.
    - **set_final_exam(course, grade)** - sets the final exam grade of a course. This function will also call
      *set_course_average(), set_numeric_gpa(), set_unweighted_gpa(), and set_weighted_gpa()*. See those methods below.
    - **get_final_exam(course)** - returns the final exam score
    - **set_course_average(course)** - sets the course average key for specified course. Uses *get_category_average(
      course, category)*. See below:
    - **get_category_average(course, category)** - Helper method that returns the average of a category within a courses
      assignments. Used in set_course_average(course) for Formative and Summative.
    - **get_course_average(course)** - simple getter method used to get the Average key from a course
    - **get_letter_grade(course)** - returns the courses' Average as a letter grade using the table seen below.
    - **def get_course_qp(course, isAP=False)** - returns the quality points for a course based on average. isAP is
      defaulted to False for quickly calculating unweighted GPA. Overwrite the parameter when needed during weighted GPA
      calculations
    - **set_numeric_gpa()** - sets the numeric GPA key by adding all course averages together and dividing by total
      number of courses
    - **get_numeric_gpa()** - returns Numeric GPA value
    - **set_unweighted_gpa()** - sets Unweighted GPA based on the quality points in the table below
    - **get_unweighted_gpa()** - returns Unweighted GPA value
    - **set_weighted_gpa()** - sets the weighted GPA based on the quality points in the table below. Only AP classes
      earn weights
    - **get_weighted_gpa()** - returns Weighted GPA value
    - **setup_db()** - deletes any keys in current database and creates initial database using some of the above methods

   | Letter |	Range | GPA Quality Points | Weighted GPA Quality Points |
                                           | :----: | :----: |   :----:   |    :----:           |
   |  A		 | 90-100	|		   4.0   |      5.0            |
   |  B		 | 80-89	|		   3.0   |      4.0            |
   |  C		 | 71-79	|	     2.0   |      3.0            |
   |  D		 | 70			|      1.0   |      2.0            |
   |  F		 |69 and Below|	 0.0   |      0.0            |

***Note***: When a new assignment is added to a course the courses average and all three forms of GPA need to be
updated. This will keep the number of calculations to a minimum when moving from page to page.  
***Also Note***: You may need more than the functions listed above, and comment your functions using docstrings!

4. Create and test out your database. This can be easily done writing code at the bottom of your controller file.

## Part 2 - Viewing with the View (25 Points)

In this section you will create 2 html docs. One will be your homepage and the other will display the specific
assignments for a single course. You are encouraged to use AI for the creation of the HTML and CSS. Learning to write a
good prompt for AI will become a valuable tool as you enter the world of IT over the next 5 years.

**This part only includes handling the actions to render either html template. You do not need to incorporate routes to
handle adding/removing grades and final exams. We will do this in part 3.**

You might need to reference the [Jinja Control Structures Docs](https://tedboy.github.io/jinja2/templ11.html).

1. Use ChatGPT to create your homepage (*index.html*). Be detailed and descriptive. Focus on have the AI get the content
   on the page before worrying about how it all looks. Use the default route to render this page and pass any jinja
   variables through the template. Your homepage should contain the following:

    - All course names with the average and letter grade of each course.
    - Numeric GPA, Unweighted GPA, and Weighted GPA
    - Links (using nav or ul elements) to all the individual courses and one link that directs back to the homepage
    - Header for the page

2. Use ChatGPT to create a page called *course_view.html*. This page uses the GET array to display a specific course.
   This means that any of the links from the homepage to a specific course will route to this page and pass the course
   name through the GET array. Focus on getting all the data displayed, **making all the buttons work will be in
   Part 3**. This page needs to contain the following:

    - Header for the page including the course name
    - Links (using nav or ul elements) to all the individual courses and one link that directs back to the homepage
    - Course Average
    - All formative assignments with both name and grade
    - All summative assignments with both name and grade
    - Final Exam score (should be 'NA' if score is -1)
    - Buttons that remove an assignment or reset the final exam grade
    - A form that allows the user to add a new assignment or set the final exam grade

## Part 3 - Adding Functionality (25 Points)

This part will require you to add the functionality to all the form elements you added in the previous part. This
will most likely require you to edit parts of your html templates and add new routes to your controller. Also, do not be
afraid to add new functions to your model if they are needed.

1. Add a new route and function to handle adding a new assignment via the form on your course_view template. This
   function and the form that triggers it should be able to create a Summative, Formative, or update the Final Exam.
   When testing this, make sure the homepage is updated when the new assignment or final exam is added.
2. Create one or two new routes and functions to handle the remove assignment and reset final exam buttons within the
   course_view template. Resetting the final exam should set it back to -1 which will in turn display 'NA'. When testing
   this, make sure the homepage is updated when the new assignment or final exam is added.

## Part 4 - Validation & Front-End Clean Up (10 Points)

This part will have you briefly complete some data validation for the only input form on the website. You will also make
the front end (html templates and css) look clean and professional.

1. Your model should only include functions that are attached to routes, and our goal should be to keep the controller
   as clean as possible. If you feel that you need to create helper methods, make a new python file in the model and
   import it. There are 3 pieces of data to validate within the add assignment / final exam form. Please make sure the
   following is tested.

- A category, *Formative, Summative, or Final Exam*, must be selected
- Assignment Name cannot be empty for a Formative or Summative, but can be empty for a final exam
- Grade must be an integer between 0 and 100, inclusive

2. Utilize Jinja to create error text that appears next to your form when data is not valid (this error text should only
   appear after an invalid input is caught). The error message must correspond to the reason for error. Also, all data *
   *does not** have to remain on submit even if there is an error. However, if you have the time, feel free to add in
   this feature.
3. You also need a success message to show when an assignment or final exam has been added/updated. The success message
   must contain the assignment name, category (if applicable), and grade. For example, "Homework 1 has been added to
   Formative with a grade of 93". Make sure to differentiate between success messages and error messages (usually green
   and red respectively).

**Hint**: If you are having trouble getting the error/success messages to pass through to your course view, then there
are a few quick tools you can use that might help. Try to stay away from the redirect function unless it is needed.

- ```Python
    @app.route('/course_view', methods=['GET'])
    def course_view(error_message="", success_message=""):
      course = request.args.get('course')
    ```
  Inside your add_assignment function you might try to return a call to course_view. You can rewrite the course_view
  function to have defaulted parameters that can set the error/success message. The only problem that arises is now
  there was no data passed through the get array (see fix below).
- ```HTML
    <form method="POST" action="/add_assignment?course={{ course }}">
    ```
  Notice that we can set a portion of the get array within the specified action of a form.

4. Your HTML templates should have a modern style to them (i.e. the look like a website that was made after 2010). Your
   content should be centered and the site should be easily navigable. Bootstrap can help improve the look of your site.
   ChatGPT can be great for explaining how certain parts of HTML can be improved using bootstrap.

## Part 5 - Multiple Users (5 Points)

In this part, you will refactor your project to handle multiple students via logging in. You will need to make changes
to your database, model, view, and controller.

1. Update your database to be able to hold multiple students. You will need a key for each student that will consist of
   their *lastName.firstName*. Each student will also need a key for *First Name*, *Last Name*, and *Hashed Password*.
   See the example below:

```json
{
  "doe.jane": {
    "First Name": "Jane",
    "Last Name": "Doe",
    "Hashed Password": "scrypt:32768:8:1$Qkauq9Xde373wXc0$d8abac7b51b495d19a2c19a9aa55564ac261edbb8dce1cfef440d4eb1365012ad9400b86cdc5a209b8322e39b2588ac8786986d7b0a2b76483709be08f457964",
    "Courses": {
      "Computer Science": {
        "Assignments": {
          "Formative": {
            "Homework 1": 75,
            "Quiz 1": 85,
            "Homework 2": 95
          },
          "Summative": {
            "Test 1": 90,
            "Project 1": 100
          },
          "Final Exam": 99
        },
        "isAP": true,
        "Average": 95
      }
    },
    "Numeric GPA": 93.25,
    "Unweighted GPA": 3.75,
    "Weighted GPA": 3.8
  }
}
```

**Hint:** When setting the hashed password, use the *generate_password_hash* from the werkzeug.security module to print
out the hash in console and move it into the database since this part will not include a form of registration.

2. Update you model and DAL accordingly. Since the entire base of the data structure has changed, you will need to make
   changes to accommodate this in almost all the functions. You will also need to create the following 3 functions and
   add them to your DAL:

- get_all_users_as_list()
- get_user_hashed_password(user)
- get_user_full_name(user)

3. Create a login page to go along with your project. The page should fit in well stylistically with the rest of the
   site. The login page will need a single form with inputs for username and password. You will not need a link to a
   registration page as this is not one of the core requirements. **If you and your partner do not
   feel comfortable with authentication via passwords, feel free to just authenticate using their username only.**

4. Create a login route to handle authentication, and update your other routes to only be accessed if the user is logged
   in. Make sure to use the session cookie!

5. Add a section to your index and course_view that show the *First* and *Last Name* of the user that is currently
   logged in along with a **Logout** button that can be pressed to clear the session cookie and reroute back to the
   login page.

6. Finally, build the login route! Then you are done!!!

## Extra Credit (5 Points)

Create a way for users to register via a registration page. During the registration process, they should be able to
create all the courses that they will be taking.