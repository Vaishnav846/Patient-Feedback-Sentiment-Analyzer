import os
import pickle
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

# Path definitions
DATASET_PATH = 'dataset.csv'
MODEL_PATH = 'model.pkl'
VECTORIZER_PATH = 'vectorizer.pkl'

def generate_synthetic_data():
    """Generates a high-quality synthetic patient feedback dataset for training."""
    print("Generating synthetic patient feedback dataset...")
    
    # 80 Positive Feedback Examples
    positive_reviews = [
        "The doctor was extremely patient and explained the diagnosis and treatment plan clearly.",
        "The hospital was clean, well-maintained, and the staff were incredibly helpful and polite.",
        "Short waiting time, very professional staff, and excellent care from the nurses.",
        "The cardiology department is top-notch. Dr. Ravi is knowledgeable and supportive.",
        "Excellent surgical outcome. The post-operative care team was prompt and caring.",
        "Very clean rooms, comfortable beds, and hygienic environment. Excellent hospital stay.",
        "The nurses were highly attentive and took care of my mother like family.",
        "Quick registration process and minimal delay in meeting the doctor.",
        "Great experience at JSS Hospital. The pediatric department took great care of my son.",
        "Dr. Sharma is a wonderful pediatrician. She made my kids feel very comfortable.",
        "The pharmacy staff were quick and all prescribed medicines were available.",
        "Very satisfied with the treatment. The staff answered all my queries patiently.",
        "Clean toilets, sanitized waiting area, and friendly reception desks.",
        "Dr. Mehta explained the surgical procedure thoroughly and relieved my anxiety.",
        "The billing department was efficient and handled my insurance claim smoothly.",
        "Helpful security staff and well-guided signage throughout the building.",
        "Wonderful nursing team. They were very gentle, kind, and responsive.",
        "Dr. Patel is a great general physician. Very thorough in checking symptoms.",
        "State of the art medical equipment and very professional radiologists.",
        "Short waiting time at the outpatient department. Highly recommend this clinic.",
        "Excellent consultation. The doctor took his time and didn't rush through the appointment.",
        "The hospital canteen serves healthy and clean food. Sanitization is top notch.",
        "Very clean outpatient department. Sanitizers are available at every corner.",
        "Dr. Verma is an outstanding orthopedist. The physiotherapy team is also excellent.",
        "The ambulance arrived on time and the paramedics were well-equipped and trained.",
        "Very prompt service. I got my lab test results online within four hours.",
        "The doctors are highly qualified and very empathetic to the patients.",
        "Staff was very cooperative during the admission process of my grandfather.",
        "Beautifully designed lobby, calm atmosphere, and excellent patient relations department.",
        "I had a smooth experience. The doctor is polite and the medicines worked quickly.",
        "Nurses are very disciplined and regular with checking vitals.",
        "Clean ward rooms, regular sweeping, and clean bedsheets provided daily.",
        "Very supportive staff at the diagnostic center. The MRI scan was done efficiently.",
        "Dr. Nair listened to all my health issues with great patience and empathy.",
        "Fast check-in and check-out. Very digital and paperless workflow.",
        "The orthopedic surgery was a success, and I can walk without pain now.",
        "Excellent ICU staff. They monitored my father 24/7 with utmost care.",
        "Very supportive administration and helpful customer service.",
        "The medical counseling before the surgery was very detailed and transparent.",
        "Dr. Gupta is very skilled and has a great bedside manner.",
        "I was treated with respect and dignity by all the staff members.",
        "Good experience at Fortis Hospital. Very hygienic and modern setup.",
        "Quick service at the emergency ward. The doctors acted immediately.",
        "Dr. Joshi is very friendly and explained the root cause of my back pain.",
        "Warm reception, polite nurses, and very clean examination rooms.",
        "Great healthcare services. The staff is highly trained and professional.",
        "The diagnostic labs are highly accurate and prompt in giving reports.",
        "I am very grateful to the nurses who took care of me overnight.",
        "The doctor's prescription was clear and he advised natural remedies too.",
        "Excellent counseling session by the nutritionist. Very practical advice.",
        "The hospital is very accessible with plenty of wheelchair ramps and elevators.",
        "Staff was extremely helpful in arranging a wheelchair for my grandmother.",
        "Very polite lab technician, did the blood draw painlessly.",
        "The doctor diagnosed my problem correctly in the first visit itself.",
        "Professional services and reasonable billing for the high-quality care provided.",
        "The recovery room was quiet and peaceful, which helped me rest well.",
        "Dr. Ravi's treatment worked like magic. My chest pain is completely gone.",
        "Clean, spacious rooms with good ventilation. Felt like home.",
        "Nurses always came with a smile, which made the hospital stay much easier.",
        "The booking process was online and very user-friendly.",
        "Excellent medical care and highly clean environment. Worth every penny.",
        "Doctors here prioritize patient wellness over making profits.",
        "Great communication from the doctors regarding post-discharge precautions.",
        "The front desk staff resolved my billing query immediately and politely.",
        "Excellent emergency team. They handled a critical case with high efficiency.",
        "The hospital has a great pharmacy that is open 24/7. Very convenient.",
        "Very systematic process from check-in to meeting the doctor.",
        "Dr. Sharma was gentle and very professional during the child checkup.",
        "Nurses were very prompt in providing pain relief medication when requested.",
        "Very clean and hygienic toilet facilities in the outpatient block.",
        "The doctor's diagnosis was spot on and my recovery has been incredibly fast.",
        "Excellent physiotherapy sessions. The exercises helped reduce joint stiffness.",
        "Staff was very cooperative in helping us with the discharge documentation.",
        "Dr. Mehta is an expert surgeon. I felt completely safe under his care.",
        "The diagnostic center has high-tech MRI and CT scan machines.",
        "Great experience overall. Highly recommended for quality healthcare.",
        "Hospitable environment, skilled doctors, and very caring nurse staff.",
        "The hospital operates very systematically. Minimal chaos or confusion.",
        "I am fully satisfied with the orthopedic treatment received here.",
        "Dr. Patel is very understanding and doesn't prescribe unnecessary medicines."
    ]
    
    # 80 Negative Feedback Examples
    negative_reviews = [
        "The waiting time was extremely long. I had to wait for two hours even with an appointment.",
        "The nurse was very rude and did not answer my questions properly when I asked for help.",
        "Dirty rooms and unhygienic toilets. The bedsheets were not changed for two days.",
        "The doctor was in a hurry and did not listen to my symptoms properly. Very unprofessional.",
        "Extremely expensive treatment and hidden charges in the final bill. Total rip-off.",
        "Poor communication between the staff. Nobody knew where the lab reports were.",
        "Incompetent staff at the reception. They lost my registration details and made me fill them again.",
        "The hospital was overcrowded, noisy, and had poor air conditioning in the waiting lounge.",
        "Dr. Ravi did not explain the side effects of the medicines and just rushed me out.",
        "The billing process took forever. I had to wait for three hours just to get discharged.",
        "Very bad experience. The staff was unsupportive and ignored my complaints of pain.",
        "The toilets were smelly, dirty, and lacked basic hygiene or hand soap.",
        "The pharmacy was out of stock for common medicines. I had to buy them from outside.",
        "Dr. Sharma was very impatient with my child and scolded him for crying.",
        "The receptionist was busy on her phone and ignored patients standing in the queue.",
        "No proper guidance or signs. I got lost looking for the cardiology department.",
        "The food provided by the canteen was cold, tasteless, and very unhygienic.",
        "The nurses were slow to respond to the call button. I had to call them thrice.",
        "Dr. Mehta charged high consultation fees but spent only two minutes with me.",
        "The insurance desk was extremely uncooperative and delayed my claim process.",
        "Dirty floors and dusty tables in the ward rooms. Very disappointed with cleanliness.",
        "The lab technician was unprofessional and caused a big bruise while drawing blood.",
        "Dr. Verma prescribed too many unnecessary laboratory tests and expensive medicines.",
        "Very disorganized systems. They scheduled two patients for the same time slot.",
        "The ambulance service was delayed by an hour, which could have been fatal.",
        "Poor security. My mobile phone was stolen from the waiting room.",
        "The doctor was very cold, distant, and showed no empathy towards my condition.",
        "No wheelchair was available and the staff refused to help my disabled father.",
        "Long queue at the billing counter. Only one counter was active out of four.",
        "Dr. Gupta's prescription was illegible and the pharmacy staff couldn't read it.",
        "The ward was noisy at night, making it impossible to get any sleep.",
        "Unprofessional behavior. The doctors and nurses were arguing in front of patients.",
        "They did not provide proper discharge summary or instructions on medicines.",
        "The diagnostic scan was delayed and they lost my digital copy of reports.",
        "Dr. Patel didn't listen to my medical history and prescribed medicines that caused allergies.",
        "Unclean clinical equipment. I felt unsafe during the checkup.",
        "The reception staff was very arrogant and talked rudely to senior citizens.",
        "The appointment booking system is broken. It takes money but doesn't book slots.",
        "Extremely long wait at the pharmacy counter. Only one person was serving.",
        "Dr. Joshi was dismissive of my knee pain and said it is just due to old age.",
        "The hospital environment is depressing and the rooms lack proper ventilation.",
        "Very slow response in the emergency room. The duty doctor arrived very late.",
        "The pediatric ward was dirty and didn't have basic toys or child-friendly design.",
        "Billing department was highly unprofessional and double-charged my credit card.",
        "The nurses forgot to give me my scheduled medication in the morning.",
        "The laboratory reports were delayed by three days, delaying my treatment.",
        "Dr. Nair was very arrogant and refused to explain the details of the diagnosis.",
        "The elevators were not working, and we had to climb three floors with a patient.",
        "Very bad post-operative care. The staff didn't check on my wound for hours.",
        "The hospital charges high prices for low quality services and basic care.",
        "The emergency triage was chaotic and the staff was panicking.",
        "Dr. Gupta did not check my test reports properly and gave wrong diagnosis.",
        "The receptionists were clueless about doctor timings and kept misinforming us.",
        "The bedsheets were stained and had a terrible smell. Very unhygienic.",
        "The nurse was rough while changing the bandages, which caused immense pain.",
        "No parking space available, and the security staff was very unhelpful.",
        "The online consultation link did not work, and the hospital refused to refund.",
        "Dr. Ravi did not show up for the scheduled appointment and no prior notice was given.",
        "The pediatric clinic was filled with dust and the play area was broken.",
        "The pharmacy sold expired medicine. This is a serious safety concern.",
        "The discharge process is extremely slow and painful for the patient.",
        "The nurse refused to help me to the restroom and told me to wait.",
        "Dr. Sharma did not answer my questions and looked annoyed when I asked them.",
        "Unclean floor in the waiting room with spilled coffee and trash left untouched.",
        "The lab reports had spelling errors and mismatched names. Very careless.",
        "The diagnostic center was stuffy and lacked proper ventilation.",
        "The hospital charges extra for basic amenities like drinking water and pillows.",
        "The emergency response number was unreachable when we needed it urgently.",
        "Dr. Mehta's treatment did not help at all. My symptoms have actually worsened.",
        "The ward staff is highly untrained and they do not follow safety protocols.",
        "Very noisy staff corridor, nurses laughing and talking loudly near ICU.",
        "The registration counter staff did not enter my email correctly, so no reports received.",
        "Dr. Verma was extremely late for the clinic, making 20 patients wait.",
        "No sanitizers in the dispensers and toilets lacked running water.",
        "The staff was very lazy and slow in responding to my requests.",
        "Dr. Patel rushed through the consultation and did not check my blood pressure.",
        "The hospital is very old, dark, and lacks clean modern facilities.",
        "The billing officer was rude and refused to give an itemized breakdown of costs.",
        "I was given the wrong dosage of medicine by an inattentive nurse.",
        "The outpatient department was extremely chaotic with no lines or queue system."
    ]
    
    # Combine into DataFrame
    feedbacks = positive_reviews + negative_reviews
    sentiments = ['Positive'] * len(positive_reviews) + ['Negative'] * len(negative_reviews)
    
    df = pd.DataFrame({
        'Feedback': feedbacks,
        'Sentiment': sentiments
    })
    
    df.to_csv(DATASET_PATH, index=False)
    print(f"Dataset created successfully with {len(df)} rows and saved to {DATASET_PATH}.")

