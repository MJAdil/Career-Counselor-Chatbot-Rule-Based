# app.py
import streamlit as st
from rules_engine import RulesEngine
# Ensure all necessary components are imported from knowledge_base
from knowledge_base import ATTRIBUTES, QUESTIONS, AFFIRMATIVE_RESPONSES, NEGATIVE_RESPONSES, MULTI_CHOICE_MAPPINGS, YES_NO_KEYWORDS

# --- Session State Initialization ---
if 'rules_engine' not in st.session_state:
    st.session_state.rules_engine = RulesEngine()
    print(f"DEBUG (app.py): RulesEngine initialized. Total questions loaded: {len(st.session_state.rules_engine.questions)}")

if 'messages' not in st.session_state:
    st.session_state.messages = []

# NEW: Store the ID of the question currently displayed/being answered
if 'current_question_id' not in st.session_state:
    st.session_state.current_question_id = None # Initially no question is displayed

if 'quiz_started' not in st.session_state:
    st.session_state.quiz_started = False

if 'answered_facts' not in st.session_state:
    st.session_state.answered_facts = []

if 'chat_input_key' not in st.session_state:
    st.session_state.chat_input_key = 0

# --- Helper Functions ---

def add_message(role, content):
    """
    Adds a message to the chat history.
    Prevents adding exact duplicate messages if a rapid rerun occurs,
    improving visual cleanliness.
    """
    if not st.session_state.messages or \
       not (st.session_state.messages[-1]["role"] == role and st.session_state.messages[-1]["content"] == content):
        st.session_state.messages.append({"role": role, "content": content})

def get_next_question_from_engine_with_pruning():
    """
    Gets the next relevant question from RulesEngine, considering viable careers.
    This function acts as a wrapper to call the pruning logic in the RulesEngine.
    """
    engine = st.session_state.rules_engine
    
    _, viable_careers, _ = engine.get_current_viable_careers_and_suggestions()
    
    print(f"DEBUG (app.py): get_next_question_from_engine_with_pruning called. Current State:")
    print(f"DEBUG (app.py):   Viable careers from engine: {viable_careers}")
    print(f"DEBUG (app.py):   Answered questions in engine: {engine.answered_questions}")
    print(f"DEBUG (app.py):   User facts in engine: {engine.user_facts}")

    return engine.get_next_question(viable_careers)


