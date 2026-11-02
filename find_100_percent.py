import pickle

def test_extreme_cases():
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('vectorizer.pkl', 'rb') as f:
        vectorizer = pickle.load(f)
        
    classes = list(model.classes_)
    
    # Let's test some positive combinations
    pos_phrases = [
        "The doctor was extremely patient and explained everything clearly and the staff were supportive.",
        "Excellent surgical outcome. The post-operative care team was prompt and caring. Very clean rooms.",
        "Short waiting time, very professional staff, and excellent care from the nurses. Highly recommend JSS Hospital.",
        "Dr. Ravi is the best cardiologist, very professional and friendly. Warm reception, polite nurses.",
        "Dr. Sharma is a wonderful pediatrician. She made my kids feel very comfortable. Excellent consultation."
    ]
    
    # Let's test some negative combinations
    neg_phrases = [
        "The waiting time was extremely long. I had to wait for two hours even with an appointment.",
        "Dirty rooms and unhygienic toilets. The bedsheets were not changed for two days. Very bad experience.",
        "The nurse was very rude and did not answer my questions properly when I asked for help. Unsupportive staff.",
        "The doctor was in a hurry and did not listen to my symptoms properly. Very unprofessional. Total rip-off.",
        "Extremely expensive treatment and hidden charges in the final bill. Smelly dirty toilets. Rude receptionists."
    ]
    
    print("--- Testing Positive Sentences ---")
    for text in pos_phrases:
        vec = vectorizer.transform([text])
        probs = model.predict_proba(vec)[0]
        pos_idx = classes.index('Positive')
        neg_idx = classes.index('Negative')
        print(f"Text: \"{text}\"")
        print(f" -> Positive Prob: {probs[pos_idx]*100:.4f}% | Negative Prob: {probs[neg_idx]*100:.4f}%")
        print()
        
    print("--- Testing Negative Sentences ---")
    for text in neg_phrases:
        vec = vectorizer.transform([text])
        probs = model.predict_proba(vec)[0]
        pos_idx = classes.index('Positive')
        neg_idx = classes.index('Negative')
        print(f"Text: \"{text}\"")
        print(f" -> Positive Prob: {probs[pos_idx]*100:.4f}% | Negative Prob: {probs[neg_idx]*100:.4f}%")
        print()

if __name__ == '__main__':
    test_extreme_cases()
