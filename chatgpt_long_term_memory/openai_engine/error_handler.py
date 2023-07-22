import functools

import openai.error


def retry_on_openai_errors(max_retry):
    """
    this function retries the function that it decorates in case of openai errors (RateLimitError, Timeout, APIError, APIConnectionError, ServiceUnavailableError, InvalidRequestError)`
    :param max_retry: the maximum number of retries
    :return: the decorator
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            retry = 0
            while retry < max_retry:
                try:
                    return func(*args, **kwargs)
                except (openai.error.RateLimitError, openai.error.Timeout, openai.error.APIError,
                        openai.error.APIConnectionError, openai.error.ServiceUnavailableError,
                        openai.error.InvalidRequestError) as error:
                    retry += 1
                    print(f"Retrying {retry} time due to error: {error}")
            raise Exception(f"Reached maximum number of retries ({max_retry})")
        return wrapper
    return decorator
