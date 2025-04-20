import pandas as pd
from faker import Faker
import random 


fake = Faker() 
email_count = {} 
def emails(name,num):
    unique_emails = []
    for i in range(num):
        whole_name = name[i].replace(" ", "")
        base = f"{whole_name}@uwi.mona.edu"
        count = email_count.get(base, 0)

        email = base if count == 0 else f"{whole_name}{count + 1}@uwi.mona.edu"
        email_count[base] = count + 1
        unique_emails.append(email)
    return unique_emails

course_names = {

    "COMP": [
        "Intro to Computing", "Data Structures", "Algorithms", "Operating Systems",
        "Software Engineering", "Database Systems", "Artificial Intelligence", "Computer Networks",
        "Web Development", "Mobile App Development", "Cybersecurity Fundamentals", "Machine Learning",
        "Cloud Computing", "Human-Computer Interaction", "Compiler Design"
    ],

    "PHYS": [
        "General Physics", "Mechanics", "Electromagnetism", "Thermodynamics",
        "Quantum Physics", "Optics", "Nuclear Physics", "Astrophysics",
        "Fluid Dynamics", "Solid State Physics", "Mathematical Methods for Physicists"
    ],

    "MATH": [
        "Calculus I", "Calculus II", "Linear Algebra", "Discrete Mathematics",
        "Probability Theory", "Abstract Algebra", "Differential Equations",
        "Numerical Methods", "Real Analysis", "Complex Analysis", "Topology"
    ],

    "CHEM": [
        "General Chemistry", "Organic Chemistry", "Inorganic Chemistry",
        "Physical Chemistry", "Analytical Chemistry", "Biochemistry",
        "Environmental Chemistry", "Industrial Chemistry", "Chemistry Lab Techniques"
    ],

    "BIOL": [
        "Intro to Biology", "Genetics", "Microbiology", "Cell Biology", "Ecology",
        "Human Anatomy", "Evolution", "Neuroscience", "Immunology", "Botany",
        "Zoology", "Molecular Biology"
    ],

    "ECON": [
        "Microeconomics", "Macroeconomics", "Econometrics", "Public Economics",
        "International Economics", "Game Theory", "Development Economics",
        "Behavioral Economics", "Financial Economics", "Economics of Education"
    ],

    "PSYC": [
        "Intro to Psychology", "Developmental Psychology", "Social Psychology",
        "Abnormal Psychology", "Cognitive Psychology", "Neuropsychology",
        "Psychological Assessment", "Forensic Psychology", "Research Methods in Psychology"
    ],

    "HIST": [
        "World History", "Ancient Civilizations", "Modern History", "American History",
        "European History", "History of the Caribbean", "African History",
        "History of Revolutions", "Colonialism and Empire"
    ],

    "ENGL": [
        "English Composition", "Creative Writing", "Literary Analysis",
        "Shakespeare Studies", "Modern Literature", "Postcolonial Literature",
        "Introduction to Linguistics", "Technical Writing", "English for Academic Purposes"
    ],

    "PHIL": [
        "Intro to Philosophy", "Ethics", "Logic", "Philosophy of Mind",
        "Political Philosophy", "Existentialism", "Philosophy of Science",
        "Eastern Philosophy", "Philosophy of Religion"
    ],
    "STAT": [
        "Intro to Statistics", "Probability and Statistics", "Regression Analysis",
        "Statistical Inference", "Time Series Analysis", "Multivariate Statistics",
        "Bayesian Statistics", "Statistical Computing", "Sampling Techniques"
    ],

    "SOCI": [
        "Intro to Sociology", "Social Theory", "Urban Sociology",
        "Sociology of Education", "Gender Studies", "Criminology",
        "Race and Ethnic Relations", "Sociology of Religion", "Sociological Research Methods"
    ],

    "GEOG": [
        "Physical Geography", "Human Geography", "Cartography",
        "Geographical Information Systems", "Environmental Geography",
        "Urban Geography", "Climate Change and Society", "Geopolitics"
    ],

    "ARTS": [
        "Art History", "Painting Techniques", "Sculpture Basics", "Modern Art",
        "Photography", "Digital Art", "Visual Communication", "Graphic Design Fundamentals"
    ],

    "MUSC": [
        "Music Theory", "History of Music", "Composition", "Instrumental Techniques",
        "Choral Studies", "Music Technology", "Ethnomusicology", "Jazz Studies",
        "Digital Music Production"
    ]

}

subject_codes = [
"COMP",  # Computer Science
"PHYS",  # Physics
"MATH",  # Mathematics
"CHEM",  # Chemistry
"BIOL",  # Biology
"ECON",  # Economics
"PSYC",  # Psychology
"HIST",  # History
"ENGL",  # English
"PHIL",  # Philosophy
"STAT",  # Statistics
"SOCI",  # Sociology
"GEOG",  # Geography
"ARTS",  # Arts
"MUSC",  # Music
]

def insert_person(type,num):
    data = pd.DataFrame()
    
    if type == "Student":
        ids = [fake.unique.random_int(min=620000000, max=629999999) for _ in range(num)]
        role = [type for _ in range(num)]

        data["user_id"] = ids
        data["role"] = role             
        return data
    
    elif type == "Lecturer":
        ids = [fake.unique.random_int(min=1000000, max=1009999) for _ in range(num)]
        role = [type for _ in range(num)]

        data["user_id"] = ids
        data["role"] = role 
        return data
    
    elif type == "Admin":
        ids = [fake.unique.random_int(min=99900000, max=99999999) for _ in range(num)]
        role = [type for _ in range(num)]
        
        data["user_id"] = ids
        data["role"] = role 
        return data