def train_and_evaluate():
    """Loads the dataset, trains a TF-IDF + Logistic Regression model, and saves the artifacts."""
    if not os.path.exists(DATASET_PATH):
        generate_synthetic_data()
        
    df = pd.read_csv(DATASET_PATH)
    
    # Data splitting
    X = df['Feedback']
    y = df['Sentiment']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    print("Training TF-IDF Vectorizer...")
    # TF-IDF Vectorizer with English stopwords and unigrams + bigrams
    vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
    X_train_vectorized = vectorizer.fit_transform(X_train)
    X_test_vectorized = vectorizer.transform(X_test)
    
    print("Training Logistic Regression Model...")
    # Logistic Regression classifier
    model = LogisticRegression(C=1.0, random_state=42, max_iter=1000)
    model.fit(X_train_vectorized, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test_vectorized)
    acc = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy on Test Set: {acc * 100:.2f}%")
    print("\nClassification Report:\n", classification_report(y_test, y_pred))
    
    # Save the artifacts
    print(f"Saving model to {MODEL_PATH}...")
    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(model, f)
        
    print(f"Saving vectorizer to {VECTORIZER_PATH}...")
    with open(VECTORIZER_PATH, 'wb') as f:
        pickle.dump(vectorizer, f)
        
    print("Training pipeline completed successfully!")

if __name__ == '__main__':
    train_and_evaluate()
