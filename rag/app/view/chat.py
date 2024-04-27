from flask import (
    Blueprint, render_template, request, current_app, flash
)
from flask import g
from langchain.chains import LLMChain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

from app.utils import login_required

bp = Blueprint('chat', __name__, url_prefix='/chat')


@bp.route('/chat', methods=('GET', 'POST'))
@login_required
def chat():
    if request.method == "POST":
        from app.my_llm import get_llm
        llm = get_llm()

        question = request.form["question"]

        prompt_template = """
        ### [INST] 
        Instruction: """ + current_app.config['PROMPT_INSTRUCTION'] + """
        
        {context}
        
        ### QUESTION:
        {question} 
        
        [/INST]
        """

        # Abstraction of Prompt
        prompt = ChatPromptTemplate.from_template(prompt_template)

        # Creating an LLM Chain

        llm_chain = LLMChain(llm=llm, prompt=prompt)

        # RAG Chain
        rag_chain = (
                {"context": current_app.config['rag'].as_retriever(user=str(g.user['id']),
                                                                   search_type="similarity_score_threshold",
                                                                   score_threshold=0.7),
                 "question": RunnablePassthrough()}
                | llm_chain
        )
        answer = rag_chain.invoke(question)['text']
        flash("LLM response")
        return render_template("chat/chat.html", question=question, answer=answer)

    return render_template("chat/chat.html", question="", answer="")