def process_user_input(user_input_text):
    """
    Processes the user's typed input, attempting to match it against
    the expected answers for the current question.
    """
    engine = st.session_state.rules_engine
    
    print(f"DEBUG (app.py): process_user_input called with input: '{user_input_text}'")
    print(f"DEBUG (app.py): current_question_id before processing input: {st.session_state.current_question_id}")

    # Retrieve the question data using the stored ID
    current_q_data = None
    if st.session_state.current_question_id:
        # Find the question in the QUESTIONS list by its ID
        for q in QUESTIONS:
            if q["id"] == st.session_state.current_question_id:
                current_q_data = q
                break
    
    if not current_q_data:
        add_message("assistant", "It seems I don't have a question active right now. Would you like to start over?")
        print("DEBUG (app.py): No active question data found to process user input.")
        return

    print(f"DEBUG (app.py): Processing answer for question ID: {current_q_data['id']}")
    user_input_cleaned = user_input_text.lower().strip()
    
    matched_fact_id = None
    matched_option_text = None 

    is_yes_no_question = 'Yes' in current_q_data["options"] and 'No' in current_q_data["options"]

    # 1. Try to match using explicit Multi-Choice Mappings (highest priority)
    if current_q_data["id"] in MULTI_CHOICE_MAPPINGS:
        for keyword, fact_id in MULTI_CHOICE_MAPPINGS[current_q_data["id"]].items():
            if keyword in user_input_cleaned:
                matched_fact_id = fact_id
                for opt_text, f_id in current_q_data["options"].items():
                    if f_id == matched_fact_id:
                        matched_option_text = opt_text
                        break
                print(f"DEBUG (app.py): Match found via MULTI_CHOICE_MAPPINGS: {matched_fact_id}")
                break 

    # 2. If not matched yet, and it's a Yes/No question, try attribute-specific keywords.
    #    Make sure the question is actually a Yes/No type.
    if matched_fact_id is None and is_yes_no_question and current_q_data["id"] in YES_NO_KEYWORDS:
        for keyword in YES_NO_KEYWORDS[current_q_data["id"]]:
            if keyword.lower() in user_input_cleaned:
                matched_fact_id = current_q_data["options"]['Yes']
                matched_option_text = 'Yes'
                print(f"DEBUG (app.py): Match found via YES_NO_KEYWORDS: {matched_fact_id}")
                break

    # 3. If not matched yet, and it's a Yes/No question, try general affirmative/negative phrases.
    if matched_fact_id is None and is_yes_no_question: # Ensure it's explicitly a Yes/No question
        if any(phrase in user_input_cleaned for phrase in AFFIRMATIVE_RESPONSES):
            matched_fact_id = current_q_data["options"]['Yes']
            matched_option_text = 'Yes'
            print(f"DEBUG (app.py): Match found via AFFIRMATIVE_RESPONSES: {matched_fact_id}")
        elif any(phrase in user_input_cleaned for phrase in NEGATIVE_RESPONSES):
            # For negative responses, we explicitly set matched_fact_id to None
            # if the 'No' option in knowledge_base maps to None.
            # This ensures the question is marked as answered without adding a fact.
            matched_fact_id = current_q_data["options"].get('No', None) # Safely get 'No' fact or None
            matched_option_text = 'No'
            print(f"DEBUG (app.py): Match found via NEGATIVE_RESPONSES: {matched_fact_id}")


    # 4. Fallback: If still not matched, try to match direct canonical options.
    if matched_fact_id is None:
        for option_text, fact_id in current_q_data["options"].items():
            if option_text.lower().strip() == user_input_cleaned:
                matched_fact_id = fact_id
                matched_option_text = option_text
                print(f"DEBUG (app.py): Match found via direct option text: {matched_fact_id}")
                break
            
    # --- Process the result of matching ---
    # A response is considered valid if a fact_id was matched OR if it's a recognized "No" answer
    if matched_fact_id is not None or (is_yes_no_question and matched_option_text == 'No'):
        if matched_fact_id: # Only add fact if it's not None (i.e., it's a positive fact)
            engine.add_fact(matched_fact_id)
            if matched_fact_id in ATTRIBUTES:
                st.session_state.answered_facts.append(ATTRIBUTES[matched_fact_id])
        
        # Always mark the question as answered if a valid response was provided
        engine.mark_question_answered(current_q_data["id"]) # CORRECTED: Changed 'mark_Youtubeed' to 'mark_question_answered'
        st.session_state.current_question_id = None # Clear current question ID after answering
        
        print(f"DEBUG (app.py): Fact added: '{matched_fact_id}'. Question marked answered: '{current_q_data['id']}'.")
        print(f"DEBUG (app.py): State after processing: User Facts: {engine.user_facts}, Answered Questions: {engine.answered_questions}")

        display_confirmation_text = matched_option_text if matched_option_text else user_input_text
        add_message("assistant", f"Got it! You've indicated '{display_confirmation_text}'.")
        
        ask_next_question_or_show_results()
    else:
        # No valid match found, prompt for re-entry
        options_hint = ", ".join([f"'{opt}'" for opt in current_q_data['options'].keys()])
        add_message("assistant", f"I'm sorry, I didn't quite understand '{user_input_text}'. Please try again, specifically choosing from: {options_hint}.")


