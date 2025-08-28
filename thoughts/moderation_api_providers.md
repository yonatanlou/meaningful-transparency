
**TL;DR \
I think the best is to use OpenAI, perspective and maybe google (We can also do LLama its really cheap).**



* 
* **OpenAI Moderation API:**
    * It's free!
    * Works with both text and images.
    * Comes with a fixed list of categories like 'sexual', 'harassment', 'hate', 'self-harm', and 'violence' (some with more specific sub-categories like '/minors' or '/graphic').
    * [https://platform.openai.com/docs/guides/moderation](https://platform.openai.com/docs/guides/moderation)
* **Perspective API:**
    * Also free!
    * Only for text.
    * Has a fixed list of categories like THREAT, PROFANITY, INSULT, IDENTITY_ATTACK, SEVERE_TOXICITY, and TOXICITY.
    * <code>[https://developers.perspectiveapi.com/s/about-the-api-attributes-and-languages?language=en_US](https://developers.perspectiveapi.com/s/about-the-api-attributes-and-languages?language=en_US)</code>
    * [https://developers.perspectiveapi.com/s/docs-sample-requests?language=en_US](https://developers.perspectiveapi.com/s/docs-sample-requests?language=en_US) 
    * 
* <strong>Azure:</strong>
    * Offers a free tier: up to 5,000 text records (where a "text record" is 1,000 words!) and 5,000 images analyzed per month.
    * After the free tier, it's pay-as-you-go: around $0.38 per 1,000 text records and $0.75 per 1,000 images.
    * Seems to focus on categories like hate, self_harm, sexual, and violence.
    * [https://learn.microsoft.com/en-us/azure/ai-services/content-safety/quickstart-text?tabs=visual-studio%2Cwindows&pivots=programming-language-python](https://learn.microsoft.com/en-us/azure/ai-services/content-safety/quickstart-text?tabs=visual-studio%2Cwindows&pivots=programming-language-python)  \

* <strong>Amazon Comprehend:</strong>
    * Comes with an AWS Free Tier for the first 12 months, covering 5 million characters per month.
    * Handles text only.
    * Categories include 'GRAPHIC', 'HARASSMENT_OR_ABUSE', 'HATE_SPEECH', 'INSULT', 'PROFANITY', 'SEXUAL', 'VIOLENCE_OR_THREAT', and 'TOXICITY'.
    * [https://docs.aws.amazon.com/comprehend/latest/APIReference/API_DetectToxicContent.html](https://docs.aws.amazon.com/comprehend/latest/APIReference/API_DetectToxicContent.html) 
* <strong>Google Cloud Natural Language API:</strong>
    * Not completely free, but gives you a small monthly allowance.
    * Everyone gets 5,000 free "units" for basic features.
    * There's also a larger free tier for specific features, like 30,000 characters for content classification and 50,000 for moderation
    * 'Toxic', 'Insult', 'Profanity', 'Derogatory', 'Sexual', 'Death, Harm & Tragedy', 'Violent', 'Firearms & Weapons', 'Public Safety', 'Health', 'Religion & Belief', 'Illicit Drugs', 'War & Conflict', 'Politics', 'Finance', 'Legal'
* <strong>LlamaGuard (Meta)</strong>
* Docs: https://huggingface.co/meta-llama/Llama-Guard-3-8B (open weights) \
Free (self-hosted) or cheap on APIs like Groq or together (~$0.20 per million tokens)
* Supports: Text (Llama Guard 3), Text+Image (Llama Guard 4)
* Categories: open-source schema, includes <code>sexual</code>, `violence`, `self-harm`, `hate`, `criminal/illegal activity`, etc. (schema is configurable, designed for safety guardrails - 14 cateogris)