# Jerusalem Declaration - Annotation Guidelines for Classifying Antisemitic Text on Facebook

## 1. Task Description

### Introduction
You will be classifying Facebook posts and comments to determine whether they contain antisemitic content.  
This is a **binary classification task**:

- **ANTISEMITIC**  
- **NOT_ANTISEMITIC**

### Purpose
These annotations will help develop automated systems to detect and address antisemitic content on social media platforms, contributing to safer online spaces while protecting legitimate political discourse and criticism.

### What You Will Do
- Read Facebook posts and comments carefully  
- Apply the provided definitions and guidelines  
- Assign exactly ONE label: **ANTISEMITIC** or **NOT_ANTISEMITIC**  
- Use edge case guidelines for ambiguous content  

---

## 2. Label Descriptions

### ANTISEMITIC
Text that contains discrimination, prejudice, hostility, or violence against Jews as Jews (or Jewish institutions as Jewish). This includes:

- **Direct antisemitism**: Explicit hatred or discrimination targeting Jews  
- **Coded antisemitism**: Indirect references using known tropes or dog whistles  
- **Classical stereotypes**: Conspiracies about Jewish power, wealth, or evil  
- **Holocaust denial or minimization**  
- **Antisemitic anti-Israel content**: Criticism of Israel that invokes antisemitic imagery or holds all Jews responsible  

### NOT_ANTISEMITIC
Text that does **not** target Jews as Jews, including:

- Legitimate criticism of Israel’s policies  
- Political advocacy (e.g., Palestinian rights)  
- Religious or cultural discussions (neutral/positive)  
- Historical discussions without denial or distortion  
- General political discourse without antisemitic tropes  

---

## 3. Annotation Examples

### Clear Examples of ANTISEMITIC Content
| Text | Label | Explanation |
|------|-------|-------------|
| “The Jews control all the banks and media” | ANTISEMITIC | Classic conspiracy theory |
| “Another hoax by the (((globalists))) to control us” | ANTISEMITIC | Triple parentheses = antisemitic code |
| “Hitler should have finished the job” | ANTISEMITIC | Violence + Holocaust reference |
| “Of course Sarah supports Israel, she’s Jewish after all” | ANTISEMITIC | Assumes dual loyalty |
| “The Holocaust numbers are greatly exaggerated” | ANTISEMITIC | Holocaust minimization |
| “Rothschilds pulling the strings again” | ANTISEMITIC | Banking conspiracy |
| “Israel is a cancer that needs to be removed, and so do all its supporters worldwide” | ANTISEMITIC | Extends hatred to all Jews |

### Clear Examples of NOT_ANTISEMITIC Content
| Text | Label | Explanation |
|------|-------|-------------|
| “Israel’s settlement policy violates international law” | NOT_ANTISEMITIC | Evidence-based criticism |
| “I support BDS to pressure Israel on human rights” | NOT_ANTISEMITIC | Legitimate political protest |
| “Palestinians deserve equal rights and self-determination” | NOT_ANTISEMITIC | Rights advocacy |
| “Happy Hanukkah to all my Jewish friends!” | NOT_ANTISEMITIC | Positive cultural reference |
| “The Israeli government’s treatment of Palestinians is apartheid” | NOT_ANTISEMITIC | Political comparison |
| “Netanyahu’s policies are destroying chances for peace” | NOT_ANTISEMITIC | Criticism of leader |
| “My synagogue is hosting a charity drive this weekend” | NOT_ANTISEMITIC | Neutral religious mention |

