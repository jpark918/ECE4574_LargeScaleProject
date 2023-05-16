Specification: 
For the semester-long course project, I want you to develop a software system for an
engineering application or use. As an Engineering application, your project should involve
some form of control, data analysis, computation, performance requirements (throughput
or accuracy, for example) or other engineering aspect. You are working in teams of three or
four; the teams will be assigned in Canvas as Groups.
For this project, you MUST use the scrum methodology as I have explained it. Of course,
there are variants of scrum in use, but it’s required that you use the following approaches:
a) Product backlog and sprint backlogs
b) Three 3-week sprints
c) Scrum meetings (for this course, I am OK if you only have three actual meetings per
week, to ask the three questions, but exchange status by email on other days of the
working week).
d) Sprint wrap-ups and retrospectives
e) Most importantly, incremental deliverables at the end of each sprint
Here are the important due dates, and some information on what I am looking for:
 Project Proposal – Group assignment
 25 points; the Scrum Master submits on behalf of the team
 A single Word document containing the following information:
• Team name, names of members and title of project
• Name of the designated Scrum master
♦ Which team member will run the meetings and make sure everything is
recorded?
• One-half to one page description of the desired result (the completed
project), its use and why you want to do it
• Project backlog: the list of requirements for the entire system
♦ Include both functional (what the code will do) and non-functional
requirements (for example, what language(s), what platforms or APIs,
what data, etc.)
♦ Use good form for your requirements (“As an Administrator, I want to be
able to change user’s account details so that users whose role changes
won’t have improper access”)
♦ Remember to include priority
• Your sprint backlog for sprint 1
♦ What requirements will you tackle in the first sprint, who will do them in
what order
• What tools and/or communication methods will you use to track your work
♦ git for code control? Slack, a Wiki or something else for communication?
Email?

 Due Monday, September 5 at 11:59 PM
 Sprint 1 wrap-up report – Group assignment
 20 points; the Scrum Master submits a single document for the team, containing:
• Sprint wrap-up: address each item on the sprint backlog: did you get it done?
How did it go? Any changes to the product backlog? This is best done by
adding a “disposition” column to the sprint backlog.

• Sprint retrospective: any changes needed to how you are doing things?
• Your sprint backlog for sprint 2
 Due October 3 at 11:59 PM
 Sprint 2 wrap-up report – Group assignment
• 20 points; the Scrum Master submits a single document for the team,
containing:
• Sprint wrap-up: address each item on the sprint backlog: did you get it done?
How did it go? Any changes to the product backlog?
• Sprint retrospective: any changes needed to how you are doing things?
• Your sprint backlog for sprint 3
 Due October 24 at 11:59 PM
 Sprint 3 wrap-up report – Group assignment
• 20 points; the Scrum Master submits a single document for the team,
containing:
• Sprint wrap-up: address each item on the sprint backlog: did you get it done?
How did it go? Any changes to the product backlog?
• Sprint retrospective: any changes needed to how you are doing things?
 Due November 14 at 11:59 PM
 Brief project presentation
 25 points; all team members participate equally
 Walk through and ideally demonstrate your project
 I would like 3-6 slides to use as a framework for your presentation
 These will be submitted via Canvas by December 1; all team members submit the
same
 Occurs on November 30 or December 5 during class
 Project final report
 50 points; each team member submits their own report
 The final report should contain:
• A one-page executive summary of your final deliverable
♦ What does it do? How is it used? What are the benefits from its use?
• Summarize the project:
♦ How did the final deliverable work out? Many differences from what you
planned?
♦ Your reflection on the process of doing the project: methodology,
teamwork, anything
• A copy of all code written in your project, pasted in plain-text as an appendix
• An attached zip file of all of your code (source and project files only, no
compiled code or libraries). Of course, all team members submit the same
code.
 Due December 7 at 11:59 PM

IMPORTANT NOTES:
Each team member is expected to contribute to the development. Be SURE and
insert comments in the code to record who wrote which class, function or file. All
source and header files MUST contain a good file header. Here is one example,
but other formats are acceptable:
/* main.cpp Creed Jones Virginia Tech August 22, 2020
* This is the main app for the HW1 distribution display project
* Qt creator, using UI form design
* Modified August 29, 2020 to add bounds checking
*/
All submissions are to be a SINGLE WORD OR PDF FILE, with the exception of
the final report which will be accompanied by a zip file of all of your code
(source and project files only, no compiled code or libraries).
What is the right size or scope of a project? The task should be about the effort of
three homework assignments for each of the team members. So, roughly,
something about ten times as involved as one of the homework assignments.
Note that each team member submits something for each deliverable. In most
cases they are the same, but don’t fail to submit your work.
You are encouraged to rename your team if you wish.


Overview:
We are creating an expense tracker where users can keep track of how they are spending their monthly income. The main goal is to have set goals for spending monthly that we can monitor. We will keep track of spending on a month to month basis which will help adjust monthly spending goals. We wanted to do this as a group because as young adults, keeping track of where our money is going is essential. We want to have fun but at the same time make sure we have enough for important expenses. People may use excel to do all these expense tracking, but our software will generate the graphs as data is given and help users adjust their expense plans. 
WireShark has been used in order to keep track of the users' URL visits. Initially, the project was to be built on the C++ language and libraries through qt creator since we wanted the end product to have an interactive GUI, however, we switched over to Python, after having many difficulties with C++, as we saw that python had many helpful libraries that made connections to the database much easier to manage. The downside was that the QT Widget implementation became a lot more difficult without the drag/drop UI. The UI was still kept from C++ and was imported into our python code. The AWS databse was used in order to have a relational database, as the tables are all joined by customer ID and this would make querying more simple.
