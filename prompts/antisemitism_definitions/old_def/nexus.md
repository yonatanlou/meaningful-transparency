# Nexus Document - Annotation Guidelines for Identifying Antisemitic Content on Facebook

## 1. Task Description

### Overview
You will be annotating Facebook posts, comments, and messages to identify whether they contain antisemitic content.  
This is a **binary classification task**:

- **ANTISEMITIC**: Contains antisemitic content  
- **NOT_ANTISEMITIC**: Does not contain antisemitic content  

### Purpose
These annotations will help train systems to detect and moderate antisemitic content on social media platforms, protecting Jewish users from harassment and hate speech while preserving legitimate discourse about Israel, Judaism, and related topics.

### Important Context
Antisemitism consists of anti-Jewish beliefs, attitudes, actions, or systemic conditions. It includes negative beliefs and feelings about Jews, hostile behavior directed against Jews, and conditions that discriminate against Jews and impede their ability to participate equally in society.

---

## 2. Label Descriptions

### ANTISEMITIC
Content should be labeled as **ANTISEMITIC** if it:

- Promotes harmful stereotypes:
  - Claims about Jewish control of media, banks, governments, or institutions  
  - Accusations of dual loyalty  
  - Blood libel accusations  
  - Claims about Jewish greed or manipulation  
  - Derogatory physical stereotypes  

- Denies or minimizes the Holocaust  
- Calls for violence or discrimination against Jews  
- Uses antisemitic symbols or coded language:
  - `(((echo)))`  
  - ZOG (Zionist Occupied Government)  
  - 1488, 88, 14 words  
  - Caricatures or antisemitic imagery  

- Holds Jews collectively responsible for the actions of individuals or Israel  
- Promotes conspiracy theories:
  - Global Jewish conspiracies  
  - Hidden Jewish control of events or institutions  

- Applies double standards to Israel because it is a Jewish state  
- Denies Jews the right to self-determination or safety  

### NOT_ANTISEMITIC
Content should be labeled as **NOT_ANTISEMITIC** if it:

- Criticizes Israeli government policies without antisemitic tropes  
- Discusses Judaism, Jewish culture, or history neutrally or positively  
- Opposes Zionism or supports Palestinian rights without antisemitic rhetoric  
- Mentions Jews without stereotypes or hostility  
- Contains legitimate political discourse about Israel-Palestine  
- Uses the word *Zionist* in its political sense, not as a slur  

---

## 3. Annotation Examples

### Clear Examples of ANTISEMITIC Content
| Text | Label | Explanation |
|------|-------|-------------|
| “Jews control all the banks and media, wake up people!” | ANTISEMITIC | Classic conspiracy theory |
| “6 million? More like 600,000.” | ANTISEMITIC | Holocaust denial |
| “Every. Single. Time. Check the early life section.” | ANTISEMITIC | Coded antisemitic phrase |
| “Of course (((they))) are behind this” | ANTISEMITIC | Triple parentheses |
| “Synagogue of Satan strikes again” | ANTISEMITIC | Religious slur |
| “Because AIPAC owns Congress” | ANTISEMITIC | Antisemitic ownership trope |

### Clear Examples of NOT_ANTISEMITIC Content
| Text | Label | Explanation |
|------|-------|-------------|
| “Israel’s settlement policy violates international law” | NOT_ANTISEMITIC | Legitimate criticism |
| “Happy Hanukkah to all my Jewish friends!” | NOT_ANTISEMITIC | Positive cultural reference |
| “The Israeli military’s actions in Gaza are disproportionate” | NOT_ANTISEMITIC | Policy criticism |
| “I support a two-state solution” | NOT_ANTISEMITIC | Political stance |
| “Bernie Sanders’ healthcare plan would help millions” | NOT_ANTISEMITIC | Neutral statement |
| “BDS is a nonviolent way to pressure Israel” | NOT_ANTISEMITIC | Political activism |

