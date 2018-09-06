import logging

def get_response_from_context(input_statement, response_list, prior_responses):
    """
    :param input_statement: A statement, that closely matches an input to the chat bot.
    :type input_statement: Statement
    :param response_list: A list of statement options to choose a response from.
    :type response_list: list
    :return: Return the first statement in the response list.
    :rtype: Statement
    """
    logger = logging.getLogger(__name__)
    logger.info(u'Selecting first response from list of {} options.'.format(
        len(response_list)
    ))
    print input_statement, response_list, prior_responses
    return response_list[0]
