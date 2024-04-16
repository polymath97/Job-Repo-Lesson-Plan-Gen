import os
import json
from openai import OpenAI
from flask import Flask, request, jsonify
# the model function is the function description parameter for the openai completion api
from model_function import software_list, function_summary, function_key_concept, function_prior_knowledge, function_objectives, function_outcomes, function_application, function_overview, function_preparation, function_troubleshooting, function_assessment, opening_activity_description, function_opening, main_activity_description, function_main, closing_activity_description, function_closing, function_content_gen

# ensures that the app object is created before attempting to run the Flask application with app.run
app = Flask(__name__)
app.json.sort_keys = False

# Initialize the OpenAI client
OPENAI_API_TOKEN = "USE-YOUR-OWN-API-TOKEN"
# extract the token from your environment variable
api_key =  os.environ["OPENAI_API_KEY"] = OPENAI_API_TOKEN
client = OpenAI(api_key=OPENAI_API_TOKEN)

def generate_response(topic, subject, grade, student_profile, tech_domain):
    '''
    The generate_response function will generate 13 different section of the lesson plan separately with openai completion API.
    Each section of the lesson plan is generated by a single openai completion call to yield better output. 
    Because having multiple completion call will produced more detailed generated content than having only a single completion call.
    Prompt engineering method are implemented in this function where each completion will take input from the output of the previous completion.
    
    The input of this function will require 5 parameter such as topic, subject, grade,
    student profile, and tech domain. 
    The parameter student profile and tech domain are optional and can receive an empty string.
    These parameter are all string type.

    Example call --> generate_response(topic='cell division', subject='biology' , grade='high' , student_profile='hearing impairment' , tech_domain='AI and machine learning')
    Example call without specifying student profile and tech domain --> generate_response(topic='cell division', subject='biology' , grade='high' , student_profile='' , tech_domain='')
    This function will return a python dictionary object that contains all the generated section of the lesson plan.
    '''

    # call the function_content_gen() from model_function.py
    function_content = function_content_gen(grade)

    # check if tech_domain and student_profile are both selected
    # the if condition below will build the user prompt based on the corresponding input from the user

    ##### THE PROMPT WORDINGS WILL BE MASKED WITH *****

    if tech_domain and student_profile:
        user_prompt = f" ***** {grade} *****, ***** {topic} ***** {grade} ***** {subject} *****. ***** {tech_domain} *****. ***** {student_profile} *****. *****"
    elif tech_domain:
        user_prompt = f"***** {grade} *****, ***** {topic} ***** {grade} ***** {subject} *****. ***** {tech_domain} *****. *****"
    elif student_profile.strip() != "":
        user_prompt = f"***** {grade} *****, ***** {topic} ***** {grade} ***** {subject} *****. ***** {student_profile} *****"
    else:
        user_prompt = f"***** {grade} *****, ***** {topic} ***** {grade} ***** {subject} *****. *****"

    # build the system prompt that corresponds to the user input
    if student_profile:
        system_prompt = f"Y***** {grade} ***** {student_profile} *****. *****. *****."
    else:
        system_prompt = f"***** {grade} *****. *****. *****"


    client = OpenAI(timeout=30)

    # each completion will generate specific section of the lesson plan
    # completion request will generate the principal/main section of the lesson plan such as summary of the lesson plan
    completion = client.chat.completions.create(
        model="your-fine-tuned-model",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
        response_format={ "type": "json_object" },
        functions=function_summary,
        function_call={'name': 'create_lesson_summary'},
        max_tokens=2000,
        temperature=0.6,
        presence_penalty=0.6,
        top_p=0.8,
        seed=10
    )
    # call the completion, parse, and store the completion result in corresponding variable
    output_content = completion.choices[0].message.function_call.arguments
    topic = json.loads(output_content).get('topic',{})
    summary = json.loads(output_content).get('summary',{})
    tech_domain = json.loads(output_content).get('tech domain',{})
    software = json.loads(output_content).get('software', {})

    # this completion generate the key concepts section of the lesson plan
    secondCompletion = client.chat.completions.create(
        model="your-fine-tuned-model",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": f"""***** {grade} *****, *****:
                topic: {topic},
                grade: {grade},
                subject: {subject},
                student profile: {student_profile},
                tech domain: {tech_domain},
                software: {software}""",
            },
        ],
        response_format={ "type": "json_object" },
        functions=function_key_concept,
        function_call={'name': 'create_key_concepts'},
        max_tokens=500,
        temperature=0.6,
        presence_penalty=0.6,
        top_p=0.8,
        seed=2000
    )
    # call the completion, parse, and store the completion result in corresponding variable
    output_content = secondCompletion.choices[0].message.function_call.arguments
    key_concepts = json.loads(output_content).get('key concepts',{})

    # completion to generate the prior knowledge section of the lesson plan
    thirdCompletion = client.chat.completions.create(
        model="your-fine-tuned-model",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": f"""***** {grade} *****, *****:
                topic: {topic},
                grade: {grade},
                subject: {subject},
                student profile: {student_profile},
                tech domain: {tech_domain},
                software: {software},
                key concepts: {key_concepts}""",
            },
        ],
        response_format={ "type": "json_object" },
        functions=function_prior_knowledge,
        function_call="auto",
        max_tokens=500,
        temperature=0.6,
        presence_penalty=0.6,
        top_p=0.8,
        seed=3000
    )
    # call the completion, parse, and store the completion result in corresponding variable
    output_content = thirdCompletion.choices[0].message.function_call.arguments

    # this condition handle the inconsistent output of openai completion api.
    # currently the chat completion from openai may produce unexpected output at some occasion
    if 'prior knowledge' in json.loads(output_content):
        prior_knowledge = json.loads(output_content)['prior knowledge']
    elif 'priorKnowledge' in json.loads(output_content):
        prior_knowledge = json.loads(output_content)['priorKnowledge']
    elif 'prior_knowledge' in json.loads(output_content):
        prior_knowledge = json.loads(output_content)['prior_knowledge']

    # build objective_prompt based on the presence of student profile
    # in prompt engineering this constructed prompt will be passed into the next completion helping to create a more detailed completion result
    if student_profile:
        objectives_prompt = f"***** {grade} ***** {student_profile} *****, ***** {topic},*****: {grade},*****: {subject},*****: {student_profile},*****: {software},*****: {key_concepts},*****: {prior_knowledge}."
    else:
        objectives_prompt = f"***** {grade} *****, *****: {topic},*****: {grade},*****: {subject},*****: {student_profile},*****: {software},*****: {key_concepts},*****: {prior_knowledge}."

    # completion to generate the key objectives section of the lesson plan
    fourthCompletion = client.chat.completions.create(
        model="your-fine-tuned-model",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": objectives_prompt,
            },
        ],
        response_format={ "type": "json_object" },
        functions=function_objectives,
        function_call={'name': 'create_lesson_objectives'},
        max_tokens=500,
        temperature=0.9,
        presence_penalty=0.6,
        top_p=0.8,
        seed=4100
    )
    # call the completion, parse, and store the completion result in corresponding variable
    output_content = fourthCompletion.choices[0].message.function_call.arguments
    objectives = json.loads(output_content).get('objectives',{})

    # build prompt for to be called in the next completion 
    if student_profile:
        outcomes_prompt = f"***** {grade} ***** {student_profile} *****, *****: {topic},*****: {grade},*****: {subject},*****: {student_profile},*****: {software},*****: {key_concepts},*****: {prior_knowledge},*****: {objectives}. *****: *****"
    else:
        outcomes_prompt = f"***** {grade} *****, *****: {topic},*****: {grade},*****: {subject},*****: {student_profile},*****: {software},*****: {key_concepts},*****: {prior_knowledge},*****: {objectives}. *****"

    # completion to generate the outcomes section of the lesson plan
    fifthCompletion = client.chat.completions.create(
        model="your-fine-tuned-model",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": outcomes_prompt,
            },
        ],
        response_format={ "type": "json_object" },
        functions=function_outcomes,
        function_call={'name': 'create_learning_outcomes'},
        max_tokens=1000,
        temperature=0.8,
        presence_penalty=0.6,
        top_p=1,
        seed=5000
    )
    # call the completion, parse, and store the completion result in corresponding variable
    output_content = fifthCompletion.choices[0].message.function_call.arguments
    outcomes = json.loads(output_content).get('outcomes',{})

    # completion to generate the real world application section of the lesson plan
    sixthCompletion = client.chat.completions.create(
        model="your-fine-tuned-model",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": f"***** {grade} *****, *****: {topic},*****: {grade},*****: {subject},*****: {student_profile},*****: {software},*****: {key_concepts},*****: {prior_knowledge},*****: {objectives},*****: {outcomes}",
            },
        ],
        response_format={ "type": "json_object" },
        functions=function_application,
        function_call={'name': 'create_real_world_application'},
        max_tokens=500,
        temperature=0.9,
        presence_penalty=0.6,
        top_p=0.8,
        seed=6000
    )
    # call the completion, parse, and store the completion result in corresponding variable
    output_content = sixthCompletion.choices[0].message.function_call.arguments
    real_world_application = json.loads(output_content).get('real world application',{})

    # build prompt for to be called in the next completion
    if student_profile:
        overview_prompt = f"***** {grade} ***** {student_profile} *****: {topic},*****: {grade},*****: {subject},*****: {student_profile},*****: {software},*****: {key_concepts},*****: {prior_knowledge},*****: {objectives},*****: {outcomes},*****: {real_world_application}. ***** {software} *****"
    else:
        overview_prompt = f"***** {grade} *****, *****: {topic},*****: {grade},*****: {subject},*****: {student_profile},*****: {software},*****: {key_concepts},*****: {prior_knowledge},*****: {objectives},*****: {outcomes},*****: {real_world_application}. *****: ***** {software} *****."

    # completion to generate the lesson overview section of the lesson plan
    seventhCompletion = client.chat.completions.create(
        model="your-fine-tuned-model",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": overview_prompt,
            },
        ],
        response_format={ "type": "json_object" },
        functions=function_overview,
        function_call={'name': 'create_lesson_overview'},
        max_tokens=2000,
        temperature=0.4,
        presence_penalty=0.6,
        top_p=0.8,
        seed=7800
    )
    # call the completion, parse, and store the completion result in corresponding variable
    output_content = seventhCompletion.choices[0].message.function_call.arguments
    lesson_overview = json.loads(output_content).get('lesson overview',{})

    # completion to generate the pre lesson preparation section of the lesson plan
    eightCompletion = client.chat.completions.create(
        model="your-fine-tuned-model",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": f"***** {grade} *****, *****: {topic},*****: {grade},*****: {subject},*****: {student_profile},*****: {software},*****: {key_concepts},*****: {prior_knowledge},*****: {objectives},*****: {outcomes},*****: {real_world_application},*****: {lesson_overview}",
            },
        ],
        response_format={ "type": "json_object" },
        functions=function_preparation,
        function_call={'name': 'create_pre_lesson_preparation'},
        max_tokens=800,
        temperature=0.9,
        presence_penalty=0.6,
        top_p=0.8,
        seed=8000
    )
    # call the completion, parse, and store the completion result in corresponding variable
    output_content = eightCompletion.choices[0].message.function_call.arguments
    pre_lesson_preparation = json.loads(output_content).get('pre-lesson preparation',{})

    # completion to generate the troubleshooting section of the lesson plan
    ninthCompletion = client.chat.completions.create(
        model="your-fine-tuned-model",
            messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": f"***** {grade} *****, *****: {topic},*****: {grade},*****: {subject},*****: {student_profile},*****: {software},*****: {key_concepts},*****: {prior_knowledge},*****: {objectives},*****: {outcomes},*****: {real_world_application},*****: {lesson_overview},*****: {pre_lesson_preparation}",
            },
        ],
        response_format={ "type": "json_object" },
        functions=function_troubleshooting,
        function_call={'name': 'create_lesson_troubleshooting'},
        max_tokens=2000,
        temperature=0.5,
        presence_penalty=0.6,
        top_p=0.8,
        seed=9500
    )
    # call the completion, parse, and store the completion result in corresponding variable
    output_content = ninthCompletion.choices[0].message.function_call.arguments
    troubleshooting = json.loads(output_content).get('troubleshooting',{})

    # completion to generate the assessment rubric section of the lesson plan
    tenthCompletion = client.chat.completions.create(
        model="your-fine-tuned-model",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": f"***** {grade} *****, *****: {topic},*****: {grade},*****: {subject},*****: {student_profile},*****: {software},*****: {key_concepts},*****: {prior_knowledge},*****: {objectives},*****: {outcomes},*****: {real_world_application},*****: {lesson_overview},*****: {pre_lesson_preparation}",
            },
        ],
        response_format={ "type": "json_object" },
        functions=function_assessment,
        function_call={'name': 'create_assessment'},
        max_tokens=2000,
        temperature=0.8,
        presence_penalty=0.6,
        top_p=0.8,
        seed=12345
    )
    # call the completion, parse, and store the completion result in corresponding variable
    output_content = tenthCompletion.choices[0].message.function_call.arguments
    assessment_rubric = json.loads(output_content).get('assessment',{})

    # specify the system slide prompt to be used in the next completion
    if student_profile:
        system_slide = f"***** {grade} ***** {student_profile} *****. *****, *****. *****"
    else:
        system_slide = f"***** {grade} *****, *****"

    # completion to generate the opening activity section of the lesson plan
    openingCompletion = client.chat.completions.create(
        model="your-fine-tuned-model",
        messages=[
            {
                "role": "system",
                "content": system_slide
            },
            {
                "role": "user",
                "content": f"***** {grade} *****, ***** {grade} *****. *****: {topic},*****: {grade},*****: {subject},*****: {student_profile},*****: {software},*****: {key_concepts},*****: {prior_knowledge},*****: {objectives},*****: {outcomes},*****: {real_world_application},*****: {lesson_overview},*****: {pre_lesson_preparation}.",
            },
        ],
        response_format={ "type": "json_object" },
        functions=function_opening,
        max_tokens=4096,
        temperature=0.5,
        presence_penalty=0.6,
        top_p=0.8,
    )
    # call the completion, parse, and store the completion result in corresponding variable
    output_content = openingCompletion.choices[0].message.function_call.arguments
    
    '''
    currently the output of this completion are not in suitable format
    for example will output like this :'Slide 1: xxxxx' 
    the formatting that we want is like this : 'Slide 1': 'xxx'
    the conditional below handle that kind of formatting
    '''
    opening_activity_slides = {}
    last_slide = ""
    if 'opening_activity' in json.loads(output_content) or 'opening activity' in json.loads(output_content):
        opening_activity_data = json.loads(output_content).get('opening_activity') or json.loads(output_content).get('opening activity')
        opening_activity_slides = {}

        if isinstance(opening_activity_data, list):
            if len(opening_activity_data) == 1:
                slides = opening_activity_data[0]
                slide_parts = []

                if '. Slide' in slides:
                    slide_parts = slides.split('. ')
                elif '\nSlide ' in slides:
                    slide_parts = slides.split('\nSlide ')
                    if slide_parts[0] == '':
                        slide_parts = slide_parts[1:]
                elif '\n\nSlide ' in slides:
                    slide_parts = slides.split('\n\nSlide ')
                    if slide_parts[0] == '':
                        slide_parts = slide_parts[1:]
                elif '\\nSlide ' in slides:
                    slide_parts = slides.split('\\nSlide ')
                    if slide_parts[0] == '':
                        slide_parts = slide_parts[1:]

                for part in slide_parts:
                    if part.strip():
                        slide_info = part.split(': ', 1)
                        if len(slide_info) == 2:
                            slide_number, slide_content = slide_info
                            slide_number = slide_number.strip()
                            if slide_number[0].isdigit():
                                slide_number = f"Slide {slide_number}"
                            slide_content = slide_content.strip()
                            opening_activity_slides[slide_number] = slide_content
                            last_slide = slide_number
            else:
                for item in opening_activity_data:
                    slide_number, slide_content = item.split(': ', 1)
                    slide_number = slide_number.strip()
                    if slide_number[0].isdigit():
                        slide_number = f"Slide {slide_number}"
                    slide_content = slide_content.strip()
                    opening_activity_slides[slide_number] = slide_content
                    last_slide = slide_number
        else:
            raise ValueError("Invalid format for opening_activity data")

    if last_slide:
        last_slide_number = int(last_slide.split()[1])
        next_slide_number = last_slide_number + 1
        next_slide = f"Slide {next_slide_number}"

    # store the correctly formatted slides
    opening_activity = {'opening_activity': opening_activity_slides}


    # completion to generate the main activity section of the lesson plan
    mainCompletion = client.chat.completions.create(
        model="your-fine-tuned-model",
        messages=[
            {
                "role": "system",
                "content": system_slide
            },
            {
                "role": "user",
                "content": f"***** {grade} *****, ***** {grade} *****. *****: {lesson_overview.get('main overview',{})}; *****: {lesson_overview.get('main objectives',{})}; *****:  {opening_activity}; ***** {software} ***** {topic}; ***** {next_slide}; *****, ***** {software} *****, *****",
            },
        ],
        response_format={ "type": "json_object" },
        functions=function_main,
        max_tokens=4096,
        temperature=0.8,
        presence_penalty=0.6,
        top_p=0.8,
        #seed=11112
    )
    # call the completion, parse, and store the completion result in corresponding variable
    output_content = mainCompletion.choices[0].message.function_call.arguments

    '''
    currently the output of this completion are not in suitable format
    for example will output like this :'Slide 1: xxxxx' 
    the formatting that we want is like this : 'Slide 1': 'xxx'
    the conditional below handle that kind of formatting
    '''
    main_activity_slides = {}
    last_slide = ""
    if 'main_activity' in json.loads(output_content) or 'main activity' in json.loads(output_content):
        main_activity_data = json.loads(output_content).get('main_activity') or json.loads(output_content).get('main activity')
        main_activity_slides = {}

        if isinstance(main_activity_data, list):
            if len(main_activity_data) == 1:
                slides = main_activity_data[0]
                slide_parts = []

                if '. Slide' in slides:
                    slide_parts = slides.split('. ')
                elif '\nSlide ' in slides:
                    slide_parts = slides.split('\nSlide ')
                    if slide_parts[0] == '':
                        slide_parts = slide_parts[1:]
                elif '\n\nSlide ' in slides:
                    slide_parts = slides.split('\n\nSlide ')
                    if slide_parts[0] == '':
                        slide_parts = slide_parts[1:]
                elif '\\nSlide ' in slides:
                    slide_parts = slides.split('\\nSlide ')
                    if slide_parts[0] == '':
                        slide_parts = slide_parts[1:]

                for part in slide_parts:
                    if part.strip():
                        slide_info = part.split(': ', 1)
                        if len(slide_info) == 2:
                            slide_number, slide_content = slide_info
                            slide_number = slide_number.strip()
                            if slide_number[0].isdigit():
                                slide_number = f"Slide {slide_number}"
                            slide_content = slide_content.strip()
                            main_activity_slides[slide_number] = slide_content
                            last_slide = slide_number
            else:
                for item in main_activity_data:
                    slide_number, slide_content = item.split(': ', 1)
                    slide_number = slide_number.strip()
                    if slide_number[0].isdigit():
                        slide_number = f"Slide {slide_number}"
                    slide_content = slide_content.strip()
                    main_activity_slides[slide_number] = slide_content
                    last_slide = slide_number
        else:
            raise ValueError("Invalid format for main_activity data")

    if last_slide:
        last_slide_number = int(last_slide.split()[1])
        next_slide_number = last_slide_number + 1
        next_slide = f"Slide {next_slide_number}"

    # store the correctly formatted slides
    main_activity = {'main_activity': main_activity_slides}

    # completion to generate the closing activity section of the lesson plan
    closingCompletion = client.chat.completions.create(
        model="your-fine-tuned-model",
        messages=[
            {
                "role": "system",
                "content": system_slide
            },
            {
                "role": "user",
                "content": f"***** {grade} *****. *****, ***** {next_slide}, ***** {grade} *****; *****: {lesson_overview.get('closing overview',{})}; *****: {lesson_overview.get('closing objectives',{})}; *****,*****."
            },
        ],
        response_format={ "type": "json_object" },
        functions=function_closing,
        max_tokens=4096,
        temperature=0.8,
        presence_penalty=0.8,
        top_p=0.8,
        #seed=8888
    )
    # call the completion, parse, and store the completion result in corresponding variable
    output_content = closingCompletion.choices[0].message.function_call.arguments

    '''
    currently the output of this completion are not in suitable format
    for example will output like this :'Slide 1: xxxxx' 
    the formatting that we want is like this : 'Slide 1': 'xxx'
    the conditional below handle that kind of formatting
    '''
    closing_activity_slides = {}

    if 'closing_activity' in json.loads(output_content) or 'closing activity' in json.loads(output_content):
        closing_activity_data = json.loads(output_content).get('closing_activity') or json.loads(output_content).get('closing activity')
        closing_activity_slides = {}

        if isinstance(closing_activity_data, list):
            if len(closing_activity_data) == 1:
                slides = closing_activity_data[0]
                slide_parts = []

                if '. Slide' in slides:
                    slide_parts = slides.split('. ')
                elif '\nSlide ' in slides:
                    slide_parts = slides.split('\nSlide ')
                    if slide_parts[0] == '':
                        slide_parts = slide_parts[1:]
                elif '\n\nSlide ' in slides:
                    slide_parts = slides.split('\n\nSlide ')
                    if slide_parts[0] == '':
                        slide_parts = slide_parts[1:]
                elif '\\nSlide ' in slides:
                    slide_parts = slides.split('\\nSlide ')
                    if slide_parts[0] == '':
                        slide_parts = slide_parts[1:]

                for part in slide_parts:
                    if part.strip():
                        slide_info = part.split(': ', 1)
                        if len(slide_info) == 2:
                            slide_number, slide_content = slide_info
                            slide_number = slide_number.strip()
                            if slide_number[0].isdigit():
                                slide_number = f"Slide {slide_number}"
                            slide_content = slide_content.strip()
                            closing_activity_slides[slide_number] = slide_content
            else:
                for item in closing_activity_data:
                    slide_number, slide_content = item.split(': ', 1)
                    slide_number = slide_number.strip()
                    if slide_number[0].isdigit():
                        slide_number = f"Slide {slide_number}"
                    slide_content = slide_content.strip()
                    closing_activity_slides[slide_number] = slide_content
        else:
            raise ValueError("Invalid format for closing_activity data")

    # store the correctly formatted slides
    closing_activity = {'closing_activity': closing_activity_slides}

    # build prompt for next completion
    if student_profile:
        system_content = f"***** {grade} ***** {student_profile} *****, *****. *****, *****. *****"
    else:
        system_content = f"***** {grade} *****, *****. *****. *****"

    # the result of previous 3 completion will be used as input on following completion to yield a more detailed slide from the activities section
    activities = {
        'opening_activity': opening_activity,
        'main_activity': main_activity,
        'closing_activity': closing_activity
    }

    output_data = {}
    slide_tokens = openingCompletion.usage.total_tokens + mainCompletion.usage.total_tokens + closingCompletion.usage.total_tokens
    content_prompt = 0
    content_completion = 0

    # this loop will call the completion to generate a more detailed slide to the opening, main, and closing activity
    for activity_key, activity_data in activities.items():
        activity_slides = activity_data.get(activity_key, {})
        activity_output = {}
        for slide_number, slide_content in activity_slides.items():
            activity_overview = lesson_overview.get(f"{activity_key} overview", [])
            activity_objectives = lesson_overview.get(f"{activity_key} objectives", [])

            contentCompletion = client.chat.completions.create(
                model="your-fine-tuned-model",
                messages=[
                    {
                        "role": "system",
                        "content": system_slide
                    },
                    {
                        "role": "user",
                        "content": f"***** {grade} *****, ***** {topic} ***** {subject} *****. ***** {slide_number} *****: {slide_content}. *****: {activity_overview}, *****: {activity_objectives}."
                    },
                ],
                response_format={ "type": "json_object" },
                functions=function_content,
                max_tokens=4096,
                temperature=0.8,
                presence_penalty=0.8,
                top_p=0.8,
                seed=990000
            )

            output_content = contentCompletion.choices[0].message.function_call.arguments
            slide_output = json.loads(output_content)
            activity_output[slide_number] = slide_output
            slide_tokens += contentCompletion.usage.total_tokens
            content_prompt += contentCompletion.usage.prompt_tokens
            content_completion += (contentCompletion.usage.total_tokens - contentCompletion.usage.prompt_tokens)

        # the overall slide from all activity will be stored in output_data variable
        output_data[activity_key] = activity_output

    # store the main body and the slides of the lesson plan into a dictionary
    model_response_dict = {
        "core": json.loads(completion.choices[0].message.function_call.arguments),
        "key_concepts": key_concepts,
        "prior_knowledge" : prior_knowledge,
        "objectives" : objectives,
        "outcomes" : outcomes,
        "real_world_application" : real_world_application,
        "lesson_overview" : lesson_overview,
        "pre_lesson_preparation" : pre_lesson_preparation,
        "troubleshooting" : troubleshooting,
        "assessment" : assessment_rubric,
        "detailed_slides" : output_data,
        "debug":activities
    }

    # return the dictionary that contains all the section of the lesson plan
    return model_response_dict

@app.route('/generate-response', methods=['POST'])
def api_generate_response():
    '''
    this function serve as the api endpoint to request the models prediction
    Inference service will only have one endpoint which is /generate response

    Example curl request to the endpoint
    1. curl -X POST -H "Content-Type: application/json" -d '{"topic":"heat transfer simulation","subject":"science","grade":"middle","student_profile":"","tech_domain":""}' http://localhost:5000/generate-response
    2. curl -X POST -H "Content-Type: application/json" -d '{"topic":"cell division","subject":"biology","grade":"high","student_profile":"hearing impairment","tech_domain":""}' http://localhost:5000/generate-response
    '''
    try: 
        req = request.get_json()

        res = generate_response(
            req['topic'], req['subject'], req['grade'],
            req['student_profile'], req['tech_domain']
        )

        return jsonify(res), 200
    except Exception as e:
        error_message = {'error': str(e)}
        return jsonify(error_message), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
