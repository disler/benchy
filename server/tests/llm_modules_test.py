import pytest
from modules.openai_llm import predictive_prompt
from modules.llm_models import simple_prompt
from modules.data_types import ModelAlias, PromptResponse


def test_predictive_prompt():
    code = """
    public class User {
        public string FirstName { get; set; }
        public string LastName { get; set; }
        public string Username { get; set; }
    }
    """

    test_prompt = (
        "Replace the Username property with an Email property. Respond only with code."
    )
    result = predictive_prompt(prompt=test_prompt, prediction=code, model="gpt-4o-mini")

    assert isinstance(result, PromptResponse)
    assert isinstance(result.response, str)
    assert len(result.response) > 0
    assert "Email" in result.response
    assert "Username" not in result.response
    assert result.inputAndOutputCost >= 0
    assert result.runTimeMs == 0


@pytest.mark.parametrize(
    "input_text,expected_completion",
    [
        ("Let's cal", "calculate_total_price"),
        ("We need to val", "validate_user_input"),
        ("Time to pro", "process_payment"),
    ],
)
def test_predictive_prompt_autocomplete(input_text, expected_completion):
    functions = """
    def calculate_total_price(items, tax_rate):
        pass
        
    def validate_user_input(data):
        pass
        
    def process_payment(amount):
        pass
    """

    prompt = f"""# Provide an autocomplete suggestion given the following function names and Input Text

    ## Instructions
    - Respond only with your top single suggestion and nothing else.
    - Your autocompletion will replace the last word of the input text.
    - For example, if the input text is "We need to analy", and there is a function name is "analyze_user_expenses", then your autocomplete should be "analyze_user_expenses".

    ## Function names
    {functions}

    ## Input text
    '{input_text}'
    """

    result = predictive_prompt(prompt=prompt, prediction=prompt, model="gpt-4o-mini")

    assert isinstance(result, PromptResponse)
    assert isinstance(result.response, str)
    assert len(result.response) > 0
    assert expected_completion in result.response
    assert result.response.strip() == expected_completion.strip()
    assert result.inputAndOutputCost >= 0
    assert result.runTimeMs == 0


@pytest.mark.parametrize(
    "model_alias",
    [
        ModelAlias.gpt_4o,
        ModelAlias.gpt_4o_mini,
        ModelAlias.gpt_4o_predictive,
        ModelAlias.gpt_4o_mini_predictive,
        ModelAlias.gemini_pro_2,
        ModelAlias.gemini_flash_2,
        ModelAlias.gemini_flash_8b,
        ModelAlias.sonnet,
        ModelAlias.haiku,
    ],
)
def test_prompt_ping(model_alias):
    test_prompt = "Say 'pong' and nothing else"
    result = simple_prompt(test_prompt, model_alias)

    assert isinstance(result, PromptResponse)
    assert isinstance(result.response, str)
    assert len(result.response) > 0
    assert (
        "pong" in result.response.lower()
    ), f"Model {model_alias} did not respond with 'pong'"
    assert result.inputAndOutputCost >= 0