def ask_next_question_or_show_results():
    """
    Determines if there's a next relevant question or if results should be shown.
    Uses the new pruning logic.
    """
    print(f"DEBUG (app.py): ask_next_question_or_show_results called.")
    
    next_q_data = get_next_question_from_engine_with_pruning()

    if next_q_data:
        add_message("assistant", next_q_data["text"])
        options_hint = ", ".join([f"'{opt}'" for opt in next_q_data["options"].keys()])
        add_message("assistant", f"(Please respond with one of the following: {options_hint})")
        st.session_state.current_question_id = next_q_data["id"] # STORE THE ID OF THE ASKED QUESTION
        print(f"DEBUG (app.py): Next question asked: {st.session_state.current_question_id}") # Added debug
    else:
        print("DEBUG (app.py): No next question found. Displaying final results.")
        st.session_state.current_question_id = None # Clear if no more questions
        display_final_results_in_chat()


def display_final_results_in_chat():
    """Displays career suggestions and summary in the chat."""
    engine = st.session_state.rules_engine
    
    suggestions, _, fallback_suggestions = engine.get_current_viable_careers_and_suggestions()
    print(f"DEBUG (app.py): Final Suggestions: {suggestions}, Fallback: {fallback_suggestions}")

    if suggestions:
        suggestion_text = "Based on your answers, here are some potential career paths for you:\n\n"
        for career in suggestions:
            suggestion_text += f"- **{career}**\n"
        add_message("assistant", suggestion_text)
    elif fallback_suggestions:
        fallback_text = "We couldn't find a direct match for a career path, but based on your answers, you might also consider:\n\n"
        for career in fallback_suggestions:
            fallback_text += f"- **{career}**\n"
        add_message("assistant", fallback_text)
    else:
        add_message("assistant", "We couldn't find a direct match or even close alternatives for a career path based on your answers.")
        add_message("assistant", "It's possible we need more information, or to broaden our career profiles.")

    if st.session_state.answered_facts:
        facts_summary = "Here's a summary of your indicated interests and preferences:\n\n"
        for fact_text in st.session_state.answered_facts:
            facts_summary += f"- {fact_text}\n"
        add_message("assistant", facts_summary)
    else:
        add_message("assistant", "No specific preferences were recorded for this session.")
    
    add_message("assistant", "To start a new session, please type 'start over' or click the 'Restart Conversation' button below.")


# --- Main Streamlit Application UI Layout ---

st.set_page_config(page_title="Career Counselor Chatbot", layout="centered")
st.title("Career Counselor Chatbot 🤖")
st.markdown("---")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if not st.session_state.quiz_started:
    if st.button("Start Conversation"):
        st.session_state.quiz_started = True
        st.session_state.messages = []
        st.session_state.rules_engine.clear_session()
        st.session_state.current_question_id = None # Reset
        st.session_state.answered_facts = []
        st.session_state.chat_input_key += 1
        
        add_message("assistant", "Hello! I'm here to help you explore potential career paths.")
        add_message("assistant", "To get started, I'll ask you a few questions about your interests and preferences.")
        ask_next_question_or_show_results()
        st.rerun()
    
if st.session_state.quiz_started:
    prompt = st.chat_input("Type your answer here...", key=f"chat_input_{st.session_state.chat_input_key}")
    
    if prompt:
        add_message("user", prompt)
        
        if prompt.lower().strip() == "start over":
            st.session_state.quiz_started = False
            st.session_state.messages = []
            st.session_state.rules_engine.clear_session()
            st.session_state.current_question_id = None # Reset
            st.session_state.answered_facts = []
            st.session_state.chat_input_key += 1
            st.rerun()
        else:
            process_user_input(prompt)
            st.session_state.chat_input_key += 1
            st.rerun() 

    if st.session_state.messages and st.session_state.messages[-1]["role"] == "assistant" and \
       ("Based on your answers, here are some potential career paths for you:" in st.session_state.messages[-1]["content"] or \
        "We couldn't find a direct match" in st.session_state.messages[-1]["content"]):
        if st.button("Restart Conversation", key="final_restart_button"):
            st.session_state.quiz_started = False
            st.session_state.messages = []
            st.session_state.rules_engine.clear_session()
            st.session_state.current_question_id = None # Reset
            st.session_state.answered_facts = []
            st.session_state.chat_input_key += 1
            st.rerun()
