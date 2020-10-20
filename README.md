## Attentive

Attentive is an online tool that helps teachers to determine a student’s level of engagement and focus during a class. It creates a report describing the amount of time spent on an assignment, the average attention span of the student, and times when the student was distracted. This can be used to improve online learning and ensure that students are being taught knowledge they will need throughout their lives.

## How It Works
[Video Demo](https://youtu.be/HtqbOsGRn9M)

First, students/teachers sign into Attentive using their Google account. Then, through the use of Google Classroom API, they are automatically shown their classes and assignments. The first time students login to Attentive, they need to go through a one-time training step (similar to FaceID setup). Over the course of two 45 second intervals, around 1000 images are taken of the student looking at and away from their computer. These images train a Convolutional neural network (CNN) which is used to analyze images of the student while they are working. The model is a simple binary classification, which determines if a student is looking at their computer, or if they have turned their face away. The only data that is used is from the training images which were provided by the student (I didn't use any external face orientation dataset). Each student gets their own ML model trained to their face and environment. Once training has been completed, students can start the program. They simply select the class and assignment they would like to work on, and then hit the start button in the center of the screen. This begins a process that takes an image of the student every second. Once they click End, the custom ML model analyzes the images taken during the session and writes the info gathered from the images (amount of time spent on an assignment, the average attention span of the student, and times when the student was distracted) into a MongoDB database. This info is then displayed inside the teacher portal, who can use it to revise their lectures/assignments and improve online learning.

## Accomplishments I'm Proud Of
 - Achieved a 99% validation accuracy while testing the ML model trained to my environment. ("Aryan-Jain.model" is the package)
 - Attentive creates a custom Machine Learning model for every student and their environment. Because no outside datasets are used, this prevents biased data from misclassifying images of any user.
 - Attentive is very CPU and Memory efficient because the only operation that would occur on the user's computer is the action of taking a picture. Everything else (training of ML model, analysis of images, displaying info onto the website) is done on a server. This structure allows Attentive to be run on any computer with a camera.
 - Attentive is able to successfully maintain user privacy because no one has access to any images, and once they have been analyzed both the training and working images are deleted. The training data can be deleted because we save the weights in a .model file ("Aryan-Jain.model"), and the information from the working images is saved in a MongoDB database.

## What I Learned:
 - Displaying Live Video with OpenCV
 - Taking images with OpenCV
 - Using Google Sign In and Google APIs with OAuth
 - The process of preparing images to make them efficient in training a ML model
 - Using Tensorflow and Keras to create a CNN which classifies images
 - Using threads
 - Making AJAX calls to a server which allows Javascript to interact with Python
 - Storing and finding information in a MongoDB database

## Challenges I Ran Into
Before this hackathon, I had no idea that a project like this could even be created. It took countless hours of watching YouTube tutorials, and trial and error to get everything working. Some key problems I overcame: Google Classroom API integration (this is key to the project, as Google Classroom became the central vessel for teachers to communicate with students during COVID-19), transferring data from Google Classroom API to my flask server, learning about Machine Learning Image Classification and fine-tuning of models, using OpenCV to take the image and convert it to grayscale, and finally the UI design and execution of the website. I'm extremely happy I was able to complete it and I have learned many new things from this project.

## Built With

* [Flask](https://flask.palletsprojects.com/en/1.1.x/) - Web Framework
* [Google Classroom API For Browser(JS)](https://developers.google.com/classroom) - API
* [TensorFlow](https://www.tensorflow.org/) - Machine Learning
* [Numpy](https://numpy.org/) - Machine Learning
* [OpenCV](https://opencv.org/) - Machine Learning
* [MongoDB](https://www.mongodb.com/) - Database
* Check the requirements.txt file for other libraries

## Inspiration
Due to COVID-19, my school was moved online. All my teachers had to change their plans, and all my friends and I agreed that online learning wasn't effective. We all agreed that we missed out on knowledge that we would probably need in the future. I did some more research and I found a [survey](http://ir.mit.edu/remote-experience) by MIT which found that 64% of students felt that distractions at home made it difficult to learn, and 79% of students couldn't focus as well as in person. Then, when this hackathon started, I came back to this topic and decided to try and solve this problem. 

## What's Next For Attentive
I'm confident that this product can improve online learning and help ensure that students aren't left behind in a post COVID world. I'm going to try and run a pilot program in my high school, and I'm going to use that information to make some improvements and also generate guidelines on how a teacher can interpret data. Currently, I define attention span as the length of time that a student is classified as facing the computer screen. I want to improve my metric for attention by tracking other movements such as eye position. Another direction I'm planning to head is modifying the structure of Attentive to provide teachers with live results. This allows them to make effective revisions live and re-engage students in the lesson.

## Author

* **Aryan Jain** - [Github](https://github.com/Not-Aryan)

## License

This project is licensed under the MIT License

Thank you for reading and I hope you have a wonderful day! :)
