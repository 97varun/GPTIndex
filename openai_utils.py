import openai


def request_api(prompt: str, parameters: dict):
    openai.api_key = parameters['api_key']

    try:
        response = openai.Completion.create(
            prompt=prompt,
            engine=parameters['model'],
            temperature=parameters['temperature'],
            max_tokens=parameters['max_length'],
            top_p=parameters['top_p'],
            n=parameters['best_of'],
            logprobs=10,
            stop=[']', '.'],
        )

    except openai.error.Timeout as e:
        #Handle timeout error, e.g. retry or log
        print(f"OpenAI API request timed out: {e}")
        pass
    except openai.error.APIError as e:
        #Handle API error, e.g. retry or log
        print(f"OpenAI API returned an API Error: {e}")
        pass
    except openai.error.APIConnectionError as e:
        #Handle connection error, e.g. check network or log
        print(f"OpenAI API request failed to connect: {e}")
        pass
    except openai.error.InvalidRequestError as e:
        #Handle invalid request error, e.g. validate parameters or log
        print(f"OpenAI API request was invalid: {e}")
        pass
    except openai.error.AuthenticationError as e:
        #Handle authentication error, e.g. check credentials or log
        print(f"OpenAI API request was not authorized: {e}")
        pass
    except openai.error.PermissionError as e:
        #Handle permission error, e.g. check scope or log
        print(f"OpenAI API request was not permitted: {e}")
        pass
    except openai.error.RateLimitError as e:
        #Handle rate limit error, e.g. wait or log
        print(f"OpenAI API request exceeded rate limit: {e}")
        pass

    return response

def parse_api_result(result, parameters):
    
    text_generated = []
    
    for idx, g in enumerate(result['choices']):
        text = g['text']
        logprob = sum(g['logprobs']['token_logprobs'])
        text_generated.append((text, logprob))
    
    # sort the text generated from model by logprobs
    text_generated = sorted(text_generated, key=lambda tup: tup[1], reverse=True)
    text_generated = [r[0] for r in text_generated]
    
    def print_multi_res(params):
        outtxt = ''
        for i in range(params['best_of']):
            outtxt += text_generated[i].strip()
            outtxt += '\n\n\n'
        return outtxt
    
    return print_multi_res(parameters)

def parse_api_result_rank(result):
    logprob = result['choices'][0]['logprobs']['top_logprobs'][0]
    logprob_list = [(x.strip(), logprob[x]) for x in logprob]
    sorted_logprob_list = sorted(logprob_list, key=lambda tup: tup[1], reverse=True)
    probs = [x[1] for x in sorted_logprob_list]
    softmax_prob = np.exp(probs) / np.sum(np.exp(probs), axis=0)
    to_return = []
    
    for x, p in zip(sorted_logprob_list, softmax_prob):
        try:
            to_return.append((int(x[0]), p))
        except:
            continue
    
    return to_return
