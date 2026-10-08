# CVXpert report: cv.txt

## Review

**Overall Score: 40/100** (the model's estimate, not a measurement)

The CV is structured sensibly (contact details at the top, reverse-chronological experience, education and a skills list) but the writing is weak throughout. The profile is written in the first person and is pure self-praise; most bullets are duties, weak-verb openers or passive constructions with no results and no numbers; the current role's bullets are in the past tense; dates use three different formats; the A-Levels sit beside a degree; several listed skills (Python, Docker, AWS, leadership, problem solving) are never shown in any experience entry. The strongest backend-relevant material for the Python role (API and database work) is the thinnest and vaguest text on the page, and the ~13-month gap between Feb 2020 and Mar 2021 is unaccounted for. Fixing the profile, the bullet construction (verb + what + how + [result]) and the skills evidence would lift this considerably.

### Sections

- Header
- PROFILE
- EXPERIENCE
- EDUCATION
- SKILLS

### Findings

#### F1 [high]: G10 Use no personal pronouns

- Section: PROFILE
- Text: I am a highly skilled and passionate software developer with excellent communication skills. I am a team player who is responsible for delivering outstanding results in a fast-paced environment.
- Problem: The profile uses first-person pronouns ("I am", "I am a team player"), which resumes are written without; it should use implied first person.
- Proposed change: Rewrite without pronouns, e.g. "Software developer with [X] years' experience delivering [project/result] in [context]." Supply [X] years and the actual project or result from your experience.

#### F2 [high]: G13 Remove self-praise; let the facts show quality

- Section: PROFILE
- Text: highly skilled and passionate ... excellent communication skills ... outstanding results in a fast-paced environment
- Problem: Unsupported self-assessments ("highly skilled", "passionate", "excellent", "outstanding") tell the reader nothing and are not backed by evidence anywhere in the CV.
- Proposed change: Delete the adjectives and let facts carry the claim, e.g. "Software developer building [what] with Python and SQL; delivered [result] for [team/audience]." Take the specifics from your experience entries.

#### F7 [high]: G01 Describe achievements and results, not duties

- Section: EXPERIENCE
- Text: Fixed bugs and attended daily stand-ups with the team.
- Problem: The bullet lists duties and activities with no accomplishment, contribution or effect (bug volume, severity, impact on the service, or anything changed).
- Proposed change: Keep the action but add an outcome from your own knowledge of the work, e.g. "Diagnosed and fixed [number/type] bugs, [result]." Use placeholders rather than guessing figures.

#### F8 [high]: G11 Match verb tense to whether the role is current

- Section: EXPERIENCE
- Text: Software Developer, Brightfield Logistics (fictional) — March 2021 - Present ... Worked on various tasks related to the API. / Helped with projects ... / Reports were prepared ... / Fixed bugs and attended daily stand-ups ...
- Problem: The role is dated "Present" but every bullet uses past tense ("Worked", "Helped", "were prepared", "Fixed", "attended"), so the tense does not match the role's ongoing status.
- Proposed change: Convert the bullets to present tense for this ongoing role, e.g. "Build and maintain the company website and the internal booking tool"; "Fix bugs and take part in daily stand-ups with the team."

#### F10 [high]: G10 Use no personal pronouns

- Section: EXPERIENCE
- Text: I build landing pages for clients using HTML and CSS.
- Problem: First-person pronoun "I" in an experience bullet.
- Proposed change: Drop the pronoun and lead with the verb: "Built landing pages for clients using HTML and CSS, [result]."

#### F22 [high]: G04 Evidence skills; don't just list them

- Section: SKILLS
- Text: Python, JavaScript, SQL, Docker, leadership, problem solving, AWS
- Problem: Several listed skills are never shown in use: Python, Docker and AWS appear in no experience or education entry, and "leadership" and "problem solving" appear nowhere else in the CV.
- Proposed change: Back each skill with an existing entry that demonstrates it (e.g. tie Python and SQL to the API and database work, and Docker/AWS to specific work you actually did), and remove any skill — such as leadership or problem solving — that no entry supports. Do not add new skills to make the list fit.

#### F3 [medium]: G09 Remove duty phrases

- Section: EXPERIENCE
- Text: Responsible for the company website and the internal booking tool.
- Problem: Duty phrase "Responsible for" opens the bullet and states ownership rather than an action or result.
- Proposed change: Start with the action: "Built and maintained [which parts/what work] of the company website and the internal booking tool, using [tools]."

#### F4 [medium]: G03 Be specific about what was done and how

- Section: EXPERIENCE
- Text: Worked on various tasks related to the API.
- Problem: "Various tasks related to the API" is completely general: no specific action, endpoint, feature, method or tool is named, and no detail is given about how the work was done.
- Proposed change: Name the concrete work the CV can support, e.g. "Built and maintained [endpoint/feature] on the [system] API using [language/tool], handling [volume] requests." Replace the placeholders with the real details.

#### F5 [medium]: G08 Start each bullet with a strong action verb

- Section: EXPERIENCE
- Text: Helped with projects for the warehouse team.
- Problem: The bullet opens with the weak verb "Helped" and names no contribution, so the reader cannot tell what you did.
- Proposed change: Open with a strong action verb and the contribution: "Delivered [what] for the warehouse team using [tools], [result]."

#### F6 [medium]: G12 Prefer active voice

- Section: EXPERIENCE
- Text: Reports were prepared for management every month.
- Problem: Passive construction ("were prepared") makes it unclear who prepared the reports; your contribution is left implicit.
- Proposed change: Make yourself the implied subject: "Prepared monthly [type of] reports for management, [result/use of the reports]."

#### F9 [medium]: G09 Remove duty phrases

- Section: EXPERIENCE
- Text: Duties included maintaining the database.
- Problem: "Duties included" is an explicit filler opener listed as a duty phrase; the reader has to reach the end of the line to find the action.
- Proposed change: Delete the opener and lead with the action: "Maintained the [system/name] database, including [tasks], [result]."

#### F12 [medium]: G14 Write concise phrases, not narrative

- Section: EXPERIENCE
- Text: Involved in the migration to the new CMS, which was a big project and took a long time and many people were involved in it.
- Problem: A single run-on, narrative sentence with several clauses; it is far longer than the concise phrase style expected and buries the action.
- Proposed change: Split and shorten into a phrase, e.g. "Migrated [what] to the new CMS, working with [team size] colleagues over [duration]." Keep only what you can state accurately.

#### F13 [medium]: G02 Quantify only with numbers the candidate supplied

- Section: EXPERIENCE
- Text: which was a big project and took a long time and many people were involved in it
- Problem: Scale and effort are described with vague qualifiers ("big", "a long time", "many people") and no figure, so the size of the work cannot be judged.
- Proposed change: Replace with numbers you can verify, e.g. "over [duration]" and "with [team size] colleagues"; if no figure is available, add the placeholder as written and fill it in.

#### F16 [medium]: G20 Format dates, styles and grammar consistently

- Section: EXPERIENCE
- Text: March 2021 - Present / 06/2018 - 02/2020 / 2014 - 2016
- Problem: Three different date formats are used for the same kind of information (month name + year, numeric month/year, year only).
- Proposed change: Choose one format and apply it to every entry, e.g. "Mar 2021 - Present", "Jun 2018 - Feb 2020", "2014 - 2016".

#### F19 [medium]: G05 Tailor by selecting and ordering, never by adding

- Section: EXPERIENCE
- Text: Worked on various tasks related to the API. ... Duties included maintaining the database.
- Problem: The content most relevant to the target Python backend role (API work, database work) is the thinnest and vaguest on the page, while irrelevant material (Shop Assistant, website duties) occupies equal or clearer space.
- Proposed change: Using only facts already in the CV, give the API and database bullets more room and more detail (what was built, with what tools, [result]) and trim the unrelated entries, so the backend evidence appears first and in most depth.

#### F20 [medium]: G07 Cut irrelevant, repetitive or out-of-date content

- Section: EDUCATION
- Text: A-Levels: Maths, Physics, English
- Problem: School-leaving qualifications are listed alongside a completed degree; the degree supersedes them and they add nothing.
- Proposed change: Remove the A-Levels line, keeping the BSc as the only education entry.

#### F23 [medium] (uncertain): G06 Mirror job-posting terms only where the CV truthfully supports them

- Section: SKILLS
- Text: SQL ... AWS ... the API / the database
- Problem: The posting's terms REST APIs, PostgreSQL and CI/CD do not appear, even though the CV describes similar things in other words ("the API", "the database"); keyword scanning for this posting may miss it.
- Proposed change: If accurate, consider the posting's terms for work you already describe — "REST APIs" for the API work and "PostgreSQL" for the database work, and "CI/CD" if you genuinely work with pipelines. You decide whether each term is true; keep your own wording otherwise and do not add a term for anything the CV does not evidence.

#### F11 [low]: G21 Eliminate spelling, grammar and punctuation errors

- Section: EXPERIENCE
- Text: I build landing pages for clients using HTML and CSS.
- Problem: The verb form is wrong for the time period of the role and reads as a grammar error ("build" for an ended role).
- Proposed change: Correct to "Built landing pages for clients using HTML and CSS" (the HTML and CSS tool names stay as written).

#### F14 [low]: G15 Avoid slang, jargon and repetition

- Section: EXPERIENCE
- Text: Involved in the migration ... many people were involved in it
- Problem: "Involved" is repeated twice in one bullet (and "Worked"/"Helped" are used as near-identical openers elsewhere), which reads repetitively.
- Proposed change: Vary the wording and remove the repetition, e.g. "Migrated [what] to the new CMS together with [team size] colleagues"; use distinct verbs for each bullet.

#### F15 [low]: G22 Spell out acronyms on first use

- Section: EXPERIENCE
- Text: Involved in the migration to the new CMS
- Problem: The acronym "CMS" is used without its expanded form on first appearance; a reader outside your workplace may not know which system it means.
- Proposed change: Expand on first use: "the migration to the new content management system (CMS)", then use "CMS" afterwards.

#### F17 [low]: G23 Flag unexplained gaps; do not explain them

- Section: EXPERIENCE
- Text: 02/2020 (end of Junior Developer, Northpoint Digital) to March 2021 (start of Software Developer, Brightfield Logistics)
- Problem: Roughly thirteen months between the end of the Northpoint Digital role and the start of the Brightfield Logistics role are unaccounted for.
- Proposed change: Add a brief, factual line for the period, or a "[gap: reason]" placeholder that you complete yourself — do not leave the reader to guess.

#### F18 [low]: G07 Cut irrelevant, repetitive or out-of-date content

- Section: EXPERIENCE
- Text: Shop Assistant, Corner Books (fictional) 2014 - 2016 - Served customers and handled the till.
- Problem: An old, unrelated retail role from before your professional software work takes up the same space as the roles relevant to a backend developer job.
- Proposed change: Delete this entry or shorten it to a single line (or drop the bullet entirely); it adds nothing for a Python backend reader.

#### F21 [low]: G17 Give every entry an organisation, a title and dates, newest first

- Section: EDUCATION
- Text: A-Levels: Maths, Physics, English
- Problem: This entry has no institution and no dates, unlike the degree entry, so the reader cannot place it in time.
- Proposed change: Either remove it (see the superseded-qualification finding) or add the institution and dates, e.g. "A-Levels: Maths, Physics, English — [school], [dates]".

### Guidelines cited

- G01 Describe achievements and results, not duties. Rule: Each experience entry should say what the candidate accomplished or changed. A list of responsibilities is not enough. When a bullet has no outcome, the Rewrite adds a `[result]` placeholder and never writes an outcome itself. Sources: MIT-W (accomplishments and contributions, not just responsibilities; descriptions should not read like job descriptions); MIT-PDF "Emphasize your accomplishments, contributions, and outcomes."; HAR (lists "Not demonstrating results" among the top five mistakes); USF (use action verbs instead of task descriptions; incorporate results); IMP (STAR, ending in Result).
- G02 Quantify only with numbers the candidate supplied. Rule: Where scale or impact can be measured (people, money, time, volume, %), express it as a number taken from the CV. If the CV has no number, the Rewrite inserts a placeholder such as `[X%]` or `[team size]` and never estimates one. Sources: MIT-PDF "Quantify bullet points to convey size and/or scale of project, budget, team, time or results."; MIT-W (quantify if you can; attendees, money raised or managed); HAR (fact-based: quantify and qualify); EUP "If necessary, quantify your responsibilities".
- G03 Be specific about what was done and how. Rule: Replace general statements with the concrete action, method or tool the CV already mentions. When the CV gives no specifics, flag the gap and do not supply any. Sources: MIT-W (include how you performed tasks, not just what you did); HAR (specific rather than general).
- G04 Evidence skills; don't just list them. Rule: Every skill the CV claims as a strength should be backed by at least one experience entry that shows it in use. The Rewrite may move or link existing evidence and must never add a skill. Sources: USF (showcase skills and competencies, not merely list them); MIT-PDF "Give evidence of your skills and personal impact"; IMP (make skills evident with a summary followed by STAR examples).
- G05 Tailor by selecting and ordering, never by adding. Rule: When a target role is given, put the entries most relevant to it first and give them more space, using only content already in the CV. Sources: MIT-W (target a specific position; select experiences that show the required skills); NCS (match the CV to the job and company; review the advert); HAR (tailor to the type of position); EUP "highlight your advantages according to the specific requirements of the prospective employer."
- G06 Mirror job-posting terms only where the CV truthfully supports them. Rule: If the posting uses a term for something the CV already shows in other words, the Finding advises the candidate: "if accurate, consider the posting's term X". The Rewrite never applies a posting term itself; it keeps the CV's wording, and only the candidate decides whether the term is true. Never insert a keyword for a skill or tool the CV does not evidence, and never stuff keywords. Sources: MIT-ATS (use posting keywords meaningfully; avoid spamming; you must be able to account for everything on the resume); MIT-W (employers may use keyword scanning); ILL (borrow wording from the job posting).
- G07 Cut irrelevant, repetitive or out-of-date content. Rule: Recommend removing material that adds nothing for the target reader. Rewrites may only delete or shorten here, never replace with new content. Sources: MIT-PDF "Omit unrelated memberships and information that is repetitive, implicit (e.g. high school graduation for a college graduate), or out-of-date."; EUP "work experience or training which is old or not relevant for the application can be omitted."; NCS (remove outdated information).
- G08 Start each bullet with a strong action verb. Rule: Experience bullets begin with a verb that names the candidate's contribution. Sources: MIT-W (start with a strong action verb such as built, managed, developed); DUKE (begin with a strong, active verb); MIT-PDF "Use action verbs"; HAR (use action words, not passive language).
- G09 Remove duty phrases. Rule: Remove filler openers and start with the action instead. Sources: MIT-PDF "Leave out unnecessary words, sentences, and phrases e.g. "Duties included / Hired to / Project involved / Responsible for..."; DUKE (avoid "responsible for" and "duties include").
- G10 Use no personal pronouns. Rule: Write in implied first person, with no "I", "me", "my", "we", "he" or "she". Sources: MIT-PDF "Don't use the first person, I, or any pronouns."; HAR (do not use personal pronouns such as I or We); DUKE; ILL.
- G11 Match verb tense to whether the role is current. Rule: Use present tense for roles and activities that are ongoing and past tense for those that have ended. Keep the tense consistent within each entry. Sources: DUKE (present tense for current activities, past tense for past ones); ILL (keep verb tenses consistent; present tense for current roles); USF (present tense for current positions, past tense for previous ones).
- G12 Prefer active voice. Rule: Rewrite passive constructions so the candidate is the implied subject. Sources: HAR (active rather than passive; lists passive language among the top five mistakes); MIT CAPD, https://capd.mit.edu/resources/resume-tips-avoid-the-passive-voice/ (eliminating passive voice helps; the full guide it links to is off-site and was not read).
- G13 Remove self-praise; let the facts show quality. Rule: Delete unsupported self-assessments rather than strengthening them. The Rewrite must not replace them with invented evidence. Sources: MIT-PDF "Avoid self-flattering terms such as "highly skilled, outstanding, or excellent." … let readers decide for themselves that you are well-qualified."; HAR (written to express, not impress; articulate rather than "flowery").
- G14 Write concise phrases, not narrative. Rule: Bullets are short phrases, and complete sentences or paragraphs are not required. Keep each role's description brief. Sources: HAR (no narrative style; written for people who scan quickly); MIT-W (resumes don't require complete sentences); EUP "use short sentences"; NCS (usually 2 to 3 lines per role).
- G15 Avoid slang, jargon and repetition. Rule: Use plain professional wording, vary verbs, and do not repeat the same phrase across bullets. Sources: MIT-PDF "Avoid repeating words or phrases, as well as using jargon"; HAR (no slang or colloquialisms); ILL (use a variety of action verbs).
- G17 Give every entry an organisation, a title and dates, newest first. Rule: Each experience and education entry names the organisation, the role or qualification, and its dates, and entries within a section run in reverse chronological order. The Rewrite flags missing fields with placeholders (`[employer]`, `[dates]`). Sources: NCS (list the most recent experience first; include employer, job title, dates and what you did); HAR (reverse chronological within headings).
- G20 Format dates, styles and grammar consistently. Rule: Use one date format, one bullet style, one way of emphasising text and one grammatical pattern throughout the CV. Sources: HAR (be consistent in format and content); MIT-PDF "Be consistent and use the same grammatical style throughout."; DUKE (consistent styling and formatting across all sections); NCS (use the same style throughout).
- G21 Eliminate spelling, grammar and punctuation errors. Rule: Correct errors and keep to one English variant (US or UK) throughout. The Rewrite fixes spelling but never changes proper nouns, product names or job titles. Sources: HAR (spelling and grammar errors are the first of the top five mistakes); MIT-PDF "Proofread one more time to ensure correct spelling, grammar and punctuation."; NCS (have someone check spelling and grammar); EUP "there is no excuse for mistakes in spelling and punctuation!"
- G22 Spell out acronyms on first use. Rule: Write the expanded form, then the acronym in parentheses, the first time an acronym appears, except for universally known ones. The Rewrite expands an acronym only when the expansion is unambiguous; otherwise it writes `[expand ACRONYM]`. Sources: ILL (spell out acronyms the first time, followed by the acronym in parentheses); HAR (do not abbreviate). The two sources differ in strictness; G22 follows ILL because a reviewer can check it in text.
- G23 Flag unexplained gaps; do not explain them. Rule: The Review points out unaccounted periods between dated entries. The Rewrite may add only a `[gap: reason]` placeholder and never invents a reason or an activity. Sources: HAR (avoid information gaps such as a missing summer); EUP "explain any breaks in your studies or career"; NCS (says gaps are normal and links to advice on explaining them, so a gap finding is advisory, never a defect).

