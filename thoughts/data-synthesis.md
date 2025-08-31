
[Synthetic Data Generation Using Large Language Models: Advances in Text and Code](https://arxiv.org/pdf/2503.14023)
# Prompt-Based Data Augmentation with LLMs

Prompting techniques guide LLMs to generate synthetic text data for specific tasks. Each strategy balances **relevance**, **diversity**, and **control** differently.

---

## Strategies

### Zero-Shot Generation
- **Definition**: Prompt includes only task instructions.  
- **Example Prompt**:  
  *"Generate a sentence expressing positive sentiment about a product."*  
- **Possible Output**:  
  *"I absolutely love this phone, it works perfectly."*  

---

### One-Shot Generation
- **Definition**: Prompt includes task instruction + **one example**.  
- **Example Prompt**:  
```
Task: Generate a sentence expressing positive sentiment about a product.
Example: "This laptop is amazing and very fast."
Now generate another example.
```

- **Possible Output**:  
*"This tablet runs smoothly and feels premium."*  

---

### Few-Shot Generation
- **Definition**: Prompt includes task instruction + **multiple examples (3–5)**.  
- **Example Prompt**:  

```
Task: Generate a sentence expressing positive sentiment about a product.
Example 1: "This phone has excellent battery life."
Example 2: "I love how clear the screen looks."
Example 3: "The sound quality of these headphones is fantastic."
Now generate another example.
```

- **Possible Output**:  
*"This smartwatch is stylish and very easy to use."*  

---

### Topic/Controlled Generation
- **Definition**: First generate **topics** or scenarios, then prompt with each topic.  
- **Example Flow**:  
1. Prompt: *"List 3 topics for product reviews."*  
   → *["Restaurant review", "Electronics review", "Movie review"]*  
2. Prompt with topic:  
   *"Generate a positive restaurant review."*  
   → *"The pasta was fresh and the service outstanding."*  
3. Prompt with topic:  
   *"Generate a positive electronics review."*  
   → *"This laptop is lightweight yet powerful."*  

---

## Comparison Table

| Strategy                | Prompt Format | Strengths | Weaknesses | Example Output |
|--------------------------|---------------|-----------|-------------|----------------|
| **Zero-Shot**            | Instruction only | Simple, quick; no examples needed | Can be generic, low diversity | "I love this product, it’s fantastic." |
| **One-Shot**             | Instruction + 1 example | Anchors style, more relevant | Lower diversity, tied to example | "This tablet runs smoothly and feels premium." |
| **Few-Shot**             | Instruction + 3–5 examples | Higher quality, task-specific, structured | Risk of repeating limited examples | "This smartwatch is stylish and very easy to use." |
| **Topic/Controlled**     | Instruction + generated topics | Controlled diversity, varied datasets | Requires two-step prompting | "The pasta was fresh and the service outstanding." |

---
