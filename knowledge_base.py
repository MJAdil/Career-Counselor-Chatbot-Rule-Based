# knowledge_base.py

# Define attributes (skills/preferences) that can be asked about.
ATTRIBUTES = {
    "analytical_thinking": "analytical thinking",
    "creative_thinking": "creative thinking",
    "math_aptitude": "a strong aptitude for math",
    "problem_solving": "problem solving",
    "working_with_people": "working with people",
    "working_alone": "working alone",
    "helping_others": "helping others",
    "visual_thinking": "visual thinking",
    "detail_oriented": "being detail-oriented",
    "communication_skills": "strong communication skills",
    "scientific_interest": "an interest in scientific research",
    "design_aesthetics": "an eye for design and aesthetics",
    "hands_on_work": "hands-on practical work",
    "research_oriented": "being research-oriented",
    "strategic_planning": "strategic planning",
    "empathy": "empathy",
    "listening": "active listening",
    "situational_awareness": "situational awareness",
    "calm_under_pressure": "staying calm under pressure",
    "technical_proficiency": "technical proficiency",
    "memorization_skills": "memorization skills",
    "physical_stamina": "physical stamina",
    "vocal_technique": "vocal technique",
    "observational_skills": "observational skills",
    "leadership_skills": "leadership_skills",
    "resilience": "resilience",
    "continuous_learning": "a commitment to continuous learning",
    "patience": "patience",
    "ability_to_take_direction": "ability to take direction"
}


# Define careers and their associated required skills and preferences.
# 'required_skills' are strict AND conditions.
# 'preferences' are now considered 'soft' matches: if at least one preference matches, it's a positive.
CAREERS = {
    "Engineer": {
        "required_skills": ["analytical_thinking", "problem_solving", "math_aptitude"],
        "preferences": ["hands_on_work", "detail_oriented", "technical_proficiency"]
    },
    "Psychologist": {
        "required_skills": ["communication_skills", "empathy", "listening", "helping_others"],
        "preferences": ["working_with_people", "observational_skills", "resilience"]
    },
    "Graphic Designer": {
        "required_skills": ["creative_thinking", "visual_thinking", "design_aesthetics"],
        "preferences": ["detail_oriented", "hands_on_work"]
    },
    "Data Scientist": {
        "required_skills": ["analytical_thinking", "problem_solving", "math_aptitude", "research_oriented"],
        "preferences": ["detail_oriented", "continuous_learning", "communication_skills"]
    },
    "Teacher": {
        "required_skills": ["communication_skills", "helping_others", "patience"],
        "preferences": ["working_with_people", "leadership_skills", "resilience", "continuous_learning"]
    },
    "Writer/Editor": {
        "required_skills": ["creative_thinking", "detail_oriented", "communication_skills"],
        "preferences": ["working_alone", "research_oriented"]
    },
    "Architect": {
        "required_skills": ["creative_thinking", "analytical_thinking", "problem_solving", "visual_thinking", "detail_oriented"],
        "preferences": ["hands_on_work"]
    },
    "Researcher": {
        "required_skills": ["analytical_thinking", "research_oriented", "problem_solving", "continuous_learning"],
        "preferences": ["detail_oriented", "working_alone"]
    },
    "UX Researcher": { 
        "required_skills": ["analytical_thinking", "research_oriented", "communication_skills", "problem_solving", "observational_skills"],
        "preferences": ["working_with_people", "visual_thinking", "helping_others", "empathy"]
    },
    "Project Manager": {
        "required_skills": ["communication_skills", "problem_solving", "strategic_planning", "leadership_skills", "detail_oriented"],
        "preferences": ["working_with_people", "hands_on_work", "resilience"]
    },
    "Pilot": {
        "required_skills": ["analytical_thinking", "problem_solving", "calm_under_pressure", 
                            "situational_awareness", "communication_skills", "detail_oriented", 
                            "technical_proficiency", "leadership_skills", "resilience"],
        "preferences": ["hands_on_work", "working_alone", "physical_stamina"]
    },
    "Doctor": {
        "required_skills": ["empathy", "listening", "communication_skills", 
                            "problem_solving", "calm_under_pressure", "detail_oriented",
                            "resilience", "continuous_learning", "scientific_interest", "helping_others"],
        "preferences": ["working_with_people", "observational_skills", "physical_stamina"]
    },
    "Actor": {
        "required_skills": ["creative_thinking", "communication_skills", "memorization_skills", 
                            "ability_to_take_direction", "observational_skills", "resilience"],
        "preferences": ["working_with_people", "physical_stamina", "vocal_technique", "hands_on_work"]
    }
}