### Edge Cases and Ambiguous Examples
| Text | Label | Explanation |
|------|-------|-------------|
| “Israel is an apartheid state” | NOT_ANTISEMITIC | Harsh but political |
| “Zionist lobby has too much influence in Washington” | NOT_ANTISEMITIC (borderline) | Context matters |
| “Rich New York lawyers defending Israel again” | ANTISEMITIC | Wealth/location stereotype |
| “From the river to the sea” | NOT_ANTISEMITIC | Political slogan; context matters |
| “Rothschilds pulling the strings as usual” | ANTISEMITIC | Classic banking conspiracy |
| “Why does such a small group have so much power?” | ANTISEMITIC | Jewish power trope |
| “I’m anti-Zionist, not antisemitic” | NOT_ANTISEMITIC | Political position |
| “Jewish space lasers” (serious) | ANTISEMITIC | Conspiracy theory |
| “Another Hollywood producer exposed - check his background” | ANTISEMITIC | Dog whistle |

---

## 4. Handling Ambiguous Cases

### Decision Tree
1. Does the content criticize Israel or Zionism?  
   - Yes → Check for antisemitic tropes or collective blame  
   - No → Step 2  
2. Does it mention Jews or coded references?  
   - Yes → Check for stereotypes or conspiracies  
   - No → Likely NOT_ANTISEMITIC  
3. Does it use legitimate political terminology?  
   - Yes → Ensure it doesn’t invoke antisemitism  
   - No → Step 4  
4. Historical references?  
   - Yes → Check for Holocaust denial  
   - No → Step 5  
5. Is overall intent hostile to Jews as Jews?  
   - Yes → ANTISEMITIC  
   - No → NOT_ANTISEMITIC  

### Special Considerations
- **Context matters**: Same phrase may be antisemitic in one context, not in another  
- **Coded language**: Watch for evolving dog whistles  
- **Sarcasm/Irony**: Sarcasm used to promote antisemitism = still ANTISEMITIC  
- **Mixed content**: If both legitimate criticism and antisemitic tropes are present → ANTISEMITIC  
- **Ambiguous “Zionist”**:
  - Political descriptor = NOT_ANTISEMITIC  
  - Slur/synonym for Jew = ANTISEMITIC  

---

## 5. Default Actions for Difficult Cases

- Holocaust references ambiguous → **ANTISEMITIC** if denial/minimization suggested  
- “Zionist” usage unclear → If no antisemitic indicators, default to **NOT_ANTISEMITIC**  
- Criticism of Israel with borderline language → **NOT_ANTISEMITIC** unless clear tropes  
- Suspected coded language but uncertain → Default to **NOT_ANTISEMITIC**  
- Sarcasm/irony unclear → If it could be read as antisemitic → **ANTISEMITIC**  

---

## 6. Important Reminders

### What This Task Is NOT
- NOT judging if criticism of Israel is fair  
- NOT deciding legitimate vs illegitimate political opinions  
- NOT censoring Jewish topics  

### What This Task IS
- Identifying antisemitic hatred, stereotypes, and discrimination  
- Protecting users from harassment while preserving free discourse  
- Applying consistent standards  

### Key Principles
- Criticism of Israel ≠ Antisemitism (unless tropes are used)  
- Supporting Palestinian rights ≠ Antisemitism (unless denying Jewish peoplehood/safety)  
- Anti-Zionism ≠ Antisemitism (unless denying Jewish self-determination)  
- Look for **antisemitic elements**, not just negative sentiment  

---

## 7. Quality Checklist
Before submitting each annotation, verify:  

- [ ] Read the complete text carefully  
- [ ] Considered the context, not just isolated phrases  
- [ ] Checked for both obvious and coded antisemitic language  
- [ ] Distinguished between legitimate discourse and antisemitism  
- [ ] Applied guidelines consistently  
- [ ] Used the decision tree for ambiguous cases  
- [ ] Kept personal politics out of annotation  

---

## 8. Additional Notes
- Document new coded language or dog whistles if encountered  
- Track patterns of borderline content  
- Remember antisemitism evolves → stay alert  
- If truly uncertain, choose the label that **best protects potential targets** while preserving discourse  

---

*These guidelines are based on the Nexus Document’s framework for understanding antisemitism and international best practices for content moderation.*
