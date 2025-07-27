# rules_engine.py
from knowledge_base import CAREERS, ATTRIBUTES, QUESTIONS

class RulesEngine:
    def __init__(self):
        self.careers = CAREERS
        self.attributes = ATTRIBUTES
        self.questions = QUESTIONS
        self.user_facts = set()    # To store what we know about the user (positive attributes)
        self.answered_questions = set() # To keep track of questions already asked

    def add_fact(self, fact_id):
        """Adds a new fact (attribute) about the user to the working memory."""
        self.user_facts.add(fact_id)

    def mark_question_answered(self, question_id):
        """Marks a question as answered."""
        self.answered_questions.add(question_id)

    def clear_session(self):
        """Clears all facts and answered questions for a new session."""
        self.user_facts.clear()
        self.answered_questions.clear()

    def get_current_viable_careers_and_suggestions(self):
        """
        Evaluates current user facts against career requirements.
        Returns:
            - suggested_careers (list): Careers that fully match all criteria (required_skills AND at least one preference).
            - viable_careers_in_progress (list): Careers that are still possible
              (have not been disqualified by any *known* required_skills mismatch).
            - fallback_suggestions (list): Careers that are a 'near match' based on required skills met,
              if no perfect suggestions are found.
        """
        suggested_careers = set()
        
        # Initialize viable_careers_in_progress with ALL careers at the start.
        # This set will be pruned as facts are gathered.
        viable_careers_in_progress = set(self.careers.keys()) 
        
        # To store careers and their match scores for fallback suggestions
        career_required_skills_match_counts = {} 

        for career_name, career_data in self.careers.items():
            career_required_skills = set(career_data.get("required_skills", []))
            career_preferences = set(career_data.get("preferences", []))

            # --- 1. Determine if career meets all required skills for a 'perfect' suggestion ---
            # This check is for the final 'suggested_careers' list.
            meets_all_required_skills_for_suggestion = True
            matched_required_skills_count = 0
            
            if career_required_skills:
                for skill in career_required_skills:
                    if skill in self.user_facts:
                        matched_required_skills_count += 1
                    else:
                        meets_all_required_skills_for_suggestion = False
            
            career_required_skills_match_counts[career_name] = matched_required_skills_count

            # --- 2. Pruning for `viable_careers_in_progress` (dynamic pruning) ---
            # A career is removed from `viable_careers_in_progress` if a required skill is missing
            # AND the question related to that skill has been answered.
            # This is the core of the pruning logic.
            if career_required_skills:
                for skill in career_required_skills:
                    if skill not in self.user_facts:
                        # Find the question that infers this specific skill
                        question_id_for_skill = None
                        for q in self.questions:
                            if skill in q["options"].values():
                                question_id_for_skill = q["id"]
                                break
                        
                        # If the question related to this missing required skill has been answered,
                        # then this career is no longer viable.
                        if question_id_for_skill and question_id_for_skill in self.answered_questions:
                            viable_careers_in_progress.discard(career_name)
                            break # This career is disqualified from viable_careers_in_progress, move to next career

            # --- 3. Final 'perfect' suggestions check ---
            # This part remains the same, it determines the final suggestions.
            if meets_all_required_skills_for_suggestion:
                meets_preferences = True 
                if career_preferences:
                    found_matching_preference = False
                    for preference in career_preferences:
                        if preference in self.user_facts:
                            found_matching_preference = True
                            break
                    if not found_matching_preference:
                        meets_preferences = False
                if meets_preferences:
                    suggested_careers.add(career_name)
        
        # --- Fallback Logic: If no perfect suggestions, find near matches ---
        fallback_suggestions = []
        if not suggested_careers: # Only calculate fallbacks if no perfect matches
            max_matched_skills = 0
            if career_required_skills_match_counts:
                max_matched_skills = max(career_required_skills_match_counts.values())

            if max_matched_skills > 0:
                top_scoring_careers = [
                    c_name for c_name, score in career_required_skills_match_counts.items() 
                    if score == max_matched_skills
                ]
                
                fallback_candidates_with_pref_score = []
                for career_name in top_scoring_careers:
                    career_preferences = set(self.careers[career_name].get("preferences", []))
                    pref_match_count = 0
                    if career_preferences:
                        for pref in career_preferences:
                            if pref in self.user_facts:
                                pref_match_count += 1
                    fallback_candidates_with_pref_score.append((career_name, pref_match_count))
                
                fallback_candidates_with_pref_score.sort(key=lambda x: x[1], reverse=True)

                for career_name, _ in fallback_candidates_with_pref_score:
                    if career_name not in suggested_careers:
                        fallback_suggestions.append(career_name)
                    if len(fallback_suggestions) >= 3:
                        break
                
        return list(suggested_careers), list(viable_careers_in_progress), fallback_suggestions

    def get_next_question(self, viable_careers_in_progress):
        """
        Determines the next relevant question to ask based on viable careers.
        Prioritizes questions that infer unknown required skills for viable careers.
        """
        # 1. Identify all unknown required skills from currently viable careers
        unknown_required_skills = set()
        for career_name in viable_careers_in_progress:
            career_data = self.careers[career_name]
            if "required_skills" in career_data:
                for skill in career_data["required_skills"]:
                    if skill not in self.user_facts:
                        unknown_required_skills.add(skill)
        
        # 2. Prioritize questions that infer these unknown required skills
        for q_data in self.questions:
            if q_data["id"] not in self.answered_questions:
                for option_fact_id in q_data["options"].values():
                    if option_fact_id and option_fact_id in unknown_required_skills:
                        return q_data

        # 3. If no more unknown required skills to ask about,
        #    ask about unknown preferences for viable careers
        unknown_preferences = set()
        for career_name in viable_careers_in_progress:
            career_data = self.careers[career_name]
            if "preferences" in career_data:
                for preference in career_data["preferences"]:
                    if preference not in self.user_facts:
                        unknown_preferences.add(preference)
        
        for q_data in self.questions:
            if q_data["id"] not in self.answered_questions:
                for option_fact_id in q_data["options"].values():
                    if option_fact_id and option_fact_id in unknown_preferences:
                        return q_data

        # 4. If no more relevant questions for viable careers, return None
        return None