# Common affirmative and negative phrases for parsing user input.
AFFIRMATIVE_RESPONSES = [
    "yes", "yeah", "yep", "yup", "sure", "absolutely", "i do", "i am", "definitely",
    "of course", "true", "totally", "agree", "correct", "affirmative", "ok", "okay",
    "positive", "you bet", "go for it", "indeed", "that's right", "i think so", "for sure",
    "with numbers", "oh yaa", "i like", "a lot", "oh ya", "yess", "i do a lot", "yea", "y",
    "totes", "for sure", "totally yes", "very much", "definitely yes", "absolutely yes",
    "yeah sure", "i enjoy", "i love", "it's good", "sounds good", "great", "awesome",
    "always", "mostly", "quite a bit", "i am usually", "precise", "hell yeah", "yupp", "yes sir", "ahan",
    "yeah"
]
NEGATIVE_RESPONSES = [
    "no", "nope", "nah", "not really", "i don't", "i am not", "never", "not at all",
    "disagree", "incorrect", "negative", "by no means", "not for me", "not interested",
    "don't like", "dislike", "a lot of no", "not a lot", "n", "not at all", "not really",
    "not much", "hardly", "rarely", "not my thing", "nope"
]

# Mapping for specific multi-choice answers to their canonical forms/facts.
MULTI_CHOICE_MAPPINGS = {
    "q1_analytical_creative": {
        "analytical": "analytical_thinking",
        "logic": "analytical_thinking",
        "rational": "analytical_thinking",
        "creative": "creative_thinking",
        "artistic": "creative_thinking",
        "innovative": "creative_thinking",
        "imaginative": "creative_thinking"
    },
    "q3_working_preference": {
        "people": "working_with_people",
        "team": "working_with_people",
        "social": "working_with_people",
        "collaborate": "working_with_people",
        "alone": "working_alone",
        "independent": "working_alone",
        "solo": "working_alone",
        "with": "working_with_people",
        "together": "working_with_people",
        "individual": "working_alone",
        "myself": "working_alone",
        "in between": None,
        "both": None
    }
}

# New: Keywords that imply a "Yes" for specific Yes/No questions, based on the attribute itself.
# This helps catch synonyms of the attribute being asked about.
YES_NO_KEYWORDS = {
    "q7_detail_oriented": ["precise", "meticulous", "accurate"],
    "q15_vocal_expressiveness": ["vocal", "public speaking", "speaking", "expressive"],
    "q17_leadership": ["leader", "guiding"],
    "q14_physical_stamina": ["stamina", "energy", "demanding"],
    "q25_take_direction": ["feedback", "adapt", "direction"]
}


