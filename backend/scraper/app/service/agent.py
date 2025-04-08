import re

from loguru import logger
from langchain_core.messages import SystemMessage, HumanMessage

from app.dependencies.llm import llm
from app.service.tools.search import search_duckduckgo
from app.schema.financial_data import FinancialData
from app.service.prompts import EXTRACT_INFORMATION_PROMPT

def extract_information(name: str) -> FinancialData:
    # search web for share price
    share_price = _extract_information(name, "share price")

    # search web for earnings per share
    earnings_per_share = _extract_information(name, "earnings per share")

    # search web for dividend yield
    dividend_yield = _extract_information(name, "dividend yield")

    # search web for market cap
    market_cap = _extract_information(name, "market cap")

    # search web for debt
    debt = _extract_information(name, "debt")

    # search web for net assets
    net_assets = _extract_information(name, "net assets")

    # search web for net profits
    net_profits = _extract_information(name, "net profits")

    return FinancialData(
        share_price=share_price,
        earnings_per_share=earnings_per_share,
        dividend_yield=dividend_yield,
        market_cap=market_cap,
        debt=debt,
        net_assets=net_assets,
        net_profits=net_profits
    )


def _extract_information(name: str, metric: str) -> int | float:
    """
    Extract information from the web using the provided name and metric.
    
    :param str name: The name of the entity to search for
    :param str metric: The metric to extract information for
    :return str: The extracted information
    """
    search_query = f"{name} {metric}"
    web_results = search_duckduckgo(search_query, max_results=10)
    if not web_results:
        logger.warning(f"No results found for {search_query}")
        return 0
    
    # format search snippets into string
    results_str = ""
    for result in web_results:
        results_str += f"** {result.title}\n {result.snippet}\n\n"
    results_str.strip("\n")

    # attempt to extract the information from just snippets
    prompt = EXTRACT_INFORMATION_PROMPT.format(query=search_query, information=results_str)
    logger.trace(f"Prompt:\n{prompt}")
    llm_response = llm.invoke(HumanMessage(content=prompt))
    logger.trace(f"LLM response:\n{llm_response}")

    # parse LLM response 
    matches = re.findall(r"S\$[0-9]+[\.,]*[0-9]*\s*(?:(?:million)|(?:billion))*", llm_response)
    logger.debug(f"Matches: {matches}")
    if matches:
        # if there are multiple matches, return the first one
        llm_response = matches[0]
        try:
            # remove S$ and convert to float
            llm_response = re.sub(r"S\$", "", llm_response).replace(",", "").replace(" ", "")
            if "million" in llm_response:
                llm_response = float(llm_response.replace("million", "")) * 1_000_000
            elif "billion" in llm_response:
                llm_response = float(llm_response.replace("billion", "")) * 1_000_000_000
            else:
                llm_response = float(llm_response)
            if metric == "earnings per share":
                return llm_response
            else:
                return int(llm_response)
        except ValueError:
            logger.warning(f"LLM response is not a valid number: {llm_response}")
            return 0
    
    logger.info(f"No matches found in LLM response, scraping from first site")
    web_results[0].link