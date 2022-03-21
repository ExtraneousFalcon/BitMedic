# BitMedic
![Capture](https://user-images.githubusercontent.com/91358365/159170299-4b51c5c6-3c3e-4ab1-9166-9e82f349b59f.PNG)

## Our Goal: 
Build an intuitive all-in-one healthcare ecosystem to enhance doctor-patient communication

## What we offer:
- Patients are able to add and remove doctors, giving them the ability to provide prescriptions and access medical records
- Patients can add to their medical history by uploading in their files
- Once there is an available prescription, patients are able to send payment through Ethereum for their prescriptions created by the doctor. Once the payment has been sent, the order will then be unavailable to buy again.
- Doctors are able to view patient profiles and access their medical history. They can also upload new files to the patient's database.
- Doctors can create patient descriptions through the use of digital signature over the Ethereum blockchain. They must input their private key as a method of "signing' the transaction which will later deliver to the patient.

## What we used: 
We made BitMedic possible through Django which runs on a python framework. In order to build the frontend, we styled with JavaScript, HTML, and CSS. We incorporated Web3 libraries in order to take advantage of the Ethereum Blockchain. The website is hosted on Google Cloud.

## Visit the website!
https://www.bitmedic.tech/

## How to use
- Clone this repo onto your local machine.
- Open the folder sample that contains the manage.py file.
- Then, do python manage.py makemigrations or python3 manage.py runserver
- python manage.py migrate
- python manage.py runserver
- Open localhost:8000 on your web browser!
