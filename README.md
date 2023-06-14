# capstone-twitter-project
__name__ == "__main__"

Goals: Learn about implementation of E2E data processing pipelines using kafka for processing social media data (twitter)

Instructions:

Prepare a datatset - twitter dataset or a connector to twitter.
Prepare a kafka environment.
Implement a “generator” microservice that splits the dataset to messages, sends them to kafka as message or requests tweets from the twitter.
Implement a microservice that detects a language of a tweet
Implement a microservice that recognizes sentiment class of a tweet. List of sentiment classes: Negative, Positive
Implement a microservice that recognizes Named Entities (persons) a tweet
Implement a microservice that generates and displays statistics :
               a) list of languages with numbers of messages

               b) number of messages among sentiment classes

               c) top 10 Named Entities



A report should include:

A link to a source code repository with the implementation of microservices
Instructions on how to run the implementation
Link to the dataset
Statistics (p.7 in the Instructions)
