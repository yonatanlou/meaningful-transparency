# Annotation Guidelines for Antisemitic Text Classification on Facebook - IHRA Definition

## 1. Task Description

### Overview
You will be annotating Facebook posts and comments to identify whether they contain antisemitic content.  
This is a **binary classification task**:

- **ANTISEMITIC**: Contains antisemitic content  
- **NOT_ANTISEMITIC**: Does not contain antisemitic content  

### Purpose
These annotations will be used to train machine learning models to automatically detect antisemitic content on social media platforms, helping to combat online hate speech and protect Jewish communities from harassment.

### Important Note
Each text should receive exactly one label.  
There is **no neutral or uncertain category** — you must make a determination based on the guidelines.

---

## 2. Label Descriptions

### ANTISEMITIC
Text that contains any form of antisemitism, defined as:

> “A certain perception of Jews, which may be expressed as hatred toward Jews. Rhetorical and physical manifestations of antisemitism are directed toward Jewish or non-Jewish individuals and/or their property, toward Jewish community institutions and religious facilities.”

This includes but is not limited to:

- Direct hatred or calls for violence against Jews  
- Conspiracy theories about Jewish control or influence  
- Holocaust denial or distortion  
- Antisemitic stereotypes and tropes  
- Holding Jews collectively responsible for wrongdoing  
- Denying Jewish people’s right to self-determination  
- Applying double standards to Israel not expected of other nations  
- Using antisemitic imagery to characterize Israel/Israelis  

### NOT_ANTISEMITIC
Text that does **not** contain antisemitic content. This includes:

- Legitimate criticism of Israeli government policies  
- Discussion of Jewish culture, religion, or history without negative stereotypes  
- News reporting about Jewish communities or Israel without bias  
- Personal experiences or opinions without invoking antisemitic tropes  
- Mentions of Jews/Judaism/Israel in neutral or positive context  

---

## 3. Annotation Examples

### Clear Examples of ANTISEMITIC Content
| Text | Label | Explanation |
|------|-------|-------------|
| “Jews control all the banks and media” | ANTISEMITIC | Conspiracy theory |
| “The Holocaust never happened, it’s all propaganda” | ANTISEMITIC | Holocaust denial |
| “Hitler should have finished the job” | ANTISEMITIC | Call for genocide |
| “These (((people))) are destroying our country” | ANTISEMITIC | Triple parentheses |
| “Of course he’s greedy, look at his last name” | ANTISEMITIC | Jewish money stereotype |
| “Israel is a cancer that needs to be removed” | ANTISEMITIC | Calls for destruction of Jewish state |
| “Jews are more loyal to Israel than to America” | ANTISEMITIC | Dual loyalty trope |

### Clear Examples of NOT_ANTISEMITIC Content
| Text | Label | Explanation |
|------|-------|-------------|
| “I disagree with Netanyahu’s policies on settlements” | NOT_ANTISEMITIC | Legitimate political criticism |
| “My Jewish neighbor makes the best challah bread” | NOT_ANTISEMITIC | Positive cultural reference |
| “The synagogue on Main Street has beautiful architecture” | NOT_ANTISEMITIC | Neutral description |
| “Israel’s tech industry is really innovative” | NOT_ANTISEMITIC | Positive factual statement |
| “I’m learning Hebrew for my trip to Tel Aviv” | NOT_ANTISEMITIC | Personal statement |
| “The Israeli-Palestinian conflict is complex” | NOT_ANTISEMITIC | Neutral political observation |

### Edge Cases and Boundary Examples
| Text | Label | Explanation |
|------|-------|-------------|
| “Zionists have too much influence in Congress” | ANTISEMITIC | “Zionist” used as code for Jews |
| “AIPAC lobbies just like any other group” | NOT_ANTISEMITIC | Legitimate observation |
| “Israel gets too much US foreign aid” | NOT_ANTISEMITIC | Political opinion |
| “Jews run Hollywood” | ANTISEMITIC | Conspiracy + discriminatory |
| “Many Hollywood executives happen to be Jewish” | NOT_ANTISEMITIC | Factual observation |
| “IDF soldiers = Nazis” | ANTISEMITIC | Nazi comparison |
| “Some IDF actions violate international law” | NOT_ANTISEMITIC | Specific legal criticism |
| “Rothschilds pulling the strings again 🙄” | ANTISEMITIC | Conspiracy trope |
| “George Soros funds many liberal causes” | NOT_ANTISEMITIC | Factual statement |
| “#FromTheRiverToTheSea Palestine will be free” | ANTISEMITIC | Calls for elimination of Israel |
| “Palestinians deserve equal rights” | NOT_ANTISEMITIC | Human rights advocacy |

---

## 4. Handling Ambiguous Cases

### Decision Tree
1. Does the text mention Jews, Judaism, Israel, or related terms?  
   - No → NOT_ANTISEMITIC  
   - Yes → Step 2  
2. Does it invoke stereotypes, conspiracies, or antisemitic tropes?  
   - Yes → ANTISEMITIC  
   - No → Step 3  
3. Is it criticism of Israel?  
   - If similar to criticism of any other country → NOT_ANTISEMITIC  
   - If it denies Israel’s right to exist or uses Nazi comparisons → ANTISEMITIC  
   - If it holds all Jews responsible for Israeli actions → ANTISEMITIC  
4. Does it use coded language?  
   - Triple parentheses `((()))` → ANTISEMITIC  
   - “Globalists” / “cosmopolitans” (negative context) → ANTISEMITIC  
   - “Zionists” meaning all Jews → ANTISEMITIC  
   - Otherwise legitimate discourse → NOT_ANTISEMITIC  

### Special Considerations

#### Sarcasm & Irony
- Mocking antisemites → NOT_ANTISEMITIC  
- Ambiguous sarcasm → Use guidelines  
- If message could be taken at face value → ANTISEMITIC  

#### Historical Quotes
- Approvingly quoting antisemitic figures → ANTISEMITIC  
- Quoting critically/educationally → NOT_ANTISEMITIC  

#### Dog Whistles & Codes
Watch for:  
- `(((Triple parentheses)))`  
- “Cosmopolitan elite”  
- “Globalists” (in conspiracy context)  
- “Cultural Marxists”  
- “International bankers”  
- Number codes: 14/88, 6MWE  
- “Khazar” theories  

#### Criticism of Individual Jews
- Based on actions/policies → NOT_ANTISEMITIC  
- Invoking stereotypes → ANTISEMITIC  
- Attributing actions to being Jewish → ANTISEMITIC  

---

## 5. Additional Notes

### Context Limitations
- Annotate based only on text provided  
- Don’t assume intent or outside knowledge  
- Focus strictly on antisemitic content  

### Intersectionality
Text may also contain other forms of hate.  
E.g., “Jews and Muslims are destroying Europe” → **ANTISEMITIC** (also Islamophobic, but only antisemitism is in scope).

### What This Task Does NOT Include
- Rating severity of antisemitism  
- Identifying other hate speech types  
- Fact-checking claims  
- Making political judgments  

### Quality Checks
Before submission, ask:  
1. Would a reasonable Jewish person feel targeted?  
2. Does it perpetuate harmful stereotypes?  
3. Am I applying consistent standards?  
4. Did I separate political discourse from antisemitism?  

---

## Final Reminders
- One label per text — no exceptions  
- Refer to **IHRA definition examples** when in doubt  
- Err on the side of caution for ambiguous cases  
- Be consistent across similar examples  
- Take breaks if content is disturbing  

*Your work helps protect vulnerable communities from online hate. Thank you for your careful attention to these guidelines.*
