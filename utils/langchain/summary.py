import dotenv
import click
import clipboard

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain.chat_models import ChatOpenAI
from langchain.callbacks.base import BaseCallbackHandler
from langchain.callbacks.streaming_stdout_final_only import (
    FinalStreamingStdOutCallbackHandler,
)
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

dotenv.load_dotenv()


class StreamingPrintCallbackHandler(BaseCallbackHandler):
    def on_llm_new_token(self, token, **kwargs) -> None:
        print(token, end="", flush=True)


def summary(text, objective: str = None, callbacks: list = []):
    llm = ChatOpenAI(
        temperature=0,
        model="gpt-3.5-turbo-16k",
        streaming=True,
        # callbacks=callbacks,
    )

    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n"], chunk_size=10_000, chunk_overlap=500
    )
    docs = text_splitter.create_documents([text])

    map_prompt = ""
    if objective:
        map_prompt += "OBJECTIVE: {objective}\n\n"
    map_prompt += 'TEXT:\n"""\n{text}\n"""\n\nSUMMARY:\n'
    map_prompt_template = PromptTemplate(
        template=map_prompt, input_variables=["text", "objective"]
    )

    summary_chain = load_summarize_chain(
        llm=llm,
        chain_type="map_reduce",
        map_prompt=map_prompt_template,
        combine_prompt=map_prompt_template,
        verbose=False,
    )

    output = summary_chain.run(
        input_documents=docs,
        objective=objective,
        callbacks=callbacks,
        verbose=False,
    )

    return output


@click.command()
@click.option("--objective", help="Objective of the summary")
@click.argument("text", type=str)
def main(
    text,
    objective: str = None,
):
    print("\nSUMMARY:\n")
    output = summary(
        text=text,
        objective=objective,
        # callbacks=[StreamingStdOutCallbackHandler()],
    )
    print(output)
    clipboard.copy(output)


if __name__ == "__main__":
    main()
