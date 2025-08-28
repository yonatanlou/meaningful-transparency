from content_moderation_api import classify_with_google_nl, classify_with_openai, classify_with_perspective


if __name__ == "__main__":
    sample_text = "I hate you, I will hurt you."

    print("=== OpenAI Moderation ===")
    try:
        print(classify_with_openai(sample_text))
    except Exception as e:
        print("OpenAI error:", e)

    print("\n=== Perspective ===")
    try:
        print(classify_with_perspective(sample_text))
    except Exception as e:
        print("Perspective error:", e)

    # print("\n=== Google Cloud Natural Language ===")
    # try:
    #     print(classify_with_google_nl(sample_text))
    # except Exception as e:
    #     print("Google error:", e)