### Edge Cases and Ambiguous Examples
| Text | Label | Explanation |
|------|-------|-------------|
| “Israel controls US foreign policy” | ANTISEMITIC | Invokes “Jewish control” trope |
| “Israeli influence on US politics should be examined” | NOT_ANTISEMITIC | Legitimate concern |
| “Zionists have too much power” | ANTISEMITIC | “Zionist” used as code for Jews |
| “I oppose Zionism as a political ideology” | NOT_ANTISEMITIC | Legitimate opposition |
| “Disgusting what Israel does, typical behavior” | ANTISEMITIC | Suggests stereotype |
| “Disgusting what Israel did in Gaza yesterday” | NOT_ANTISEMITIC | Criticizes action |
| “Why do they always play the victim?” (re: antisemitism) | ANTISEMITIC | Uses antisemitic stereotype |
| “Israel often invokes security concerns to justify policies” | NOT_ANTISEMITIC | Analytical observation |

---

## 4. Handling Ambiguous Cases

### Decision Tree
1. Does the text mention Jews, Israelis, or codes?  
   - **No** → NOT_ANTISEMITIC  
   - **Yes** → Step 2  
2. Is criticism directed at:  
   - Jews → ANTISEMITIC  
   - Israeli government/policies → Step 3  
   - Both/unclear → Step 3  
3. Does the text use stereotypes or tropes?  
   - **Yes** → ANTISEMITIC  
   - **No** → Step 4  
4. Does it:  
   - Hold all Jews responsible for Israel’s actions → ANTISEMITIC  
   - Deny Jewish self-determination → ANTISEMITIC  
   - Use Holocaust imagery inappropriately → ANTISEMITIC  
   - Compare Israel to Nazis (to hurt Jews) → ANTISEMITIC  
   - None of the above → NOT_ANTISEMITIC  

### Context Considerations
- **User identity**: Palestinian, Jewish, extremist → affects interpretation  
- **Thread context**: Replies, surrounding content may reveal coding  
- **Current events**: Conflicts/holidays can influence tone  

### Default Rules
- Truly ambiguous → **NOT_ANTISEMITIC** (protects free speech)  
- **Sarcasm/Irony**:  
  - Mocking antisemites → NOT_ANTISEMITIC  
  - Ambiguous → Apply guidelines  
  - Masking antisemitism → ANTISEMITIC  
- **Quotations**:  
  - Quoting to criticize → NOT_ANTISEMITIC  
  - Quoting approvingly → ANTISEMITIC  
  - Ambiguous → Check context  
- **Multiple possible targets**:  
  - “Bankers are destroying society” → NOT_ANTISEMITIC  
  - “Soros is destroying society” → Check for antisemitic tropes  

---

## 5. Special Considerations

### Coded Language & Dog Whistles
- `(((name)))` = Jew  
- “Globalists,” “cosmopolitans,” “international bankers” → often mean Jews  
- “Zionist” outside Israel context → often code for Jew  
- Numbers: 14, 88, 109, 110 = Nazi codes  
- Pronouns like “they,” “them,” “those people” → sometimes mean Jews  

### Cultural and Regional Differences
- Harsh Middle Eastern criticism ≠ necessarily antisemitic  
- European references carry historical weight  
- American discourse has unique patterns  

### Platform-Specific Elements
- **Emojis**: 👃 🐀 👹 → antisemitic in context  
- **Memes**: Pepe, Happy Merchant, etc.  
- **Hashtags**: May carry antisemitic content  

---

## 6. Quality Checklist
Before submitting, confirm:  
- [ ] Read entire text (including hashtags)  
- [ ] Considered context  
- [ ] Applied decision tree for ambiguity  
- [ ] Checked for coded language  
- [ ] Distinguished Israel criticism vs antisemitism  
- [ ] Assigned **exactly one label**  

---

## 7. Common Mistakes to Avoid
- Don’t assume all criticism of Israel is antisemitic  
- Don’t ignore coded language/dog whistles  
- Don’t let personal politics bias decisions  
- Don’t rush → ambiguous cases require care  
- Don’t annotate based only on keywords  

---

## 8. Final Reminders
- Focus on content, not agreement  
- Refer back to core definitions when in doubt  
- Protect Jewish safety **and** legitimate political speech  
- Take breaks if content is disturbing  
- Ask for clarification if uncertain  

---
