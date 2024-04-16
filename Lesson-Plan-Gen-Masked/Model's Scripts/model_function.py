'''
this is the list of function description used by the completions in the endpoint.
all this function description act as parameter that guide the content generation of corresponding completion in the main script.

Confidential prompt will be substituted with '*****'
'''

software_list='''
WARNING: THIS SECTION CAN NOT BE EMPTY.
IMPORTANT: Select relevant softwares in this list which align with the TECH DOMAIN, LESSON TOPIC, and STUDENT PROFILE.\
PRIORITIZE USING SOFTWARES FROM THIS LIST (if there is no topic-relevant software in this list, you can explore other software):
1. Blender
2. ChatterOn
3. CoSpaces
4. Fusion 360
5. Inkscape
6. Python
7. QGIS
8. Scratch
9. Tinkercad Circuits
10. Unity
11. AI Dungeon
12. Ansys 3D
13. Ansys Virtual
14. Arduino
15. Autodesk
16. Robotibockly
17. Roller Coaster Tycoon
18. Scratch
19. Sony Vegas
20. StoryBoardThat
21. Thunkable
22. TinkerCAD
23. Webot Xemo
24. YawCam
25. ChatGPT
26. Canva
27. Adobe Express
28. AI Dungeon
29. AI Experiments with Google
30. Animaker
31. Assemblr Edu
32. Brush Ninja
33. CoSpaces
34. Flip
35. Food Chain Simulator
36. Genially
37. Google Arts and Culture
38. Google AutoDraw
39. Google Forms
40. Google Maps
41. Google Sheets
42. Infinite Drum Machine
43. Jamboard
44. Machine Learning for Kids
45. Mathigon
46. Mecabricks
47. MegaMinds
48. MIT App Inventor
49. Pencil Code
50. PictoBlox
51. Piktochart
52. ReadWriteThink Timeline Creator
53. Scratch
54. SimCity
55. StoryMap JS
56. Teachable Machine - Google
57. Thinglink
58. Thunkable
59. Tinkercad
60. YAHAHA
61. StoryMap JS
62. Canva
63. AI Dungeon
64. Google Autodraw
65. Mathigon
66. MIT App Inventor
'''

function_summary = [
      {
        "name": "create_lesson_summary",
        "description": "*****",
        "parameters": {
          "type": "object",
          "properties": {
            "summary": {
              "type": "string",
              "description": "*****"
            },
            "topic": {
              "type": "string",
              "description": "The topic of the lesson"
            },
            "grade": {
              "type": "string",
              "description": "The grade of the targeted student, e.g. lower elementary student. IMPORTANT: Lower Elementary is 2nd and 3rd. Upper Elementary is 4th, 5th, 6th grade. Middle School is 7th, 8th, 9th grade. High school is everything above. Lower Elementary is 1st, 2nd, 3rd. Upper Elementary is 4th, 5th. Middle School is 6th, 7th, 8th. High school is 9th grade and above"
            },
            "subject": {
              "type": "string",
              "description": "The subject of the lesson"
            },
            "tech domain": {
              "type": "string",
              "description": "Should be one from this list (do not choose outside of given list): App Development, Artificial Intelligence, Design & Simulation, Extended Reality (AR/VR/MR), Multimedia and Animation, Programming & Coding"
            },
            "software": {
              "type": "array",
              "description": software_list,
              "items": {
                "type": "string"
              }
            },
        },
         "required": [
            "summary",
            "topic",
            "grade",
            "subject",
            "tech domain",
            "software"
        ]
      }
    }]


function_key_concept= [{
        "name": "create_key_concepts",
        "description": "*****",
        "parameters": {
          "type": "object",
          "properties": {
            "key concepts": {
              "type": "array",
              "description": "*****",
              "items": {
                "type": "string"
              }
            },
        },
         "required": [
            "key concepts"
        ]
      }
    }]

function_prior_knowledge= [{
        "name": "create_prior_knowledge",
        "description": "*****",
        "parameters": {
          "type": "object",
          "properties": {
            "prior knowledge": {
              "type": "array",
              "description": "*****",
              "items": {
                "type": "string"
              }
            },
        },
         "required": [
            "prior knowledge"
        ]
      }
    },]

function_objectives= [{
        "name": "create_lesson_objectives",
        "description": "*****",
        "parameters": {
          "type": "object",
          "properties": {
            "objectives": {
              "type": "array",
              "description": "*****",
              "items": {
                "type": "string"
              }
            },
        },
         "required": [
            "objectives"
        ]
      }
    }]

function_outcomes= [{
        "name": "create_learning_outcomes",
        "description": "*****",
        "parameters": {
          "type": "object",
          "properties": {
            "outcomes": {
              "type": "array",
              "description": "*****",
              "items": {
                "type": "string"
              }
            },
        },
         "required": [
            "outcomes"
        ]
      }
    }]

function_application= [{
        "name": "create_real_world_application",
        "description": "*****",
        "parameters": {
          "type": "object",
          "properties": {
            "real world application": {
              "type": "string",
              "description": "*****"
            },
        },
         "required": [
            "real world application"
        ]
      }
    }]


function_overview= [{
        "name": "create_lesson_overview",
        "description": "*****",
        "parameters": {
          "type": "object",
          "properties": {
            "lesson overview": {
              "type": "object",
              "description": "*****",
              "properties": {
                "opening overview": {
                  "type": "array",
                  "description": "*****",
                  "items": {
                      "type": "string"
                  }
                },
                "opening objectives": {
                  "type": "array",
                  "description": "*****",
                  "items": {
                      "type": "string"
                  }
                },
                "main overview": {
                  "type": "array",
                  "description": "*****",
                  "items": {
                      "type": "string"
                  }
                },
                "main objectives": {
                  "type": "array",
                  "description": "*****",
                  "items": {
                      "type": "string"
                  }
                },
                "closing overview": {
                  "type": "array",
                  "description": "*****",
                  "items": {
                      "type": "string"
                  }
                },
                "closing objectives": {
                  "type": "array",
                  "description": "*****",
                  "items": {
                      "type": "string"
                  }
                }
              },
              "required": [
                "opening overview",
                "opening objectives",
                "main overview",
                "main objectives",
                "closing overview",
                "closing objectives"
              ]
            }
        },
         "required": [
            "lesson overview"
        ]
      }
    }]

function_preparation= [{
        "name": "create_pre_lesson_preparation",
        "description": "*****",
        "parameters": {
          "type": "object",
          "properties": {
            "pre-lesson preparation": {
              "type": "array",
              "description": "*****",
              "items": {
                "type": "string"
              }
            },
        },
         "required": [
            "pre-lesson preparation"
        ]
      }
    }]

function_troubleshooting= [{
        "name": "create_lesson_troubleshooting",
        "description": "*****",
        "parameters": {
          "type": "object",
          "properties": {
            "troubleshooting": {
              "type": "object",
              "description": "*****",
              "properties": {
                "issues": {
                  "type": "array",
                  "description": "*****",
                  "items": {
                    "type": "object",
                    "properties": {
                      "issue": {
                        "type": "string",
                        "description": "*****"
                      },
                      "possible_reasons": {
                        "type": "array",
                        "description": "*****",
                        "items": {
                          "type": "string"
                        }
                      },
                      "resolution": {
                        "type": "array",
                        "description": "*****",
                        "items": {
                          "type": "string"
                        }
                      }
                    },
                    "required": ["issue", "possible_reasons", "resolution"]
                  }
                }
              },
              "required": ["issues"]
            },
        },
         "required": [
            "troubleshooting"
        ]
      }
    }]

function_assessment= [{
        "name": "create_assessment",
        "description": "*****",
        "parameters": {
          "type": "object",
          "properties": {
            "assessment": {
              "type": "object",
              "description": "*****",
              "properties": {
                "assessment": {
                  "type": "array",
                  "description": "*****",
                  "items": {
                    "type": "object",
                    "properties": {
                      "assessment": {
                        "type": "string",
                        "description": "*****"
                      },
                      "emerging": {
                        "type": "string",
                        "description": "*****"
                      },
                      "developing": {
                        "type": "array",
                        "description": "*****",
                        "items": {
                          "type": "string"
                        }
                      },
                      "proficient": {
                        "type": "array",
                        "description": "*****",
                        "items": {
                          "type": "string"
                        }
                      }
                    },
                    "required": ["emerging", "developing", "proficient"]
                  }
                }
              },
              "required": ["assessment"]
            }
        },
         "required": [
            "assessment"
        ]
      }
    }]

opening_activity_description = '''
*****
'''

function_opening= [{
        "name": "opening_activity_slide",
        "description": "*****",
        "parameters": {
            "type": "object",
            "properties": {
                "opening activity": {
                    "type": "array",
                    "description": opening_activity_description,
                    "items": {"type": "string"}
                }
            },
            "required": ["opening activity"],
        }
      }]

main_activity_description = '''
*****
'''

function_main= [{
        "name": "main_activity_slide",
        "description": "*****",
        "parameters": {
            "type": "object",
            "properties": {
                "main activity": {
                    "type": "array",
                    "description": main_activity_description,
                    "items": {"type": "string"}
                }
            },
            "required": ["main activity"],
        }
      }]

closing_activity_description = '''
*****
'''

function_closing= [{
        "name": "closing_activity_slide",
        "description": "*****",
        "parameters": {
            "type": "object",
            "properties": {
                "closing activity": {
                    "type": "array",
                    "description": closing_activity_description,
                    "items": {"type": "string"}
                },
            },
            "required": ["closing activity"],
        }
      }]


def function_content_gen(grade):
  function_content = [{
      "name": "create_slide_content",
      "description": f"*****",
      "parameters": {
          "type": "object",
          "properties": {
              "slideContent": {
                  "type": "array",
                  "description": '''*****
                  ''',
                  "items": {
                      "type": "string"
                  }
              },
              "slideNotes": {
                  "type": "array",
                  "description": "*****",
                  "items": {
                      "type": "string"
                  }
              }
          },
          "required": [
              "slideContent",
              "slideNotes"
          ]
      }
  }]


  return function_content



