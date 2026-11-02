# 🏥 Patient Feedback Sentiment Analyzer

### Machine Learning-Based Sentiment Analysis Using Python and Flask

A machine learning web application that analyzes patient feedback and classifies it as **Positive** or **Negative** using Natural Language Processing (NLP). The application helps interpret patient feedback and understand patient satisfaction through automated sentiment classification.

---

## 📌 Overview

Patient feedback is valuable for understanding the quality of healthcare services and patient satisfaction. Manually reviewing large amounts of feedback can be time-consuming.

The **Patient Feedback Sentiment Analyzer** uses Natural Language Processing and machine learning to analyze textual feedback and predict its sentiment.

The application uses **TF-IDF for text feature extraction** and **Logistic Regression for sentiment classification**. A Flask backend connects the trained model to a simple web interface where users can submit feedback and view the predicted sentiment.

## ✨ Features

- 📝 **Feedback Analysis:** Accepts textual patient feedback.
- 🤖 **Machine Learning Prediction:** Classifies feedback as Positive or Negative.
- 🔤 **Text Vectorization:** Converts text into numerical features using TF-IDF.
- 🌐 **Web Interface:** Provides a user interface built with HTML, CSS, and JavaScript.
- ⚙️ **Flask Backend:** Handles feedback submissions and model predictions.
- 💾 **Feedback Storage:** Supports saving submitted feedback using the project's configured storage mechanism.
- 🔄 **Trained Model Loading:** Uses serialized machine learning components for predictions.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Flask | Backend web framework |
| Scikit-learn | Machine learning and text processing |
| TF-IDF Vectorizer | Text feature extraction |
| Logistic Regression | Sentiment classification |
| Pandas | Data manipulation |
| NumPy | Numerical operations |
| HTML | Web page structure |
| CSS | Web page styling |
| JavaScript | Frontend interactions |
| Pickle | Model and vectorizer serialization |

## 🔍 How It Works

The application follows these steps:

1. **Input Feedback:** The user enters patient feedback through the web interface.
2. **Text Preprocessing:** The feedback is prepared for analysis using the preprocessing steps implemented in the project.
3. **Feature Extraction:** The TF-IDF vectorizer converts the text into numerical features.
4. **Sentiment Prediction:** The trained Logistic Regression model predicts the sentiment.
5. **Display Result:** The application displays the predicted sentiment to the user.
6. **Feedback Storage:** The application stores feedback using its configured storage mechanism.

```text
        Patient Feedback
                |
                v
         Web Interface
          HTML / CSS / JS
                |
                v
          Flask Backend
                |
                v
        Text Preprocessing
                |
                v
         TF-IDF Vectorizer
                |
                v
       Logistic Regression
                |
                v
      Sentiment Classification
          /           \
         v             v
     Positive        Negative
                |
                v
       Display Prediction
                |
                v
        Feedback Storage
```

## 🧠 Machine Learning Methodology

### 1. TF-IDF Vectorization

Term Frequency–Inverse Document Frequency (TF-IDF) converts textual feedback into numerical features that a machine learning model can process.

It assigns importance to words based on their frequency in a document and how common they are across the collection of documents.

### 2. Logistic Regression

Logistic Regression is a supervised machine learning algorithm used for classification.

In this project, it learns patterns from labeled patient feedback and predicts whether new feedback expresses Positive or Negative sentiment.

### 3. Model Serialization

Pickle is used to save trained machine learning components so that the Flask application can load them without retraining the model for every prediction.

## 📂 Project Structure

The following is an illustrative structure. Adjust the filenames to match your actual repository.

```text
patient_feedback_sentiment_analyzer/
│
├── static/
│   ├── script.js
│   └── style.css
│
├── templates/
│   ├── admin.html
│   ├── dashboard.html
│   ├── history.html
│   ├── login.html
│   ├── profile.html
│   └── register.html
│
├── .gitignore
├── app.py
├── dataset.csv
├── feedback.csv
├── find_100_percent.py
├── model.pkl
├── requirements.txt
├── test_app.py
├── train_model.py
├── users.csv
├── vectorizer.pkl
```

**Note:** Include `model.pkl`, `vectorizer.pkl`, and other files only if those are their actual names in your project. Your saved model and vectorizer must match the versions expected by the application.

## 🚀 Getting Started

Follow these instructions to run the project locally.

### Prerequisites

Install Python and Git. A virtual environment is recommended.

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
```

Replace the example repository URL with your actual GitHub repository URL.

### 2. Navigate to the Project Folder

```bash
cd YOUR_REPOSITORY
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

**Windows:**

```bash
venv\Scripts\activate
```

**Linux/macOS:**

```bash
source venv/bin/activate
```

### 5. Install Dependencies

If the repository contains `requirements.txt`, run:

```bash
pip install -r requirements.txt
```

### 6. Run the Application

If `app.py` is the Flask entry point, run:

```bash
python app.py
```

Open the local address printed in your terminal, commonly:

```text
http://127.0.0.1:5000
```

## 💻 Usage

1. Start the Flask application.
2. Open the application in your browser.
3. Enter patient feedback into the input field.
4. Submit the feedback for analysis.
5. View the predicted Positive or Negative sentiment.
6. Review stored feedback if the application provides a storage-viewing feature.

## 🎯 Applications

- Understanding patient satisfaction.
- Analyzing textual feedback about healthcare services.
- Identifying positive and negative feedback patterns.
- Supporting feedback analysis in healthcare environments.

The predictions are intended to support feedback analysis, not to make medical diagnoses or replace professional judgment.

## 🔮 Future Enhancements

Potential improvements include:

- Adding a Neutral sentiment category.
- Displaying sentiment distribution using charts.
- Improving classification performance with additional labeled data.
- Adding a dashboard for analyzing feedback trends.
- Implementing secure feedback storage and access controls.
- Evaluating additional classification algorithms.

These are potential enhancements, not claims about existing functionality.

## 👨‍💻 Author

**Vaishnav Kulkarni**

Computer Science and Engineering Student

## ⭐ Acknowledgment

This project demonstrates the application of Natural Language Processing, machine learning, and web development to patient feedback analysis.

---

*Built with Python, Scikit-learn, Flask, and NLP.*