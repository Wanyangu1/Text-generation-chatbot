from flask import Flask, render_template, request
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import random

tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

app = Flask(__name__)

intents = {
    "activitiesOfFlamingoScoutRovers": {
        "examples": ["What are the typical experiences and activities of members in the Kisii University Flamingo Scout Rovers?", "What do members of the Flamingo Scout Rovers at Kisii University do?"],
        "responses": ["Members of the Flamingo Scout Rovers at Kisii University typically engage in activities such as camping, hiking, community service projects, leadership development, and outdoor skills training."]
    },
    "whatIsFlamingoscouts": {
"examples": ["what is kisii university flamingo scout rovers"],
"responses": ["The Kisii University Flamingo Scout Rovers is a student scouting organization that operates as part of the extracurricular activities at Kisii University in Kenya. The group likely engages in scouting-related events, community service, and outdoor adventures for the university's students."]
},
    "advancementInScouting": {
        "examples": ["At what level does one achieve to be in a certain category in scouting?", "How do participants advance in scouting categories?"],
        "responses": ["Advancement through the scouting categories is typically based on age and level of personal development. As young people grow older and acquire new skills and responsibilities, they progress from one category to the next."]
    },
    "categoriesInScouting": {
        "examples": ["How many categories are there in scouting?", "What are the different categories in scouting?"],
        "responses": ["Scouting is typically divided into various categories or sections based on the age groups of the participants. The specific categories may vary by country, but common ones include Beavers, Cubs, Scouts, Venturers, and Rovers."]
    },
    "communityContribution": {
        "examples": ["How do scouts contribute to the community through their activities?", "How does scouting contribute to the wider community beyond its own membership?"],
        "responses": ["Scouts contribute to the community through service projects such as conservation efforts, environmental clean-ups, and volunteering for local organizations."]
    },
    "communityEngagementInitiatives": {
        "examples": ["What initiatives does scouting undertake to address social issues and community challenges?", "How does scouting address social issues?"],
        "responses": ["Scouting undertakes initiatives to address social issues and community challenges through advocacy, awareness campaigns, and community service projects aimed at making a positive impact."]
    },
    "contactInformationForFlamingoScoutRovers": {
        "examples": ["How can I reach out to the leadership or administration of the Kisii University Flamingo Scout Rovers?", "Who can I contact in the Flamingo Scout Rovers at Kisii University?"],
        "responses": ["You can find contact information for reaching out to the Flamingo Scout Rovers leadership on their official website or through their official social media profiles."]
    },
    "coreValuesOfFlamingoScoutRovers": {
        "examples": ["What are the core values upheld by the Kisii University Flamingo Scout Rovers?", "What values does the Flamingo Scout Rovers at Kisii University stand for?"],
        "responses": ["The core values upheld by the Flamingo Scout Rovers include integrity, loyalty, service, teamwork, and respect for others."]
    },
    "culturalDiversityAndInclusion": {
        "examples": ["What role does the Kisii University Flamingo Scout Rovers play in promoting cultural diversity and inclusion?", "How does the Flamingo Scout Rovers at Kisii University support cultural diversity?"],
        "responses": ["The Flamingo Scout Rovers promote cultural diversity and inclusion by organizing events that celebrate different cultures, participating in intercultural exchange programs, and promoting understanding and respect for diverse backgrounds."]
    },
    "crewsWithinFlamingoScoutRovers": {
        "examples": ["How many crews are there within the Kisii University Flamingo Scout Rovers?", "What crews are part of the Flamingo Scout Rovers at Kisii University?"],
        "responses": ["There are five crews within the Flamingo Scout Rovers: Crane Crew, Falcon Crew, Eagle Crew, Phoenix Crew, and Peacock Crew."]
    },
    "diversityPromotion": {
        "examples": ["How does scouting promote inclusivity and diversity within its programs?", "What efforts does scouting make to ensure equal opportunities for all participants, regardless of their background?"],
        "responses": ["Scouting promotes inclusivity and diversity by welcoming members from all backgrounds, cultures, and abilities, and by fostering mutual understanding and respect."]
    },
    "eShopForFlamingoScoutRovers": {
        "examples": ["Is there an e-shop where I can find merchandise related to the Kisii University Flamingo Scout Rovers?", "Where can I buy Flamingo Scout Rovers merchandise?"],
        "responses": ["Yes, there is an e-shop where you can find merchandise and materials related to the Flamingo Scout Rovers."]
    },
    "environmentalConservationInitiatives": {
        "examples": ["How does the Kisii University Flamingo Scout Rovers promote environmental conservation?", "What does the Flamingo Scout Rovers at Kisii University do for the environment?"],
        "responses": ["The Flamingo Scout Rovers promote environmental conservation through tree planting initiatives, waste management projects, and awareness campaigns on sustainable living practices."]
    },
    "environmentalStewardship": {
        "examples": ["In what ways does scouting help young people develop a sense of environmental stewardship and awareness?", "How does scouting encourage environmental responsibility?"],
        "responses": ["Scouting encourages environmental stewardship and awareness through nature study, conservation projects, and promoting sustainable practices."]
    },
    "ethicalDevelopment": {
        "examples": ["How does scouting promote ethical decision-making and character development in young people?", "What role does scouting play in fostering ethical values?"],
        "responses": ["Scouting promotes ethical decision-making and character development through the Scout Law and Oath, which emphasize honesty, kindness, and moral responsibility."]
    },
    "founderOfScouting": {
        "examples": ["Who founded scouting?", "Who was the founder of scouting?"],
        "responses": ["The founder of scouting is Robert Baden-Powell, also known as Lord Baden-Powell. He established the scouting movement in 1907."]
    },
    "scouting": {
        "examples": ["What is scouting?", "Can you tell me about scouting?", "Tell me about scouting"],
        "responses": ["Scouting is a global youth movement that aims to support young people in their physical, mental, and spiritual development, helping them become responsible, active citizens. It involves outdoor activities, learning new skills, and contributing to the community."]
    },
    "formationOfKisiiUniversityScoutsMovement": {
        "examples": ["When was the Kisii University Scouts Movement formed?", "When was the scouts movement at Kisii University established?"],
        "responses": ["The Kisii University Scouts Movement was formed in the year 2010 under the umbrella of The Kenya Scouts Association and Kisii University."]
    },
    "foundersOfKisiiUniversityScoutsMovement": {
        "examples": ["Who were the individuals involved in starting the Kisii University Scouts Movement?", "Who founded the scouts movement at Kisii University?"],
        "responses": ["The Kisii University Scouts Movement was started by three people: Rodgers Mwai, Risper Bet, and Justus Ngari during the September-December semester of 2010."]
    },
    "goodbyes": {
        "examples": ["bye", "goodbye", "see you later"],
        "responses": ["Goodbye!", "See you later!", "Bye!"]
    },
    "greetings": {
        "examples": ["hello", "hi", "hey"],
        "responses": ["Hello!", "Hi there!", "Hey!"]
    },
    "historicalBackgroundOfFlamingoScoutRovers": {
        "examples": ["What historical background is associated with the Kisii University Flamingo Scout Rovers?", "What is the history of the Flamingo Scout Rovers at Kisii University?"],
        "responses": ["Scouting in Kenya started in 24th November 1910 and was a subsidiary of the British Scouts Association up to 1963 when Kenya got independence, then Kenya Scouts Association was formed."]
    },
    "involvementWithFlamingoScoutRovers": {
        "examples": ["How can I get involved with the Flamingo Scout Rovers at Kisii University?", "How do I join the Flamingo Scout Rovers?"],
        "responses": ["To become a member of the Flamingo Scout Rovers, interested individuals can join through the university's scouting club and participate in the activities and events organized by the group."]
    },
    "mentalHealthInitiatives": {
        "examples": ["What resources and initiatives does scouting offer to address mental health awareness and support?", "How does scouting support mental health?"],
        "responses": ["Scouting offers resources and initiatives such as mental health education, peer support networks, and initiatives to reduce stigma and promote well-being."]
    },
    "mentalHealthSupport": {
        "examples": ["How does scouting support the mental and emotional well-being of its members?", "What mental health resources does scouting provide?"],
        "responses": ["Scouting supports mental and emotional well-being by providing a supportive environment, promoting resilience, and offering opportunities for personal growth and self-expression."]
    },
    "missionOfFlamingoScoutRovers": {
        "examples": ["What is the mission of the Kisii University Flamingo Scout Rovers?", "What does the Flamingo Scout Rovers at Kisii University aim to achieve?"],
        "responses": ["The mission of the Kisii University Flamingo Scout Rovers is to promote scouting values, leadership, and community service among its members."]
    },
    "outdoorActivities": {
        "examples": ["What kind of outdoor activities do scouts participate in?", "What outdoor activities are part of scouting?"],
        "responses": ["Scouts participate in a wide range of outdoor activities, including camping, hiking, orienteering, nature study, and adventure sports."]
    },
    "outdoorEthicsPromotion": {
        "examples": ["What does scouting do to promote responsible outdoor behavior?"],
        "responses": ["Scouting promotes responsible outdoor ethics and environmental conservation through programs such as Leave No Trace, wildlife conservation, and environmental education."]
    },
    "personalDevelopment": {
        "examples": ["How does scouting contribute to the personal development of young people?", "What personal growth opportunities does scouting offer?"],
        "responses": ["Scouting contributes to personal development by fostering self-confidence, resilience, independence, and a sense of responsibility."]
    },
    "photoLibraryOfFlamingoScoutRovers": {
        "examples": ["Can I find a photo library showcasing the activities of the Kisii University Flamingo Scout Rovers?", "Where can I see photos of Flamingo Scout Rovers activities?"],
        "responses": ["Yes, you can access a photo library displaying the activities and events of the Flamingo Scout Rovers."]
    },
    "responsibleTechnologyUse": {
        "examples": ["In what ways does scouting address the responsible use of technology and digital media among young people?", "How does scouting promote responsible technology use?"],
        "responses": ["Scouting promotes the responsible use of technology and digital media through education on online safety, cyber ethics, and digital literacy."]
    },
    "roleOfFlamingoScoutRovers": {
        "examples": ["What activities do Flamingo Scout Rovers do?", "What is the role of the Flamingo Scout Rovers at Kisii University?"],
        "responses": ["The Flamingo Scout Rovers at Kisii University are likely involved in a wide range of scouting activities, which may include camping, hiking, community service projects, leadership development, outdoor skills training, and other activities aimed at promoting personal development, teamwork, and community engagement."]
    },
    "roverScoutsMotto": {
    "examples": ["What is the scout motto for Rover Scouts?", "Can you tell me the motto of Rover Scouts?"],
    "responses": ["For Rover Scouts, the motto is 'Service to Others'."]
},
"chipukiziScoutsMotto": {
    "examples": ["What is the scout motto for Chipukizi Scouts?", "Can you tell me the motto of Chipukizi Scouts?"],
    "responses": ["The motto for Chipukizi Scouts is 'Tayari', which means 'Always Ready' in Swahili."]
},
"mwambaScoutsMotto": {
    "examples": ["What is the scout motto for Mwamba Scouts?", "Can you tell me the motto of Mwamba Scouts?"],
    "responses": ["The motto for Mwamba Scouts is 'Daima Tatu', translating to 'Always Prepared' in Swahili."]
},
"sunguraScoutsMotto": {
    "examples": ["What is the scout motto for Sungura Scouts?", "Can you tell me the motto of Sungura Scouts?"],
    "responses": ["The motto for Scouts is generally Be Prepared."]
},
    "scoutPromise": {
        "examples": ["What is the scout promise?", "Can you tell me about the scout promise?", "What's the promise scouts make?"],
        "responses": ["On my honor, I will do my best To do my duty to God and my country and to help other people at all times and to obey the Scout Law.This version of the Scout Promise reflects the core values and principles of the scouting movement and is often recited as a solemn commitment by scouts."]
    },
    "scoutVision": {
    "examples": ["What is the vision of the scouting movement?"],
    "responses": ["The vision of the scouting movement is to create a better world where young people are empowered to play a constructive role in society."]
},
    "scoutMission": {
    "examples": ["What is the mission of the scouting movement?"],
    "responses": ["The mission of the scouting movement is to contribute to the education of young people, through a value system based on the Scout Promise and Law, to help build a better world where people are self-fulfilled as individuals and play a constructive role in society."]
},

    "scoutingActivities": {
        "examples": ["What kind of outdoor activities do scouts typically participate in?", "What activities are part of scouting?"],
        "responses": ["Scouts participate in a wide range of outdoor activities, including camping, hiking, orienteering, nature study, and adventure sports."]
    },
    "scoutingInKenya": {
        "examples": ["Which association is found in Kenya that deals with scouting?", "What is the scouting association in Kenya?"],
        "responses": ["The scouting association in Kenya is The Kenya Scouts Association, which oversees scouting activities and programs across the country."]
    },
    "scoutingMovementInKenya": {
        "examples": ["When did scouting start as a movement in Kenya?", "What is the history of scouting as a movement in Kenya?"],
        "responses": ["Scouting started as a movement in Kenya in 1910, initially as a subsidiary of the British Scouts Association. After Kenya gained independence in 1963, The Kenya Scouts Association was formed to oversee scouting activities in the country."]
    },
    "scoutingValues": {
        "examples": ["What are the values promoted by scouting?", "What values does scouting emphasize?"],
        "responses": ["Scouting promotes values such as integrity, loyalty, respect for others, responsibility, and community service."]
    },
    "socialMediaPresenceOfFlamingoScoutRovers": {
        "examples": ["Does the Kisii University Flamingo Scout Rovers have a social media presence?", "Where can I find the social media profiles of the Flamingo Scout Rovers?"],
        "responses": ["Yes, the Flamingo Scout Rovers at Kisii University have social media profiles where you can follow their activities and events."]
    },
    "supportForMembers": {
        "examples": ["What kind of support is available for members of the Kisii University Flamingo Scout Rovers?", "How does the Flamingo Scout Rovers support its members?"],
        "responses": ["The Flamingo Scout Rovers offer support to their members through mentorship, training programs, counseling services, and a supportive community environment."]
    },
    "uniformAndInsignia": {
        "examples": ["What is the uniform for Kisii University Flamingo Scout Rovers?", "What does the uniform and insignia of the Flamingo Scout Rovers at Kisii University look like?"],
        "responses": ["The uniform for the Flamingo Scout Rovers at Kisii University typically consists of a khaki shirt, shorts or trousers, a scarf, and a hat or beret. The insignia includes badges that represent the scout's achievements and participation in various scouting activities."]
    },
    "volunteerOpportunities": {
        "examples": ["Are there volunteer opportunities available with the Kisii University Flamingo Scout Rovers?", "How can I volunteer with the Flamingo Scout Rovers?"],
        "responses": ["Yes, there are volunteer opportunities available with the Flamingo Scout Rovers. Interested individuals can inquire with the group's leadership to learn more about how they can get involved."]
    }
}



def classify_intent(user_input):
    user_input = user_input.lower()
    for intent, data in intents.items():
        for example in data["examples"]:
            if example.lower() in user_input:
                return intent
    return None

def get_response_by_intent(intent):
    if intent in intents:
        responses = intents[intent]["responses"]
        return random.choice(responses)
    else:
        return "I'm not sure how to respond to that."

def get_Chat_response(text):
    chat_history_ids = tokenizer.encode(text + tokenizer.eos_token, return_tensors='pt')
    bot_input_ids = chat_history_ids
    chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
    return tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)

def get_response_by_intent_or_model(user_input):
    intent = classify_intent(user_input)
    if intent:
        return get_response_by_intent(intent)
    else:
        return get_Chat_response(user_input)

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["GET", "POST"])
def chat():
    user_input = request.form["msg"]
    response = get_response_by_intent_or_model(user_input)
    return response

if __name__ == '__main__':
    app.run()
