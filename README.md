# Taktile ML Engineerig Take-Home Challenge

## Introduction

Welcome to the Taktile ML Engineer (MLE) Take-Home Challenge. In this challenge, you'll build a mini KYC (Know Your Customer) app that allows users to submit their name, address, and bank statement to prove their identity. Through this exercise, we aim to evaluate your ability to design and implement reliable, end-to-end solutions.

This challenge is designed to assess your technical and communication skills. We understand this requires balancing multiple tasks within a limited timeframe. Focus on producing a solution that showcases your strengths and prioritizes quality over quantity.

## Assignment

You will develop a mini KYC app with the following features:
- A REST API to classify uploaded documents as a bank statement, extract the person's name, address, and document date, and compare the extracted name and address with the user-provided name and address to verify their identity.
- A lightweight front end where users can upload documents and see the results of the API call

### Task 1: API Development
Your first task is to develop a simple REST API with an endpoint that accepts a single-file (jpeg or png) input, as well as the user's name and address. 
The endpont should respond with a JSON object containing the name, address, and document date extracted from the uploaded document, as well as a boolean indicating whether the extracted name and address match the user-provided name and address.
We've put some sample documents in the `data/documents` folder. You can use these samples to develop and test your API.

Other than that, you are free to implement the API in any way you want. Specifically,
- You can use any python REST API framework (django, fastapi, flask, etc.).
- You can use any machine learning model or LLM to extract the name, address, and document date from the uploaded document.
- You can use any method to compare the extracted name and address with the user-provided name and address to verify their identity.
- You can install any external libraries you need.

### Task 2: Frontend Development
Your second task is to develop a (very) lightweight front end where users can upload an image and see the results of the API call. You can use both python or typescript for your solution, you are free to use any framework or library you want.

### Task 3: Dockerization
Your final task is to package both services (API and frontend) as Docker images and write a docker compose file to run the end-to-end application locally.

### Task 4 (Bonus task): Address verification
As an optional extension of your application, you can add an address verification step to your frontend, after the API call. You can use any 3rd party API to verify the address (e.g. https://www.geoapify.com/), but it should be a simple step that can be done with an external API.

## Objectives

We give roughly equal weight to each of the following:

- Code quality
- Readability
- Code structure & modularity
- Documentation
- Creative thinking
- Business understanding
