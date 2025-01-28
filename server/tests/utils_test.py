def test_think_tag_parsing():
    from utils import deepseek_r1_distil_separate_thoughts_and_response
    
    sample = '''<think>
This is a test thought process
spanning multiple lines
</think>

This is the final answer'''
    
    thoughts, response = deepseek_r1_distil_separate_thoughts_and_response(sample)
    
    assert thoughts == "This is a test thought process\nspanning multiple lines"
    assert response == "This is the final answer"

def test_partial_xml_handling():
    from utils import deepseek_r1_distil_separate_thoughts_and_response
    
    # Test with unclosed think tag
    sample = '''<think>
Unclosed thought process
This is the answer'''
    
    thoughts, response = deepseek_r1_distil_separate_thoughts_and_response(sample)
    
    assert thoughts == "Unclosed thought process"
    assert response == "This is the answer"