# Questions that the chatbot will ask.
# Reordered to prioritize broadly differentiating skills early.
QUESTIONS = [
    {
        "id": "q1_analytical_creative",
        "text": "Are you generally more **analytical** or **creative**?",
        "type": "open",
        "options": {
            "Analytical": "analytical_thinking",
            "Creative": "creative_thinking",
        }
    },
    {
        "id": "q3_working_preference",
        "text": "Do you prefer **working with people** (teams, clients) or **alone** (independent tasks)?",
        "type": "open",
        "options": {
            "With people": "working_with_people",
            "Alone": "working_alone"
        }
    },
    {
        "id": "q4_problem_solving",
        "text": "Do you enjoy **tackling complex problems** and finding solutions?",
        "type": "open",
        "options": {
            "Yes": "problem_solving",
            "No": None
        }
    },
    {
        "id": "q2_likes_math",
        "text": "Do you enjoy solving **math problems** or working with numbers?",
        "type": "open",
        "options": {
            "Yes": "math_aptitude",
            "No": None
        }
    },
    {
        "id": "q8_communication",
        "text": "Do you consider yourself to have **strong communication skills**?",
        "type": "open",
        "options": {
            "Yes": "communication_skills",
            "No": None
        }
    },
    {
        "id": "q7_detail_oriented",
        "text": "Are you generally **detail-oriented** and precise in your work?",
        "type": "open",
        "options": {
            "Yes": "detail_oriented",
            "No": None
        }
    },
    {
        "id": "q10_research",
        "text": "Are you inclined towards **research and deep investigation**?",
        "type": "open",
        "options": {
            "Yes": "research_oriented",
            "No": None
        }
    },
    {
        "id": "q9_hands_on",
        "text": "Do you prefer **hands-on, practical work** over purely theoretical tasks?",
        "type": "open",
        "options": {
            "Yes": "hands_on_work",
            "No": None
        }
    },
    {
        "id": "q12_technical_aptitude",
        "text": "Do you enjoy understanding and working with **complex technical systems**?",
        "type": "open",
        "options": {
            "Yes": "technical_proficiency",
            "No": None
        }
    },
    {
        "id": "q19_continuous_learning",
        "text": "Are you committed to **continuous learning** and staying updated in your field?",
        "type": "open",
        "options": {
            "Yes": "continuous_learning",
            "No": None
        }
    },
    {
        "id": "q5_helping_others",
        "text": "Are you interested in **helping others** and understanding their perspectives?",
        "type": "open",
        "options": {
            "Yes": "helping_others",
            "No": None
        }
    },
    {
        "id": "q11_calm_under_pressure",
        "text": "Can you remain **calm and focused under high pressure** situations?",
        "type": "open",
        "options": {
            "Yes": "calm_under_pressure",
            "No": None
        }
    },
    {
        "id": "q18_resilience",
        "text": "Are you **resilient** and able to bounce back from setbacks?",
        "type": "open",
        "options": {
            "Yes": "resilience",
            "No": None
        }
    },
    {
        "id": "q17_leadership",
        "text": "Do you see yourself as a **leader** or enjoy guiding others?",
        "type": "open",
        "options": {
            "Yes": "leadership_skills",
            "No": None
        }
    },
    {
        "id": "q23_strategic_planning",
        "text": "Are you good at **strategic planning** and organizing complex projects?",
        "type": "open",
        "options": {
            "Yes": "strategic_planning",
            "No": None
        }
    },
    {
        "id": "q6_visual_design",
        "text": "Do you have an **eye for design** and enjoy visual thinking?",
        "type": "open",
        "options": {
            "Yes": "visual_thinking",
            "No": None
        }
    },
    {
        "id": "q16_observational_skills",
        "text": "Do you enjoy **observing people** and understanding human behavior?",
        "type": "open",
        "options": {
            "Yes": "observational_skills",
            "No": None
        }
    },
    {
        "id": "q20_empathy",
        "text": "Do you have **empathy** and find it easy to understand others' feelings?",
        "type": "open",
        "options": {
            "Yes": "empathy",
            "No": None
        }
    },
    {
        "id": "q21_listening",
        "text": "Are you a **good listener** and do you pay close attention when others speak?",
        "type": "open",
        "options": {
            "Yes": "listening",
            "No": None
        }
    },
    {
        "id": "q22_patience",
        "text": "Do you consider yourself a **patient** person, especially when dealing with others?",
        "type": "open",
        "options": {
            "Yes": "patience",
            "No": None
        }
    },
    {
        "id": "q24_scientific_interest",
        "text": "Do you have a strong **interest in scientific research** and discovery?",
        "type": "open",
        "options": {
            "Yes": "scientific_interest",
            "No": None
        }
    },
    {
        "id": "q13_memorization",
        "text": "Are you good at **memorizing information** (e.g., facts, lines, procedures)?",
        "type": "open",
        "options": {
            "Yes": "memorization_skills",
            "No": None
        }
    },
    {
        "id": "q14_physical_stamina",
        "text": "Do you have good **physical stamina** and energy for demanding tasks?",
        "type": "open",
        "options": {
            "Yes": "physical_stamina",
            "No": None
        }
    },
    {
        "id": "q15_vocal_expressiveness",
        "text": "Are you interested in developing your **vocal expressiveness** or public speaking?",
        "type": "open",
        "options": {
            "Yes": "vocal_technique",
            "No": None
        }
    },
    {
        "id": "q25_take_direction",
        "text": "Are you comfortable **taking direction** and adapting to feedback?",
        "type": "open",
        "options": {
            "Yes": "ability_to_take_direction",
            "No": None
        }
    }
]

