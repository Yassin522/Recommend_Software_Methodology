from experta import *
import easygui
import re
from random import choices
from string import Template




methodologies = [
    ('Waterfall (Cascade)', (0.8, 1.0)),
    ('Agile', (0.6, 0.8)),
    ('Scrum', (0.4, 0.6)),
    ('Kanban', (0.2, 0.4)),
    ('Feature Driven Development (FDD)', (0.4, 0.6)),
    ('Incremental', (0.4, 0.6)),
    ('Prototype', (0.2, 0.4)),
    ('Extreme Programming (XP)', (0.4, 0.6))
]



methodology_template = Template(
    "Based on the provided inputs, a suitable methodology for your project is $methodology. \n The system make an prediction about your request and the accurate of this result is based on the accurate of your given information.")


sm_list = []
sm_char = []
sm_map = {}
s_sm_map = {}

project_sizes = {
    '1': 'small',
    '2': 'medium',
    '3': 'large'
}

team_sizes = {
    '1': 'small',
    '2': 'medium',
    '3': 'large'
}

complexitys = {
    '1': 'simple',
    '2': 'complex',
    '3': 'very complex'
}

timelines = {
    '1': 'short-term',
    '2': 'medium-term',
    '3': 'long-term'
}

scopes = {
    '1': 'small',
    '2': 'medium',
    '3': 'large'
}

involvements = {
    '1': 'high involvement',
    '2': 'medium involvement',
    '3': 'low involvement'
}

expertises = {
    '1': 'high',
    '2': 'medium',
    '3': 'low'
}

flexibilitys = {
    '1': 'highly flexible',
    '2': 'moderately flexible',
    '3': 'not flexible'
}

risk_tolerances = {
    '1': 'highly risk-tolerant',
    '2': 'moderately risk-tolerant',
    '3': 'not risk-tolerant'
}


## Measures Maps##

project_size_by_task = {
    'small': 70,
    'medium': 150,
    'large': 400,
    'huge': 700,
}

number_of_task_by_level = {
    'junior': 2,
    'med-level': 4,
    'senior': 5
}


class Total_Time:
    def __init__(self, project_size, junior_number, med_number, senior_number,):
        self.project_size = project_size
        self.junior_number = junior_number
        self.med_number = med_number
        self.senior_number = senior_number


class Total_Cost:
    def __init__(self, junior_num, med_num, senior_num, junior_salary, med_salary, senior_salary, project_size):
        self.junior_num = junior_num
        self.med_num = med_num
        self.senior_num = senior_num
        self.junior_salary = junior_salary
        self.med_salary = med_salary
        self.senior_salary = senior_salary
        self.project_size = project_size


def total_cost(info):
    junior_per_day = info.junior_salary/30
    med_per_day = info.med_salary/30
    senior_per_day = info.senior_salary/30
    total_cost_per_day = info.junior_num*junior_per_day + \
        info.med_num*med_per_day + info.senior_num*senior_per_day
    days = total_time(Total_Time('medium', info.junior_num,
                      info.med_num, info.senior_num))
    return [round(total_cost_per_day*days[0]), round(total_cost_per_day*days[1])]


def total_time(info):
    number_of_tasks = project_size_by_task[info.project_size]
    number_of_task_per_day = info.junior_number * \
        number_of_task_by_level["junior"] + info.med_number*number_of_task_by_level["med-level"] + \
        info.senior_number*number_of_task_by_level["senior"]
    best_number_of_days = number_of_tasks/number_of_task_per_day
    best_number_of_days = best_number_of_days + \
        ((info.junior_number+info.med_number+info.senior_number)/3)
    worst_number_of_days = number_of_tasks / \
        (info.junior_number*number_of_task_by_level["junior"])

    # print([round(min(best_number_of_days,worst_number_of_days)), round(max(best_number_of_days,worst_number_of_days))])
    return [round(min(best_number_of_days, worst_number_of_days)), round(max(best_number_of_days, worst_number_of_days))]


print(total_time(Total_Time('medium', 6, 9, 2)))

print(total_cost(Total_Cost(junior_num=4, med_num=3, senior_num=2, junior_salary=150,
                            med_salary=400, senior_salary=800, project_size='meduim')))


methodology_explanations = {
    "Waterfall": "The Waterfall methodology follows a sequential approach to software development. It involves distinct phases such as requirements gathering, design, implementation, testing, and maintenance.",
    "Scrum": "Scrum is an agile framework that focuses on iterative and incremental development. It emphasizes collaboration, frequent feedback, and adaptability to changing requirements.",
    "Agile": "Agile is an iterative and incremental approach that emphasizes flexibility, customer collaboration, and rapid delivery of working software. It allows for changing requirements and encourages adaptive planning.",
    "Kanban": "Kanban is a visual framework that helps manage work and limit work in progress. It promotes a continuous flow of work, visualizes bottlenecks, and encourages process improvement.",
    "XP": "Extreme Programming (XP) is an agile methodology that emphasizes close collaboration between developers and customers. It focuses on frequent releases, continuous testing, and simplicity.",
    "FDD": "Feature Driven Development (FDD) is an iterative and incremental approach that focuses on delivering features incrementally. It emphasizes domain object modeling, iterative design, and regular inspections.",
    "Prototype": "The Prototype methodology involves building a working model of the software early in the development process. It helps gather feedback, validate requirements, and refine the design.",
    "Incremental": "The Incremental methodology breaks the development process into smaller increments or modules. Each increment delivers a portion of the functionality and undergoes testing and feedback.",
    "Software methodology not detected": "No matching methodology was found based on the provided characteristics. Please provide more details about your project requirements and characteristics."
}


def preprocess():
    global sm_char, sm_map
    sm = open("Methodologies.txt")
    sm_t = sm.read()
    sm_list = sm_t.split("\n")
    sm.close()
    for m in sm_list:
        if m == "":
            continue
        sm_s_file = open("All_Methodologies/" + m + ".txt")
        sm_s_data = sm_s_file.read()
        sm_s_file.close()
        sm_list = sm_s_data.split("\n")
        sm_char.append(sm_list)
        sm_map[str(sm_list)] = m


def identify_sm(*arguments):
    char_list = []
    for char in arguments:
        char_list.append(char)
    return sm_map.get(str(char_list), "Software methodology not detected")


def if_not_matched(m):
    id_m = m
    if m == "Software methodology not detected":
        easygui.msgbox(
            "No matching methodology was found based on the provided characteristics.")
        easygui.msgbox(
            "Please provide more details about your project requirements and characteristics.")
    else:
        easygui.msgbox(
            "The software development methodology that you had to choose to manage your software development project is: %s\n" % (id_m))
        explanation = methodology_explanations.get(
            id_m, "Explanation not available")
        print("kkkk")
        print(id_m)
        easygui.msgbox("Explanation: %s" % explanation)


