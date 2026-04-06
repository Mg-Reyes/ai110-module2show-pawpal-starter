# PawPal+ Project Reflection

## 1. System Design

A User shuould be able to add a pet, create and update tasks (complete or incomplete), and see pending tasks.

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

My initial UML design has 3 classes, Owner, Task, and Pet. An owner has the ability to add a pet, create and update tasts.
The Owner class can have a list of Pet objects and a list of Tasks assigned to each pet. The Pet class has all the information for a single Pet. The Task object will hold a petId and assing a specific task to the pet with this ID.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
I added a duplicate checker to the add_pet function in the Owner class because it was possible to contienually add the same pet over and over again. As well as the 4th class, Scheduler.
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

The scheduler considers due date when it sorts the tasks. I chose the due_date because when a user wants to see their tasks they would want to see them sorted from closes due date to the latests.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

The Scheduler sorts the tasks by their due date instead of priority or preference. I think this is a good tradeoff because the due date is the most important information when it comes to scheduling tasks.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
