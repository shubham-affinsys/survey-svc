# Survey Builder Documentation

## 1. INTRODUCTION
The Survey Builder is a drag-and-drop tool that enables users to design surveys by creating custom question flows, controlling the order and selection of questions asked throughout the survey.

## 2. FUNCTIONAL SPECIFICATIONS

### Features to be derived from Node-red:
- **Palette of specific reusable nodes**
- **Drag and drop feature** on nodes with connectors to paint the flow on the canvas
- **Deployment** of one or all flows
- **Subflow creation** and saving of the subflows as additional nodes, with environment variables provided to these subflows
- **Generation of JSON output** for the flow
- **Importing and exporting** one or all flows
- Ability to **copy-paste** certain parts of a flow or the entire selected flow to another flow

## 3. Application Design Overview

### Major Components

#### Survey:
- **Start**: Declares the start of the flow or survey questions. The question corresponding to the start node will be set as the First Question.
  
- **Question**: A new question can be created using the node, with endpoints that can be connected to other questions to simulate a flow. Conditions/rules can be set to show a question only when a specified condition is met (e.g., show the next question based on the option selected or response given by the user).
  
  **Fields in Question Node:**
  - `id`: Unique identifier of the Node as shown in the flow
  - `text`: The actual question being asked (e.g., "How satisfied were you with the product?")
  - `description`: Description of the question, e.g., example, image, etc.
  - `type`: The type of question, e.g., multiple-choice, yes/no, rating (1-5), score (1-10), multiple choice, checkbox, radio, or text field
  - `options`: Not applicable for text fields. Options for the question, with each option potentially mapped to a user sentiment (positive, negative, neutral, or no sentiment)
  - `depends_on`: The visibility of the question can be set to show only when a condition or rule is met (e.g., if the user had a positive response to `question_001`)

- **End Node**: Marks the end of the survey; user responses are stored and sent to the server.

### SAMPLE JSON SURVEY PAYLOAD
#### Structure of Question Object

- **Question**: An object with the following attributes:
  - `type`: Stores the type of question
  - `text`: Actual question text
  - `description`: Stores images, URL, or question description
  - `is_required`: Boolean to check if the question is mandatory
  - `data`: Data regarding the question
  - `options`: Options for multiple-choice questions, with each option's value and sentiment (e.g., positive, negative, neutral, no sentiment)
  - `input`: For text fields; includes a placeholder value and sentiment (no sentiment for text fields)
  - `depends_on`: List of conditions for when this question should be displayed
  - `question_id`: The question ID on which the visibility depends
  - `sentiment`: Sentiment to render only on a specific sentiment (e.g., positive, negative, neutral, no_sentiment, ANY for multi-choice or text fields)
  - `next`: Mapping for the next question based on user response sentiment

```json
{
 "survey_title": "Customer Feedback Survey",
 "survey_id": "survey123",
 "description": "A survey to collect feedback on customer satisfaction.",
 "total_questions": 10,
 "questions": {
    "question_001": {
       "type": "mcq",
       "text": "How satisfied are you with our service?",
       "description": "https://image.url.com/",
       "is_required": "true",
       "data": {
          "options": [
             { "value": "Very Satisfied", "sentiment": "positive" },
             { "value": "Satisfied", "sentiment": "positive" },
             { "value": "Not Satisfied", "sentiment": "negative" },
             { "value": "Neutral", "sentiment": "neutral" }
          ]
       },
       "depends_on": [],
       "next": {
          "positive": "question_001",
          "negative": "question_002",
          "neutral": "question_003",
          "no_sentiment": "question123"
       }
    },
    "question_003": {
       "type": "text_field",
       "text": "How was your experience with our insurance policy?",
       "description": "https://terms.and.conditions.com/",
       "is_required": "true",
       "data": {
          "input": { "value": "placeholder value", "sentiment": "no_sentiment" }
       },
       "depends_on": [
          { "question_id": "question123", "sentiment": "negative" },
          { "question_id": "question123", "sentiment": "ANY" }
       ],
       "next": {
          "positive": "",
          "negative": "",
          "neutral": "",
          "no_sentiment": "question123"
       }
    }
 },
 "timestamp": "2024-11-05T10:30:00Z",
 "tenant": "tenant123",
 "channel_id": "1234567890",
 "created_by": ["admin_user", "survey_manager"],
 "theme_data": {
    "logo": "https://example.com/logo.png",
    "colors": "#3498db"
 }
}
```

## Storing User Response

The user's responses are stored as a JSON object, structured as a list of individual question responses. This JSON updates with each answered question. Each response entry includes:

- **question_id**: Unique identifier for the question
- **type**: Type of the question (e.g., multiple-choice, text)
- **text**: Text of the question
- **value**: Value of the selected option or user input
- **sentiment**: Sentiment of the response (use `no_sentiment` for text fields)
- **next**: Reference to the next question, if related to the previous answer

### Additional Metadata Attributes for Response

- **responses**: List of all responses
- **response_id**: Unique identifier for the response
- **user_id**: Identifier for the responding user
- **survey_id**: Identifier for the survey
- **tenant**: Identifier for the tenant
- **channel_id**: Identifier for the survey channel (e.g., WhatsApp, web)
- **created_by**: Survey author identifiers

### Response JSON Example

```json
{
   "response_id": "res1234",
   "user_id": "user123",
   "survey_id": "survey123",
   "survey_title": "Customer Feedback Survey",
   "description": "A survey to collect feedback on customer satisfaction.",
   "responses": [
       {
         "question_id": "question_001",
         "type": "mcq",
         "text": "How satisfied are you with our service?",
         "value": "Satisfied",
         "sentiment": "positive",
         "next": ["question_002"],
         "is_required": "true"
       },
       {
         "question_id": "question_002",
         "type": "text_field",
         "text": "How was your experience with our insurance policy?",
         "value": "I was not able to claim my insurance",
         "sentiment": "no_sentiment",
         "next": ["end"],
         "is_required": "true"
       }
   ],
   "status": "completed",
   "timetaken": 200,
   "total_questions": 10,
   "questions_asked": 2,
   "questions_answered": 2,
   "response_timestamp": "2024-11-05T10:30:00Z",
   "timestamp": "2024-11-05T10:30:00Z",
   "tenant": "tenant123",
   "channel_id": "1234567890",
   "created_by": ["admin_user", "survey_manager"]
}