## Tailoring

**Job Match Score: 58/100** (the model's estimate, not a measurement)

The candidate is a developer with roughly five years of experience across two software roles, including one at a logistics company, which aligns well with the freight/logistics domain. The listed skills (Python, SQL, Docker, AWS) map onto several of the core requirements, and there is some API-related work. However, the CV does not clearly demonstrate the depth the role asks for: Python is only listed as a skill rather than evidenced in the experience bullets, there is no explicit REST API design, CI/CD, automated testing, code review, or Kubernetes content, and the database and cloud experience is described only vaguely. Overall a partial fit with meaningful gaps to address.

### Matches

- Python is listed among the candidate's skills, matching the role's primary language requirement.
- Docker is listed as a skill, matching the requirement for Docker experience.
- AWS is listed as a skill, matching the preferred major cloud provider.
- SQL is listed as a skill and the Junior Developer role involved maintaining the database, matching the relational database requirement in part.
- The current role at Brightfield Logistics is at a logistics company, matching the nice-to-have experience in logistics or freight.
- There is API-related work mentioned ("various tasks related to the API"), matching the API-facing nature of the role.
- Worked with a warehouse team on projects, which relates to the requirement to work with operations staff.
- Attended daily stand-ups and fixed bugs, showing team-based software delivery experience.
- BSc in Computer Science plus A-Levels including Maths and Physics, providing a technical foundation.
- The profile claims excellent communication skills, partially matching the clear communication requirement.
- Total professional development experience spans roughly 2018-2020 plus 2021-present, which is in the range of the 3+ years requested.

### Gaps

Asked for in the Job Description but not shown in the CV. Add one only if you have that experience.

- 3+ years of professional experience specifically with Python is not shown — Python appears only in the skills list, with no experience bullet demonstrating it.
- Experience designing relational databases is not shown — the database content is limited to "maintaining the database" and SQL as a listed skill.
- PostgreSQL specifically is not mentioned anywhere in the CV.
- Designing and building REST APIs is not shown — the API reference is vague ("various tasks related to the API") and REST is not mentioned.
- CI/CD pipelines are not mentioned in the CV.
- Kubernetes is not mentioned in the CV.
- Writing automated tests is not shown — only bug fixing is mentioned.
- Taking part in code review is not shown.
- Improving the performance and reliability of existing services is not shown.
- Turning requests from operations staff into features is only loosely implied by the warehouse team projects; no direct evidence of gathering requirements from operational users.
- Clear written communication is asserted in the profile but not evidenced by any specific example.
- No details on the scale, users, or impact of the booking tool/website are given, making it hard to gauge the depth of backend experience.

### What to emphasise

- Move the Brightfield Logistics role and its logistics-industry context up so the freight domain relevance is immediately visible.
- Give more space to the API-related work in the current role so its backend nature and any specifics are clear.
- Surface the SQL/database maintenance content from the Junior Developer role rather than leaving it as a single line.
- Bring Docker, AWS, Python and SQL out of the plain skills list and connect them to the roles where they were used, if that usage exists in the CV.
- Expand the warehouse team project work, since it is the closest evidence of collaborating with operations staff.
- Trim or drop the Shop Assistant role, which is unrelated and takes space from the developer experience.
- Replace the generic profile paragraph's self-descriptions with the concrete technical stack already present in the CV, so the summary leads with relevant tools and roles.

## Rewrite

### Placeholders to fill in

- [X]
- [endpoint/feature]
- [language/tool]
- [what]
- [tools]
- [result]
- [type of]
- [number/type]
- [gap: reason]
- [system/name]
- [tasks]
- [team size]
- [duration]

### Rewritten CV

# ALEX MORGAN
alex.morgan@example.com | +44 20 7946 0000 | Leeds, UK

## PROFILE
Software developer with [X] years' experience across logistics and digital projects. Builds and maintains the company website and the internal booking tool, and works on API and database tasks. Skills include Python, JavaScript, SQL, Docker and AWS.

## EXPERIENCE

**Software Developer, Brightfield Logistics (fictional)**
Mar 2021 - Present
- Build and maintain the company website and the internal booking tool.
- Build and maintain [endpoint/feature] on the API using [language/tool].
- Deliver [what] for the warehouse team using [tools], [result].
- Prepare monthly [type of] reports for management, [result].
- Diagnose and fix [number/type] bugs, [result].
- Take part in daily stand-ups with the team.

Mar 2020 - Feb 2021 — [gap: reason]

**Junior Developer, Northpoint Digital (fictional)**
Jun 2018 - Feb 2020
- Maintained the [system/name] database, including [tasks], [result].
- Built landing pages for clients using HTML and CSS, [result].
- Migrated [what] to the new content management system (CMS) together with [team size] colleagues over [duration].

**Shop Assistant, Corner Books (fictional)** — 2014 - 2016

## EDUCATION
BSc Computer Science, University of Westmoor (fictional), 2015 - 2018

## SKILLS
Python, JavaScript, SQL, Docker, AWS

