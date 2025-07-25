# MoM (Minutes of Meetings)

## Meeting 1: 16th Jan 2024, Tuesday

Attendants: Archisha Panda, Ankith Pai, Gargi Shroff, Prakhar Jain, Rudransh and Client (Arjun Rajasekar)

### Key Points

1. Project is for an NGO. It is aimed to assist school teachers develop assessments to ensure holistic learning instead of raw textbook knowledge. Focus has to be on contextualizing tests to incorporate real-life applications, morals and ethics.
2. The front-end will have 3 pages- Form, Output display and Historic context.
3. Backend will have API calls to existing LLM models.
4. Based on inputs in the form given by the user, we must design a prompt (pre-designed prompt architecture) for the LLM.
5. The assessments generated must be stored for future reference.

### Tasks Assigned

1. Share github ids
2. Plan weekly meetings
3. Share course deadlines and exam schedules
4. Go through MERN stack and API documentations

## Meeting 2: 24th Jan 2024, Wednesday

Attendants: Archisha Panda, Ankith Pai, Gargi Shroff, Prakhar Jain, and Client (Arjun Rajasekar)

### Key Points

1. Elaborate description about each web page for the project
   - First page - Input Form, it is to be filled by the user. The fields will be number of questions required, kind of assessment (short answer questions or mcq’s), option to upload one or more files as context material.
   - Second Page - Rendered Output from the LLM’s, in editable format for the user.
   - A history of all the previous assessments generated with the date and time displayed for the users to directly use the assessments generated in the past.
2. Discussing about the Sample Input and Output for the project.
3. Clarification on how morals need to be incorporated into the assessment generated - will be provided in context
4. Schedule for the next two weeks
5. Expected a basic working UI design before mid March for R&D Showcase.
6. Clarification about the flow of the project and the documentations required.

### Tasks Assigned

1. Complete Project Synopsis
2. Distribute work among team members
3. Sample input and output (to be shared by client)
4. 2-week deadlines (to be shared by client)
5. Planning of project for next 2 weeks (depending on deadlines shared by client)

## Meeting 3: 7th Feb 2024, Wednesday

Attendants: Archisha Panda, Ankith Pai, Gargi Shroff, Prakhar Jain, and Client (Arjun Rajasekar)

### Key Points

1. Look into the ANT design (which is a React UI library). Has all the UI components needed for our purposes.

### Tasks Assigned

1. Start work on design and implementation
2. Split into a frontend team (Archisha Panda and Gargi Shroff) and a backend team (Ankith Pai and Prakhar Jain)

## Meeting 4: 16th Feb 2024, Friday

Attendants: Ankith Pai, Gargi Shroff, Prakhar Jain, and client (Arjun Rajasekar)

### Key Points

1. Discussed details of R1 and R2 (what feature goes in which version)
2. Discussed updates and changes to our current SRS document.
3. Client will provide an available PDF renderer for us to use.
4. The LLaMA LLM will be used, we will be integrating an LLM instance that the client will provide.
5. Discussed testing plans for the project
   - Usability testing (ease of use with intuitive UI/UX). Client recommends taking help from others who can give real user-side feedback, and documenting their testing in a report.
   - Bug testing of code (testing edge cases and checks for a range of form inputs).
   - Any warnings to be fixed and not ignored.

### Tasks Assigned

1. The SRS document is to be submitted to the client to review by 17th Feb afternoon.

## Meeting 5: 21th Feb 2024, Wednesday

Attendants: Ankith Pai, Gargi Shroff, Archisha Panda, and client (Arjun Rajasekar)

### Key Points

1. Discussed character limits on text boxes (125 characters).
2. Discussed question limits (20 questions).
3. We will get access to the LLM by the weekend.
4. Next meet is on Saturday, 2nd March 2024.

### Tasks Assigned

1. Suggests adding descriptions in the web page to explain the textboxes and project flow.
2. Show the prompt that is being generated on the frontend (with visual indicators on the parameters being filled).
3. Give a list of updates done before the R1 release.

## Meeting 6: 6th March 2024, Wednesday

Attendants: Ankith Pai, Gargi Shroff, Archisha Panda, Prakhar Jain and client (Arjun Rajasekar)

### Key Points

1. Discussed about the delays regarding the LLM Llama.
2. The client suggested use of alternative LLM (Hugging Face) to make API calls.
3. Discussion about the Release 1 schedule.

### Tasks Assigned

1. Completion of tasks for R1 by next wednesday, so that they can be reviewed.

## Meeting 7: 13th March 2024, Wednesday

Attendants: Ankith Pai, Gargi Shroff, Archisha Panda, Prakhar Jain and client (Arjun Rajasekar)

### Key Points

1. Client suggested to use LMStudio – used for locally running LLMs
2. For now, LLM is expected to give output considering context from 1 pdf file (2-3 pages only) but application should support uploading of multiple pdf files

### Tasks Assigned

1. Remove the word ‘description’. Shift the one line descriptions to top of the blank space.
2. Implement a print button
3. Instead of PROMPT change it to summary of user input

## Meeting 8: 27th March 2024, Wednesday

Attendants: Gargi Shroff, Archisha Panda and client (Arjun Rajasekar)

### Key Points

1. Discussed about feedback for R1
2. Re-emphasized on using LM Studio till Llama is available
3. Planned about further project goals

### Tasks Assigned

1. Prepare the prototype for the History page before next meeting on Friday (05/04/2024)
2. Start working on the Edit option of Assessment Display Page
3. Experiment with various prompt designs using LM Studio

## Meeting 9: 10th April 2024, Wednesday

Attendants: Ankith Pai, Archisha Panda, Prakhar Jain and client (Arjun Rajasekar)

### Key Points

1. Every edit on page 2 is not to be immediately saved, changes to be saved after save button is clicked.

### Tasks Assigned

1. Implement an export to doc or text (for ease of editability).
2. Fix page break issue in generated PDF.

## Meeting 10: 17th April 2024, Wednesday

Attendants: Ankith Pai, Archisha Panda, Gargi Shroff and client (Arjun Rajasekar)

### Key Points

1. Discussed about LM Studio. Our team mentioned that it is very resource intensive and runs slower than the current LM model used in the application. Therefore, it was decided to continue with the current HuggingFace LM.
2. Got feedback from the client regarding UI. He recommended pagination in the History page.
3. The current implementation saves a generated assessment by default. Further as the user makes changes and clicks on "Save Assessment" button, a new copy of the assessment is saved every time. However, this has a risk of flooding our database. Hence the client recommended to save only when user makes all the changes required.
4. The client asked for code documentation including deployment instructions, block diagrams and screen shots of the UI.

### Tasks Assigned

1. Implement pagination for HistoryPage.
2. Fix a bug in Export To PDF functionality for multi-page PDFs.
3. Change the behaviour of "Save Assessment" button in Page2.
