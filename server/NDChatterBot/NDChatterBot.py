from chatterbot import ChatBot

def NDChatterBot():
    return ChatBot("Chatterbot",
        storage_adapter="NDChatterBot.sql_storage.SQLStorageAdapter",
        preprocessors=[
            'chatterbot.preprocessors.clean_whitespace',
            'chatterbot.preprocessors.unescape_html',
            'chatterbot.preprocessors.convert_to_ascii'
        ],
        logic_adapters=[
            "chatterbot.logic.MathematicalEvaluation",
            {
                "import_path": "NDChatterBot.BestMatch.BestMatch",
                "statement_comparison_function": "chatterbot.comparisons.levenshtein_distance",
                "response_selection_method": "NDChatterBot.response_selection.get_response_from_context"
            },
            {
                'import_path': 'chatterbot.logic.LowConfidenceAdapter',
                'threshold': 0.65,
                'default_response': 'My programming is not designed to handle such inquiries. I am sorry, are you displeased?'
            },
            #{
            #    'import_path': 'chatterbot.logic.SpecificResponseAdapter',
            #    'input_text': 'Help me!',
            #    'output_text': 'Ok, here is a link: http://chatterbot.rtfd.org'
            #}
        ],
        filters=["chatterbot.filters.RepetitiveResponseFilter"]
    )