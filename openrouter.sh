response=$(curl https://openrouter.ai/api/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -d '{
  "model": "deepseek/deepseek-r1-distill-llama-70b", 
  "include_reasoning": true, # not working
  "messages": [
    {
      "role": "user",
      "content": "python: code only: def csvs_to_duck_db_table(csv_paths: List[str]) -> List[str] - new duck db file paths"
    }
  ]
  
}')

echo $response