
# pip install pyautogen

import autogen


config_list = [{"model": "gpt-4", "api_key": api_key}]
llm_config = {'config_list':config_list}

# Create the tasks

financial_tasks = [
    'What are the current stock prices of NVIDIA and TESLA? How is the performance over the past month in terms of percentage change?',
    'Investigate possible reasons of the stock performance'
]

writing_tasks = [
    'Write an engaging blog post using the information provided to you.'
]

# Create the agents

financial_assistant = autogen.AssistantAgent(
    name = 'Financial_Assistant',
    llm_config = llm_config
)

research_assistant= autogen.AssistantAgent(
    name = 'Researcher',
    llm_config = llm_config
)

writer = autogen.AssistantAgent(
    name = 'writer',
    llm_config = llm_config,
    system_message = '''
        You are a professional writer, known for you insightful
        and engaging articles.
        You transform complex concepts into compelling narratives.
        Print 'TERMINATE' at the end when evertything is done.
    '''
)


user = autogen.UserProxyAgent(
    name = 'User',
    human_input_mode = 'NEVER',
    is_termination_msg = lambda x: x.get('content','') and x.get('content','').rstrip().endswith('TERMINATE'),
    code_execution_config = {
        'last_n_messages': 1,
        'work_dir': 'tasks',
        'use_docker': False
    }
)

# Initiate the chat

chat_results = user.initiate_chats(
    [
        {
            'recipient': financial_assistant,
            'message': financial_tasks[0], # pass 1st task to financial assistant
            'clear_history': True,
            'silent': False,
            'summary_method': 'last_msg',
        },
        {
            'recipient': research_assistant,
            'message': financial_tasks[1], # pass 2nd task to research assistant
            'summary_method': 'reflection_with_llm',
        },
        {
            'recipient': writer,
            'message': writing_tasks[0],
            'carryover': 'I want to include a figure or a table of data in the blog post.',
        },
    ]
)


import streamlit as st

st.title('🔖Using AI agents for Stock Analysis')

st.header('About the App')
st.write('''
This app helps you automate stock market research using AI agents.
These agents scour the web and perform research on sites like Yahoo Finance and news websites to 
fetch you the latest updates regarding a particular stock.
The report gives you a quick gist of important information without you having to spend hours to 
put together the same information from multiple sources and websites.
''')


