# CVXpert report: cv.txt

## Review

**Overall Score: 38/100** (the model's estimate, not a measurement)

Alex Morgan's CV has the essentials — name and contact details at the top, reverse-chronological experience entries with employers and dates, and a skill list that partly matches the target Python backend role — but it reads as a list of duties rather than achievements. Nearly every bullet states a responsibility with no outcome and no numbers; the profile and several bullets use first-person pronouns and unsupported self-praise; the tense does not match a role dated "Present"; and Python, SQL, Docker, AWS, leadership and problem solving are claimed but shown nowhere in the CV. Formatting is inconsistent (two date styles), "CMS" is never expanded, an unrelated Shop Assistant role and school A-Levels take up space, roughly a year between Northpoint Digital and Brightfield Logistics is unaccounted for, and the content is not tailored or ordered around the Python/backend posting. The CV needs a rewrite of every experience bullet and a re-prioritisation around the booking-tool, API and database work already present.

### Sections

- Header
- PROFILE
- EXPERIENCE
- EDUCATION
- SKILLS

### Findings

#### F1 [high]: G01 Describe achievements and results, not duties

- Section: EXPERIENCE
- Text: Responsible for the company website and the internal booking tool. / Worked on various tasks related to the API. / Helped with projects for the warehouse team.
- Problem: These bullets state duties only; none say what the candidate accomplished, changed or contributed, so the reader learns nothing about results.
- Proposed change: Rewrite each as an accomplishment and append a [result] placeholder where the CV gives no outcome, e.g. "Maintained the company website and internal booking tool, achieving [result]"; the candidate must supply the missing outcomes.

#### F3 [high]: G03 Be specific about what was done and how

- Section: EXPERIENCE
- Text: Worked on various tasks related to the API. / Helped with projects for the warehouse team.
- Problem: "Various tasks", "related to the API" and "projects" name no concrete action, method or tool, so the reader cannot tell what was actually done or how.
- Proposed change: Replace with the specific work performed, inserting placeholders where details are missing, e.g. "Developed [feature/endpoint] for the booking API using [language/tool]" and "Delivered [project] for the warehouse team".

#### F4 [high]: G04 Evidence skills; don't just list them

- Section: SKILLS
- Text: Python, JavaScript, SQL, Docker, leadership, problem solving, AWS
- Problem: These skills appear in no experience, project or education entry; Python, Docker, AWS, SQL, leadership and problem solving are listed but never shown in use.
- Proposed change: Add evidence for each claimed skill inside the relevant experience entry (e.g. Python/Docker/AWS use at Brightfield, the database work at Northpoint) or remove the unsupported skills; do not add new skills.

#### F9 [high]: G08 Start each bullet with a strong action verb

- Section: EXPERIENCE
- Text: Worked on various tasks related to the API. / Helped with projects for the warehouse team. / I build landing pages for clients using HTML and CSS.
- Problem: Bullets open with weak verbs ("Worked", "Helped") or a pronoun ("I") rather than a strong action verb naming the candidate's contribution.
- Proposed change: Begin each bullet with a strong action verb drawn from the actual work, e.g. "Built landing pages for clients using HTML and CSS" and "Developed [feature] for the booking API".

#### F10 [high]: G09 Remove duty phrases

- Section: EXPERIENCE
- Text: Responsible for the company website and the internal booking tool. / Duties included maintaining the database.
- Problem: Filler duty openers ("Responsible for", "Duties included") delay the action instead of starting with it.
- Proposed change: Delete the openers and start with the action, e.g. "Maintained the company website and internal booking tool, [result]" and "Maintained the [database], [result]".

#### F11 [high]: G10 Use no personal pronouns

- Section: PROFILE
- Text: I am a highly skilled and passionate software developer with excellent communication skills. I am a team player who is responsible for delivering outstanding results in a fast-paced environment.
- Problem: The profile uses first-person pronouns ("I am"), and the experience bullet "I build landing pages for clients using HTML and CSS" does the same; the CV should be written in implied first person.
- Proposed change: Recast without pronouns: delete the "I am" constructions in the profile and restate the bullet as e.g. "Built landing pages for clients using HTML and CSS".

#### F12 [high]: G11 Match verb tense to whether the role is current

- Section: EXPERIENCE
- Text: March 2021 - Present — Worked on various tasks related to the API. / Helped with projects for the warehouse team. / Reports were prepared for management every month. / Fixed bugs and attended daily stand-ups with the team.
- Problem: Past-tense bullets sit under a role dated "March 2021 - Present", so the tense does not match a current role; conversely "I build landing pages" is present tense under the ended role "06/2018 - 02/2020".
- Proposed change: Use present tense throughout the current Brightfield entry and past tense throughout the finished Northpoint entry, keeping tense consistent within each entry.

#### F14 [high]: G13 Remove self-praise; let the facts show quality

- Section: PROFILE
- Text: I am a highly skilled and passionate software developer with excellent communication skills. I am a team player who is responsible for delivering outstanding results in a fast-paced environment.
- Problem: Unsupported self-assessments ("highly skilled", "passionate", "excellent", "outstanding", "team player") assert quality the CV never demonstrates.
- Proposed change: Delete the self-praise and let the experience entries carry the evidence; if a profile is kept, state only what the CV supports (the roles and skills already listed).

#### F2 [medium]: G02 Quantify only with numbers the candidate supplied

- Section: EXPERIENCE
- Text: Involved in the migration to the new CMS, which was a big project and took a long time and many people were involved in it.
- Problem: Scale is described only in vague words ("big project", "a long time", "many people") with no figure, so the size and impact cannot be judged.
- Proposed change: Add the figures the candidate can supply, using placeholders: "Contributed to a [duration] CMS migration involving [team size] people, delivering [result]".

#### F5 [medium]: G05 Tailor by selecting and ordering, never by adding

- Section: EXPERIENCE
- Text: Software Developer, Brightfield Logistics (fictional) — Worked on various tasks related to the API. / Helped with projects for the warehouse team. / Responsible for the company website and the internal booking tool.
- Problem: The role most relevant to the target Python backend job (a logistics company, with a booking tool, an API and a database) is described with the same shallow duty bullets as everything else, so its relevance is never surfaced.
- Proposed change: Select and feature the existing backend-relevant content: lead with and expand the booking-tool, API and database bullets for this role and trim the unrelated warehouse/website bullets, using only wording already in the CV.

#### F6 [medium]: G06 Mirror job-posting terms only where the CV truthfully supports them

- Section: EXPERIENCE
- Text: Worked on various tasks related to the API. / Duties included maintaining the database.
- Problem: The posting's terms for the same work are missing although the CV describes it in other words: "the API" (posting: "REST APIs") and "the database" (posting: "relational databases").
- Proposed change: Mirror the posting's wording where the CV truthfully supports it ("REST APIs", "relational database"); do not insert terms the CV does not evidence (PostgreSQL, CI/CD, Kubernetes) — the candidate should add them only if accurate.

#### F7 [medium]: G07 Cut irrelevant, repetitive or out-of-date content

- Section: EXPERIENCE
- Text: Shop Assistant, Corner Books (fictional) 2014 - 2016 / Served customers and handled the till.
- Problem: An old, unrelated role that takes up space without supporting a backend developer application.
- Proposed change: Remove the entry (or reduce it to a single line); do not replace it with new content.

#### F13 [medium]: G12 Prefer active voice

- Section: EXPERIENCE
- Text: Reports were prepared for management every month.
- Problem: A passive construction ("were prepared") in which the candidate is not the subject, leaving their role unclear.
- Proposed change: Rewrite in the active voice, e.g. "Prepared monthly reports for management, [result]".

#### F15 [medium]: G14 Write concise phrases, not narrative

- Section: PROFILE
- Text: I am a highly skilled and passionate software developer with excellent communication skills. I am a team player who is responsible for delivering outstanding results in a fast-paced environment.
- Problem: Written as full-sentence narrative prose rather than the short, scannable phrase a recruiter skims.
- Proposed change: Cut it to a short phrase or remove it; do not replace it with new claims.

#### F18 [medium]: G18 Order sections by relevance to the reader

- Section: SKILLS
- Text: Python, JavaScript, SQL, Docker, leadership, problem solving, AWS
- Problem: The section that holds the posting's key requirements (Python, SQL, Docker, AWS) is placed last, after Education and the unrelated Shop Assistant role, so the most relevant material is not seen first.
- Proposed change: Move the SKILLS section (or the role-relevant skills within it) higher, above less relevant material, using existing content only.

#### F19 [medium]: G20 Format dates, styles and grammar consistently

- Section: EXPERIENCE
- Text: March 2021 - Present / 06/2018 - 02/2020 / 2014 - 2016 (and EDUCATION: 2015 - 2018)
- Problem: Two different date formats (month-name and numeric) are mixed across the CV.
- Proposed change: Use one consistent format for every entry, e.g. "Month YYYY - Month YYYY" (or "MM/YYYY") throughout.

#### F21 [medium]: G23 Flag unexplained gaps; do not explain them

- Section: EXPERIENCE
- Text: 06/2018 - 02/2020 (Northpoint Digital) and March 2021 - Present (Brightfield Logistics)
- Problem: Roughly 13 months between the end of the Northpoint role (02/2020) and the start of the Brightfield role (03/2021) are unaccounted for.
- Proposed change: Add a [gap: reason] placeholder for the period (advisory only — gaps are normal and need no apology), and supply the reason only if it is accurate.

#### F8 [low]: G07 Cut irrelevant, repetitive or out-of-date content

- Section: EDUCATION
- Text: A-Levels: Maths, Physics, English
- Problem: School-leaving qualifications listed next to a degree are superseded and add nothing for this reader.
- Proposed change: Delete the A-Levels line.

#### F16 [low]: G15 Avoid slang, jargon and repetition

- Section: EXPERIENCE
- Text: Involved in the migration to the new CMS, which was a big project and took a long time and many people were involved in it.
- Problem: Colloquial and repetitive wording ("involved ... many people were involved", "a long time") instead of plain professional phrasing.
- Proposed change: Trim and vary the wording, e.g. "Contributed to the CMS migration ([team size] people, [duration])".

#### F17 [low]: G17 Give every entry an organisation, a title and dates, newest first

- Section: EDUCATION
- Text: A-Levels: Maths, Physics, English
- Problem: The entry gives no institution and no dates, so it lacks the organisation, qualification detail and dates that every entry should carry.
- Proposed change: If the entry is retained, add [institution] and [dates]; otherwise remove it (see F8).

#### F20 [low]: G22 Spell out acronyms on first use

- Section: EXPERIENCE
- Text: Involved in the migration to the new CMS
- Problem: The acronym "CMS" is used without ever being expanded, so a reader outside the domain cannot tell what it means.
- Proposed change: Write the expanded form on first use, e.g. "content management system (CMS)".

#### F22 [low] (uncertain): G24 Keep every claim honest and verifiable

- Section: SKILLS
- Text: leadership (in "Python, JavaScript, SQL, Docker, leadership, problem solving, AWS")
- Problem: "leadership" is claimed although no entry shows a team or leadership responsibility (Software Developer, Junior Developer, Shop Assistant), so the claim is not supported by the CV's own content.
- Proposed change: Remove "leadership" unless evidence exists, or add the existing evidence (e.g. if the candidate led [task/team]) without inflating the level; do not invent scope.

### Guidelines cited

- G01 Describe achievements and results, not duties. Sources: MIT-W (accomplishments and contributions, not just responsibilities; descriptions should not read like job descriptions); MIT-PDF "Emphasize your accomplishments, contributions, and outcomes."; HAR (lists "Not demonstrating results" among the top five mistakes); USF (use action verbs instead of task descriptions; incorporate results); IMP (STAR, ending in Result).
- G02 Quantify only with numbers the candidate supplied. Sources: MIT-PDF "Quantify bullet points to convey size and/or scale of project, budget, team, time or results."; MIT-W (quantify if you can; attendees, money raised or managed); HAR (fact-based: quantify and qualify); EUP "If necessary, quantify your responsibilities".
- G03 Be specific about what was done and how. Sources: MIT-W (include how you performed tasks, not just what you did); HAR (specific rather than general).
- G04 Evidence skills; don't just list them. Sources: USF (showcase skills and competencies, not merely list them); MIT-PDF "Give evidence of your skills and personal impact"; IMP (make skills evident with a summary followed by STAR examples).
- G05 Tailor by selecting and ordering, never by adding. Sources: MIT-W (target a specific position; select experiences that show the required skills); NCS (match the CV to the job and company; review the advert); HAR (tailor to the type of position); EUP "highlight your advantages according to the specific requirements of the prospective employer."
- G06 Mirror job-posting terms only where the CV truthfully supports them. Sources: MIT-ATS (use posting keywords meaningfully; avoid spamming; you must be able to account for everything on the resume); MIT-W (employers may use keyword scanning); ILL (borrow wording from the job posting).
- G07 Cut irrelevant, repetitive or out-of-date content. Sources: MIT-PDF "Omit unrelated memberships and information that is repetitive, implicit (e.g. high school graduation for a college graduate), or out-of-date."; EUP "work experience or training which is old or not relevant for the application can be omitted."; NCS (remove outdated information).
- G08 Start each bullet with a strong action verb. Sources: MIT-W (start with a strong action verb such as built, managed, developed); DUKE (begin with a strong, active verb); MIT-PDF "Use action verbs"; HAR (use action words, not passive language).
- G09 Remove duty phrases. Sources: MIT-PDF "Leave out unnecessary words, sentences, and phrases e.g. "Duties included / Hired to / Project involved / Responsible for..."; DUKE (avoid "responsible for" and "duties include").
- G10 Use no personal pronouns. Sources: MIT-PDF "Don't use the first person, I, or any pronouns."; HAR (do not use personal pronouns such as I or We); DUKE; ILL.
- G11 Match verb tense to whether the role is current. Sources: DUKE (present tense for current activities, past tense for past ones); ILL (keep verb tenses consistent; present tense for current roles); USF (present tense for current positions, past tense for previous ones).
- G12 Prefer active voice. Sources: HAR (active rather than passive; lists passive language among the top five mistakes); MIT CAPD, https://capd.mit.edu/resources/resume-tips-avoid-the-passive-voice/ (eliminating passive voice helps; the full guide it links to is off-site and was not read).
- G13 Remove self-praise; let the facts show quality. Sources: MIT-PDF "Avoid self-flattering terms such as "highly skilled, outstanding, or excellent." … let readers decide for themselves that you are well-qualified."; HAR (written to express, not impress; articulate rather than "flowery").
- G14 Write concise phrases, not narrative. Sources: HAR (no narrative style; written for people who scan quickly); MIT-W (resumes don't require complete sentences); EUP "use short sentences"; NCS (usually 2 to 3 lines per role).
- G15 Avoid slang, jargon and repetition. Sources: MIT-PDF "Avoid repeating words or phrases, as well as using jargon"; HAR (no slang or colloquialisms); ILL (use a variety of action verbs).
- G17 Give every entry an organisation, a title and dates, newest first. Sources: NCS (list the most recent experience first; include employer, job title, dates and what you did); HAR (reverse chronological within headings).
- G18 Order sections by relevance to the reader. Sources: HAR (list headings in order of importance); EUP (describe education and training first when work experience is limited); MIT-ATS (position sections to reflect the posting's priorities).
- G20 Format dates, styles and grammar consistently. Sources: HAR (be consistent in format and content); MIT-PDF "Be consistent and use the same grammatical style throughout."; DUKE (consistent styling and formatting across all sections); NCS (use the same style throughout).
- G22 Spell out acronyms on first use. Sources: ILL (spell out acronyms the first time, followed by the acronym in parentheses); HAR (do not abbreviate). The two sources differ in strictness; G22 follows ILL because a reviewer can check it in text.
- G23 Flag unexplained gaps; do not explain them. Sources: HAR (avoid information gaps such as a missing summer); EUP "explain any breaks in your studies or career"; NCS (says gaps are normal and links to advice on explaining them, so a gap finding is advisory, never a defect).
- G24 Keep every claim honest and verifiable. Sources: MIT-PDF "Be honest and accurate, but not overly modest."; EUP "do not artificially inflate your CV; if you do, you are likely to be found out at the interview."; MIT-ATS (be able to account for everything; falsification may lead to dismissal from the search); DUKE (evaluate language skills honestly).

## Tailoring

**Job Match Score: 48/100** (the model's estimate, not a measurement)

Alex Morgan is a software developer with roughly 4 years of professional experience and, importantly, current work at a logistics company (Brightfield Logistics), which lines up with the freight domain in the Job Description. The CV lists a relevant core stack (Python, SQL, Docker, AWS) and shows API and database exposure, so the technical keywords are largely present. However, the experience section is written in vague, passive terms and does not evidence the depth the role asks for: Python is listed only as a skill rather than shown in the roles, the API work is described as "various tasks" rather than designing/building REST APIs, database work is limited to "maintaining the database," and there is no indication of CI/CD, automated testing, code review, PostgreSQL or Kubernetes. Net: a plausible adjacent fit whose CV needs sharper framing and clearer evidence of the specific backend practices named in the ad.

### Matches

- Current role at Brightfield Logistics puts Alex in the logistics/freight domain listed as a nice-to-have
- Python listed in Skills
- SQL listed in Skills, plus 'maintaining the database' at Northpoint Digital — relevant to the relational database requirement
- Docker listed in Skills, matching the containerisation requirement
- AWS listed in Skills, matching the 'major cloud provider (AWS preferred)' requirement
- API exposure at Brightfield ('Worked on various tasks related to the API') — at least some backend/API work
- Collaboration with the warehouse team maps loosely to 'work with operations staff to turn their requests into features'
- BSc Computer Science plus Maths/Physics A-Levels — relevant technical foundation
- Profile claims 'excellent communication skills', which speaks to the clear written communication requirement

### Gaps

Asked for in the Job Description but not shown in the CV. Add one only if you have that experience.

- No demonstrated 3+ years of professional Python experience — Python appears only as a listed skill, not evidenced in any role
- No PostgreSQL experience shown (SQL is listed, but the preferred database is not named)
- No CI/CD pipeline experience shown
- No automated testing or code review experience shown ('Fixed bugs' is the closest item)
- No evidence of designing or building REST APIs — the API bullet is described only as 'various tasks'
- No Kubernetes (nice-to-have)
- No concrete evidence of clear written communication (e.g. documentation, specs) beyond a self-description
- Relational database experience is thin — only 'maintaining the database' at one role
- Performance and reliability improvement work is not evidenced

### What to emphasise

- Move the Skills block up so Python, SQL, Docker and AWS are seen early against the ad's core requirements
- Lead the Brightfield Logistics entry with the API and booking-tool work, since the JD is built around a booking platform
- Re-describe the API bullet using the JD's wording (
- REST APIs for our booking and tracking platform') wherever it truthfully applies to the work at Brightfield
- Give more space to the current Software Developer role and condense the older Shop Assistant role, which is not relevant to this position
- Reframe the warehouse-team bullet in the JD's language of working with operations staff to turn requests into features
- Expand the database work at Northpoint Digital to make the relational-database experience clearer
- Foreground Brightfield Logistics as a logistics employer, since freight/logistics is explicitly a nice-to-have
- Keep the BSc Computer Science prominent as the technical foundation supporting the backend requirements

## Rewrite

### Placeholders to fill in

- [language/tool]
- [feature/result]
- [result]
- [project]
- [team size]
- [duration]
- [gap: reason]

### Rewritten CV

# ALEX MORGAN
alex.morgan@example.com | +44 20 7946 0000 | Leeds, UK

## PROFILE
Software developer at Brightfield Logistics, with a BSc in Computer Science and a background across REST API, booking-tool, website and database work.

## SKILLS
Python, JavaScript, SQL, Docker, AWS

## EXPERIENCE

### Software Developer, Brightfield Logistics (fictional)
March 2021 - Present
- Develop REST APIs for the internal booking tool using [language/tool], delivering [feature/result]
- Maintain the company website and internal booking tool, achieving [result]
- Prepare monthly reports for management, [result]
- Deliver [project] for the warehouse team, [result]
- Fix bugs and attend daily stand-ups with the team.

### Junior Developer, Northpoint Digital (fictional)
June 2018 - February 2020
- Maintained the relational database, [result]
- Built landing pages for clients using HTML and CSS, [result]
- Contributed to the content management system (CMS) migration ([team size] people, [duration]), delivering [result]

[gap: reason] — February 2020 to March 2021

### Shop Assistant, Corner Books (fictional)
2014 - 2016
- Served customers and handled the till.

## EDUCATION
BSc Computer Science, University of Westmoor (fictional), 2015 - 2018