def insert_course(num):
    data = pd.DataFrame()
    used_codes = set()
    course_names_list = []
    course_codes = []

    for _ in range(num):
        subject = random.choice(subject_codes)

 
        course_name = random.choice(course_names.get(subject, ["Special Topics"]))

        while True:
            number = f"{random.choice(['1', '2', '3'])}{random.randint(100, 999)}"
            code = f"{subject}{number}"
            if code not in used_codes:
                used_codes.add(code)
                break

        
        course_names_list.append(course_name)
        course_codes.append(code)

    data["Course ID"] = course_codes
    data["Course_Name"] = course_names_list


    return data

def Student_Course(students,courses):

    s_id = students["user_id"].tolist()
    c_id = courses["Course ID"].tolist()
    S_C_num = [random.randint(3,6) for _ in range(len(s_id))]

    c_s_id_list ={}
    s_c_id_list = {}
    for i in range(0,len(s_id)):
        lst = []
        for j in range(0,S_C_num[i]):

            keys = list(s_c_id_list.keys())
            course = str(random.choice(c_id))

            while course in lst:
                course = str(random.choice(c_id))
                

            lst.append(course)

            if course in (keys):
                s_c_id_list[str(course)] += 1
            else:
                s_c_id_list[str(course)] = 1


        c_s_id_list[str(s_id[i])] = lst


    keys = list(s_c_id_list.keys())

    for key in keys:
        while (s_c_id_list[key]) < 10:
            i = random.randint(0,len(s_id)-1)
            if S_C_num[i] <= 5:
                if key not in c_s_id_list[str(s_id[i])]:
                    c_s_id_list[str(s_id[i])].append(str(key))
                    s_c_id_list[key] += 1
                    S_C_num[i] += 1
    
    return (c_s_id_list)

def Lecturers_course(lecturers,courses):
    l_id = lecturers["user_id"].tolist()
    c_id = courses["Course ID"].tolist()
    
    random.shuffle(c_id) 

    c_l_id_list = {str(l): [] for l in l_id}


    for i, lecturer in enumerate(l_id):
        course = c_id.pop()
        c_l_id_list[str(lecturer)].append(str(course))

    while c_id:
        course = c_id.pop()
        eligible_lecturers = [lid for lid, assigned in c_l_id_list.items() if len(assigned) < 5]

        if not eligible_lecturers:
            raise Exception("Not enough lecturers to assign all courses with current constraints")

        lecturer = random.choice(eligible_lecturers)
        c_l_id_list[str(lecturer)].append(str(course))

    return c_l_id_list

def default_login(users):
    data = pd.DataFrame()
    password= []

    for user in users:
        password.append(fake.password())
    
    data["user_id"] = users
    data["password"] = password
    return data

def login_insert(user,sql,user_type):
    sql.write(f"\n-- {user_type} Login Inserts\n")
    sql.write(
            f"""INSERT INTO Logins(user_id, user_password) Values\n""")
    for i in range(len(user["user_id"])):
        end = ",\n" if i < len(user["user_id"]) - 1 else "\n"
        sql.write(
            f"""("{user["user_id"][i]}","{user["password"][i]}"){end}\n""")
    sql.write(";\n")
    
def user_insert(user,sql,user_type):
    sql.write(f"\n-- {user_type} User Inserts\n")
    sql.write(f"""INSERT INTO User(user_id,role) Values\n""")
    for i in range(len(user["user_id"])):
        end = ",\n" if i < len(user["user_id"]) - 1 else "\n"
        sql.write(
            f"""("{user["user_id"][i]}","{user["role"][i]}"){end}\n""")
    sql.write(";\n")

def course_insert(course,sql):
    sql.write(f"\n-- Course Inserts\n")
    sql.write(f"""INSERT INTO Course(course_id,course_name) Values\n""")
    for i in range(len(course["Course ID"])):
        end = ",\n" if i < len(course["Course ID"]) - 1 else "\n"
        sql.write(f"""("{course["Course ID"][i]}","{course["Course_Name"][i]}"){end}\n""")
    sql.write(";\n")

def user_course_insert(register,sql,user_type):
    sql.write(f"\n-- {user_type} Course Inserts\n")
    sql.write(f"""INSERT INTO User_Course(user_id,course_id) Values""")

    entries = [(user, course) for user in register for course in register[user]]
    
    for i, (user, course) in enumerate(entries):
        end = "," if i < len(entries) - 1 else ""
        sql.write(f"""("{user}", "{course}"){end}\n""")
    
    sql.write(";\n")
    
if __name__ == '__main__':
    print("Start")
    students = insert_person("Student",100000)
    lecturers = insert_person("Lecturer",100)
    admin = insert_person("Admin",30)

    students_pw = default_login(students["user_id"])
    lecturers_pw = default_login(lecturers["user_id"])
    admin_pw = default_login(admin["user_id"])

    courses = insert_course(300)

    Student_Register  = (Student_Course(students,courses))
    Lecturers_Register = Lecturers_course(lecturers,courses)

    with open ("db-init-scripts\\insert.sql","w") as sql:
        
        sql.write("USE School_Management_System \n\n")
        user_insert(students,sql,"students")
        user_insert(lecturers,sql,"lecturers")
        user_insert(admin,sql,"admin")


        login_insert(students_pw,sql,"students")
        login_insert(lecturers_pw,sql,"lecturers")
        login_insert(admin_pw,sql,"admin")

        course_insert(courses,sql)

        user_course_insert(Student_Register,sql,"students")
        user_course_insert(Lecturers_Register,sql,"lecturers")

    sql.close()
    print("Done")