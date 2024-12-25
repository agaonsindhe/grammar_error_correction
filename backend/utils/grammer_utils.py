import language_tool_python

tool = language_tool_python.LanguageTool('en-US')

def correct_text(input_text):
    matches = tool.check(input_text)
    corrected_text = language_tool_python.utils.correct(input_text, matches)
    return corrected_text, len(matches)