class SM(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.knowledge = {}
    juniors = None
    midlevels = None
    seniors = None
    Juniorsalary = None
    midlevelsalary = None
    seniorlevelsalary = None
    project_size = None
    certainties = []

    @DefFacts()
    def _initial_action(self):
        easygui.msgbox(
            "Hello!  I am here to help you choose the best software development methodology for your project.")
        easygui.msgbox(
            "This expert system allows you to choose the right software development methodology to use for a specific project.")
        easygui.msgbox(
            "That is why it is preferable to analyze each project scenario in relation to a set of the following questions:")
        yield Fact(action="find_sm")

    @Rule(Fact(action='find_sm'), NOT(Fact(projetsimple=W())), salience=27)
    def char_0(self):
        try:
            projetsimple_input = easygui.enterbox(
                "Is the project simple? In other words, does the project possess a level of simplicity that suggests it can be accomplished with relative ease and without significant complexity or challenges?\n yes \n no \n): ")
            if projetsimple_input.lower() == 'yes':
                projetsimple = 'yes'
                certainty = 0.8
            elif projetsimple_input.lower() == 'no':
                projetsimple = 'no'
                certainty = 0.6
            else:
                easygui.msgbox("Invalid input. Please enter 'yes' or 'no'.")
                raise ValueError("Invalid input. Please enter 'yes' or 'no'.")
            self.certainties.append(certainty)
            self.declare(Fact(projetsimple=projetsimple, certainty=certainty))

        except ValueError as ve:
            easygui.msgbox("Error:", str(ve))
        except Exception as e:
            easygui.msgbox("Error: Invalid input. Please enter a valid value.")
            easygui.msgbox(str(e))

    @Rule(Fact(action='find_sm'), NOT(Fact(projetcomplique=W())), salience=26)
    def char_1(self):
        try:
            projetcomplique_input = easygui.enterbox(
                "Is the project mid-range or complicated? \n yes \n no \n ")
            if projetcomplique_input.lower() == 'yes':
                projetcomplique = 'yes'
                certainty = 0.7
            elif projetcomplique_input.lower() == 'no':
                projetcomplique = 'no'
                certainty = 0.5
            else:
                raise ValueError("Invalid input. Please enter 'yes' or 'no'.")

            self.certainties.append(certainty)
            self.declare(
                Fact(projetcomplique=projetcomplique, certainty=certainty))

        except ValueError as ve:
            easygui.msgbox("Error:", str(ve))
        except Exception as e:
            easygui.msgbox("Error: Invalid input. Please enter a valid value.")
            easygui.msgbox(str(e))

    @Rule(Fact(action='find_sm'), NOT(Fact(projetcomplexe=W())), salience=25)
    def char_2(self):
        try:
            projetcomplexe_input = easygui.enterbox(
                "Is the project complex? \n yes \n no \n ")
            if projetcomplexe_input.lower() == 'yes':
                projetcomplexe = 'yes'
                certainty = 0.9
            elif projetcomplexe_input.lower() == 'no':
                projetcomplexe = 'no'
                certainty = 0.3
            else:
                raise ValueError("Invalid input. Please enter 'yes' or 'no'.")
            self.certainties.append(certainty)
            self.declare(
                Fact(projetcomplexe=projetcomplexe, certainty=certainty))

        except ValueError as ve:
            easygui.msgbox("Error:", str(ve))
        except Exception as e:
            easygui.msgbox("Error: Invalid input. Please enter a valid value.")
            easygui.msgbox(str(e))

    @Rule(Fact(action='find_sm'), NOT(Fact(projetchaotique=W())), salience=24)
    def char_3(self):
        try:
            projetchaotique_input = easygui.enterbox(
                "Is the project chaotic? When considering the current state and dynamics of the project, would you describe it as chaotic? Chaos, in this context, refers to a lack of clear structure, organization, or control within the project environment. It implies a state of confusion, disorder, and unpredictability, where goals, tasks, and priorities may be unclear or constantly changing\n yes \n no \n ")
            if projetchaotique_input.lower() == 'yes':
                projetchaotique = 'yes'
                certainty = 0.7
            elif projetchaotique_input.lower() == 'no':
                projetchaotique = 'no'
                certainty = 0.4
            else:
                raise ValueError("Invalid input. Please enter 'yes' or 'no'.")
            self.certainties.append(certainty)
            self.declare(
                Fact(projetchaotique=projetchaotique, certainty=certainty))

        except ValueError as ve:
            easygui.msgbox("Error:", str(ve))
        except Exception as e:
            easygui.msgbox("Error: Invalid input. Please enter a valid value.")
            easygui.msgbox(str(e))

    @Rule(Fact(action='find_sm'), NOT(Fact(defintion=W())), salience=23)
    def char_4(self):
        try:
            defintion_input = easygui.enterbox(
                "Do you have a clear definition of the project requirements? When referring to the project requirements, we are specifically interested in understanding the level of clarity and specificity with which the project's objectives, deliverables, functionalities, constraints, and any other relevant criteria have been defined.  \n yes \n no \n ")
            if defintion_input.lower() == 'yes':
                defintion = 'yes'
                certainty = 0.9
            elif defintion_input.lower() == 'no':
                defintion = 'no'
                certainty = 0.5
            else:
                raise ValueError("Invalid input. Please enter 'yes' or 'no'.")
            self.certainties.append(certainty)
            self.declare(Fact(defintion=defintion, certainty=certainty))

        except ValueError as ve:
            easygui.msgbox("Error:", str(ve))
        except Exception as e:
            easygui.msgbox("Error: Invalid input. Please enter a valid value.")
            easygui.msgbox(str(e))

    @Rule(Fact(action='find_sm'), NOT(Fact(clients=W())), salience=22)
    def char_5(self):
        try:
            clients_input = easygui.enterbox(
                "Do you have direct contact with the client throughout the project? \n yes \n no \n ")
            if clients_input.lower() == 'yes':
                clients = 'yes'
                certainty = 0.7
            elif clients_input.lower() == 'no':
                clients = 'no'
                certainty = 0.3
            else:
                raise ValueError("Invalid input. Please enter 'yes' or 'no'.")
            self.certainties.append(certainty)
            self.declare(Fact(clients=clients, certainty=certainty))

        except ValueError as ve:
            easygui.msgbox("Error:", str(ve))
        except Exception as e:
            easygui.msgbox("Error: Invalid input. Please enter a valid value.")
            easygui.msgbox(str(e))

    @Rule(Fact(action='find_sm'), NOT(Fact(produit=W())), salience=21)
    def char_6(self):
        try:
            produit_input = easygui.enterbox(
                "Is the final product already defined? When we refer to the final product, we are referring to the ultimate deliverable or outcome that the project aims to achieve. It represents the end result or solution that addresses the project's objectives and meets the needs and expectations of the stakeholders. Defining the final product involves clearly articulating its features, functionalities, specifications, and any other relevant characteristics. By assessing whether the final product is already defined.  \n yes \n no \n ")
            if produit_input.lower() == 'yes':
                produit = 'yes'
                certainty = 0.9
            elif produit_input.lower() == 'no':
                produit = 'no'
                certainty = 0.5
            else:
                raise ValueError("Invalid input. Please enter 'yes' or 'no'.")
            self.certainties.append(certainty)
            self.declare(Fact(produit=produit, certainty=certainty))

        except ValueError as ve:
            easygui.msgbox("Error:", str(ve))
        except Exception as e:
            easygui.msgbox("Error: Invalid input. Please enter a valid value.")
            easygui.msgbox(str(e))

    @Rule(Fact(action='find_sm'), NOT(Fact(equipe=W())), salience=20)
    def char_7(self):
        try:
            equipe_input = easygui.enterbox(
                "Do you have a qualified and experienced development team?  The success of a project greatly depends on the expertise and capabilities of the development team responsible for its execution. A qualified and experienced development team possesses the necessary skills, knowledge, and proficiency to effectively handle the various aspects of the project. When we inquire about the presence of a qualified and experienced development team, we are seeking to understand the composition and competence of the team members involved in the project. This includes assessing their qualifications, experience, technical expertise, and domain knowledge relevant to the project's requirements  \n yes \n no \n ")
            if equipe_input.lower() == 'yes':
                equipe = 'yes'
                certainty = 0.7
            elif equipe_input.lower() == 'no':
                equipe = 'no'
                certainty = 0.3
            else:
                raise ValueError("Invalid input. Please enter 'yes' or 'no'.")
            self.certainties.append(certainty)
            self.declare(Fact(equipe=equipe, certainty=certainty))

        except ValueError as ve:
            easygui.msgbox("Error:", str(ve))
        except Exception as e:
            easygui.msgbox("Error: Invalid input. Please enter a valid value.")
            easygui.msgbox(str(e))

    @Rule(Fact(action='find_sm'), NOT(Fact(comfort_with_risks=W())), salience=19)
    def find_comfort_with_risks(self):
        comfort_with_risks_input = easygui.enterbox(
            "Are you comfortable taking risks in order to achieve potential rewards? When embarking on a project, it's important to consider the level of risk tolerance within the project team and organization. Risk-taking is an inherent part of innovation and progress, as it involves making decisions and taking actions that may have uncertain outcomes but also carry the potential for significant rewards. By asking if you are comfortable taking risks to achieve potential rewards, we are seeking to understand your willingness to embrace uncertainty, make bold choices, and explore uncharted territories in pursuit of project success \n yes \n no \n ")
        comfort_with_risks = comfort_with_risks_input.lower()
        valid_options = ['yes', 'no']
        if comfort_with_risks not in valid_options:
            easygui.msgbox("Error: Invalid input. Please enter 'yes' or 'no'.")
        certainties = {
            'yes': 0.8,
            'no': 0.4
        }
        certainty = certainties[comfort_with_risks]
        self.certainties.append(certainty)
        self.declare(
            Fact(comfort_with_risks=comfort_with_risks, certainty=certainty))

    @Rule(Fact(action='find_sm'), NOT(Fact(stakeholder_communication=W())), salience=18)
    def find_stakeholder_communication(self):
        communication_input = easygui.enterbox(
            "Do you require frequent communication and collaboration with stakeholders? In any project, stakeholders play a crucial role in its success. Stakeholders are individuals or groups who have an interest or influence in the project and can directly or indirectly impact its outcome. Effective communication and collaboration with stakeholders are essential for understanding their needs, gathering feedback, addressing concerns, and ensuring their buy-in throughout the project lifecycle. By asking if you require frequent communication and collaboration with stakeholders, we aim to ascertain the level of engagement and involvement you expect from stakeholders in the project \n yes \n no \n ")
        communication = communication_input.lower()
        valid_options = ['yes', 'no']
        if communication not in valid_options:
            raise ValueError("Invalid input. Please enter 'yes' or 'no'.")
        communications = {
            'yes': ('yes', 0.8),
            'no': ('no', 0.6)
        }
        self.certainties.append(communications[communication][1])
        self.declare(Fact(
            stakeholder_communication=communications[communication][0], certainty=communications[communication][1]))

    @Rule(Fact(action='find_sm'), NOT(Fact(technology_adoption=W())), salience=17)
    def find_technology_adoption(self):
        adoption_input = easygui.enterbox(
            "Are you open to adopting new technologies or frameworks? In the rapidly evolving landscape of technology, new tools, technologies, and frameworks emerge constantly, offering potential benefits and opportunities for enhancing project outcomes \n yes \n no \n")
        adoption = adoption_input.lower()
        valid_options = ['yes', 'no']
        if adoption not in valid_options:
            easygui.msgbox("Error: Invalid input. Please enter 'yes' or 'no'.")
        certainties = {
            'yes': 0.8,
            'no': 0.6
        }
        certainty = certainties[adoption]
        self.certainties.append(certainty)
        self.declare(Fact(technology_adoption=adoption, certainty=certainty))

    @Rule(Fact(action='find_sm'), NOT(Fact(requirement_change=W())), salience=16)
    def find_requirement_change(self):
        requirement_change_input = easygui.enterbox(
            "Are you open to changing requirements or evolving project needs? In the dynamic landscape of project development, requirements and project needs can evolve over time due to various factors such as market conditions, user feedback, technological advancements, or shifting business priorities. Recognizing and accommodating these changes is essential for ensuring that the project remains aligned with the desired outcomes and continues to deliver value.  \n yes \n no \n ")
        change = requirement_change_input.lower()
        valid_options = ['yes', 'no']
        if requirement_change_input not in valid_options:
            easygui.msgbox(
                "Error: Invalid input. Please enter either 'yes' or 'no'.")
        certainties = {
            'yes': 0.8,
            'no': 0.4
        }
        certainty = certainties[change]
        self.certainties.append(certainty)
        self.declare(Fact(requirement_change=change, certainty=certainty))

    @Rule(Fact(action='find_sm'), NOT(Fact(project_size=W())), salience=15)
    def char_8(self):
        try:
            project_size_input = easygui.enterbox(
                "Enter the project size\n 1-small  \n2-medium  \n3-large\n): ")
            project_size = project_size_input.lower()
            if project_size not in ['1', '2', '3']:
                raise ValueError(
                    "Invalid input. Please enter 'small', 'medium', or 'large'.")
            if project_size == '1':
                self.project_size = 'small'
                certainty = 0.8
            elif project_size == '2':
                self.project_size = 'medium'
                certainty = 0.6
            elif project_size == '3':
                self.project_size = 'large'
                certainty = 0.4
            self.certainties.append(certainty)
            self.declare(
                Fact(project_size=project_sizes[project_size], certainty=certainty))

        except ValueError as ve:
            easygui.msgbox("Error:", str(ve))
        except Exception as e:
            easygui.msgbox("Error: Invalid input. Please enter a valid value.")
            easygui.msgbox(str(e))

    @Rule(Fact(action='find_sm'), NOT(Fact(team_size=W())), salience=14)
    def char_9(self):
        try:
            team_size_input = easygui.enterbox(
                "Enter the team size\n 1-small\n 2-medium\n 3-large\n ")
            team_size = team_size_input.lower()
            if team_size not in ['1', '2', '3']:
                raise ValueError(
                    "Invalid input. Please enter 'small', 'medium', or 'large'.")
            certainty = 0.6
            self.certainties.append(certainty)
            self.declare(
                Fact(team_size=team_sizes[team_size], certainty=certainty))

        except ValueError as ve:
            easygui.msgbox("Error:", str(ve))
        except Exception as e:
            easygui.msgbox("Error: Invalid input. Please enter a valid value.")
            easygui.msgbox(str(e))

    @Rule(Fact(action='find_sm'), NOT(Fact(project_complexity=W())), salience=13)
    def find_complexity(self):
        try:
            complexity_input = easygui.enterbox(
                "Enter the complexity of the project\n 1-simple\n 2-complex\n 3-very complex\n ")
            complexity = complexity_input.lower()
            if complexity not in ['1', '2', '3']:
                raise ValueError(
                    "Invalid input. Please enter 'simple', 'complex', or 'very complex'.")
            complexitys = {
                '1': ('simple', 0.8),
                '2': ('complex', 0.6),
                '3': ('very complex', 0.4)
            }
            self.certainties.append(complexitys[complexity][1])
            self.declare(Fact(
                project_complexity=complexitys[complexity][0], certainty=complexitys[complexity][1]))

        except ValueError as ve:
            easygui.msgbox("Error:", str(ve))
        except Exception as e:
            easygui.msgbox("Error: Invalid input. Please enter a valid value.")
            easygui.msgbox(str(e))

    @Rule(Fact(action='find_sm'), NOT(Fact(project_timeline=W())), salience=12)
    def find_timeline(self):
        timeline_input = easygui.enterbox(
            "Enter the timeline of the project\n  1-short-term\n 2-medium-term\n 3-long-term\n ")
        timeline = timeline_input.lower()
        valid_timelines = ['1', '2', '3']
        if timeline not in valid_timelines:
            raise ValueError(
                "Invalid input. Please enter 'short-term', 'medium-term', or 'long-term'.")
        timelines = {
            '1': ('short-term', 0.8),
            '2': ('medium-term', 0.6),
            '3': ('long-term', 0.4)
        }
        self.certainties.append(timelines[timeline][1])
        self.declare(
            Fact(project_timeline=timelines[timeline][0], certainty=timelines[timeline][1]))

    @Rule(Fact(action='find_sm'), NOT(Fact(project_scope=W())), salience=11)
    def find_scope(self):
        scope_input = easygui.enterbox(
            "What do you think the size of scopes the project has>? \n 1-small \n  2-medium \n  3-large \n ): ")
        scope = scope_input.lower()
        valid_scopes = ['1', '2', '3']
        if scope not in valid_scopes:
            raise ValueError(
                "Invalid input. Please enter 'small', 'medium', or 'large'.")
        scopes = {
            '1': ('small', 0.8),
            '2': ('medium', 0.6),
            '3': ('large', 0.4)
        }
        self.certainties.append(scopes[scope][1])
        self.declare(
            Fact(project_scope=scopes[scope][0], certainty=scopes[scope][1]))

    @Rule(Fact(action='find_sm'), NOT(Fact(stakeholder_involvement=W())), salience=10)
    def find_stakeholder_involvement(self):
        involvement_input = easygui.enterbox(
            "How involved are the stakeholders in the project?\n 1-high involvement\n 2-medium involvement\n 3-low involvement\n ")
        involvement = involvement_input.lower()
        valid_involvements = ['1', '2', '3']
        if involvement not in valid_involvements:
            raise ValueError(
                "Invalid input. Please enter 'high involvement', 'medium involvement', or 'low involvement'.")
        involvements = {
            '1': ('high involvement', 0.8),
            '2': ('medium involvement', 0.6),
            '3': ('low involvement', 0.4)
        }
        self.certainties.append(involvements[involvement][1])
        self.declare(Fact(
            stakeholder_involvement=involvements[involvement][0], certainty=involvements[involvement][1]))

    @Rule(Fact(action='find_sm'), NOT(Fact(technical_expertise=W())), salience=9)
    def find_technical_expertise(self):
        expertise_input = easygui.enterbox(
            "What is the level of technical expertise available in your team?\n 1-high \n 2-medium\n 3-low \n): ")
        expertise = expertise_input.lower()
        valid_options = ['1', '2', '3']
        if expertise not in valid_options:
            easygui.msgbox(
                "Error: Invalid input. Please enter a valid level of technical expertise.")
        expertises = {
            '1': ('high', 0.8),
            '2': ('medium', 0.6),
            '3': ('low', 0.4)
        }
        self.certainties.append(expertises[expertise][1])
        self.declare(Fact(
            technical_expertise=expertises[expertise][0], certainty=expertises[expertise][1]))

    @Rule(Fact(action='find_sm'), NOT(Fact(flexibility=W())), salience=8)
    def find_flexibility(self):
        flexibility_input = easygui.enterbox(
            "How flexible and adaptable is your team and organization?\n 1-highly flexible\n 2-moderately flexible\n 3-not flexible ")
        flexibility = flexibility_input.lower()
        valid_options = ['1', '2', '3']
        if flexibility_input not in valid_options:
            easygui.msgbox(
                "Error: Invalid input. Please enter one of the following options: highly flexible, moderately flexible, not flexible.")
        certainties = {
            '1': 0.8,
            '2': 0.6,
            '3': 0.4
        }
        certainty = certainties[flexibility]
        self.certainties.append(certainty)
        self.declare(Fact(flexibility=flexibility, certainty=certainty))

    @Rule(Fact(action='find_sm'), NOT(Fact(risk_tolerance=W())), salience=7)
    def find_risk_tolerance(self):
        risk_tolerance_input = easygui.enterbox(
            "How risk-tolerant is your organization?\n 1-highly risk-tolerant\n 2-moderately risk-tolerant \n 3-not risk-tolerant \n ")
        risk_tolerance = risk_tolerance_input.lower()
        valid_options = ['1', '2', '3']
        if risk_tolerance not in valid_options:
            easygui.msgbox(
                "Error: Invalid input. Please enter 'highly risk-tolerant', 'moderately risk-tolerant', or 'not risk-tolerant'.")
        certainties = {
            '1': 0.8,
            '2': 0.6,
            '3': 0.4
        }
        certainty = certainties[risk_tolerance]
        self.certainties.append(certainty)
        self.declare(
            Fact(risk_tolerance=risk_tolerances[risk_tolerance], certainty=certainty))

    @Rule(Fact(action='find_sm'), NOT(Fact(juniors=W())), salience=6)
    def char_10(self):
        try:
            juniors_input = easygui.enterbox(
                "Please enter the number of junior employees in the project (Enter a number): ")
            if not juniors_input.isdigit():
                easygui.msgbox("Invalid input. Please enter a number.")
                raise ValueError("Invalid input. Please enter a number.")

            self.juniors = int(juniors_input)
            self.declare(Fact(juniors=self.juniors))
        except ValueError as ve:
            easygui.msgbox("Error: " + str(ve))
        except Exception as e:
            easygui.msgbox("Error: Invalid input. Please enter a valid value.")
            easygui.msgbox(str(e))

    @Rule(Fact(action='find_sm'), NOT(Fact(midlevels=W())), salience=5)
    def char_11(self):
        try:
            midlevels_input = easygui.enterbox(
                "Please enter the number of mid level employees in the project (Enter a number): ")
            if not midlevels_input.isdigit():
                easygui.msgbox("Invalid input. Please enter a number.")
                raise ValueError("Invalid input. Please enter a number.")

            self.midlevels = int(midlevels_input)
            self.declare(Fact(midlevels=self.midlevels))
        except ValueError as ve:
            easygui.msgbox("Error: " + str(ve))
        except Exception as e:
            easygui.msgbox("Error: Invalid input. Please enter a valid value.")
            easygui.msgbox(str(e))

    @Rule(Fact(action='find_sm'), NOT(Fact(seniors=W())), salience=4)
    def char_12(self):
        try:
            seniors_input = easygui.enterbox(
                "Please enter the number of senior employees in the project (Enter a number): ")
            if not seniors_input.isdigit():
                easygui.msgbox("Invalid input. Please enter a number.")
                raise ValueError("Invalid input. Please enter a number.")

            self.seniors = int(seniors_input)
            self.declare(Fact(seniors=self.seniors))
        except ValueError as ve:
            easygui.msgbox("Error: " + str(ve))
        except Exception as e:
            easygui.msgbox("Error: Invalid input. Please enter a valid value.")
            easygui.msgbox(str(e))

    @Rule(Fact(action='find_sm'), NOT(Fact(Juniorsalary=W())), salience=3)
    def char_13(self):
        try:
            Juniorsalary_input = easygui.enterbox(
                "Please enter the number of Junior salary in the project (Enter a number): ")
            if not Juniorsalary_input.isdigit():
                easygui.msgbox("Invalid input. Please enter a number.")
                raise ValueError("Invalid input. Please enter a number.")

            self.Juniorsalary = int(Juniorsalary_input)
            self.declare(Fact(Juniorsalary=self.Juniorsalary))
        except ValueError as ve:
            easygui.msgbox("Error: " + str(ve))
        except Exception as e:
            easygui.msgbox("Error: Invalid input. Please enter a valid value.")
            easygui.msgbox(str(e))

    @Rule(Fact(action='find_sm'), NOT(Fact(midlevelsalary=W())), salience=2)
    def char_14(self):
        try:
            midlevelsalary_input = easygui.enterbox(
                "Please enter the number of Mid level salary in the project (Enter a number): ")
            if not midlevelsalary_input.isdigit():
                easygui.msgbox("Invalid input. Please enter a number.")
                raise ValueError("Invalid input. Please enter a number.")

            self.midlevelsalary = int(midlevelsalary_input)
            self.declare(Fact(midlevelsalary=self.midlevelsalary))
        except ValueError as ve:
            easygui.msgbox("Error: " + str(ve))
        except Exception as e:
            easygui.msgbox("Error: Invalid input. Please enter a valid value.")
            easygui.msgbox(str(e))

    @Rule(Fact(action='find_sm'), NOT(Fact(seniorlevelsalary=W())), salience=1)
    def char_15(self):
        try:
            seniorlevelsalary_input = easygui.enterbox(
                "Please enter the number of senior level salary in the project (Enter a number): ")
            if not seniorlevelsalary_input.isdigit():
                easygui.msgbox("Invalid input. Please enter a number.")
                raise ValueError("Invalid input. Please enter a number.")

            self.seniorlevelsalary = int(seniorlevelsalary_input)
            self.declare(Fact(seniorlevelsalary=self.seniorlevelsalary))
        except ValueError as ve:
            easygui.msgbox("Error: " + str(ve))
        except Exception as e:
            easygui.msgbox("Error: Invalid input. Please enter a valid value.")
            easygui.msgbox(str(e))

    @Rule(Fact(action='find_sm'), Fact(prioritized_chars=MATCH.chars), Fact(m=MATCH.m), NOT(Fact(feedback=W())), salience=-999)
    def ask_feedback(self, chars, m):
        easygui.msgbox(
            "Based on your prioritized characteristics, the recommended methodology is %s." % m)
        feedback = input(
            "Was the recommended methodology suitable for your project? (yes/no): ")
        self.declare(Fact(feedback=feedback))

    @Rule(Fact(action='find_sm'), Fact(feedback="yes"), salience=-999)
    def feedback_yes(self):
        easygui.msgbox(
            "Thank you for your feedback! I'm glad the recommended methodology was suitable for your project.")

    @Rule(Fact(action='find_sm'), Fact(feedback="no"), salience=-999)
    def feedback_no(self):
        easygui.msgbox(
            "Thank you for your feedback! I apologize if the recommended methodology wasn't suitable for your project.")
        easygui.msgbox(
            "Please provide more details about your project requirements and characteristics, so I can improve my recommendations in the future.")

    @Rule(Fact(action='find_sm'), Fact(projetsimple="yes"),
          OR(Fact(projetcomplique="no"),
          Fact(projetcomplexe="no")),
          Fact(projetchaotique="no"), OR(Fact(defintion="yes"),
                                         Fact(
              clients="no"),
        Fact(produit="no")), OR(Fact(equipe="no"), NOT(Fact(clrShowed=W()))),
        Fact(project_size="small"),
        Fact(team_size="small"), OR(Fact(project_complexity="simple"),
                                    Fact(project_complexity="short-term")),
        Fact(project_timeline="short-term"), Fact(project_scope="small"), Fact(
        stakeholder_involvement="low involvement"),
        Fact(stakeholder_communication="no"), Fact(technical_expertise="low"),
        Fact(technology_adoption="no"), Fact(flexibility="not flexible"),
        Fact(requirement_change="no"), Fact(
            risk_tolerance="not risk-tolerant"), Fact(comfort_with_risks="no")
    )
    def sm_0(self):
        methodology = "Waterfall (Cascade)"
        self.declare(Fact(m=methodology))
        self.declare(Fact(clrShowed="yes"))
        explanation = methodology_explanations.get(
            methodology, "Explanation not available")
        easygui.msgbox("The recommended methodology is: %s" % methodology)
        easygui.msgbox("Explanation: %s" % explanation)
        result = total_cost(Total_Cost(
            junior_num=self.juniors, med_num=self.midlevels, senior_num=self.seniors, junior_salary=self.Juniorsalary, med_salary=self.midlevelsalary, senior_salary=self.seniorlevelsalary, project_size=self.project_size))
        min_cost = result[0]
        max_cost = result[1]

        output_string = "Min cost: ${} and Max cost: ${}".format(
            min_cost, max_cost)
        easygui.msgbox(
            "The expected cost of completing the project is shown here the lowest expected value and the most expected value: " + output_string)

        result2 = total_time(Total_Time(project_size=self.project_size,
                             junior_number=self.juniors, med_number=self.midlevels, senior_number=self.seniors))
        min_time = result2[0]
        max_time = result2[1]

        output_string2 = "Min: {} days and Max: {} days".format(
            min_time, max_time)
        easygui.msgbox(
            "The expected time of completion of the project here is displayed the least expected value and the most expected value: " + output_string2)

        # easygui.msgbox("The expected cost of completing the project is shown here the lowest expected value and the most expected value: " + str(total_cost(Total_Cost(
        #     junior_num=self.juniors, med_num=self.midlevels, senior_num=self.seniors, junior_salary=self.Juniorsalary, med_salary=self.midlevelsalary, senior_salary=self.seniorlevelsalary, project_size=self.project_size))))
        # easygui.msgbox("The expected time of completion of the project here is displayed the least expected value and the most expected value: " +
        #                str(total_time(Total_Time(project_size=self.project_size, junior_number=self.juniors, med_number=self.midlevels, senior_number=self.seniors))))

    @Rule(Fact(action='find_sm'), Fact(projetsimple="no"),
          OR(Fact(projetcomplique="yes"),
             Fact(projetcomplexe="yes")), Fact(projetchaotique="no"),
          OR(Fact(defintion="no"), Fact(clients="yes"),
             Fact(produit="yes")), OR(Fact(equipe="yes"), NOT(Fact(clrShowed=W()))),
          Fact(project_size="large"), Fact(team_size="medium"),
          OR(Fact(project_complexity="very complex"),
             Fact(project_complexity="long-term")),
          Fact(project_timeline="medium-term"),
          Fact(project_scope="large"), Fact(
              stakeholder_involvement="medium involvement"),
          Fact(stakeholder_communication="yes"), Fact(
              technical_expertise="high"), Fact(technology_adoption="yes"),
          Fact(flexibility="moderately flexible"), Fact(
              requirement_change="yes"), Fact(risk_tolerance="moderately risk-tolerant"),
          Fact(comfort_with_risks="yes")

          )
    def sm_1(self):
        methodology = "Scrum"
        self.declare(Fact(m=methodology))
        self.declare(Fact(clrShowed="yes"))
        explanation = methodology_explanations.get(
            methodology, "Explanation not available")
        easygui.msgbox("The recommended methodology is: %s" % methodology)
        easygui.msgbox("Explanation: %s" % explanation)
        result = total_cost(Total_Cost(
            junior_num=self.juniors, med_num=self.midlevels, senior_num=self.seniors, junior_salary=self.Juniorsalary, med_salary=self.midlevelsalary, senior_salary=self.seniorlevelsalary, project_size=self.project_size))
        min_cost = result[0]
        max_cost = result[1]

        output_string = "Min cost: ${} and Max cost: ${}".format(
            min_cost, max_cost)
        easygui.msgbox(
            "The expected cost of completing the project is shown here the lowest expected value and the most expected value: " + output_string)

        result2 = total_time(Total_Time(project_size=self.project_size,
                             junior_number=self.juniors, med_number=self.midlevels, senior_number=self.seniors))
        min_time = result2[0]
        max_time = result2[1]

        output_string2 = "Min: {} days and Max: {} days".format(
            min_time, max_time)
        easygui.msgbox(
            "The expected time of completion of the project here is displayed the least expected value and the most expected value: " + output_string2)

    @Rule(Fact(action='find_sm'), Fact(projetsimple="no"),
          OR(Fact(projetcomplique="yes"), Fact(projetcomplexe="yes")),
          Fact(projetchaotique="no"), OR(Fact(defintion="no"),
                                         Fact(clients="yes"), Fact(produit="yes")),
          OR(Fact(equipe="yes"), NOT(Fact(clrShowed=W()))), Fact(
              project_size="medium"),
          Fact(team_size="medium"), OR(Fact(project_complexity="complex"),
                                       Fact(project_complexity="very high")),
          Fact(project_timeline="medium-term"),
          Fact(project_scope="medium"), Fact(
              stakeholder_involvement="high involvement"),
          Fact(stakeholder_communication="yes"), Fact(
        technical_expertise="medium"),
        Fact(technology_adoption="yes"), Fact(flexibility="highly flexible"),
        Fact(requirement_change="yes"), Fact(
            risk_tolerance="highly risk-tolerant"),
        Fact(comfort_with_risks="yes"),
    )
    def sm_agile(self):
        methodology = "Agile"
        self.declare(Fact(m=methodology))
        self.declare(Fact(clrShowed="yes"))
        explanation = methodology_explanations.get(
            methodology, "Explanation not available")
        easygui.msgbox("The recommended methodology is: %s" % methodology)
        easygui.msgbox("Explanation: %s" % explanation)
        result = total_cost(Total_Cost(
            junior_num=self.juniors, med_num=self.midlevels, senior_num=self.seniors, junior_salary=self.Juniorsalary, med_salary=self.midlevelsalary, senior_salary=self.seniorlevelsalary, project_size=self.project_size))
        min_cost = result[0]
        max_cost = result[1]

        output_string = "Min cost: ${} and Max cost: ${}".format(
            min_cost, max_cost)
        easygui.msgbox(
            "The expected cost of completing the project is shown here the lowest expected value and the most expected value: " + output_string)

        result2 = total_time(Total_Time(project_size=self.project_size,
                             junior_number=self.juniors, med_number=self.midlevels, senior_number=self.seniors))
        min_time = result2[0]
        max_time = result2[1]

        output_string2 = "Min: {} days and Max: {} days".format(
            min_time, max_time)
        easygui.msgbox(
            "The expected time of completion of the project here is displayed the least expected value and the most expected value: " + output_string2)

    @Rule(Fact(action='find_sm'), Fact(projetsimple="no"),
          OR(Fact(projetcomplique="yes"),
             Fact(projetcomplexe="no")), Fact(projetchaotique="no"),
          OR(Fact(defintion="no"), Fact(clients="yes"),
             Fact(produit="yes")), OR(Fact(equipe="yes"), NOT(Fact(clrShowed=W()))),
          Fact(project_size="large"), Fact(team_size="large"),
          OR(Fact(project_complexity="very complex"), Fact(
              project_complexity="very high")),
          Fact(project_timeline="long-term"), Fact(project_scope="large"),
          Fact(stakeholder_involvement="medium involvement"),
          Fact(stakeholder_communication="no"), Fact(
        technical_expertise="high"),
        Fact(technology_adoption="no"), Fact(
        flexibility="moderately flexible"), Fact(requirement_change="yes"),
        Fact(risk_tolerance="highly risk-tolerant"), Fact(comfort_with_risks="yes"),

    )
    def sm_2(self):
        methodology = "Kanban"
        self.declare(Fact(m=methodology))
        self.declare(Fact(clrShowed="yes"))
        explanation = methodology_explanations.get(
            methodology, "Explanation not available")
        easygui.msgbox("The recommended methodology is: %s" % methodology)
        easygui.msgbox("Explanation: %s" % explanation)
        result = total_cost(Total_Cost(
            junior_num=self.juniors, med_num=self.midlevels, senior_num=self.seniors, junior_salary=self.Juniorsalary, med_salary=self.midlevelsalary, senior_salary=self.seniorlevelsalary, project_size=self.project_size))
        min_cost = result[0]
        max_cost = result[1]

        output_string = "Min cost: ${} and Max cost: ${}".format(
            min_cost, max_cost)
        easygui.msgbox(
            "The expected cost of completing the project is shown here the lowest expected value and the most expected value: " + output_string)

        result2 = total_time(Total_Time(project_size=self.project_size,
                             junior_number=self.juniors, med_number=self.midlevels, senior_number=self.seniors))
        min_time = result2[0]
        max_time = result2[1]

        output_string2 = "Min: {} days and Max: {} days".format(
            min_time, max_time)
        easygui.msgbox(
            "The expected time of completion of the project here is displayed the least expected value and the most expected value: " + output_string2)

    @Rule(Fact(action='find_sm'), Fact(projetsimple="no"),
          OR(Fact(projetcomplique="no"),
              Fact(projetcomplexe="yes")), Fact(projetchaotique="yes"),
          OR(Fact(defintion="no"),
              Fact(clients="yes"),
              Fact(produit="yes")), OR(Fact(equipe="yes"), NOT(Fact(clrShowed=W()))),
          Fact(project_size="medium"), Fact(team_size="small"),
          OR(Fact(project_complexity="complex"),
             Fact(project_complexity="medium")),
          Fact(project_timeline="medium-term"), Fact(project_scope="medium"),
          Fact(stakeholder_involvement="high involvement"),
          Fact(stakeholder_communication="yes"), Fact(
        technical_expertise="high"),
        Fact(technology_adoption="yes"), Fact(
        flexibility="highly flexible"), Fact(requirement_change="yes"),
        Fact(risk_tolerance="highly risk-tolerant"), Fact(comfort_with_risks="yes"),
    )
    def sm_3(self):
        methodology = "Extreme Programming (XP)"
        self.declare(Fact(m=methodology))
        self.declare(Fact(clrShowed="yes"))
        explanation = methodology_explanations.get(
            methodology, "Explanation not available")
        easygui.msgbox("The recommended methodology is: %s" % methodology)
        easygui.msgbox("Explanation: %s" % explanation)
        result = total_cost(Total_Cost(
            junior_num=self.juniors, med_num=self.midlevels, senior_num=self.seniors, junior_salary=self.Juniorsalary, med_salary=self.midlevelsalary, senior_salary=self.seniorlevelsalary, project_size=self.project_size))
        min_cost = result[0]
        max_cost = result[1]

        output_string = "Min cost: ${} and Max cost: ${}".format(
            min_cost, max_cost)
        easygui.msgbox(
            "The expected cost of completing the project is shown here the lowest expected value and the most expected value: " + output_string)

        result2 = total_time(Total_Time(project_size=self.project_size,
                             junior_number=self.juniors, med_number=self.midlevels, senior_number=self.seniors))
        min_time = result2[0]
        max_time = result2[1]

        output_string2 = "Min: {} days and Max: {} days".format(
            min_time, max_time)
        easygui.msgbox(
            "The expected time of completion of the project here is displayed the least expected value and the most expected value: " + output_string2)

    @Rule(Fact(action='find_sm'), Fact(projetsimple="no"), OR(Fact(projetcomplique="yes"),
                                                              Fact(projetcomplexe="yes")),
          Fact(projetchaotique="no"),
          OR(Fact(defintion="no"), Fact(clients="yes"),
             Fact(produit="yes")), OR(Fact(equipe="yes"), NOT(Fact(clrShowed=W()))),
          Fact(project_size="large"), Fact(team_size="large"),
          OR(Fact(project_complexity="very complex"), Fact(
              project_complexity="very high")),
          Fact(project_timeline="long-term"), Fact(project_scope="large"),
          Fact(stakeholder_involvement="high involvement"),
          Fact(stakeholder_communication="yes"), Fact(
              technical_expertise="high"),
          Fact(technology_adoption="yes"), Fact(flexibility="highly flexible"),
          Fact(requirement_change="yes"), Fact(
              risk_tolerance="highly risk-tolerant"),
          Fact(comfort_with_risks="yes"),

          )
    def sm_5(self):
        methodology = "Feature Driven Development (FDD)"
        self.declare(Fact(m=methodology))
        self.declare(Fact(clrShowed="yes"))
        explanation = methodology_explanations.get(
            methodology, "Explanation not available")
        easygui.msgbox("The recommended methodology is: %s" % methodology)
        easygui.msgbox("Explanation: %s" % explanation)
        result = total_cost(Total_Cost(
            junior_num=self.juniors, med_num=self.midlevels, senior_num=self.seniors, junior_salary=self.Juniorsalary, med_salary=self.midlevelsalary, senior_salary=self.seniorlevelsalary, project_size=self.project_size))
        min_cost = result[0]
        max_cost = result[1]

        output_string = "Min cost: ${} and Max cost: ${}".format(
            min_cost, max_cost)
        easygui.msgbox(
            "The expected cost of completing the project is shown here the lowest expected value and the most expected value: " + output_string)

        result2 = total_time(Total_Time(project_size=self.project_size,
                             junior_number=self.juniors, med_number=self.midlevels, senior_number=self.seniors))
        min_time = result2[0]
        max_time = result2[1]

        output_string2 = "Min: {} days and Max: {} days".format(
            min_time, max_time)
        easygui.msgbox(
            "The expected time of completion of the project here is displayed the least expected value and the most expected value: " + output_string2)

    @Rule(Fact(action='find_sm'), Fact(projetsimple="no"), OR(Fact(projetcomplique="yes"),
                                                              Fact(projetcomplexe="yes")), Fact(projetchaotique="no"),
          OR(Fact(defintion="no"), Fact(clients="yes"),
             Fact(produit="no")), OR(Fact(equipe="yes"), NOT(Fact(clrShowed=W()))),
          Fact(project_size="large"), Fact(team_size="large"),
          OR(Fact(project_complexity="very complex"), Fact(
              project_complexity="very high")),
          Fact(project_timeline="long-term"), Fact(project_scope="large"),
          Fact(stakeholder_involvement="high involvement"),
          Fact(stakeholder_communication="yes"), Fact(
        technical_expertise="high"),
        Fact(technology_adoption="no"), Fact(
        flexibility="highly flexible"), Fact(requirement_change="yes"),
        Fact(risk_tolerance="highly risk-tolerant"), Fact(comfort_with_risks="yes"),
    )
    def sm_6(self):
        methodology = "Prototype"
        self.declare(Fact(m=methodology))
        self.declare(Fact(clrShowed="yes"))
        explanation = methodology_explanations.get(
            methodology, "Explanation not available")
        easygui.msgbox("The recommended methodology is: %s" % methodology)
        easygui.msgbox("Explanation: %s" % explanation)
        result = total_cost(Total_Cost(
            junior_num=self.juniors, med_num=self.midlevels, senior_num=self.seniors, junior_salary=self.Juniorsalary, med_salary=self.midlevelsalary, senior_salary=self.seniorlevelsalary, project_size=self.project_size))
        min_cost = result[0]
        max_cost = result[1]

        output_string = "Min cost: ${} and Max cost: ${}".format(
            min_cost, max_cost)
        easygui.msgbox(
            "The expected cost of completing the project is shown here the lowest expected value and the most expected value: " + output_string)

        result2 = total_time(Total_Time(project_size=self.project_size,
                             junior_number=self.juniors, med_number=self.midlevels, senior_number=self.seniors))
        min_time = result2[0]
        max_time = result2[1]

        output_string2 = "Min: {} days and Max: {} days".format(
            min_time, max_time)
        easygui.msgbox(
            "The expected time of completion of the project here is displayed the least expected value and the most expected value: " + output_string2)

    @Rule(Fact(action='find_sm'), Fact(projetsimple="no"), OR(Fact(projetcomplique="yes"),
                                                              Fact(projetcomplexe="yes")),
          Fact(projetchaotique="no"),
          OR(Fact(defintion="yes"),
             Fact(
              clients="yes"),
             Fact(produit="no")), OR(Fact(equipe="yes"), NOT(Fact(clrShowed=W()))),
          Fact(project_size="medium"), Fact(team_size="medium"),
          OR(Fact(project_complexity="complex"), Fact(
              project_complexity="very high")),
          Fact(project_timeline="medium-term"), Fact(
        project_scope="medium"), Fact(stakeholder_involvement="medium involvement"),
        Fact(stakeholder_communication="yes"), Fact(
        technical_expertise="medium"),
        Fact(technology_adoption="yes"), Fact(
        flexibility="moderately flexible"), Fact(requirement_change="yes"),
        Fact(risk_tolerance="moderately risk-tolerant"), Fact(comfort_with_risks="yes"),

    )
    def sm_7(self):
        methodology = "Incremental"
        self.declare(Fact(m=methodology))
        self.declare(Fact(clrShowed="yes"))
        explanation = methodology_explanations.get(
            methodology, "Explanation not available")
        easygui.msgbox("The recommended methodology is: %s" % methodology)
        easygui.msgbox("Explanation: %s" % explanation)
        result = total_cost(Total_Cost(
            junior_num=self.juniors, med_num=self.midlevels, senior_num=self.seniors, junior_salary=self.Juniorsalary, med_salary=self.midlevelsalary, senior_salary=self.seniorlevelsalary, project_size=self.project_size))
        min_cost = result[0]
        max_cost = result[1]

        output_string = "Min cost: ${} and Max cost: ${}".format(
            min_cost, max_cost)
        easygui.msgbox(
            "The expected cost of completing the project is shown here the lowest expected value and the most expected value: " + output_string)

        result2 = total_time(Total_Time(project_size=self.project_size,
                             junior_number=self.juniors, med_number=self.midlevels, senior_number=self.seniors))
        min_time = result2[0]
        max_time = result2[1]

        output_string2 = "Min: {} days and Max: {} days".format(
            min_time, max_time)
        easygui.msgbox(
            "The expected time of completion of the project here is displayed the least expected value and the most expected value: " + output_string2)

    @Rule(Fact(action='find_sm'), NOT(Fact(methodology=W())), salience=-2)
    def find_methodology(self):
        if 'methodology' in self.knowledge:
            return
        certainties = self.certainties
        print("GGGG")
        print(certainties)

        selected_methodology = None
        closest_distance = float('inf')

        for methodology, (min_certainty, max_certainty) in methodologies:
            midpoint_certainty = (min_certainty + max_certainty) / 2
            distance = abs(midpoint_certainty - max(certainties))

            if distance < closest_distance:
                closest_distance = distance
                selected_methodology = methodology

        print("ll")
        print(selected_methodology)

        # if selected_methodology is None:
        #     weights = [max_certainty - min_certainty for _, (min_certainty, max_certainty) in methodologies]
        #     selected_methodology = choices([methodology for methodology, _ in methodologies], weights)[0]

        # print("s")
        # print(selected_methodology)

        if selected_methodology == None:
            easygui.msgbox(
                "No matching methodology was found based on the provided characteristics.")
        else:
            message = methodology_template.substitute(
                methodology=selected_methodology)
            easygui.msgbox(message)

            result = total_cost(Total_Cost(
                junior_num=self.juniors, med_num=self.midlevels, senior_num=self.seniors, junior_salary=self.Juniorsalary, med_salary=self.midlevelsalary, senior_salary=self.seniorlevelsalary, project_size=self.project_size))
            min_cost = result[0]
            max_cost = result[1]

            output_string = "Min cost: ${} and Max cost: ${}".format(
                min_cost, max_cost)
            easygui.msgbox(
                "The expected cost of completing the project is shown here the lowest expected value and the most expected value: " + output_string)

            result2 = total_time(Total_Time(project_size=self.project_size,
                                            junior_number=self.juniors, med_number=self.midlevels, senior_number=self.seniors))
            min_time = result2[0]
            max_time = result2[1]

            output_string2 = "Min: {} days and Max: {} days".format(
                min_time, max_time)
            easygui.msgbox(
                "The expected time of completion of the project here is displayed the least expected value and the most expected value: " + output_string2)

            self.declare(Fact(methodology=selected_methodology))

    @Rule(Fact(action='find_sm'), Fact(projetsimple="no"), OR(Fact(projetcomplique="no"),
                                                              Fact(projetcomplexe="no")), Fact(projetchaotique="no"), OR(Fact(defintion="no"), Fact(clients="no"),
                                                                                                                         Fact(produit="no")), OR(Fact(equipe="no"), NOT(Fact(clrShowed=W()))))
    def sm_4(self):
        self.declare(Fact(m="Software methodology not detected"))

    @Rule(Fact(action='find_sm'), Fact(prioritized_chars=MATCH.chars), Fact(m=MATCH.m), NOT(Fact(feedback=W())), salience=-999)
    def ask_feedback(self, chars, m):
        easygui.msgbox(
            "Based on your prioritized characteristics, the recommended methodology is %s." % m)
        feedback = input(
            "Was the recommended methodology suitable for your project? (yes/no): ")
        self.declare(Fact(feedback=feedback))

    @Rule(Fact(action='find_sm'), Fact(prioritized_chars=MATCH.chars), Fact(m=MATCH.m), Fact(feedback="yes"), salience=-999)
    def feedback_yes(self, chars, m):
        easygui.msgbox(
            "Thank you for your feedback! I'm glad the recommended methodology (%s) was suitable for your project." % m)

    @Rule(Fact(action='find_sm'), Fact(prioritized_chars=MATCH.chars), Fact(m=MATCH.m), Fact(feedback="no"), salience=-999)
    def feedback_no(self, chars, m):
        easygui.msgbox(
            "Thank you for your feedback! I apologize if the recommended methodology (%s) wasn't suitable for your project." % m)
        easygui.msgbox(
            "Please provide more details about your project requirements and characteristics, so I can improve my recommendations in the future.")

    @Rule(Fact(action='find_sm'), Fact(projetsimple=MATCH.projetsimple), Fact(projetcomplique=MATCH.projetcomplique),
          Fact(projetcomplexe=MATCH.projetcomplexe), Fact(
              projetchaotique=MATCH.projetchaotique),
          Fact(defintion=MATCH.defintion), Fact(
              clients=MATCH.clients), Fact(produit=MATCH.produit),
          Fact(equipe=MATCH.equipe), Fact(
              project_size=MATCH.project_size), Fact(team_size=MATCH.team_size),
          Fact(project_complexity=MATCH.project_complexity), Fact(
              project_timeline=MATCH.project_timeline),
          Fact(project_scope=MATCH.project_scope), Fact(
              stakeholder_involvement=MATCH.stakeholder_involvement),
          Fact(stakeholder_communication=MATCH.stakeholder_communication),
          Fact(technical_expertise=MATCH.technical_expertise), Fact(
              technology_adoption=MATCH.technology_adoption),
          Fact(flexibility=MATCH.flexibility), Fact(
              requirement_change=MATCH.requirement_change),
          Fact(risk_tolerance=MATCH.risk_tolerance), Fact(
              comfort_with_risks=MATCH.comfort_with_risks),
          NOT(Fact(m=MATCH.m)), salience=-1)
    def not_matched(self, projetsimple, projetcomplique, projetcomplexe, projetchaotique, defintion, clients, produit,
                    equipe, project_size, team_size, project_complexity, project_timeline, project_scope,
                    stakeholder_involvement, stakeholder_communication, technical_expertise, technology_adoption,
                    flexibility, requirement_change, risk_tolerance, comfort_with_risks):
        print("tm")
        # easygui.msgbox(
        #     "I have not found a software development methodology corresponding to the exact characteristics given.")
        lis = [projetsimple, projetcomplique, projetcomplexe, projetchaotique, defintion, clients, produit,
               equipe, project_size, team_size, project_complexity, project_timeline, project_scope,
               stakeholder_involvement, stakeholder_communication, technical_expertise, technology_adoption,
               flexibility, requirement_change, risk_tolerance, comfort_with_risks]

        max_count = 0
        max_sm = ""
        for key, val in sm_map.items():
            count = 0
            temp_list = eval(key)
            for j in range(0, len(lis)):
                if lis[j] != 'yes' and lis[j] != 'no':
                    if temp_list[j] == lis[j]:
                        count = count + 1
                elif lis[j] == 'yes' and temp_list[j] == 'yes':
                    count = count + 1
            if count > max_count:
                max_count = count
                max_sm = val
        print("gg")
        print(count)

        if_not_matched(max_sm)

    # @Rule(Fact(action='find_sm'))
    # def evaluate_sm(self):
    #     facts = self.facts
    #     print(facts)
    #     # ... Evaluate certainty factors and select the best software methodology ...
    #     # ... You can use the certainty factors to assign confidence scores to each methodology ...
    #     # ... The methodology with the highest confidence score can be selected as the best one ...
    #     # ... You can also define a threshold value to decide if the methodology is a good match ...

    #     # Example implementation: Select the methodology with the highest certainty factor
    #     filtered_facts = [
    #         fact for fact in facts
    #         if isinstance(fact, Fact) and hasattr(fact, 'certainty')
    #         ]

    #     print(filtered_facts)
    #     for fact in filtered_facts:
    #         certainty_value = fact.certainty
    #         print(certainty_value)
    # # Perform further processing with the certainty value

    # # Perform further processing with the certainty value

    #     if filtered_facts:  # Threshold of 0.7 for a good match
    #         best_match = max(filtered_facts, key=lambda x: float(x.certainty))
    #         if best_match.certainty >= 0.7:
    #          methodology = identify_sm(best_match.projetsimple, best_match.projetcomplique, best_match.projetcomplexe, best_match.projetchaotique,
    #                                   best_match.defintion, best_match.clients, best_match.produit, best_match.equipe, best_match.project_size, best_match.team_size , best_match.project_complexity , best_match.project_timeline,
    #                                   best_match.project_scope,  best_match.stakeholder_involvement,
    #                                 best_match.stakeholder_communication,  best_match.technical_expertise,
    #                                 best_match.technology_adoption,  best_match.flexibility,
    #                                 best_match.requirement_change,  best_match.risk_tolerance, best_match.comfort_with_risks

    #                                   )
    #         if_not_matched(methodology)
    #     else:
    #         if_not_matched("Software methodology not detected")

    #     self.declare(Fact(action='done'))

    # @Rule(Fact(action='done'))
    # def goodbye(self):
    #     easygui.msgbox("Thank you for using Mnor. Goodbye!")

    # @Rule(AND(Fact(action='find_sm'), NOT(Fact(exit_command=W()))), salience=-1)
    # def exit_system(self):
    #     exit_command = easygui.msgbox("Enter 'exit' to quit the system: ")
    #     self.declare(Fact(exit_command=exit_command))
    #     if exit_command.lower() == 'exit':
    #         easygui.msgbox("Exiting the system...")
    #         self.halt()


def main():
    preprocess()
    engine = SM()
    engine.reset()
    engine.run()


if __name__ == "__main__":
    main()
